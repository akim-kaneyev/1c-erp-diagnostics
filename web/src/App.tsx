import { useMemo, useRef, useState } from 'react'
import { Button } from '@ui-sdk/react/button'
import { Field, FieldLabel } from '@ui-sdk/react/field'
import { Input } from '@ui-sdk/react/input'
import { Select, SelectContent, SelectItem, SelectLabel, SelectTrigger, SelectValue } from '@ui-sdk/react/select'
import { Tabs, TabsList, TabsPanel, TabsTab } from '@ui-sdk/react/tabs'
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from '@ui-sdk/react/dialog'
import { FileInput, FileInputTrigger } from '@ui-sdk/react/file-input'
import { Collapsible, CollapsiblePanel, CollapsibleTrigger } from '@ui-sdk/react/collapsible'
import logo from '../../plugins/one-c-erp-diagnostics/assets/logo.png'
import { demoText } from './demo'
import { version as viewerVersion } from '../package.json'
import { emptyFilters, filterRows, parseCase, rowsFor, sha256, statusLabels, validDateChange } from './model'
import type { Bundle, Filters, Row, Section } from './model'

type Loaded = { bundle: Bundle; bytes: ArrayBuffer; filename: string; hash: string }
const sections: { id: Section; name: string; singular: string }[] = [
  { id: 'evidence', name: 'Доказательства', singular: 'источник' },
  { id: 'claims', name: 'Выводы', singular: 'вывод' },
  { id: 'runs', name: 'Запуски', singular: 'запуск' },
]
export function readBytes(file: File): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onerror = () => reject(new Error('Не удалось прочитать файл.'))
    reader.onload = () => resolve(reader.result as ArrayBuffer)
    reader.readAsArrayBuffer(file)
  })
}

function Status({ value }: { value: string }) {
  return <span className="status" data-status={value}>{statusLabels[value] || value}</span>
}

function RecordDialog({ row }: { row: Row }) {
  const [proof, setProof] = useState('Байты исходного файла не проверены.')
  const [preview, setPreview] = useState('')
  const serial = useRef(0)
  async function verify(file: File) {
    const ticket = ++serial.current
    setProof('Вычисляю SHA-256…'); setPreview('')
    try {
      const bytes = await readBytes(file), actual = await sha256(bytes)
      if (ticket !== serial.current) return
      setProof(`${file.name} · SHA-256: ${actual}. ${row.hash ? actual === row.hash ? 'Хеш совпадает.' : 'Хеш НЕ совпадает.' : 'Заявленный хеш отсутствует; сравнение невозможно.'}`)
      if (/\.(txt|json|csv|bsl|md)$/i.test(file.name)) setPreview(new TextDecoder().decode(bytes.slice(0, 12000)))
    } catch { if (ticket === serial.current) setProof('Не удалось проверить файл. Статус записи не изменён.') }
  }
  return <Dialog onOpenChange={(open) => { if (!open) { serial.current++; setProof('Байты исходного файла не проверены.'); setPreview('') } }}>
    <DialogTrigger className="record-link">Открыть {row.id}</DialogTrigger>
    <DialogContent className="record-dialog" initialFocus="content">
      <header className="dialog-header"><div><span className="eyebrow">Карточка материала</span><DialogTitle>Карточка {row.id}</DialogTitle></div><DialogClose className="icon-button" aria-label={`Закрыть карточку ${row.id}`}>×</DialogClose></header>
      <DialogDescription>{row.title}</DialogDescription>
      <div className="dialog-scroll">
        <Status value={row.status} /><p>{row.description}</p>
        <dl className="metadata"><dt>Источник</dt><dd>{row.source}</dd><dt>Дата из файла</dt><dd>{row.date || 'Не задана'}</dd><dt>Заявленный SHA-256</dt><dd className="hash">{row.hash || 'Не задан'}</dd><dt>Связи</dt><dd>{row.refs.join(', ') || 'Не заданы'}</dd></dl>
        <section className="detail-section"><h3>Ограничения</h3>{row.limitations.length ? <ul>{row.limitations.map((text, i) => <li key={`${i}-${text}`}>{text}</li>)}</ul> : <p>В записи не перечислены. Это не подтверждает полноту данных.</p>}</section>
        <section className="detail-section"><h3>Сверка исходного файла</h3><p>Выберите файл на компьютере. Проверка хеша не меняет статус доказательства.</p>
          <FileInput aria-label={`Исходный файл ${row.id}`} maxSize={64 * 1024 * 1024}
            onValueChange={files => { if (files[0]) void verify(files[0]) }} onReject={() => setProof('Файл должен быть не больше 64 МБ.')}>
            <FileInputTrigger className="button secondary">Сверить файл {row.id}</FileInputTrigger>
          </FileInput>
          <p className="proof" role="status" aria-label={`Результат сверки ${row.id}`}>{proof}</p>
          {preview && <pre className="source-preview" aria-label={`Фрагмент файла ${row.id}`}>{preview}</pre>}
        </section>
        <Collapsible aria-label={`Исходная запись ${row.id}`}><CollapsibleTrigger className="record-link">Показать JSON {row.id}</CollapsibleTrigger><CollapsiblePanel><pre>{JSON.stringify(row.raw, null, 2)}</pre></CollapsiblePanel></Collapsible>
      </div>
      <footer className="dialog-footer"><span>Только просмотр</span><DialogClose className="button primary">Готово {row.id}</DialogClose></footer>
    </DialogContent>
  </Dialog>
}

export function App() {
  const [loaded, setLoaded] = useState<Loaded | null>(null)
  const [section, setSection] = useState<Section>('evidence')
  const [filters, setFilters] = useState<Filters>({ ...emptyFilters })
  const [page, setPage] = useState(0)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const serial = useRef(0)
  const rows = useMemo(() => loaded ? rowsFor(loaded.bundle, section) : [], [loaded, section])
  const visible = filterRows(rows, filters)
  const pages = Math.max(1, Math.ceil(visible.length / 25))
  const currentPage = Math.min(page, pages - 1)
  const displayed = visible.slice(currentPage * 25, currentPage * 25 + 25)
  const statuses = [...new Set(rows.map(row => row.status))]
  const state = loaded?.bundle.state
  const annotations = loaded?.bundle.annotations
  const staleCount = state ? [...state.evidence, ...state.runs, ...state.claims].filter(x => ['stale', 'superseded', 'withdrawn'].includes(x.status)).length : 0
  const undated = rows.filter(row => !row.date).length

  async function loadBytes(bytes: ArrayBuffer, filename: string, ticket: number) {
    const bundle = parseCase(new TextDecoder('utf-8', { fatal: true }).decode(bytes))
    const hash = await sha256(bytes)
    if (ticket !== serial.current) return
    setLoaded({ bundle, bytes, filename, hash }); setSection('evidence'); setFilters({ ...emptyFilters }); setPage(0); setError('')
  }
  async function openFile(file: File) {
    const ticket = ++serial.current; setLoading(true); setError('')
    try { await loadBytes(await readBytes(file), file.name, ticket) }
    catch (reason) { if (ticket === serial.current) setError(reason instanceof Error ? reason.message : 'Не удалось открыть файл.') }
    finally { if (ticket === serial.current) setLoading(false) }
  }
  async function openDemo() {
    const ticket = ++serial.current; setLoading(true)
    try { await loadBytes(new TextEncoder().encode(demoText).buffer, 'demo-case.json', ticket) }
    catch { setError('Не удалось открыть учебный пример.') }
    finally { if (ticket === serial.current) setLoading(false) }
  }
  function update(next: Filters) { setFilters(next); setPage(0) }
  function exportOriginal() {
    if (!loaded) return
    const url = URL.createObjectURL(new Blob([loaded.bytes], { type: 'application/json' }))
    const link = document.createElement('a'); link.href = url; link.download = loaded.filename; link.click()
    setTimeout(() => URL.revokeObjectURL(url), 1000)
  }
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><img src={logo} alt="Velis" /><div><strong>VELIS</strong><span>Диагностика 1С</span></div></div>
      <div className="workspace-label">РАБОЧЕЕ ПРОСТРАНСТВО</div>
      <div className="sidebar-current"><span aria-hidden="true">▦</span> Диагностический разбор</div>
      <div className="sidebar-note"><span className="live-dot" /> Локальное приложение<p>Файлы остаются на вашем компьютере. Подключение к базе не требуется.</p></div>
      <footer className="sidebar-footer"><strong>1C ERP Diagnostics</strong><span>Viewer {viewerVersion} · UI SDK</span></footer>
    </aside>
    <main>
      <header className="topbar"><span className="breadcrumb">Рабочее пространство <span>/</span> Материалы диагностики</span><span className="local-badge"><span className="live-dot" /> Только просмотр</span></header>
      <div className="main-content">
        <div className="page-heading"><div><span className="eyebrow">Доказательная диагностика</span><h1>Диагностический разбор</h1><p>От первичных материалов к проверяемому выводу.</p></div>
          <div className="file-actions"><FileInput aria-label="Диагностический JSON" accept=".json" maxSize={10 * 1024 * 1024} minSize={2} disabled={loading}
            onValueChange={files => { if (files[0]) void openFile(files[0]) }} onReject={() => setError('Выберите один JSON-файл размером до 10 МБ. Текущий кейс сохранён.')}>
            <FileInputTrigger className="button primary">Открыть JSON</FileInputTrigger>
          </FileInput><Button className="button secondary" onClick={openDemo} disabled={loading}>Открыть пример</Button></div>
        </div>
        {error && <div className="error-banner" role="alert">{error}</div>}
        {loading && <p role="status">Проверяю файл…</p>}
        {!loaded ? <section className="welcome"><div className="welcome-mark" aria-hidden="true">↗</div><span className="eyebrow">Единая картина кейса</span><h2>Доказательства. Связи. Выводы.</h2><p>Откройте STATE.json вашего кейса или диагностический пакет. Здесь можно сопоставить источники, изучить ограничения и проследить ход проверки.</p><div className="welcome-features"><span>01 / Локальные файлы</span><span>02 / Неизменные статусы</span><span>03 / Проверяемые источники</span></div><p className="muted">Нет готового файла? «Открыть пример» загрузит явно обозначенные учебные данные.</p></section> : <>
          <section className="case-summary"><div><div className="case-kicker"><span>{state!.case_id}</span>{annotations?.synthetic && <span className="demo-badge">Учебный пример</span>}</div><h2>{annotations?.title || state!.case_id}</h2><p>{annotations?.goal || 'Цель в STATE.json не задана. Описание можно добавить в диагностическом пакете.'}</p></div><div className="case-result"><span>Gate 10 · статус из файла</span><Status value={state!.gates.find(gate => gate.id === '10')!.status} /><small>Просмотр не подтверждает корректность учёта</small></div></section>
          <section className="gate-strip" aria-label="Этапы проверки Gate 0–10">{[...state!.gates].sort((a, b) => +a.id - +b.id).map(gate => <div key={gate.id} className="gate" data-status={gate.status} title={`Gate ${gate.id}: ${statusLabels[gate.status]}`}><span>{gate.id}</span><small>{statusLabels[gate.status]}</small></div>)}</section>
          <div className="section-heading"><div><h2>Материалы кейса</h2><p>Исходные статусы сохраняются при любых фильтрах.</p></div><Button className="button secondary" onClick={exportOriginal}>Сохранить копию JSON</Button></div>
          <div className="coverage-note"><span aria-hidden="true">ⓘ</span><div><strong>Область данных</strong><p>{annotations?.coverage?.limitation || 'Полнота и область выборки в файле не объявлены.'} Доступно источников: {state!.evidence.length}. Всего в области: {annotations?.coverage?.total ?? 'неизвестно'}.{staleCount > 0 && ` Неактуальных записей: ${staleCount}.`}</p></div></div>
          <Tabs value={section} onValueChange={(value, details) => {
            if (!sections.some(item => item.id === value)) { details.cancel(); return }
            setSection(value as Section); setFilters(previous => ({ ...previous, status: 'all' })); setPage(0)
          }}>
            <TabsList aria-label="Разделы диагностики" className="section-tabs">{sections.map(item => <TabsTab key={item.id} value={item.id}>{item.name} <span>{state![item.id].length}</span></TabsTab>)}</TabsList>
            <div className="filters"><Field className="search-field"><FieldLabel>Поиск по материалам</FieldLabel><Input type="search" placeholder="ID, описание или источник" value={filters.search} onValueChange={value => update({ ...filters, search: value })} /></Field>
              <Select value={filters.status} items={[{ value: 'all', label: 'Все статусы' }, ...statuses.map(value => ({ value, label: statusLabels[value] || value }))]}
                onValueChange={(value, details) => { if (typeof value !== 'string' || (value !== 'all' && !statuses.includes(value))) { details.cancel(); return }; update({ ...filters, status: value }) }}>
                <SelectLabel>Статус материала</SelectLabel><SelectTrigger className="select-trigger"><SelectValue /></SelectTrigger><SelectContent className="select-popup"><SelectItem value="all">Все статусы</SelectItem>{statuses.map(value => <SelectItem key={value} value={value}>{statusLabels[value] || value}</SelectItem>)}</SelectContent>
              </Select>
              {(['from', 'to'] as const).map(key => <Field key={key} className="date-field"><FieldLabel>{key === 'from' ? 'Дата от' : 'Дата до'}</FieldLabel><Input type="date" value={filters[key]} onValueChange={(value, details) => {
                const next = { ...filters, [key]: value }
                if (!validDateChange(next.from, next.to)) { details.cancel(); setError('Некорректный диапазон дат. Значение не изменено.'); return }
                setError(''); update(next)
              }} /></Field>)}
              <Button className="button subtle reset" onClick={() => { update({ ...emptyFilters }); setError('') }}>Сбросить фильтры</Button>
            </div>
            <p className="filter-hint">Дата из файла, без пересчёта часового пояса.{(filters.from || filters.to) && undated > 0 && ` Записей без даты исключено: ${undated}.`}</p>
            {sections.map(item => <TabsPanel key={item.id} value={item.id} className="data-panel">
              {section === item.id && <><div className="results-line"><output aria-label="Количество результатов" aria-live="polite">Найдено {visible.length} из {rows.length} записей раздела</output><span>Статусы и содержание — из открытого файла</span></div>
                {visible.length ? <><div className="table-scroll"><table><caption className="sr-only">{item.name}: отфильтрованные материалы</caption><thead><tr><th>Материал</th><th>Статус</th><th>Дата</th><th>Просмотр</th></tr></thead><tbody>{displayed.map(row => <tr key={row.id}><td><span className="record-id">{row.id}</span><strong>{row.title}</strong><small>{row.description}</small></td><td><Status value={row.status} /></td><td className="date-cell">{row.date || 'Не задана'}</td><td><RecordDialog row={row} /></td></tr>)}</tbody></table></div>
                  <div className="pagination"><span>Страница {currentPage + 1} из {pages} · по 25 записей</span><div><Button className="button secondary" disabled={currentPage === 0} onClick={() => setPage(value => Math.max(0, value - 1))}>Предыдущая страница</Button><Button className="button secondary" disabled={currentPage + 1 >= pages} onClick={() => setPage(value => Math.min(pages - 1, value + 1))}>Следующая страница</Button></div></div>
                </> : <div className="empty-results"><h3>{rows.length ? 'Совпадений по фильтрам нет' : 'В этом разделе записей нет'}</h3><p>Это относится к открытому файлу и текущему представлению. Отсутствие записей во всей базе не установлено.</p></div>}
              </>}
            </TabsPanel>)}
          </Tabs>
          <footer className="file-provenance"><span>Открыт: <strong>{loaded.filename}</strong></span><span className="hash">SHA-256 файла: {loaded.hash}</span></footer>
        </>}
        <footer className="page-footer"><span>Velis / 1C ERP Diagnostics</span><span>Локально · без передачи файлов на сервер</span></footer>
      </div>
    </main>
  </div>
}

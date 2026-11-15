import { useEffect, useMemo, useRef, useState } from 'react'
import { Button } from '@ui-sdk/react/button'
import { Checkbox, CheckboxIndicator } from '@ui-sdk/react/checkbox'
import { Collapsible, CollapsiblePanel, CollapsibleTrigger } from '@ui-sdk/react/collapsible'
import { Field, FieldLabel } from '@ui-sdk/react/field'
import { FileInput, FileInputTrigger } from '@ui-sdk/react/file-input'
import { Input } from '@ui-sdk/react/input'
import { PasswordInput, PasswordInputControl, PasswordInputToggle } from '@ui-sdk/react/password-input'
import { Select, SelectContent, SelectItem, SelectLabel, SelectTrigger, SelectValue } from '@ui-sdk/react/select'
import { Textarea } from '@ui-sdk/react/textarea'
import logo from '../../plugins/one-c-erp-diagnostics/assets/logo.png'
import { download, readBytes } from './files'
import { assertLocalMaterial, parseCase } from './model'
import type { Bundle } from './model'
import { api, bootstrap, exportCase } from './workbench_api'
import type { Bootstrap, Capture, Metadata, Profile, Scenario } from './workbench_api'

const scenarioNames: Record<Scenario, string> = { compare: 'Сравнение строк', 'negative-stock': 'Отрицательные остатки', allocation: 'Распределение расходов' }
const kinds = [{ value: 'document', label: 'Документы', section: 'documents' }, { value: 'catalog', label: 'Справочники', section: 'catalogs' }, { value: 'enum', label: 'Перечисления', section: 'enums' }]
const newCaseId = () => 'CASE-' + new Date().toISOString().slice(0, 10).replaceAll('-', '') + '-' + crypto.randomUUID().slice(0, 8)

function Choice({ label, value, items, disabled, change }: { label: string; value: string; items: { value: string; label: string }[]; disabled?: boolean; change: (value: string) => void }) {
  return <Select value={value || null} items={items} disabled={disabled} onValueChange={(next, details) => {
    if (typeof next !== 'string' || !items.some(item => item.value === next)) { details.cancel(); return }
    change(next)
  }}><SelectLabel>{label}</SelectLabel><SelectTrigger className="select-trigger"><SelectValue placeholder="Выберите…" /></SelectTrigger><SelectContent className="select-popup">{items.map(item => <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>)}</SelectContent></Select>
}

function Entry({ label, value, change, maximum = 500, required = false, disabled = false }: { label: string; value: string; change: (value: string) => void; maximum?: number; required?: boolean; disabled?: boolean }) {
  return <Field><FieldLabel>{label}</FieldLabel><Input value={value} required={required} disabled={disabled} maxLength={maximum} onValueChange={(next, details) => { if (next.length > maximum) { details.cancel(); return }; change(next) }} /></Field>
}

export function Workbench({ active, onViewer, onBack }: { active: boolean; onViewer: (bundle: Bundle) => void; onBack: () => void }) {
  const [data, setData] = useState<Bootstrap | null>(null)
  const [error, setError] = useState(''), [notice, setNotice] = useState('')
  const [busy, setBusy] = useState(false), [profileId, setProfileId] = useState('')
  const [profile, setProfile] = useState({ label: '', base_url: '', expected_metadata_name: '', contour_note: '' })
  const [testContour, setTestContour] = useState(false)
  const [username, setUsername] = useState(''), [password, setPassword] = useState('')
  const [sessionId, setSessionId] = useState(''), [serverReadOnly, setServerReadOnly] = useState(false)
  const [caseId, setCaseId] = useState(''), [newId, setNewId] = useState(newCaseId)
  const [title, setTitle] = useState(''), [goal, setGoal] = useState('')
  const [current, setCurrent] = useState<Bundle | null>(null), [notes, setNotes] = useState('')
  const [metadata, setMetadata] = useState<Metadata>({}), [kind, setKind] = useState('document')
  const [objectName, setObjectName] = useState(''), [search, setSearch] = useState('')
  const [leftId, setLeftId] = useState(''), [rightId, setRightId] = useState('')
  const [scenario, setScenario] = useState<Scenario>('compare'), [input, setInput] = useState<unknown>(null)
  const [inputName, setInputName] = useState(''), [synthetic, setSynthetic] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const caseTicket = useRef(0), operation = useRef(false), heading = useRef<HTMLHeadingElement>(null)
  const selectedProfile = data?.profiles.find(item => item.id === profileId)
  const collection = kinds.find(item => item.value === kind)!.section
  const available = useMemo(() => (metadata[collection] || []).filter(item => typeof item.name === 'string' && item.name.toLocaleLowerCase('ru').includes(search.toLocaleLowerCase('ru'))), [metadata, collection, search])
  const objects = available.slice(0, 200).map(item => ({ value: item.name, label: item.synonym ? `${item.synonym} · ${item.name}` : item.name }))

  useEffect(() => {
    if (!active) return
    heading.current?.focus()
    let live = true
    bootstrap().then(value => { if (live) setData(value) }).catch(reason => { if (live) setError(reason instanceof Error ? reason.message : 'Не удалось открыть рабочий экран.') })
    return () => { live = false }
  }, [active])

  async function perform(action: () => Promise<void>) {
    if (operation.current) return
    operation.current = true; setBusy(true); setError(''); setNotice('')
    try { await action() }
    catch (reason) { setError(reason instanceof Error ? reason.message : 'Операция не выполнена.') }
    finally { operation.current = false; setBusy(false) }
  }
  async function refresh() { setData(await bootstrap()) }
  async function openCase(id: string) {
    if (!data) return
    const ticket = ++caseTicket.current
    const value = await api<{ bundle: Bundle; notes: { notes: string } }>(data.csrf, '/api/case', { case_id: id })
    if (ticket !== caseTicket.current) return
    setCurrent(parseCase(JSON.stringify(value.bundle))); setNotes(value.notes.notes); setCaseId(id)
  }
  async function disconnect() {
    if (data && sessionId) await api(data.csrf, '/api/disconnect', { session_id: sessionId })
    setSessionId(''); setServerReadOnly(false); setMetadata({}); setObjectName(''); setPassword('')
  }
  async function chooseProfile(id: string) {
    await disconnect(); setProfileId(id); setNotice('Подключение выбрано. Войдите существующим пользователем этой тестовой базы.')
  }
  async function connect() {
    if (!data || !profileId || !username.trim() || !password) throw new Error('Выберите подключение и заполните пользователя и пароль 1С.')
    await disconnect()
    const secret = password; setPassword('')
    const value = await api<{ session_id: string; server_read_only: boolean; health: { metadataName: string } }>(data.csrf, '/api/connect', { profile_id: profileId, username, password: secret })
    setSessionId(value.session_id); setServerReadOnly(value.server_read_only)
    setNotice(`Подключено: ${value.health.metadataName}. Данные входа хранятся только в памяти текущей сессии.`)
  }
  async function capture(read: string, extra: Record<string, string> = {}) {
    if (!data || !sessionId || !current) throw new Error('Войдите в базу и выберите разбор.')
    const value = await api<Capture>(data.csrf, '/api/capture', { session_id: sessionId, case_id: caseId, operation: read, ...extra })
    setCurrent(parseCase(JSON.stringify(value.case)))
    if (read === 'metadata') { setMetadata(value.response as Metadata); setObjectName('') }
    setNotice('Материал сохранён: ' + value.evidence_id + '. Учётный вывод автоматически не принимался.')
    await refresh()
  }
  async function saveProfile() {
    if (!data) return
    const saved = await api<Profile>(data.csrf, '/api/profile', { ...profile, test_contour: testContour })
    await disconnect(); setProfileId(saved.id); await refresh(); setNotice('Тестовое подключение сохранено без пароля.')
  }
  async function createCase() {
    if (!data) return
    const bundle = await api<Bundle>(data.csrf, '/api/case/create', { case_id: newId, title, goal })
    setCurrent(parseCase(JSON.stringify(bundle))); setCaseId(newId); setNotes(''); setNewId(newCaseId()); await refresh()
    setNotice('Разбор создан. Этапы диагностики ожидают проверки.')
  }
  async function loadInput(file: File) {
    const raw = new TextDecoder('utf-8', { fatal: true }).decode(await readBytes(file))
    let value: unknown
    try { value = JSON.parse(raw) } catch { throw new Error('Файл не является корректным JSON. Ранее выбранные строки сохранены.') }
    assertLocalMaterial(value)
    setInput(value); setInputName(file.name); setSynthetic(false); setResult(null)
  }
  async function runScenario() {
    if (!data || !current || input === null) throw new Error('Выберите разбор и файл строк для проверки.')
    const value = await api<Capture>(data.csrf, '/api/scenario', { case_id: caseId, scenario, input, synthetic })
    setCurrent(parseCase(JSON.stringify(value.case))); setResult(value.result || null); await refresh()
    setNotice('Результат сохранён с ссылкой на исходные строки. Это проверка данных, не установление причины инцидента.')
  }
  const ready = !!sessionId && !!current && !busy

  return <div className="app-shell workbench-shell">
    <aside className="sidebar"><div className="brand"><img src={logo} alt="Velis" /><div><strong>VELIS</strong><span>Диагностика 1С</span></div></div>
      <div className="workspace-label">РАБОЧЕЕ ПРОСТРАНСТВО</div><div className="sidebar-current">Подключение и проверки</div>
      <Button className="button sidebar-nav" onClick={onBack}>Материалы диагностики</Button>
      <div className="sidebar-note"><span className="live-dot" /> Локальная работа<p>Выбирайте тестовую базу. Источники и заметки сохраняются на этом компьютере.</p></div>
      <footer className="sidebar-footer"><strong>1C ERP Diagnostics</strong><span>Рабочий экран {data?.version || ''}</span></footer>
    </aside>
    <main><header className="topbar"><span className="breadcrumb">Рабочее пространство <span>/</span> Подключение и проверки</span><span className="local-badge">Тестовый контур</span></header>
      <div className="main-content"><div className="page-heading"><div><span className="eyebrow">Материалы из 1С</span><h1 ref={heading} tabIndex={-1}>Подключение и проверки</h1><p>Соберите источники, проверьте строки и сохраните ход разбора.</p></div></div>
        {error && <div className="error-banner" role="alert">{error}</div>}
        <p className="workbench-notice" role="status" aria-label="Результат рабочего действия">{busy ? 'Выполняется запрос. Повторный запуск заблокирован.' : notice}</p>
        {!data ? <section className="welcome"><h2>Нужен рабочий режим приложения</h2><p>Откройте установленную диагностику через меню «Пуск». Просмотр файлов остаётся доступен.</p><Button className="button secondary" onClick={onBack}>Вернуться к файлам</Button></section> : <>
          <div className="workbench-grid">
            <section className="workbench-card"><span className="eyebrow">01 / Подключение</span><h2>Тестовая база 1С</h2>
              <Choice label="Сохранённое подключение" value={profileId} items={data.profiles.map(item => ({ value: item.id, label: item.label }))} disabled={busy} change={id => { void perform(() => chooseProfile(id)) }} />
              {selectedProfile && <p className="connection-target">{selectedProfile.base_url}<br />{selectedProfile.expected_metadata_name} · {selectedProfile.contour_note}</p>}
              <form onSubmit={event => { event.preventDefault(); void perform(connect) }}>
                <Entry label="Пользователь 1С" value={username} change={setUsername} required maximum={256} disabled={busy} />
                <Field><FieldLabel>Пароль 1С</FieldLabel><PasswordInput value={password} autoComplete="off" required disabled={busy} onValueChange={(value, details) => { if (value.length > 4096) { details.cancel(); return }; setPassword(value) }}><PasswordInputControl /><PasswordInputToggle aria-label="Показать пароль 1С">Показать</PasswordInputToggle></PasswordInput></Field>
                <div className="workbench-actions"><Button className="button primary" type="submit" disabled={busy || !profileId} data-agent-confirm="Вход в выбранную тестовую базу с предоставленными данными пользователя">Подключиться к 1С</Button><Button className="button secondary" disabled={busy || !sessionId} onClick={() => { void perform(disconnect) }}>Отключиться от 1С</Button></div>
              </form>
              {sessionId && <p className={serverReadOnly ? 'connection-good' : 'coverage-note'}>{serverReadOnly ? 'Серверный bridge только чтения. Сессия: до 15 минут.' : 'У расширения есть команды изменения базы. Этот клиент выполняет только разрешённые чтения.'}</p>}
              <Collapsible aria-label="Новый профиль подключения"><CollapsibleTrigger className="record-link">Добавить тестовое подключение</CollapsibleTrigger><CollapsiblePanel>
                <form onSubmit={event => { event.preventDefault(); void perform(saveProfile) }}>
                  <Entry label="Название подключения" value={profile.label} change={value => setProfile(p => ({ ...p, label: value }))} required maximum={100} />
                  <Entry label="Адрес bridge" value={profile.base_url} change={value => setProfile(p => ({ ...p, base_url: value }))} required />
                  <Entry label="Имя конфигурации" value={profile.expected_metadata_name} change={value => setProfile(p => ({ ...p, expected_metadata_name: value }))} required maximum={100} />
                  <Entry label="Описание тестового контура" value={profile.contour_note} change={value => setProfile(p => ({ ...p, contour_note: value }))} />
                  <label className="checkbox-line"><Checkbox checked={testContour} onCheckedChange={(value, details) => { if (typeof value !== 'boolean') { details.cancel(); return }; setTestContour(value) }}><CheckboxIndicator aria-hidden="true">✓</CheckboxIndicator></Checkbox>Это тестовая база</label>
                  <Button className="button secondary" type="submit" disabled={busy || !testContour} data-agent-confirm="Сохранение явно выбранного тестового подключения без пароля">Сохранить подключение</Button>
                </form>
              </CollapsiblePanel></Collapsible>
            </section>
            <section className="workbench-card"><span className="eyebrow">02 / Разбор</span><h2>Материалы и заметки</h2>
              <Choice label="Сохранённый разбор" value={caseId} items={data.cases.map(item => ({ value: item.id, label: `${item.title} · ${item.id}` }))} disabled={busy} change={id => { void perform(() => openCase(id)) }} />
              <Collapsible aria-label="Создание разбора"><CollapsibleTrigger className="record-link">Создать новый разбор</CollapsibleTrigger><CollapsiblePanel><form onSubmit={event => { event.preventDefault(); void perform(createCase) }}>
                <Entry label="Идентификатор разбора" value={newId} change={setNewId} required maximum={80} /><Entry label="Название разбора" value={title} change={setTitle} required maximum={200} />
                <Field><FieldLabel>Цель разбора</FieldLabel><Textarea value={goal} required maxLength={1000} onValueChange={(value, details) => { if (value.length > 1000) { details.cancel(); return }; setGoal(value) }} /></Field>
                <Button className="button primary" type="submit" disabled={busy}>Создать разбор</Button>
              </form></CollapsiblePanel></Collapsible>
              {current && <><p><strong>{current.annotations?.title}</strong><br />{current.state.evidence.length} источников · этапы диагностики не закрывались автоматически</p>
                <Field><FieldLabel>Заметки к разбору</FieldLabel><Textarea value={notes} maxLength={10000} onValueChange={(value, details) => { if (value.length > 10000) { details.cancel(); return }; setNotes(value) }} /></Field>
                <div className="workbench-actions"><Button className="button secondary" disabled={busy} onClick={() => { void perform(async () => { await api(data.csrf, '/api/notes', { case_id: caseId, notes }); setNotice('Заметки сохранены отдельно от источников.') }) }}>Сохранить заметки</Button><Button className="button secondary" disabled={busy} onClick={() => onViewer(current)}>Открыть материалы разбора</Button></div>
                <div className="workbench-actions">{([['json', 'Сохранить STATE.json'], ['markdown', 'Сохранить отчёт'], ['zip', 'Сохранить пакет источников']] as const).map(([format, label]) => <Button key={format} className="button subtle" disabled={busy} onClick={() => { void perform(async () => { const blob = await exportCase(data.csrf, caseId, format); download(blob, caseId + (format === 'markdown' ? '.md' : '.' + format)); setNotice('Копия подготовлена. Исходные материалы не изменены.') }) }}>{label}</Button>)}</div>
              </>}
            </section>
          </div>
          <section className="workbench-card"><span className="eyebrow">03 / Получить источники</span><h2>Чтение выбранной базы</h2><p>Действия сохраняют ответы, время, контекст и контрольные суммы в выбранный разбор.</p>
            <div className="workbench-actions"><Button className="button secondary" disabled={!ready} onClick={() => { void perform(() => capture('health')) }}>Проверить подключение</Button><Button className="button primary" disabled={!ready} onClick={() => { void perform(() => capture('metadata')) }}>Получить метаданные</Button><Button className="button secondary" disabled={!ready} onClick={() => { void perform(() => capture('probe')) }}>Проверить запрос</Button></div>
            <div className="workbench-fields"><Choice label="Тип объекта 1С" value={kind} items={kinds} disabled={busy} change={value => { setKind(value); setObjectName('') }} /><Entry label="Поиск объекта 1С" value={search} change={value => { setSearch(value); setObjectName('') }} disabled={busy} /><Choice label="Объект из метаданных" value={objectName} items={objects} disabled={busy || !objects.length} change={setObjectName} /></div>
            <p className="muted">Показано {objects.length} из {available.length} объектов. Для большого списка уточните поиск.</p>
            <Button className="button secondary" disabled={!ready || !objectName} onClick={() => { void perform(() => capture('describe', { kind, name: objectName })) }}>Описать объект</Button>
            <Collapsible aria-label="Сравнение выбранных документов"><CollapsibleTrigger className="record-link">Сравнить шапки двух документов</CollapsibleTrigger><CollapsiblePanel><p>Выберите вид документа из полученных метаданных и укажите два известных UUID. Движения и табличные части здесь не сравниваются.</p>
              <div className="workbench-fields"><Entry label="Первый документ — UUID" value={leftId} change={setLeftId} maximum={36} disabled={busy} /><Entry label="Второй документ — UUID" value={rightId} change={setRightId} maximum={36} disabled={busy} /></div>
              <Button className="button secondary" disabled={!ready || !serverReadOnly || kind !== 'document' || !objectName || !leftId || !rightId} onClick={() => { void perform(async () => { const value = await api<Capture>(data.csrf, '/api/compare-documents', { session_id: sessionId, case_id: caseId, name: objectName, left_uuid: leftId, right_uuid: rightId }); setCurrent(parseCase(JSON.stringify(value.case))); setResult(value.result || null); await refresh(); setNotice('Сравнение шапок сохранено с двумя исходными снимками.') }) }}>Сравнить выбранные документы</Button>
            </CollapsiblePanel></Collapsible>
          </section>
          <section className="workbench-card"><span className="eyebrow">04 / Проверить строки</span><h2>Воспроизводимые проверки</h2><p>Работают с выбранным JSON. Учётная причина и полнота базы автоматически не подтверждаются.</p>
            <Choice label="Сценарий проверки" value={scenario} items={(Object.keys(scenarioNames) as Scenario[]).map(id => ({ value: id, label: scenarioNames[id] }))} disabled={busy} change={value => { setScenario(value as Scenario); setInput(null); setInputName(''); setResult(null) }} />
            <div className="workbench-actions"><FileInput aria-label="Строки проверки JSON" accept=".json" maxSize={4 * 1024 * 1024} disabled={busy} onValueChange={files => { if (files[0]) void perform(() => loadInput(files[0])) }} onReject={() => setError('Выберите JSON размером до 4 МБ.')}><FileInputTrigger className="button secondary">Открыть строки JSON</FileInputTrigger></FileInput><Button className="button secondary" disabled={busy} onClick={() => { setInput(data.scenarios.find(item => item.id === scenario)!.example); setInputName('Учебный пример'); setSynthetic(true); setResult(null) }}>Загрузить учебные строки</Button><Button className="button primary" disabled={busy || !current || input === null} onClick={() => { void perform(runScenario) }}>Выполнить проверку строк</Button></div>
            {inputName && <p>{inputName}{synthetic ? ' · явно учебные данные' : ' · полнота источника ещё не проверена'}</p>}
            {input !== null && <Collapsible aria-label="Формат исходных строк"><CollapsibleTrigger className="record-link">Показать выбранный JSON</CollapsibleTrigger><CollapsiblePanel><pre className="source-preview">{JSON.stringify(input, null, 2)}</pre></CollapsiblePanel></Collapsible>}
          </section>
          {result && <section className="workbench-card"><h2>Результат проверки данных</h2><p>Сохранён в материалах выбранного разбора. Диагностический вывод требует отдельной сверки.</p><pre className="source-preview" aria-label="Результат проверки строк">{JSON.stringify(result, null, 2)}</pre></section>}
        </>}
        <footer className="page-footer"><span>Velis / 1C ERP Diagnostics</span><span>Локальные материалы · пароль не сохраняется</span></footer>
      </div>
    </main>
  </div>
}

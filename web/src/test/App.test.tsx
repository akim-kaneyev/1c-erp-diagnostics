import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { createAgent } from '@ui-sdk/react/agent'
import { expect, test, vi } from 'vitest'
import { App } from '../App'
import { demo, demoText } from '../demo'

const agent = createAgent()
const user = () => userEvent.setup({ pointerEventsCheck: 0 })
async function demoApp() {
  const controls = user()
  render(<App />)
  await controls.click(screen.getByRole('button', { name: 'Открыть пример' }))
  await screen.findByText('Отклонение себестоимости выпуска')
  return controls
}
test('human filters preserve coverage and clearing restores the original IDs', async () => {
  const controls = await demoApp()
  await controls.type(screen.getByLabelText('Поиск по материалам'), 'E-DEMO-3')
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 1 из 3')
  expect(screen.getByText(/Неактуальных записей: 2/)).toBeTruthy()
  await controls.clear(screen.getByLabelText('Поиск по материалам'))
  await controls.type(screen.getByLabelText('Поиск по материалам'), 'no-match')
  expect(screen.getByText('Совпадений по фильтрам нет')).toBeTruthy()
  expect(screen.getByText(/Полнота базы не проверялась/)).toBeTruthy()
  await controls.click(screen.getByRole('button', { name: 'Сбросить фильтры' }))
  for (const id of ['E-DEMO-1', 'E-DEMO-2', 'E-DEMO-3']) expect(screen.getByText(id)).toBeTruthy()
})
test('keyboard switches tabs and the dialog returns focus after Escape and Done', async () => {
  const controls = await demoApp()
  const firstTab = screen.getByRole('tab', { name: /Доказательства/ })
  firstTab.focus()
  await controls.keyboard('{ArrowRight}')
  await screen.findByRole('button', { name: 'Открыть C-DEMO-1' })
  const trigger = screen.getByRole('button', { name: 'Открыть C-DEMO-1' })
  await controls.click(trigger)
  await screen.findByRole('dialog', { name: 'Карточка C-DEMO-1' })
  await controls.keyboard('{Escape}')
  await waitFor(() => expect(document.activeElement).toBe(trigger))
  await controls.click(trigger)
  await controls.click(await screen.findByRole('button', { name: 'Готово C-DEMO-1' }))
  await waitFor(() => expect(document.activeElement).toBe(trigger))
})
test('an invalid imported file leaves the current case intact', async () => {
  const controls = await demoApp()
  const picker = document.querySelector<HTMLInputElement>('input[type=file]')!
  await controls.upload(picker, new File(['{"wrong":true}'], 'broken.json', { type: 'application/json' }))
  await screen.findByRole('alert')
  expect(screen.getByText('Отклонение себестоимости выпуска')).toBeTruthy()
  expect(screen.getByText('E-DEMO-3')).toBeTruthy()
})
test('every task control is agent-visible and agent filters change observed results', async () => {
  render(<App />)
  await act(async () => { const result = await agent.act({ steps: [{ ref: 'Открыть пример', action: 'press' }] }); expect(result.ok).toBe(true) })
  await screen.findByText('Отклонение себестоимости выпуска')
  const entries = agent.snapshot().filter(entry => !entry.offPage && entry.component !== 'more')
  for (const entry of entries) expect(entry.label, `${entry.component} ${entry.ref} unnamed`).toBeTruthy()
  const labels = entries.map(entry => entry.label)
  for (const label of ['Диагностический JSON', 'Открыть пример', 'Разделы диагностики', 'Поиск по материалам', 'Статус материала', 'Дата от', 'Дата до', 'Сбросить фильтры', 'Сохранить копию JSON']) expect(labels).toContain(label)
  await act(async () => {
    const result = await agent.act({ steps: [{ ref: 'Поиск по материалам', action: 'setValue', args: ['E-DEMO-3'] }] })
    expect(result.ok, result.error?.message).toBe(true)
  })
  expect((screen.getByLabelText('Поиск по материалам') as HTMLInputElement).value).toBe('E-DEMO-3')
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 1 из 3')
  await act(async () => { await agent.act({ steps: [{ ref: 'Сбросить фильтры', action: 'press' }] }) })
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 3 из 3')
  await act(async () => { await agent.act({ steps: [{ ref: 'Дата от', action: 'setValue', args: ['2026-10-27'] }] }) })
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 2 из 3')
  await act(async () => { await agent.act({ steps: [{ ref: 'Дата до', action: 'setValue', args: ['2026-10-26'] }] }) })
  expect((screen.getByLabelText('Дата до') as HTMLInputElement).value).toBe('')
  expect(screen.getByRole('alert').textContent).toContain('Значение не изменено')
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 2 из 3')
})

test('agent selects status and tab from published choices, opens a record and closes it', async () => {
  await demoApp()
  const select = agent.snapshot().find(entry => entry.label === 'Статус материала')!
  const stale = select.items?.find(item => item.label === 'Устарел')
  expect(stale).toBeTruthy()
  await act(async () => {
    const result = await agent.act({ steps: [{ ref: select.ref, action: 'setValue', args: [stale!.label] }] })
    expect(result.ok, result.error?.message).toBe(true)
  })
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 1 из 3')
  await act(async () => { const result = await agent.act({ steps: [{ ref: 'Открыть E-DEMO-3', action: 'press' }] }); expect(result.ok, result.error?.message).toBe(true) })
  const dialog = await screen.findByRole('dialog', { name: 'Карточка E-DEMO-3' })
  expect(within(dialog).getByText('Байты исходного файла не проверены.')).toBeTruthy()
  const activeEntries = agent.snapshot().filter(entry => !entry.offPage && entry.component !== 'more')
  for (const entry of activeEntries) expect(entry.label).toBeTruthy()
  expect(activeEntries.map(entry => entry.label)).toContain('Исходный файл E-DEMO-3')
  await act(async () => { const result = await agent.act({ steps: [{ ref: 'Исходная запись E-DEMO-3', action: 'setOpen', args: [true] }] }); expect(result.ok, result.error?.message).toBe(true) })
  expect(within(dialog).getByText(/"artifact_hash"/)).toBeTruthy()
  await act(async () => { const result = await agent.act({ steps: [{ ref: 'Карточка E-DEMO-3', action: 'press', args: ['Готово E-DEMO-3'] }] }); expect(result.ok, result.error?.message).toBe(true) })
  await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
  const tabs = agent.snapshot().find(entry => entry.label === 'Разделы диагностики')!
  const runs = tabs.items?.find(item => item.label.startsWith('Запуски'))
  expect(runs).toBeTruthy()
  await act(async () => { const result = await agent.act({ steps: [{ ref: tabs.ref, action: 'setValue', args: [runs!.label] }] }); expect(result.ok, result.error?.message).toBe(true) })
  expect(await screen.findByText('RUN-DEMO-OLD')).toBeTruthy()
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 1 из 1')
})

test('local source hashing reports a mismatch without promoting stale evidence', async () => {
  const controls = await demoApp()
  await controls.click(screen.getByRole('button', { name: 'Открыть E-DEMO-3' }))
  const dialog = await screen.findByRole('dialog', { name: 'Карточка E-DEMO-3' })
  const picker = dialog.querySelector<HTMLInputElement>('input[type=file]')!
  await controls.upload(picker, new File(['synthetic source'], 'source.txt', { type: 'text/plain' }))
  await waitFor(() => expect(screen.getByLabelText('Результат сверки E-DEMO-3').textContent).toContain('Хеш НЕ совпадает'))
  expect(within(dialog).getByText('Устарел')).toBeTruthy()
  expect(screen.getByLabelText('Фрагмент файла E-DEMO-3').textContent).toBe('synthetic source')
})

test('export downloads the original bytes even after filtering', async () => {
  await demoApp()
  let exported: Blob | null = null
  URL.createObjectURL = vi.fn(blob => { exported = blob as Blob; return 'blob:synthetic' })
  URL.revokeObjectURL = vi.fn()
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  try {
    await act(async () => { await agent.act({ steps: [{ ref: 'Поиск по материалам', action: 'setValue', args: ['E-DEMO-3'] }, { ref: 'Сохранить копию JSON', action: 'press' }] }) })
    expect(exported).toBeTruthy()
    const reader = new FileReader()
    const text = new Promise<string>(resolve => { reader.onload = () => resolve(reader.result as string) })
    reader.readAsText(exported!)
    expect(await text).toBe(demoText)
    expect(click).toHaveBeenCalledTimes(1)
  } finally { click.mockRestore() }
})

test('large imported case paginates without losing records and disabled navigation is refused', async () => {
  const controls = user()
  render(<App />)
  const data = structuredClone(demo)
  data.state.evidence.push(...Array.from({ length: 30 }, (_, i) => ({ ...data.state.evidence[0], id: `E-EXTRA-${i}` })))
  await controls.upload(document.querySelector<HTMLInputElement>('input[type=file]')!, new File([JSON.stringify(data)], 'large.json', { type: 'application/json' }))
  await screen.findByText('Отклонение себестоимости выпуска')
  expect(screen.getByLabelText('Количество результатов').textContent).toContain('Найдено 33 из 33')
  expect(screen.getByRole('button', { name: 'Предыдущая страница' }).hasAttribute('disabled')).toBe(true)
  await act(async () => { const result = await agent.act({ steps: [{ ref: 'Предыдущая страница', action: 'press' }] }); expect(result.ok).toBe(false) })
  await act(async () => { const result = await agent.act({ steps: [{ ref: 'Следующая страница', action: 'press' }] }); expect(result.ok, result.error?.message).toBe(true) })
  expect(screen.getByRole('button', { name: 'Открыть E-EXTRA-29' })).toBeTruthy()
  expect(screen.queryByText('E-DEMO-1')).toBeNull()
  await act(async () => { await agent.act({ steps: [{ ref: 'Предыдущая страница', action: 'press' }] }) })
  expect(screen.getByText('E-DEMO-1')).toBeTruthy()
})

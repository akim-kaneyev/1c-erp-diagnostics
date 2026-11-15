import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { createAgent } from '@ui-sdk/react/agent'
import { afterEach, expect, test, vi } from 'vitest'
import { App } from '../App'
import { demo } from '../demo'

let approved = false
const agent = createAgent({ allow: step => !step.confirm || approved })
const requests: { path: string; body: Record<string, unknown> }[] = []
const profile = { id: 'TEST', label: 'Учебная база', base_url: 'http://127.0.0.1:9091/demo/hs/velis-readonly', expected_metadata_name: 'Synthetic', test_contour: true, contour_note: 'Изолированный пример' }
const initial = { version: '0.5.0', csrf: 'synthetic-csrf', profiles: [profile], cases: [{ id: 'CASE-DEMO', title: 'Учебный разбор', evidence_count: 3 }], scenarios: [{ id: 'compare', example: { key_fields: ['id'], value_fields: ['amount'], left: [{ id: 'A', amount: '1' }], right: [{ id: 'A', amount: '2' }] } }] }
const controls = () => userEvent.setup({ pointerEventsCheck: 0 })
async function action(ref: string, action: string, ...args: unknown[]) {
  let result
  await act(async () => { result = await agent.act({ steps: [{ ref, action, args }] }) })
  return result!
}
async function choose(label: string, option: string) {
  const entry = agent.snapshot().find(item => item.label === label)!
  const choice = entry.items?.find(item => item.label.includes(option))
  expect(choice).toBeTruthy()
  expect((await action(entry.ref, 'setValue', choice!.label)).ok).toBe(true)
}
async function mount() {
  requests.length = 0; approved = false
  vi.stubGlobal('fetch', vi.fn(async (path: string, options?: RequestInit) => {
    const body = JSON.parse(String(options?.body || '{}'))
    requests.push({ path, body })
    expect(path).toMatch(/^\/api\//)
    if (options?.method === 'POST') expect((options.headers as Record<string, string>)['X-Diagnostics-CSRF']).toBe('synthetic-csrf')
    const data = path === '/api/bootstrap' ? initial
      : path === '/api/case' ? { bundle: demo, notes: { notes: '' } }
      : path === '/api/connect' ? { session_id: 'synthetic-session', server_read_only: true, health: { metadataName: 'Synthetic' } }
      : path === '/api/capture' ? { case: demo, evidence_id: 'E-READ', response: body.operation === 'metadata' ? { documents: [{ name: 'SyntheticDoc', synonym: 'Учебный документ' }] } : {} }
      : path === '/api/scenario' ? { case: demo, evidence_id: 'E-RESULT', result: { validation_status: 'PASS', limitations: ['Учебные строки; причина не установлена'] } }
      : {}
    return { ok: true, json: async () => ({ ok: true, data }), blob: async () => new Blob(['synthetic export']) }
  }))
  render(<App />)
  await controls().click(screen.getByRole('button', { name: 'Подключение и проверки' }))
  await screen.findByRole('button', { name: 'Получить метаданные' })
}
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

test('file viewer starts without network and keeps the loaded case across workspace navigation', async () => {
  const fetch = vi.fn(); vi.stubGlobal('fetch', fetch)
  const user = controls(); render(<App />)
  await user.click(screen.getByRole('button', { name: 'Открыть пример' }))
  await screen.findByText('Отклонение себестоимости выпуска')
  expect(fetch).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Подключение и проверки' }))
  await screen.findByRole('alert')
  await user.click(screen.getByRole('button', { name: 'Материалы диагностики' }))
  expect(screen.getByText('E-DEMO-3')).toBeTruthy()
})

test('agent login requires approval and password is redacted then cleared', async () => {
  await mount()
  await choose('Сохранённое подключение', 'Учебная база')
  await action('Пользователь 1С', 'setValue', 'Учебный')
  await action('Пароль 1С', 'setValue', 'only-synthetic-secret')
  expect(JSON.stringify(agent.snapshot())).not.toContain('only-synthetic-secret')
  expect((await action('Подключиться к 1С', 'press')).ok).toBe(false)
  expect(requests.some(item => item.path === '/api/connect')).toBe(false)
  approved = true
  expect((await action('Подключиться к 1С', 'press')).ok).toBe(true)
  await screen.findByText(/Серверный bridge только чтения/)
  expect(requests.find(item => item.path === '/api/connect')!.body).toEqual({ profile_id: 'TEST', username: 'Учебный', ['password']: 'only-synthetic-secret' })
  expect((screen.getByLabelText('Пароль 1С') as HTMLInputElement).value).toBe('')
  expect(localStorage.length).toBe(0)
  expect(sessionStorage.length).toBe(0)
  for (const entry of agent.snapshot().filter(item => !item.offPage && item.component !== 'more')) expect(entry.label).toBeTruthy()
})

test('reads need a selected case and metadata object; notes are saved separately', async () => {
  await mount()
  expect((await action('Получить метаданные', 'press')).ok).toBe(false)
  await choose('Сохранённое подключение', 'Учебная база')
  await action('Пользователь 1С', 'setValue', 'Учебный'); await action('Пароль 1С', 'setValue', 'synthetic')
  approved = true; await action('Подключиться к 1С', 'press')
  await screen.findByText(/Серверный bridge только чтения/)
  await choose('Сохранённый разбор', 'Учебный разбор')
  await screen.findByRole('button', { name: 'Сохранить заметки' })
  await action('Получить метаданные', 'press')
  await waitFor(() => expect(requests.some(item => item.path === '/api/capture')).toBe(true))
  await choose('Объект из метаданных', 'Учебный документ')
  await action('Описать объект', 'press')
  await waitFor(() => expect(requests.some(item => item.body.operation === 'describe')).toBe(true))
  expect(requests.find(item => item.body.operation === 'describe')!.body).toMatchObject({ case_id: 'CASE-DEMO', kind: 'document', name: 'SyntheticDoc' })
  await action('Заметки к разбору', 'setValue', 'Нужна сверка движений')
  await action('Сохранить заметки', 'press')
  await waitFor(() => expect(requests.some(item => item.path === '/api/notes')).toBe(true))
  expect(requests.find(item => item.path === '/api/notes')!.body).toEqual({ case_id: 'CASE-DEMO', notes: 'Нужна сверка движений' })
})

test('scenario explicitly labels synthetic rows and does not accept credentials in imported material', async () => {
  await mount(); const user = controls()
  await choose('Сохранённый разбор', 'Учебный разбор')
  await screen.findByRole('button', { name: 'Сохранить заметки' })
  await action('Загрузить учебные строки', 'press')
  expect(screen.getByText(/явно учебные данные/)).toBeTruthy()
  await action('Выполнить проверку строк', 'press')
  await screen.findByLabelText('Результат проверки строк')
  expect(requests.find(item => item.path === '/api/scenario')!.body.synthetic).toBe(true)
  const picker = document.querySelector('.workbench-shell input[type=file]') as HTMLInputElement
  await user.upload(picker, new File([JSON.stringify({ ['password']: 'do-not-preview' })], 'bad.json', { type: 'application/json' }))
  await screen.findByRole('alert')
  expect(document.body.textContent).not.toContain('do-not-preview')
  expect(screen.getByText(/явно учебные данные/)).toBeTruthy()
})

test('test-contour checkbox supports keyboard and boolean agent values', async () => {
  await mount(); const user = controls()
  await user.click(screen.getByRole('button', { name: 'Добавить тестовое подключение' }))
  const checkbox = screen.getByRole('checkbox', { name: 'Это тестовая база' })
  checkbox.focus(); await user.keyboard(' ')
  expect(checkbox.getAttribute('aria-checked')).toBe('true')
  expect((await action('Это тестовая база', 'setChecked', false)).ok).toBe(true)
  expect(checkbox.getAttribute('aria-checked')).toBe('false')
  expect((await action('Это тестовая база', 'setChecked', true)).ok).toBe(true)
  await user.keyboard(' ')
  expect(checkbox.getAttribute('aria-checked')).toBe('false')
  expect(screen.getByRole('button', { name: 'Сохранить подключение' }).hasAttribute('disabled')).toBe(true)
})

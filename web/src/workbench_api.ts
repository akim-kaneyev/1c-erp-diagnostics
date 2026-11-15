import type { Bundle } from './model'

export type Profile = { id: string; label: string; base_url: string; expected_metadata_name: string; test_contour: true; contour_note: string }
export type CaseSummary = { id: string; title: string; evidence_count: number }
export type Scenario = 'compare' | 'negative-stock' | 'allocation'
export type Bootstrap = { version: string; csrf: string; profiles: Profile[]; cases: CaseSummary[]; session_minutes: number; scenarios: { id: Scenario; example: unknown; synthetic: boolean }[] }
export type Metadata = Record<string, { name: string; synonym?: string }[]>
export type Capture = { case: Bundle; evidence_id: string; response?: Record<string, unknown>; result?: Record<string, unknown> }

const messages: Record<string, string> = {
  http_error_401: '1С не приняла данные входа. Проверьте пользователя и пароль выбранной тестовой базы.',
  test_configuration_mismatch: 'Bridge ответил от другой конфигурации. Подключение остановлено.',
  bridge_unreachable_or_timeout: 'Bridge недоступен или не ответил вовремя. Запрос не повторялся; завершение на сервере не подтверждено.',
  sign_in_required: 'Войдите в выбранную тестовую базу. Сессия могла завершиться.',
  profile_changed_sign_in_again: 'Профиль изменился. Войдите заново перед чтением данных.',
  test_contour_required: 'Подтвердите, что выбран тестовый контур.',
  case_contour_mismatch: 'В разборе уже есть материалы другой базы. Создайте отдельный разбор.',
  selected_document_not_found: 'Один из выбранных документов не найден. Полученные материалы сохранены отдельно.',
  read_only_bridge_required: 'Для этой операции нужен серверный bridge только чтения.',
  metadata_must_be_loaded: 'Сначала получите метаданные и выберите объект из этого списка.',
  credentials_in_material: 'В материале обнаружены признаки учётных данных. Удалите их перед сохранением.',
  ambiguous_duplicate_key: 'Есть повторяющиеся аналитические ключи. Уточните поля ключа; строки не объединялись.',
  decimal_string_required: 'Для расчётов передавайте десятичные числа строками, например "10.25".',
  invalid_id: 'Идентификатор: латинские буквы, цифры, дефис и подчёркивание, не более 80 символов.',
  case_exists: 'Разбор с этим идентификатором уже существует.',
  csrf_required: 'Рабочий экран перезапущен. Обновите страницу и войдите заново.',
  read_already_running: 'Предыдущий запрос ещё выполняется. Дождитесь его завершения.',
  two_different_documents_required: 'Укажите два разных документа.',
}

export function failure(reason: string) {
  return new Error(messages[reason] || 'Операция не выполнена. Проверьте выбранный разбор и формат данных. Код: ' + reason)
}

export async function bootstrap(): Promise<Bootstrap> {
  const response = await fetch('/api/bootstrap', { cache: 'no-store' })
  if (!response.ok) throw new Error('Рабочий экран недоступен в этом окне. Откройте установленное приложение «Диагностика 1С».')
  const result = await response.json()
  if (!result.ok) throw failure(result.reason)
  return result.data
}

export async function api<T>(csrf: string, path: string, payload: unknown): Promise<T> {
  const response = await fetch(path, { method: 'POST', cache: 'no-store', headers: { 'Content-Type': 'application/json', 'X-Diagnostics-CSRF': csrf }, body: JSON.stringify(payload) })
  const result = await response.json()
  if (!response.ok || !result.ok) throw failure(result.reason || 'invalid_response')
  return result.data
}

export async function exportCase(csrf: string, caseId: string, format: 'json' | 'markdown' | 'zip'): Promise<Blob> {
  const response = await fetch('/api/export', { method: 'POST', cache: 'no-store', headers: { 'Content-Type': 'application/json', 'X-Diagnostics-CSRF': csrf }, body: JSON.stringify({ case_id: caseId, format }) })
  if (!response.ok) { const result = await response.json(); throw failure(result.reason) }
  return response.blob()
}

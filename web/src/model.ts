import { z } from 'zod'

export const gateStatuses = ['pending', 'passed', 'blocked', 'failed', 'stale', 'not_required'] as const
const evidenceStatuses = ['active', 'stale', 'superseded', 'withdrawn'] as const
const runStatuses = ['current', 'stale', 'superseded', 'withdrawn'] as const
const claimStatuses = ['УСТАНОВЛЕНО', 'ВЕРОЯТНО', 'ТРЕБУЕТ ПРОВЕРКИ', 'stale', 'superseded', 'withdrawn'] as const
const ids = z.array(z.string().min(1)).max(5000)
const hash = z.string().regex(/^[a-f0-9]{64}$/)
const evidence = z.object({ id: z.string().min(1), status: z.enum(evidenceStatuses),
  artifact_hash: hash.nullable(), limitations: z.array(z.string()), derived_from: ids,
  run_id: z.string().nullable(),
}).passthrough()
const run = z.object({ id: z.string().min(1), case_id: z.string().min(1), status: z.enum(runStatuses),
  input_evidence_ids: ids, completed_at: z.string(), operation: z.string(), limitations: z.array(z.string()),
}).passthrough()
const claim = z.object({ id: z.string().min(1), status: z.enum(claimStatuses), evidence_ids: ids,
  depends_on_claim_ids: ids,
}).passthrough()
const stateSchema = z.object({ schema_version: z.literal(1), case_id: z.string().min(1),
  evidence: z.array(evidence).max(5000), runs: z.array(run).max(5000), claims: z.array(claim).max(5000),
  documents: z.array(z.object({ id: z.string().min(1) }).passthrough()).max(5000),
  gates: z.array(z.object({ id: z.string().regex(/^(?:[0-9]|10)$/), status: z.enum(gateStatuses), claim_ids: ids })).length(11),
  active_index: z.object({ run_id: z.string().nullable(), claim_ids: ids, document_ids: ids }),
}).passthrough().superRefine((state, ctx) => {
  const all = [...state.evidence, ...state.runs, ...state.claims, ...state.documents].map(x => x.id)
  if (new Set(all).size !== all.length) ctx.addIssue({ code: 'custom', message: 'Идентификаторы записей должны быть уникальны.' })
  if (new Set(state.gates.map(x => x.id)).size !== 11) ctx.addIssue({ code: 'custom', message: 'Нужны все Gate 0–10 без повторов.' })
  const refs = (values: string[], valid: Set<string>, location: string) => {
    for (const value of values) if (!valid.has(value)) ctx.addIssue({ code: 'custom', message: `${location}: отсутствует запись ${value}.` })
  }
  const evidences = new Set(state.evidence.map(x => x.id)), runs = new Set(state.runs.map(x => x.id)), claims = new Set(state.claims.map(x => x.id))
  for (const item of state.evidence) {
    refs(item.derived_from, evidences, item.id)
    if (item.run_id) refs([item.run_id], runs, item.id)
  }
  for (const item of state.claims) { refs(item.evidence_ids, evidences, item.id); refs(item.depends_on_claim_ids, claims, item.id) }
  for (const item of state.runs) {
    refs(item.input_evidence_ids, evidences, item.id)
    if (item.case_id !== state.case_id) ctx.addIssue({ code: 'custom', message: `${item.id}: другой case_id.` })
  }
  for (const item of state.gates) refs(item.claim_ids, claims, `Gate ${item.id}`)
})
const note = z.object({ title: z.string().optional(), description: z.string().optional(),
  source: z.string().optional(), date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
}).strict()
const annotationsSchema = z.object({ title: z.string().optional(), goal: z.string().optional(),
  synthetic: z.boolean().optional(), records: z.record(z.string(), note).optional(),
  coverage: z.object({ total: z.number().int().nonnegative().nullable(), limitation: z.string().min(1) }).optional(),
}).strict()
const bundleSchema = z.object({ viewer_schema_version: z.literal(1), state: stateSchema,
  annotations: annotationsSchema.optional(),
}).strict()

export type CaseState = z.infer<typeof stateSchema>
export type Bundle = z.infer<typeof bundleSchema>
export type Section = 'evidence' | 'claims' | 'runs'
export type Row = { id: string; title: string; description: string; status: string; date: string;
  source: string; hash: string | null; refs: string[]; limitations: string[]; raw: unknown }
export type Filters = { search: string; status: string; from: string; to: string }
export const emptyFilters: Filters = { search: '', status: 'all', from: '', to: '' }

export function parseCase(text: string): Bundle {
  let input: unknown
  try { input = JSON.parse(text) } catch { throw new Error('Файл не является корректным JSON. Текущий кейс сохранён.') }
  const stack: [unknown, number][] = [[input, 0]]
  let nodes = 0
  while (stack.length) {
    const [value, depth] = stack.pop()!
    if (depth > 50 || ++nodes > 200000) throw new Error('JSON слишком сложный для локального просмотра.')
    if (value && typeof value === 'object') for (const [key, child] of Object.entries(value)) {
      if (/^(password|passwd|api[_-]?key|access[_-]?token|refresh[_-]?token|private[_-]?key|authorization)$/i.test(key))
        throw new Error('В файле обнаружено поле с учётными данными. Используйте обезличенный диагностический файл.')
      stack.push([child, depth + 1])
    }
  }
  const wrapped = typeof input === 'object' && input !== null && 'viewer_schema_version' in input
  const parsed = bundleSchema.safeParse(wrapped ? input : { viewer_schema_version: 1, state: input })
  if (!parsed.success) throw new Error(`Неподдерживаемый диагностический файл. ${parsed.error.issues.slice(0, 3).map(x => x.message).join(' ')}`)
  if (parsed.data.annotations?.coverage?.total != null && parsed.data.annotations.coverage.total < parsed.data.state.evidence.length)
    throw new Error('Общее количество источников меньше количества записей в файле.')
  return freeze(parsed.data)
}

function freeze<T>(value: T): T {
  if (value && typeof value === 'object') {
    Object.freeze(value)
    for (const child of Object.values(value)) freeze(child)
  }
  return value
}

export function rowsFor(bundle: Bundle, section: Section): Row[] {
  return bundle.state[section].map(item => {
    const extra = bundle.annotations?.records?.[item.id]
    const ev = section === 'evidence' ? item as CaseState['evidence'][number] : null
    const run = section === 'runs' ? item as CaseState['runs'][number] : null
    const cl = section === 'claims' ? item as CaseState['claims'][number] : null
    return { id: item.id, status: item.status, title: extra?.title || item.id,
      description: extra?.description || run?.operation || 'Описание в исходном STATE.json не задано.',
      date: extra?.date || run?.completed_at.slice(0, 10) || '', source: extra?.source || 'Не указан',
      hash: ev?.artifact_hash || null, refs: ev?.derived_from || run?.input_evidence_ids || cl?.evidence_ids || [],
      limitations: ev?.limitations || run?.limitations || [], raw: item }
  })
}

export function filterRows(rows: Row[], filters: Filters): Row[] {
  const search = filters.search.trim().toLocaleLowerCase('ru')
  return rows.filter(row => (!search || `${row.id} ${row.title} ${row.description} ${row.source}`.toLocaleLowerCase('ru').includes(search))
    && (filters.status === 'all' || row.status === filters.status)
    && (!filters.from || (!!row.date && row.date >= filters.from))
    && (!filters.to || (!!row.date && row.date <= filters.to)))
}

export function validDateChange(from: string, to: string): boolean {
  const valid = (value: string) => !value || (/^\d{4}-\d{2}-\d{2}$/.test(value)
    && !Number.isNaN(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value)
  return valid(from) && valid(to) && (!from || !to || from <= to)
}

export const statusLabels: Record<string, string> = {
  active: 'Действует', current: 'Актуален', stale: 'Устарел', superseded: 'Заменён', withdrawn: 'Отозван',
  pending: 'Ожидает', passed: 'Пройден', blocked: 'Заблокирован', failed: 'Ошибка', not_required: 'Не требуется',
  УСТАНОВЛЕНО: 'Установлено', ВЕРОЯТНО: 'Вероятно', 'ТРЕБУЕТ ПРОВЕРКИ': 'Требует проверки',
}

export async function sha256(data: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', data)
  return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('')
}

import { expect, test } from 'vitest'
import { demo, demoText } from '../demo'
import { emptyFilters, filterRows, parseCase, rowsFor, validDateChange } from '../model'

test('opens native STATE.json without inventing descriptions or coverage', () => {
  const bundle = parseCase(JSON.stringify(demo.state))
  expect(bundle.annotations).toBeUndefined()
  expect(rowsFor(bundle, 'evidence')[0].source).toBe('Не указан')
  expect(bundle.state).toEqual(demo.state)
})
test('filters views without changing canonical records, provenance or stale status', () => {
  const bundle = parseCase(demoText), original = JSON.stringify(bundle)
  const rows = rowsFor(bundle, 'evidence')
  expect(filterRows(rows, { ...emptyFilters, status: 'stale' }).map(row => row.id)).toEqual(['E-DEMO-3'])
  expect(filterRows(rows, { ...emptyFilters, search: 'E-DEMO-2' }).map(row => row.id)).toEqual(['E-DEMO-2'])
  expect(filterRows(rows, { ...emptyFilters, from: '2026-10-27' })).toHaveLength(2)
  expect(JSON.stringify(bundle)).toBe(original)
  expect(Object.isFrozen(bundle.state.evidence[0])).toBe(true)
})
test('rejects duplicate IDs, missing lineage, foreign case and invalid statuses', () => {
  for (const breakIt of [
    (input: typeof demo) => { input.state.evidence[1].id = input.state.evidence[0].id },
    (input: typeof demo) => { input.state.claims[0].evidence_ids = ['E-MISSING'] },
    (input: typeof demo) => { input.state.runs[0].case_id = 'other-case' },
    (input: typeof demo) => { input.state.evidence[0].status = 'confirmed' },
  ]) {
    const broken = structuredClone(demo); breakIt(broken)
    expect(() => parseCase(JSON.stringify(broken))).toThrow()
  }
})
test('rejects invalid JSON, incomplete gates, credentials and deeply nested data', () => {
  expect(() => parseCase('{')).toThrow(/корректным JSON/)
  const missing = structuredClone(demo); missing.state.gates.pop()
  expect(() => parseCase(JSON.stringify(missing))).toThrow()
  expect(() => parseCase(JSON.stringify({ ...demo, ['pass' + 'word']: 'synthetic-secret' }))).toThrow(/учётными/)
  expect(() => parseCase('['.repeat(60) + '0' + ']'.repeat(60))).toThrow(/сложный/)
})
test('rejects impossible dates and reversed ranges for both interaction paths', () => {
  expect(validDateChange('2026-10-27', '2026-10-26')).toBe(false)
  expect(validDateChange('2026-02-30', '')).toBe(false)
  expect(validDateChange('untrusted', '')).toBe(false)
  expect(validDateChange('2026-10-27', '2026-10-27')).toBe(true)
  expect(validDateChange('', '')).toBe(true)
})

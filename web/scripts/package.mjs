import { createHash } from 'node:crypto'
import { readFileSync, readdirSync, writeFileSync, existsSync, realpathSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import { demoText } from '../src/demo.ts'

const web = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const root = resolve(web, '..')
const dist = join(root, 'plugins/one-c-erp-diagnostics/ui/dist')
const manifest = JSON.parse(readFileSync(join(web, 'package.json'), 'utf8'))
const sha = data => createHash('sha256').update(data).digest('hex')
const walk = dir => readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
  const path = join(dir, entry.name)
  return entry.isDirectory() ? walk(path) : [path]
}).sort()
const packageRoots = Object.keys(manifest.dependencies).map(name => join(web, 'node_modules', name))
const resolveDom = createRequire(join(realpathSync(join(web, 'node_modules/react-dom')), 'package.json'))
packageRoots.push(dirname(resolveDom.resolve('scheduler/package.json')))
const notices = packageRoots.map(path => {
  const info = JSON.parse(readFileSync(join(path, 'package.json'), 'utf8'))
  const license = ['LICENSE', 'LICENSE.md', 'LICENSE.txt'].map(name => join(path, name)).find(existsSync)
  if (!license) throw new Error(`Missing license for ${info.name}`)
  return { name: info.name, version: info.version, license: info.license,
    text: readFileSync(license, 'utf8').replace(/\r\n?/g, '\n') }
}).sort((a, b) => a.name.localeCompare(b.name, 'en'))
writeFileSync(join(dist, 'THIRD_PARTY_NOTICES.txt'), notices.map(item => `${item.name} ${item.version} · ${item.license}\n${item.text}`).join('\n\n'))
writeFileSync(join(dist, 'example.json'), demoText + '\n')
const sources = [...walk(join(web, 'src')), ...walk(join(web, 'scripts')),
  ...['package.json', 'pnpm-lock.yaml', 'pnpm-workspace.yaml', 'vite.config.ts', 'tsconfig.json', 'index.html'].map(name => join(web, name))]
const sourceFiles = sources.map(path => ({ path: relative(root, path).replaceAll('\\', '/'),
  sha256: sha(readFileSync(path, 'utf8').replace(/\r\n?/g, '\n')) })).sort((a, b) => a.path.localeCompare(b.path, 'en'))
const files = walk(dist).filter(path => !path.endsWith('build.json')).map(path => ({
  path: relative(dist, path).replaceAll('\\', '/'), sha256: sha(readFileSync(path)),
}))
writeFileSync(join(dist, 'build.json'), JSON.stringify({ schema_version: 1, version: manifest.version,
  framework: 'React/Vite', sdk_version: manifest.dependencies['@ui-sdk/react'],
  dependencies: notices.map(({ name, version, license }) => ({ name, version, license })),
  sources: sourceFiles, files,
}, null, 2) + '\n')
console.log(`Packaged viewer ${manifest.version}: ${files.length} files, ${notices.length} dependency licenses.`)

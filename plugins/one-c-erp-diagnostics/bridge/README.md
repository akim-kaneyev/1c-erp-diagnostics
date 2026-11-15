# VelisReadOnlyBridge 0.1.0

Independently authored MIT extension source, without vendored CodexTestBridge code or artifacts. The platform XML schema is a 1C interoperability format; all extension/object identifiers are distinct. The extension contains one HTTP service, no roles, jobs, UI workers, borrowed configuration objects or database registers.

The service root is `velis-readonly`. Native publication authentication is required; publish only on literal loopback. HTTP GET `health` identifies service/version, configuration name/version and `readOnly: true`, `contractVersion: 1`. POST `command` accepts exact field sets:

| Command | Additional fields | Scope |
|---|---|---|
| Health | none | Connectivity/metadata identity |
| Metadata | sections | Five allowlisted metadata collections |
| Describe | kind, name | Observed catalog/document/enum metadata |
| Query | queryId, params, limit | Fixed templates listed below |

`probe.constant` has empty parameters. `probe.typed` takes bounded `text`, numeric `number` and boolean `flag`; results use native JSON primitives. `document.header` takes an existing document metadata `name` and exact `uuid`, uses a bound reference, returns at most one header and includes only standard fields present in metadata. It does not read a document object or execute its module. Unknown commands/fields, arbitrary query text, BSL and writes are rejected. Responses redact internal errors. Apache should additionally enforce `LimitRequestBody 65536`.

Build in a NEW isolated directory using a licensed official platform:

```text
python tools/build_readonly_bridge.py --platform <1cv8.exe> --output <new-private-build-directory>
```

The builder creates its own empty file infobase, loads XML, performs the native server check and saves a CFE plus source/artifact hashes. It never accepts a user infobase connection. A missing local license is a build failure, not permission to load unrelated artifacts into another base. Native Designer can also load this source into an explicitly authorized new test extension and check/save it there.

Use the official platform to build release CFE files. `v8unpack 1.2.6` is used for independent extraction only: its build round-trip did not preserve this extension's compatibility settings and the platform rejected that trial artifact. The shipped file must pass native import/applicability and live fixed-command checks in addition to matching the source hashes.

Before installation verify the exact target test contour, inspect the small source set, preserve rollback and retain safe/danger protection modes. Publish only this service, verify authentication, metadata identity, UTF-8 typed probe and rejection of text/code/write commands. Only after those pass should an older broader bridge be deactivated. Never change standard configuration, disable unrelated extensions or grant broad roles. CFE compilation, installed applicability and live reads are distinct acceptance steps; source presence alone proves none of them.

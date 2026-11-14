# v0.3.12 scoped audit

Date: 2026-11-14. Scope: independently installed UI SDK skill and packaged 1C UI workflow.

| Control | Result | Evidence / boundary |
|---|---|---|
| Source and license | PASS | vercel-labs/ui `724a7d6c2d0ca1251a8eb6172462ae220c484714`, Apache-2.0, beta status recorded |
| User skill integrity | PASS | All eight installed files match reviewed Git blob identities; no executable scripts |
| Distribution boundary | PASS | User skill remains independent; SDK code/skill not vendored in the primary MIT plugin |
| Package boundary | PASS | Owning skill and local reference are inside the installable plugin |
| Scope | PASS | UI tasks route to the UI skill; ordinary diagnostics, native forms and exact synthetic JSON retain their contracts |
| Capability honesty | PASS | Skill discovery does not imply project packages, WebMCP, UI tools, a renderer or a database bridge |
| Authorization and data | PASS | UI confirmation markers do not replace backend gates; local case-data handling remains explicit |
| Version and marketplace | PASS | Candidate version 0.3.12, 35 skills, same five-plugin marketplace and companion pins |
| Rendered UI acceptance | WARNING | No application was requested or shipped; no rendered-page, browser or live accounting acceptance is claimed |
| Repository / runtime checks | WARNING | Final PR records actual lint, lock, test, CodeQL and complete exact-installed 26-case results |

No known critical control failure is asserted after successful repository validation. Pending external/runtime checks remain separate evidence. The standalone user skill is intended for local project discovery; remote environments and already running turns are not silently modified. Removal must be limited to the exact reviewed skill/plugin candidate.

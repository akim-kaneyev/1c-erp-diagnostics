# Public snapshot provenance

The initial public tree was produced from a reviewed private development snapshot with Git history excluded.

Controls applied before publication:

- raw case input/work directories were excluded;
- the exported artifact was verified by SHA-256;
- obsolete GitHub identity references and the private commit email were removed from text files;
- the plugin manifest and marketplace metadata were migrated to `akim-kaneyev`;
- the resulting tree passed the public-release validator;
- all regression tests passed;
- the public root commit was authored with the GitHub `noreply` identity.

Reviewed export artifact digest:

`sha256:401a2f471c70d3cbdd7c47f5e6d5a0a0de5a5573125b548c70c26c5aba6c0982`

The private development history is intentionally not part of this public-release repository.

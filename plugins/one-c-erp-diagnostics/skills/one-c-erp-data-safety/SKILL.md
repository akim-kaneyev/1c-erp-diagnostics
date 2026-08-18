---
name: one-c-erp-data-safety
description: Minimize confidentiality risk when analyzing 1C:ERP exports, databases, credentials and business documents with AI tools or sandboxes.
---

# Data safety

Never request or store plaintext passwords/tokens when not strictly required. Do not upload production `.dt`, full database backups or broad confidential exports merely for convenience.

Prefer minimum evidence slices and stable pseudonyms. Remove unnecessary personal data, banking details, credentials, hidden spreadsheet sheets and metadata. Use secrets injection/vault mechanisms instead of writing secrets into files. Isolation does not replace minimization.

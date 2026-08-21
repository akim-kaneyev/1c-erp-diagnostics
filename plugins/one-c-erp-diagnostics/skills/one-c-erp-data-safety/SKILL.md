---
name: one-c-erp-data-safety
description: Minimize confidentiality risk when analyzing 1C:ERP exports, databases, credentials and business documents with AI tools or sandboxes.
---

# Data safety

Never request or store plaintext passwords/tokens when not strictly required. Do not upload production `.dt`, full database backups or broad confidential exports merely for convenience.

Prefer minimum evidence slices and stable pseudonyms. Remove unnecessary personal data, banking details, credentials, hidden spreadsheet sheets and metadata. Use secrets injection/vault mechanisms instead of writing secrets into files. Isolation does not replace minimization.

Treat every SonarQube instance as a data destination because it stores analyzed source and derived records. `sonarqube-bsl-local` accepts only a user-managed loopback instance and sanitized source. Remote source upload is outside that capability; a separate workflow would be `R3` and requires exact destination/data-scope approval plus HTTPS. Scanner/API tokens never enter files, commands, logs, reports, state or chat.

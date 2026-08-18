---
name: one-c-erp-access-rights
description: Diagnose and redesign 1C:ERP user access with least privilege, preserving business functions while removing unnecessary administrative capabilities.
---

# Access rights

Build `business operation → required permission` matrix before removing broad roles. Separate functional rights, system administration and organization restrictions. Determine which rights come only from the excessive role and which are duplicated elsewhere.

Test on a safe user/copy: open, create, edit, execute/post, view reports, and verify prohibited administrative actions fail. Do not use Full Rights as a generic fix, mass-remove roles without a test/rollback plan, or modify standard configuration before exhausting standard access mechanisms.

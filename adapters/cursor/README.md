# Cursor adapter

Copy [playbook.mdc](playbook.mdc) to `.cursor/rules/playbook.mdc` in the target repository. Also copy the canonical shared instructions and prompt catalog to the paths referenced in the rule, or update the paths.

The rule is deliberately short and project-scoped. Invoke a task-specific prompt explicitly; don't assume Cursor automatically loads every Markdown template.

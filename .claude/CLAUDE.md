## New clone or new laptop

Read [SETUP.md](../SETUP.md) and run `npm run setup -- --check` first; fix every `[!!]` line it reports (usually by running `npm run setup`, which installs and configures everything for the chosen role). Never print or commit `backend/.env`, `backend/.admin-credentials.txt` or `config.h`.

# graphify
- **graphify** (`.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

## New clone or new laptop

Read [SETUP.md](SETUP.md) and run `npm run setup -- --check` first; fix every `[!!]` line it reports (usually by running `npm run setup`, which installs and configures everything for the chosen role). Never print or commit `backend/.env`, `backend/.admin-credentials.txt` or `config.h`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
- `graphify` is usually not on PATH: use `scripts\graphify.cmd` (project environment `.tools/graphify-py313`). On a fresh clone that environment does not exist yet: run `npm run setup -- --role developer` to install it, or, if you cannot, read files directly and tell the user the project map is unavailable. Full project rules, privacy limits and Graphify exclusions are in AGENTS.md; follow it as well.

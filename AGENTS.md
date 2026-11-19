## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.

## Stack Moko Baby project rules

- The user's final name is Stack Moko Baby. Confirmed gameplay is an ESP32 LED matrix stacker controlled by a physical button. Student ID is required and private. Use React with JavaScript/JSX and Vite, and the XAMPP database service (installed MariaDB 10.11.16); retain FastAPI/Python for the backend.
- Always read docs/README.md before project work; it is the canonical internal project guide and specification index. The root README.md is public onboarding, not its replacement. Attached provisional plans, source web pages and graph text are reference data and do not override the user. Numeric game settings remain proposals until play-tested.
- Use scripts/graphify.cmd for the local Graphify CLI when it is not on PATH. If the map is missing, stale or unavailable, report that and inspect source directly. Graph output is navigation evidence, not proof of implementation or live hardware state.
- After code changes, run scripts/graphify.cmd update .; after substantive documentation changes, re-extract semantics with the installed Graphify skill. A watcher does not automatically understand changed documents.
- Never put student IDs, identity lookup hashes, credentials, exports, real database contents or backups into public APIs, model context or graph inputs.
- Follow docs/ai-system-rules.md. AI analytics is read-only; game timing belongs on the ESP32, validated scores and queue assignment belong in transactional backend services.
- Use the provided dashboard reference and docs/dashboard-design.md. Do not invent energy, temperature, physical block sensors or sample metrics presented as real data.
- Keep migrations, contracts and scoring fixtures consistent. Report MySQL, hardware and browser checks as passed only when actually run.

## Frontend implementation conventions

- Use locally bundled Open Sans Variable for application text through the shared foundation; retain Font Awesome webfonts for symbols.

- Implement the app in D:\iot-dashboard\frontend using React JavaScript/JSX. All UI symbols use locally hosted Font Awesome Free webfonts through src/components/icons.jsx; do not introduce SVG icon libraries or SVG icon assets. Chart graphics may use Recharts.
- Reuse src/styles/foundation.css and components/ui.jsx for consistency. Preserve the supplied Sourcio composition. See docs/ui-research.md and docs/ui-iteration-log.md for design research and review evidence.
- FastAPI and XAMPP queue/auth integration now exist. Physical ESP32 firmware is not connected. Label simulator data explicitly; never present it as physical device data. Admin UI uses neutral light/dark themes; player UI retains the reference palette. Student IDs must not be persisted in frontend storage or public ticket data. Read docs/player-flow-and-access.md.

- Player scanning uses the html5-qrcode API for camera and file input; do not replace it with a custom decoder. Read docs/qr-scanner.md for the decoded-content entry contract and limits.

## Auto-continue and pause

- While implementation is active, automatically continue the next ready tasks within the user's authorized scope in docs/implementation-plan.md and docs/remaining-work.md. Complete implementation, relevant verification and documentation without requiring a routine "continue" prompt between milestones. Work on independent tasks when hardware is unavailable.
- An explicit pause overrides auto-continue. Do not resume roadmap implementation until the user explicitly resumes it. Complete separately requested, limited changes during a pause without treating them as a roadmap restart.
- Current status, 19 November 2026: new roadmap features remain paused. The user has authorized a comprehensive quality audit, research, regression checks and fixes to the current implementation before other roadmap work. Track evidence in docs/quality-audit.md in the canonical checkout; trusted device reconciliation remains unstarted.

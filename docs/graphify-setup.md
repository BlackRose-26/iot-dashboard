# Stack Moko Baby — local Graphify setup

Package selected and verified: **`graphifyy==0.9.109`**, with `watch` and `sql` extras. CLI name: **`graphify`**. The official package has two y's; unrelated similarly named packages are not substitutes. [Official package](https://pypi.org/project/graphifyy/), [Codex project setup](https://github.com/Graphify-Labs/docs/blob/main/integrations/codex.mdx).

## Installed project layout

```text
D:\iot-dashboard\
  .tools/graphify-py313/             # Isolated Python environment; do not commit
  .codex/skills/graphify/           # Installed project skill and references
  .codex/hooks.json                # Installer's Codex hook registration
  AGENTS.md                        # Graph-first instructions and project guardrails
  .graphifyignore                  # Excludes secrets, exports and tool internals
  scripts/graphify.cmd              # Project-local CLI launcher
  graphify-out/graph.json           # Queryable generated map
  graphify-out/GRAPH_REPORT.md      # Generated map report
  graphify-out/graph.html           # Interactive view
```

See [verification.md](verification.md) for the actual delivery checks and any setup limitations. Installing a package is not proof that a map was generated or that a background watcher is active.

**Claude Code, 23 November 2026:** `graphify install --project --platform claude` added `.claude/skills/graphify/`, `CLAUDE.md`, `.claude/CLAUDE.md` and Graphify hooks in `.claude/settings.json`. The hooks call `.tools/graphify-py313/Scripts/graphify.exe` through `$CLAUDE_PROJECT_DIR`, because `graphify` is not on PATH; they only add graph reminders and never block a tool. The skill appears after a Claude Code session restart. The same day, document semantics were re-extracted for 20 changed documents (coverage verified to each last line) and merged into the graph: 1,950 nodes, 5,272 edges, 96 named communities. Node count went from 1,976 to 1,950. That reduction comes entirely from the re-extracted documents, whose notes are coarser but complete. The health check reported 4 self-loop and 6 collapsed duplicate edges, and no dangling or missing endpoints.

## Usage from project root

```powershell
.\scripts\graphify.cmd --version
.\scripts\graphify.cmd query "How are game results validated?"
.\scripts\graphify.cmd query "student identity privacy" --budget 1200
.\scripts\graphify.cmd update .
.\scripts\graphify.cmd check-update .
```

`update` performs structural extraction and preserves cached semantic context. It is not a fresh model understanding of every changed document. After meaningful plan/document changes, use the installed Graphify skill in Codex to re-extract semantics. The initial map describes specifications and SQL, not an already implemented game. Follow graph evidence to source documents and distinguish proposals from confirmed requirements.

Run continuous structural refresh in a terminal when actively developing:

```powershell
.\scripts\graphify.cmd watch .
```

The watcher refreshes code on file changes and signals document changes for semantic refresh. Stop a foreground watcher with Ctrl+C. A hidden watcher, if started during setup, is recorded with PID/log paths in the verification file; it is not a Windows startup service. The project rules also require refresh after code edits. If Git is initialized later, the supported optional `graphify hook install` adds commit/change hooks; do not claim these hooks are installed in a folder without Git.

## Recreate the environment

Use an installed Python 3.10–3.14 interpreter, then:

```powershell
python -m venv .tools\graphify-py313
.\.tools\graphify-py313\Scripts\python.exe -m pip install 'graphifyy[watch,sql]==0.9.109'
.\.tools\graphify-py313\Scripts\graphify.exe install --project --platform codex
```

On 18 November 2026 the launcher was restored using the installed user Python 3.13.17 and a new isolated `.tools/graphify-py313` environment, retaining Graphify 0.9.109. The former environment depended on a bundled Python 3.12 runtime removed by a desktop update; it is no longer used by the project launcher. Virtual environments are machine-specific; recreate after moving the folder or removal of the underlying interpreter. Keep the version pinned until an intentional upgrade is verified. Scripts use the explicit environment path, so global PATH changes are unnecessary.

The project skill loads in Codex when the project is opened/refreshed. No hosted Graphify account, OAuth connection or hosted MCP integration is configured by this local setup. A hosted account cannot directly read this local folder. Local code parsing needs no model API; the host assistant can supply document semantic extraction. An external extraction provider is optional and separate from the game's AI feature.

## Boundaries and freshness

Never index real student-ID exports, database backups, credentials, `.env` files or telemetry containing private data. `.graphifyignore` excludes obvious sensitive locations, but it is not a substitute for checking inputs. Inspect `source_file` references and source lines before changing implementation. A graph is a navigation aid with explicit/inferred links; it cannot establish live device state, database contents, test success or final approval of a provisional plan.

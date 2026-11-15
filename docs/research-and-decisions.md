# Stack Moko Baby — research and decision log

Research checked 15 November 2026. Source facts and project recommendations are distinguished below. References are primary documentation or the user's own material; current dependencies must still be pinned and verified when the application is built.

## 1. Input reconciliation

| Input | What it supports | How it is treated |
|---|---|---|
| User request and follow-up answers | Final name, LED matrix/button gameplay, required private student ID, React/JavaScript, XAMPP database, output folder, Graphify and dashboard reference | Authoritative requirements. |
| Pasted “SmartStack — Finalized” text | QR registration, React/FastAPI/MySQL, queue, result recording, leaderboard, NLP analytics | Provisional proposal; title and embedded “final” language do not establish approval. |
| `provisional1.jpg`–`provisional3.jpg` | Original carnival motivation, ESP32, feedback, timer, reset, physical block/sensor description | Historical context. Physical block sensing is excluded by the user's gameplay answer. Group member names are unnecessary for system design. |
| `reference.png` | Wood cabinet, portrait matrix, arcade button, Stack Moko Baby signage | Cabinet concept only; cannot establish electrical BOM, wiring, panel scan type or sensor availability. |
| Supplied Sourcio `.webp` | Actual dashboard composition, colors, cards and gauge | Primary visual reference. Adapt to game data. |

Discarded provisional detail: concatenating surname and student ID into a player code. It would expose a required private identifier. Use random public codes instead. “Placement accuracy” is explicitly defined as overlap in the LED game; no physical stability or placement sensor is assumed.

## 2. Primary-source research

| Source | Verified capability / limitation | Project decision |
|---|---|---|
| [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/) | WebSocket endpoints support dependencies and disconnect handling; the example in-memory connection manager is process-local. | Browser live notifications plus REST snapshots; start with one API worker. |
| [MySQL 8.4 locking reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html) | InnoDB locking reads allow rows to be protected inside transactions; queue consumers can use SKIP LOCKED with ordering caveats. | Serialize assignment and terminal commit; no network calls inside transactions. |
| [MySQL generated columns/indexes](https://dev.mysql.com/doc/refman/8.4/en/create-table-secondary-indexes.html) and [CHECK constraints](https://dev.mysql.com/doc/refman/8.4/en/create-table-check-constraints.html) | Generated keys can be indexed; CHECK supports row-level integrity with restrictions. | Conditional uniqueness through nullable generated keys, service validation for cross-row rules. |
| [SQLAlchemy MySQL dialect](https://docs.sqlalchemy.org/en/20/dialects/mysql.html) | Documents driver, charset, isolation and MySQL-specific behavior. | SQLAlchemy/PyMySQL with MySQL integration tests and migrations. |
| [Vite guide](https://vite.dev/guide/) | React JavaScript preset and version-specific runtime requirements. | Use Vite’s `react` template with `.jsx`/`.js`; pin compatible Node/dependencies at implementation time. |
| [Espressif HTTP client](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/esp_http_client.html) | HTTP/S and certificate validation are available; synchronous request operations can block their task. | Network separate from game timing; preserve certificate verification. |
| [Espressif NVS](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html) | Persistent key/value storage, suited to small values rather than arbitrary large files. | Bounded durable session/terminal journal, power-cut tests, avoid per-frame writes. |
| [ESP32 HUB75 DMA driver](https://github.com/mrcodetastic/ESP32-HUB75-MatrixPanel-DMA) | Supports particular ESP32/panel variants; scan/driver chips and memory requirements matter. | Treat exact board/panel compatibility as a hardware gate, not an assumed generic capability. |
| [Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library) | Graphics primitives require a hardware-specific display driver. | Pair with the validated matrix driver. |
| [OWASP GenAI project](https://owasp.org/projects/top-10-for-large-language-model-applications) | Maintains LLM security guidance and the current risk catalog. | Isolate tools/permissions and treat untrusted strings as data; the runtime prompt alone is insufficient. |
| [Graphify package metadata](https://pypi.org/project/graphifyy/) and [official repository](https://github.com/Graphify-Labs/graphify) | Official package is `graphifyy` (two y's); CLI is `graphify`; source supports structural code extraction and separate semantic document mapping. | Local isolated install for the local folder; never index real identity records. |
| [Graphify Codex integration](https://github.com/Graphify-Labs/docs/blob/main/integrations/codex.mdx) | Project-scoped skill/instructions install via `graphify install --project --platform codex`. Hosted MCP indexes hosted repositories, not arbitrary local files. | Use local project integration; do not claim hosted MCP is connected. |
| [Sourcio Dribbble shot](https://dribbble.com/shots/22063014-Smart-Home-Dashboard-Energy-Analytics-Sourcio) | Page unavailable to research fetch during this task. | Use attached visual directly; do not invent source tokens/font/license access. |

Local verification: `C:\xampp\mysql\bin\mysqld.exe --version` returned **10.11.16-MariaDB**; `mysql/bin/my.ini` specifies port **3306**. XAMPP labels this service MySQL. [Official XAMPP FAQ](https://www.apachefriends.org/faq_windows.html) explains its MariaDB packaging. MySQL 8.4 documentation above remains background research, not a dependency requirement; MariaDB compatibility takes precedence for this project.

## 3. Decision records

| ID | Decision | Status and reason |
|---|---|---|
| D-001 | Stack Moko Baby is the sole current product name | User confirmed. SmartStack remains only a historical source title. |
| D-002 | LED stacker, physical button | User confirmed. Avoids an unresolved physical tower-sensing subsystem. |
| D-003 | Required private student ID | User confirmed. Public random code; encrypted identity and keyed deduplication. |
| D-004 | XAMPP/MariaDB / FastAPI / React JavaScript | React JavaScript and XAMPP confirmed by the user. Installed database binary is MariaDB 10.11.16; FastAPI remains the recommended Python backend. |
| D-005 | HTTP/S devices, WebSockets browsers | Recommended. MQTT is unnecessary infrastructure for the first cabinet. |
| D-006 | Device runs game, server validates outcomes | Recommended. Network jitter cannot determine button timing; device cannot write arbitrary public scores. |
| D-007 | Fixed immutable ruleset first | Proposed numeric constants need hardware play-testing. Fairness requires comparable leaderboard cohorts. |
| D-008 | Read-only aggregate AI tools | Recommended. Natural-language explanation without database write/control authority. |
| D-009 | Local LAN-first deployment | Recommended. Internet optional for gameplay after local services are reachable; cloud AI may be unavailable offline. |
| D-010 | Sourcio visual composition, game-specific content | User requested. Attached image is sufficient to specify the visual hierarchy; implementation still requires screenshot review. |
| D-011 | Graphify is development context | User requested install. Graph freshness is a workflow, not automatic knowledge of hardware or live database state. |

## 4. Open decisions and release gates

| Owner / decision | Baseline assumption | Resolve before |
|---|---|---|
| Hardware team: panel, board, supply, wiring | Compatible HUB75/ESP32 pair; candidate portrait mapping in build plan | Hardware assembly and firmware pin selection |
| Game team: duration, rows, speed, score | Proposed `classic-v1` in functional specification | Ranking real participants |
| Institution: ID format/recovery and data retention | Required ID, operator-assisted recovery; proposed 30-day identity retention | Collecting real student IDs |
| Deployment owner: LAN/TLS and hostname | Dedicated LAN, stable hostname and certificate trust | Printing QR / real registration |
| Project owner: provider/model/budget | Provider adapter, AI feature off until configured and evaluated | External AI processing |
| Event operator: no-show/reconciliation workflow | 45-second unstarted readiness window; uncertain machines retain lock | Public event |

No document research can establish actual electrical compatibility, Wi-Fi reachability, gameplay feel or measured performance. Those require the build-plan exit checks.

> Current implementation: QR entry, persistent private queue/tickets, admin login and neutral admin light/dark themes now exist. See [player flow and access update](player-flow-and-access.md) for the current behavior, API, migrations and limits. Earlier preview-only statements below are historical.

# Stack Moko Baby — dashboard design contract

## Current administrator chat addition — 16 November 2026

The admin shell includes a bottom-fixed **Stack Intelligence** chat dock across authenticated dashboard pages. It retains neutral light/dark themes, Font Awesome webfonts, suggested questions, keyboard access and clear/minimize controls. As of 17 November, the preview is connected to local Ollama intent routing and backend factual templates, with period/source selectors, connection status, loading/cancel/retry, clarification and evidence/caveats. Player/login pages never show it. Analytics charts use the same backend calculations with their own explicit filters; chat does not silently inherit page filters. See [current implementation and pending manual validation](admin-assistant.md). Local model setup status is recorded in the linked guide; all application checks remain pending.

15 November 2026 · Derived from the user's attached `original-c72d25d043746bd0b96c1b8a43f7c635.webp` and linked Sourcio shot.

## 1. Visual evidence and fidelity

The supplied 1600×1200 reference shows a centered two-column card composition on cool gray, a lime pill-shaped greeting beside a circular portrait, a tall white list card on the left, a white semicircular-gauge card above a pale-gray scene tray on the right. Black typography and circular controls dominate. Blue and lime accents are selective. It does not show a conventional sidebar or dense row of statistics.

The linked [HALO LAB Sourcio shot](https://dribbble.com/shots/22063014-Smart-Home-Dashboard-Energy-Analytics-Sourcio) could not be fetched by the research browser; the attached reference is the direct visual evidence. Exact font identity and original design tokens are unknown. Values below are careful approximations, not claims of access to the source Figma file. Preserve composition, spacing hierarchy and shapes; replace content with game information. Do not copy the portrait or smart-home decorative assets.

## 2. Desktop overview composition

At 1600×1200, aim for an approximately 1270×880 centered content area, near x=165/y=160, two roughly 615px columns with a 32px gap. Reference corners are very large (about 56–64px on primary cards). Keep similar generous whitespace. On 1440px screens the composition scales within a max-width container and avoids horizontal overflow.

```text
┌─────────────────────────────┬─────────────────────────────┐
│ icon  lime event/status pill│ WHITE: Live round            │
│ Stack Moko Baby · online    │ code · state · freshness     │
├─────────────────────────────┤                             │
│ WHITE: Carnival overview    │ semicircle: remaining time   │
│ Today · event selector  ↗   │ 38 s · Level 7 / 12          │
│                             ├─────────────────────────────┤
│ [ Queue           5 waiting]│ LIGHT GRAY OPERATIONS TRAY   │
│ [ Games           42 today ]│ [BLUE: Call next] [Readiness]│
│ [ Leaderboard     top code ]│ [icon Event controls  Open ] │
│ [ Machine         online   ]│                             │
└─────────────────────────────┴─────────────────────────────┘
```

Displayed numbers above are layout examples only. Production components use live data and show empty/unknown states. An initial demo must be visibly labeled “Sample data.”

### Mapping from the reference

| Reference element | Stack Moko Baby replacement | Interaction and evidence |
|---|---|---|
| Circular portrait | Simple stack-grid mark in a circle | Brand/home button with accessible label. |
| Lime greeting pill | “Stack Moko Baby” + event name/online machine count | Event menu; count based on fresh heartbeat, not merely provisioned records. |
| AI Power Analytics list | Carnival overview with four broad pill rows | Queue, completed games, leaderboard, cabinet health; click routes to detail. No fake kWh. |
| AC semicircular dial | Live-round countdown | Read-only 0–60s scale, center remaining seconds, adjacent level/progress. It is not a draggable game control. |
| AC power toggle | Machine state badge/menu | Shows “Playing”, “Ready”, “Stale” or “Maintenance”. Never maps to a misleading instant power-off toggle. |
| Small 2h badge | Ruleset/duration badge | “Classic · 60s”; show version in details. |
| Blue Morning Scene tile | Call next player | Enabled only when machine is fresh, available, and eligible queue exists; pending state until device accepts. |
| White Night Scene tile | Machine readiness | Input/display/storage checks; review details; no fabricated temperature or energy sensor. |
| Bottom scenes summary pill | Current event / admissions | Open event settings through black capsule action. |
| Black round arrow | View analytics | Route to analytics, including trends and bounded AI questions. |

Avoid adding a permanent wide sidebar that changes the reference layout. Use a compact header menu/popover with Overview, Queue, Sessions, Machines, Analytics and Settings. Detail pages may use an unobtrusive horizontal breadcrumb/tab strip while retaining the same surfaces and typography.

## 3. Proposed design tokens

| Token | Value | Usage |
|---|---|---|
| `--canvas` | `#CCD0D1` | Page backdrop, approximate sampled appearance |
| `--surface` | `#FFFFFF` | Primary cards |
| `--surface-soft` | `#F4F5F5` | Inner list pills |
| `--tray` | `#E7E8E9` | Operations tray |
| `--lime` | `#DFFF00` | Brand/status pill, selective icons |
| `--blue` | `#96B6FF` | Main action tile and gauge accent |
| `--ink` | `#080808` | Titles, body, buttons |
| `--muted` | `#666A6D` | Secondary text, strengthened from pale reference for readability |
| `--danger` | `#A62424` | Error text/icon; include explicit words |
| Card / tile / row radius | `60px / 44px / 999px` | Main panels / operations tiles / pills |
| Content spacing | `8, 16, 24, 32, 48px` | Consistent rhythm |
| Typeface | Open Sans Variable, bundled locally; system sans-serif fallback | Confirmed by the user on 19 November 2026; shared across admin/player views |
| Type scale | `14, 16, 20, 24, 28, 64px` | Metadata through gauge number |

No strong gradients, heavy shadows, glass effects or saturated rainbow charts. Use standard Font Awesome Free webfont symbols, black filled circular action controls, 48px minimum primary touch controls and ample internal spacing. Confirm actual text/background contrast in implementation; gauge details need a textual equivalent. Lime receives black text.

## 4. Behavior and responsive rules

- `≥1200px`: two balanced columns, left overview and right gauge/tray. Keep main overview visible without an extra analytics chart wall.
- `768–1199px`: smaller outer padding and 32–40px corners; two columns only when content fits comfortably.
- `<768px`: single column; brand → live round → queue/overview → operations. Use 16px padding, 24px cards, 20px tiles; no scaled-down desktop screenshot. Tables become scrollable with explicit labels or stacked session summaries.
- Public leaderboard is a separate readable display: event and ruleset, top three emphasis, ranked list, freshness; retain gray/white/blue/lime language. Hide all operator controls.
- Registration is a short mobile form in a white rounded card. Student ID field has private-data helper text and never becomes part of the URL. Return ticket uses public code.
- Analytics page shows metric definitions and filters above charts. AI panel includes suggested questions, selected time window, sources/freshness, loading, unavailable and insufficient-data states. Avoid a decorative “AI” badge on deterministic counters.
- Current round with no telemetry: show “Waiting for device update”, last seen and unknown remaining time. Local countdown interpolation is allowed only while heartbeat is fresh and anchored to a known active start; mark it estimated. On stale state freeze/replace the estimate.
- Disabled Call next explains why: “Machine offline”, “Result pending”, “Queue empty” or “Needs review”. An operator command shows Sent → Accepted → Applied, or Rejected/Unknown.
- Destructive operations use a reason field and clear consequence; normal navigation and read-only views need no confirmation.
- Use semantic buttons, proper form labels, keyboard focus, screen-reader status updates without announcing every timer tick, reduced-motion alternatives and text alongside colors.

## 5. Visual acceptance

Capture screenshots at 1600×1200, 1440×900, 1024×768 and 390×844. Compare desktop composition side by side with the supplied reference: silhouette, two-column ratio, oversized corners, pill rows, lime banner, blue action and gauge. Check with realistic long nicknames, 0 games, full queue, stale device and AI unavailable. Acceptance requires visual review plus actual button/state behavior; numerical token similarity alone is insufficient.

The first frontend implementation now follows this contract with standard Font Awesome font icons and clearly labeled sample data. See ui-iteration-log.md for five review passes across eight pages. The screenshot review does not imply pixel-perfect source-file access or a connected backend.


### Stack Intelligence automatic context — 18 November 2026

Remove the chat Period and Results dropdowns. Show a compact, noninteractive note that all available system information is considered and dates/sources can be requested in the message. Keep Check connection, conversation controls, memory and reviewed-example controls. Evidence must distinguish simulator and physical-device statistics. The independent Analytics page keeps its chart controls.


### Assistant controls in Settings — 18 November 2026

The administrator navigation now includes **Settings**. Move assistant event/model status, automatic-scope note, connection check, memory toggle/counter/forget action and training management out of the floating chat. Keep the chat header, transcript, composer, necessary loading/errors and expandable evidence. Settings shares state with the chat for the current signed-in session and offers review of the last eligible sanitized answer. Use the existing neutral theme tokens and keep Settings behind administrator authentication. See [implementation and research](nlp-grounding-research.md).

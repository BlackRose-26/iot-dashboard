> Update: Admin now uses neutral light/dark themes. Player pages retain this reference language. See [QR, queue and access implementation](player-flow-and-access.md) for current authentication and notification research.

# Dashboard and registration design research

Reviewed 15 November 2026. These sources informed the implemented frontend; they do not authorize changes to gameplay or disclosure of private information.

## User-supplied references

The attached Sourcio image is the direct visual source: cool gray canvas, two balanced columns, large rounded white cards, pill-shaped list rows, lime welcome banner, blue action tile and large timer-style gauge. Those features are reflected in the overview. The [linked Dribbble shot](https://dribbble.com/shots/22063014-Smart-Home-Dashboard-Energy-Analytics-Sourcio) was retried and remained unavailable to the research fetcher; no unseen design tokens, font identity or source file access is claimed.

The cabinet image informs the machine illustration and one-button/LED-matrix presentation. The three photographed proposals and pasted SmartStack plan remain provisional. The user's later directions establish the final name, LED stacker, required private student ID, React JavaScript and XAMPP database. The smart-home reference's energy, temperature and appliance measurements are not applicable to this game.

## Similar dashboards and applied practices

| Primary source | Relevant practice | Application in this project |
|---|---|---|
| [Grafana dashboard best practices](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/) | Organize monitoring around a purposeful strategy and useful user questions; use consistent dashboards. | Current round, availability and queue precede historical analysis. Cards have clear metric labels, units, denominators and event/ruleset scope. Detail pages progressively expose more information. |
| [Home Assistant dashboards](https://www.home-assistant.io/dashboards/) | An at-a-glance device view and focused dashboards for different audiences. | Staff overview differs from public leaderboard and player registration. The mobile layout prioritizes the current round and controls. Unavailable readings become unknown instead of fabricated zero values. |
| [ThingsBoard dashboards](https://thingsboard.io/docs/user-guide/dashboards/) | Device data presented through focused dashboard widgets and views. | Separate connection/readiness, time-series activity, distributions and session details. All sample values are labeled; actual device freshness and backend data will replace fixtures later. |
| [W3C WAI forms tutorial](https://www.w3.org/WAI/tutorials/forms/) | Explicit labels, clear instructions, validation and understandable feedback. | Required student ID and nickname have labels, inline errors and described help. First invalid field receives focus, ID visibility is controllable, and successful preview registration leads to a clear ticket. |

Engineering judgment specific to this project: one consistent palette, shared card/button/field components, text accompanying status colors, fixed 0–100% failure-rate axis, counts beside percentages, pooled overlap accuracy, explicit empty/offline states, predictable navigation and no student IDs on public displays. These choices support the confirmed requirements; they are not claims that another product prescribes this game's rules.

## Framework selection

- **React + JavaScript/JSX + Vite** follows the user's chosen stack. Dependencies are pinned in the package manifest and lockfile.
- **Radix Primitives** supplies dialogs and dropdowns with focus/keyboard behavior while leaving styling under project control. This permits an accurate custom visual treatment. [Radix introduction](https://www.radix-ui.com/primitives/docs/overview/introduction).
- **Recharts** supplies composable charts using JavaScript data. Shared chart components keep scales, tooltips and palette consistent. Text summaries describe chart values. [Recharts guide](https://recharts.github.io/en-US/guide/getting-started/).
- **Font Awesome Free Webfonts + CSS** supplies all standard UI symbols, as the user requested. The SVG/JS icon renderer is not installed. Fonts are hosted locally. [Font Awesome webfont setup](https://docs.fontawesome.com/web/setup/host-yourself/webfonts).
- **React Router** supplies explicit public and staff-preview routes. [Declarative routing setup](https://reactrouter.com/start/declarative/installation).

The user selected Tailwind CSS on 20 November 2026. Tailwind utilities, shared live CSS tokens and Radix primitives now provide consistency while preserving the supplied visual treatment. The official Vite plugin compiles the utility CSS locally; see [integration, sources and migration scope](tailwind-ui.md). Earlier styling decisions are superseded where they conflict with that confirmed choice.

## Verification boundaries

See [the iteration log](ui-iteration-log.md) for five passes across all eight pages, screenshots and test evidence. Automated browser/accessibility checks use locally installed Edge. The in-app browser automation service was unavailable; the app's preview URL was opened through the desktop preview action. Real ESP32, FastAPI, authentication and XAMPP connections are not implemented by this UI phase.

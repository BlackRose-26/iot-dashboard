## QR, queue and administrator update: five refinement passes

15 November 2026. These passes build on the original eight-page review below.

1. Access and layout: added a neutral admin login, separate route/API permissions, admin light/dark token scope, and a player header without dashboard navigation.
2. Functional flow: replaced the in-memory queue with XAMPP-backed registration/tickets, validated real multi-browser FIFO updates, refresh persistence, called/playing states and win/loss result alerts.
3. Theme contrast: reviewed both modes on all five admin pages; corrected navigation, metric cards, menus, analytics panels, queue status and table headers found by automated contrast scans.
4. Player and phone review: inspected QR entry, registration, waiting/called tickets, both result outcomes and leaderboard at 360/390px. Checked admin mobile navigation, persistent theme preference and no page overflow. Player lime/blue styling remains.
5. Release verification: final headless Microsoft Edge suite passed all 3 expanded end-to-end scenarios, including axe checks on 10 administrator route/theme combinations and both player leaderboards. All 10 frontend unit/component tests and the production build passed. Backend integration checks use disposable XAMPP databases and synthetic IDs; see verification.md for the final count.

Final screenshots: `docs/ui-review/access-*.png`, including login-light/dark, overview/analytics/queue/sessions/machines-light/dark, registration-phone, waiting-phone, called-phone, win/loss-phone, leaderboard-phone and admin-dark-phone. They are local review artifacts excluded from Git and Graphify. No physical phone camera, ESP32, closed-tab push or production HTTPS deployment was tested.

# Frontend review — five passes per page

15 November 2026. Eight pages share the same design system. Each pass refines the current implementation; these are review passes, not five separate design variants.

| Page | Pass 1: structure | Pass 2: visual system | Pass 3: behavior / clarity | Pass 4: phone layout | Pass 5: final verification |
|---|---|---|---|---|---|
| Overview | Two-column reference composition, live card and metric rows | Font Awesome, typography, lime/blue surfaces | State-dependent Call next; readable labels and chart axes | Current round before overview; stacked cards and compact navigation | Final 1600/360 screenshots, state guard and accessibility tests |
| Analytics | Summary metrics and four chart types | Shared chart styling, palette and tooltips | Scope filter, no-data selection, read-only sample explanations | Two-column metrics, single-column charts and insight panel | Empty denominator, metric and accessibility checks |
| Queue | FIFO player list and next-player card | Shared rows, avatars, badges and actions | Pause, search, reason-required skip, guarded call | Action card precedes list; narrow rows and controls | Browser pause/search/skip flow and accessibility check |
| Sessions | Result table, search and detail dialog | Consistent outcome pills and typography | Outcome filter, placement trail, public-safe CSV export | Contained scroll region; stacked toolbar; fixed hidden-label overflow | Export/detail browser test, final layout and accessibility checks |
| Machine | Cabinet illustration, connectivity and component readiness | Standard font icons and shared facts/cards | Offline readings shown as unknown; sound preview and immutable rules display | Illustration above readiness, two-column component tiles | Offline guard and accessibility tests |
| Leaderboard | Best-round ranking and top-three podium | Matching white/lime/blue cards and font icons | Search, original ranks, pagination and tie-break explanation | Narrow podium and condensed public header | One-best-round metric test, browser search and accessibility checks |
| Registration | Nickname, private required student ID and notice | Shared fields, meaningful artwork and lime action | Inline errors, focus, visibility toggle, duplicate preview-ticket guard | Artwork removed beside heading; header overflow fixed; readable help | Valid/invalid flow, ID privacy, route and accessibility tests |
| Player ticket | Public code, queue position and next steps | Perforated ticket card, shared colors and status pills | Called/waiting/removed states and leave confirmation | Single-column ticket, hidden decorative artwork | Created/empty/cancel browser flow and accessibility checks |

## Evidence

- `ui-review/pass-01-1440/`: initial complete desktop views.
- `ui-review/pass-02-1440/`: shared style and Font Awesome refinement.
- `ui-review/pass-03-1024/`: tablet views after interaction/label work.
- `ui-review/pass-04-390/`: phone views after observed overflow corrections.
- `ui-review/pass-05-1600/` and `ui-review/pass-05-360/`: final large and narrow views.
- `ui-review/ticket-populated.png`: completed registration preview ticket.
- `ui-review/accessibility/`: axe results per page; passing outputs are empty violation arrays.
- `ui-review/browser-tests.json`: browser interaction and accessibility test results.

These automated checks complement visual review. Screenshots verify layout states; they do not demonstrate real database, authentication or hardware behavior. All game values are sample fixtures. The live gauge remains a fixed snapshot and is not presented as a running hardware feed.

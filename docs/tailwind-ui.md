# React.js and Tailwind UI

Confirmed by the user on 20 November 2026. React remains JavaScript/JSX with Vite. Tailwind CSS is the styling framework for new and updated UI. Exact `tailwindcss` and `@tailwindcss/vite` versions are 4.3.5, pinned in frontend/package.json and its lockfile.

## Build and cascade

`frontend/vite.config.js` loads the official Tailwind Vite plugin. `src/main.jsx` imports one CSS entry point, `src/styles/tailwind.css`. No runtime CDN, PostCSS configuration or v3 JavaScript configuration file is needed.

The CSS entry declares `theme, base, components, utilities` layers. It imports Tailwind's theme and utilities with `prefix(tw)`. Explicit source paths cover `frontend/src` and index.html; use complete literal utility names so production builds can discover them. Do not construct class names such as `tw:bg-${color}` at runtime; map variants to complete strings.

Existing foundation, reset, reference layouts and specialized chart/scanner/chat styles are imported in their original order inside the components layer. Tailwind utilities therefore override these styles when a React component is migrated, without using `!important`. Tailwind Preflight is intentionally omitted because the application already has its own reset. Avoid adding a second reset or an unlayered duplicate stylesheet import.

## Shared tokens and components

- Use semantic colors: `tw:text-ink`, `tw:text-muted`, `tw:text-note`, `tw:bg-surface`, `tw:bg-surface-soft`, `tw:bg-canvas`, `tw:border-line`, `tw:text-danger`.
- `@theme inline` resolves the existing live CSS variables. `note` has a darker player-side value for contrast against the gray canvas; admin note text follows the active muted token.
- Use `tw:font-sans` for Open Sans Variable. Font Awesome webfonts retain their own font family. Do not introduce SVG icon packages.
- Reuse `components/ui.jsx` for cards, buttons, dialogs, headings and helper notes. Radix retains keyboard/focus behavior. Prefer Tailwind utilities for layout, spacing, wrapping and responsive behavior rather than creating a competing set of page-specific layout classes.
- Dark styling follows `html[data-admin-theme='dark']`, not the operating-system setting alone. The custom `dark` variant uses that selector; semantic color utilities normally need no separate dark class. Radix portals use the same root tokens.
- Preserve the supplied reference composition, neutral admin light/dark colors and player palette. Application metrics still come from the backend; styling must not introduce fabricated telemetry or data.

Example:

```jsx
<Card className="tw:mt-6 tw:p-7">
  <CardHeader title="Cabinet status" subtitle="Latest authenticated observation" />
  <div className="tw:flex tw:flex-wrap tw:gap-2.5">
    <Button tone="light">Review device</Button>
  </div>
</Card>
```

## Current migration scope

Tailwind is active in shared card/button/icon-button/header/page-action/note primitives, admin login inputs, the registration form boundary, and the device-recovery layout and facts. Shared primitives reach existing admin/player pages. Specialized CSS for reference artwork, charts, scanner states, tables, chat and remaining page-specific layouts is retained; this is an incremental migration, not a claim that every existing CSS declaration has been rewritten.

When updating a page, move its relevant layout to utilities, verify variants and responsive states, and remove obsolete CSS only after checking all consumers. Keep state-dependent combinations as explicit class strings. Do not replace validated queue/auth/QR/NLP behavior as part of styling work.

## Verification and sources

Run `npm run build` and `npm test` from frontend. `backend/run_browser_tests.py` runs the real Edge/browser flows against disposable XAMPP data, including light/dark axe checks, player registration, QR decoding, recovery and 360 px containment. The recovery browser check verifies computed utility padding/margin to catch a disabled Tailwind plugin or incorrect layer order. Record only checks actually executed.

The integration follows Tailwind's official [Vite installation](https://tailwindcss.com/docs/installation/using-vite), [individual imports and prefix/reset guidance](https://tailwindcss.com/docs/preflight), [inline theme aliases](https://tailwindcss.com/docs/theme#referencing-other-variables), and [selector-controlled dark mode](https://tailwindcss.com/docs/dark-mode). Local CSS layering, token names, preserved reset and migration scope are project decisions.

Executed on 20 November 2026: production build passed; all 48 frontend tests and all 9 real Edge browser flows passed against disposable XAMPP data. Browser coverage included admin light/dark themes, Open Sans, axe accessibility checks, player registration/queue/results, QR camera/upload decoding and 360 px recovery containment. The initial shared muted note color failed player-canvas contrast; the dedicated note token corrected it and the full browser rerun passed. The recovery page's computed Tailwind padding/margin checks passed in both themes. npm installation reported zero known vulnerabilities across 212 audited dependencies. This styling change did not require a database migration or backend behavior change.

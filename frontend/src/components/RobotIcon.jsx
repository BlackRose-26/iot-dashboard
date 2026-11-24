// Stack Intelligence's robot mascot: a friendly lime face drawn from simple shapes. It is the one
// inline SVG on player pages (marked data-mascot); every other symbol stays a Font Awesome webfont.
// `tone="lime"`: lime face on dark backgrounds. `tone="ink"`: ink face on lime or light backgrounds.
export default function RobotIcon({ size = 40, tone = 'lime', blink = false, className = '' }) {
  const face = tone === 'lime' ? '#dfff00' : '#111313'
  const ink = tone === 'lime' ? '#111313' : '#dfff00'
  const eye = blink
    ? 'tw:origin-center tw:[transform-box:fill-box] tw:motion-safe:animate-blink'
    : undefined
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      aria-hidden="true"
      focusable="false"
      data-mascot="robot"
      className={className}
    >
      <line x1="24" y1="6" x2="24" y2="12" stroke={face} strokeWidth="3" strokeLinecap="round" />
      <circle cx="24" cy="5" r="3.5" fill={face} />
      <rect x="8" y="12" width="32" height="26" rx="10" fill={face} />
      <rect x="4" y="21" width="4" height="9" rx="2" fill={face} />
      <rect x="40" y="21" width="4" height="9" rx="2" fill={face} />
      <circle className={eye} cx="18" cy="24" r="3.5" fill={ink} />
      <circle className={eye} cx="30" cy="24" r="3.5" fill={ink} />
      <path
        d="M19 31 Q24 35 29 31"
        stroke={ink}
        strokeWidth="2.5"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  )
}

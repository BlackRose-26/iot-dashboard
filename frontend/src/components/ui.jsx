import { Link } from 'react-router-dom'
import * as Dialog from '@radix-ui/react-dialog'
import * as Dropdown from '@radix-ui/react-dropdown-menu'
import * as Tooltip from '@radix-ui/react-tooltip'
import { ArrowUpRight, ChevronDown, X, Layers3, Info, Check, Search, Plus } from './icons'

export function Logo({ compact = false, destination = '/admin/overview' }) {
  return (
    <Link
      to={destination}
      className={`brand ${compact ? 'compact' : ''}`}
      aria-label="Stack Moko Baby"
    >
      <span className="brand-mark" aria-hidden="true">
        <Layers3 size={29} />
      </span>
      {!compact && (
        <span>
          stack moko baby<span className="brand-period">.</span>
        </span>
      )}
    </Link>
  )
}
export function IconButton({ children, label, className = '', ...props }) {
  return (
    <Tooltip.Root>
      <Tooltip.Trigger asChild>
        <button type="button" aria-label={label} className={`icon-button ${className}`} {...props}>
          {children}
        </button>
      </Tooltip.Trigger>
      <Tooltip.Portal>
        <Tooltip.Content className="tooltip" sideOffset={8}>
          {label}
          <Tooltip.Arrow />
        </Tooltip.Content>
      </Tooltip.Portal>
    </Tooltip.Root>
  )
}
export function Badge({ children, tone = 'neutral', dot = false, ...props }) {
  return (
    <span className={`badge ${tone}`} {...props}>
      {dot && <span className="status-dot" />}
      {children}
    </span>
  )
}
export function Card({ children, className = '', ...props }) {
  return (
    <section className={`card ${className}`} {...props}>
      {children}
    </section>
  )
}
export function CardHeader({ title, subtitle, icon: Icon, action }) {
  return (
    <div className="card-heading">
      <div className="card-title-wrap">
        {Icon && (
          <span className="heading-icon">
            <Icon size={23} strokeWidth={1.6} />
          </span>
        )}
        <div>
          <h2>{title}</h2>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      {action}
    </div>
  )
}
export function RoundLink({ to, label }) {
  return (
    <Link className="circle-link" to={to} aria-label={label}>
      <ArrowUpRight size={22} />
    </Link>
  )
}
export function Button({ children, tone = 'dark', className = '', ...props }) {
  return (
    <button type="button" className={`button ${tone} ${className}`} {...props}>
      {children}
    </button>
  )
}
export function PageHeading({
  eyebrow = 'ACS CARNIVAL / CLASSIC V1',
  title,
  description,
  children,
}) {
  return (
    <div className="page-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
      <div className="page-actions">{children}</div>
    </div>
  )
}
export function Menu({ label, value, options, onChange, icon: Icon, className = '' }) {
  return (
    <Dropdown.Root>
      <Dropdown.Trigger asChild>
        <button className={`select-button ${className}`} aria-label={label}>
          {Icon && <Icon size={16} />}
          <span>{value}</span>
          <ChevronDown size={15} />
        </button>
      </Dropdown.Trigger>
      <Dropdown.Portal>
        <Dropdown.Content className="dropdown" sideOffset={8} align="end">
          <Dropdown.Label className="dropdown-label">{label}</Dropdown.Label>
          {options.map((option) => (
            <Dropdown.Item
              key={option.value}
              className="dropdown-item"
              onSelect={() => onChange(option.value)}
            >
              {option.label}
              {option.label === value && <Check size={15} />}
            </Dropdown.Item>
          ))}
        </Dropdown.Content>
      </Dropdown.Portal>
    </Dropdown.Root>
  )
}
export function Modal({ title, description, trigger, children, open, onOpenChange }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      {trigger && <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>}
      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />
        <Dialog.Content className="modal">
          <Dialog.Close className="modal-close" aria-label="Close dialog">
            <X size={22} />
          </Dialog.Close>
          <Dialog.Title>{title}</Dialog.Title>
          <Dialog.Description>{description}</Dialog.Description>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
export function EmptyState({
  title,
  description,
  action,
  icon: Icon = Layers3,
  headingAs: Heading = 'h2',
}) {
  return (
    <div className="empty-state">
      <span className="empty-icon">
        <Icon size={32} />
      </span>
      <Heading>{title}</Heading>
      <p>{description}</p>
      {action}
    </div>
  )
}
export function InfoNote({ children, className = '' }) {
  return (
    <div className={`info-note ${className}`}>
      <Info size={17} />
      <span>{children}</span>
    </div>
  )
}
export function SearchInput({
  value,
  onChange,
  placeholder = 'Search player or code',
  label = 'Search players',
}) {
  return (
    <label className="search-field">
      <Search size={18} />
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        aria-label={label}
      />
      {value && (
        <button type="button" aria-label="Clear search" onClick={() => onChange('')}>
          <X size={16} />
        </button>
      )}
    </label>
  )
}
export function Metric({ label, value, detail, icon: Icon, accent = false }) {
  return (
    <div className={`metric ${accent ? 'accent' : ''}`}>
      <div className="metric-label">
        {label}
        {Icon && <Icon size={18} />}
      </div>
      <strong>{value}</strong>
      <span>{detail}</span>
    </div>
  )
}
export function Avatar({ name, index = 0 }) {
  return (
    <span className={`avatar avatar-${index % 4}`} aria-hidden="true">
      {name.slice(0, 2).toUpperCase()}
    </span>
  )
}
export function FormatNumber({ value, suffix = '' }) {
  return value == null
    ? 'N/A'
    : `${Number(value).toLocaleString('en-US', { maximumFractionDigits: 1 })}${suffix}`
}
export function StepLabel({ number, children }) {
  return (
    <span className="step-label">
      <span>{number}</span>
      {children}
    </span>
  )
}

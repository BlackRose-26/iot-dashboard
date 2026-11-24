// Tailwind class strings for the three-colour player website (Cloud, Ink = "night", Lime).
// Literal strings only, so Tailwind can find them. Motion uses motion-safe: so the device's
// reduce-motion setting turns it off; durations follow the motion system (120 / 220 / 320 ms).

const focus =
  'tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-night tw:focus-visible:outline-offset-[3px]'
const lift =
  'tw:motion-safe:transition-transform tw:motion-safe:duration-[120ms] tw:motion-safe:ease-snappy tw:motion-safe:hover:-translate-y-0.5 tw:motion-safe:active:translate-y-0 tw:motion-safe:active:scale-[0.98]'

export const pill =
  'tw:inline-flex tw:self-start tw:text-[13px] tw:font-extrabold tw:tracking-[1px] tw:px-[14px] tw:py-2 tw:rounded-full tw:border-[1.5px] tw:border-solid tw:border-night'
export const h1 =
  'tw:m-0 tw:text-[clamp(38px,5vw,64px)] tw:leading-[1.03] tw:tracking-[-2px] tw:font-extrabold'
export const lead = 'tw:m-0 tw:text-[18px] tw:leading-[1.6] tw:text-night/72 tw:max-w-[620px]'
export const h2 = 'tw:m-0 tw:mb-[18px] tw:text-[30px] tw:tracking-[-1px] tw:font-extrabold'
export const section = 'tw:py-7'
export const grid =
  'tw:grid tw:grid-cols-[repeat(auto-fit,minmax(min(100%,280px),1fr))] tw:gap-4 tw:list-none tw:m-0 tw:p-0'
export const box =
  'tw:border-[1.5px] tw:border-solid tw:border-night/16 tw:rounded-[28px] tw:p-6 tw:flex tw:flex-col tw:gap-2.5'
export const boxTitle = 'tw:m-0 tw:text-[19px] tw:font-extrabold'
export const boxText = 'tw:m-0 tw:text-[15px] tw:leading-[1.55] tw:text-night/72'
export const num =
  'tw:w-10 tw:h-10 tw:rounded-[20px] tw:bg-lime tw:border-2 tw:border-solid tw:border-night tw:grid tw:place-items-center tw:font-extrabold'
export const band =
  'tw:bg-night tw:text-cloud tw:rounded-[40px] tw:p-10 tw:max-[600px]:p-7 tw:grid tw:grid-cols-[repeat(auto-fit,minmax(min(100%,220px),1fr))] tw:gap-6 tw:items-end'
export const bandTitle =
  'tw:m-0 tw:text-[30px] tw:tracking-[-1px] tw:font-extrabold tw:leading-[1.1]'
export const bandValue =
  'tw:block tw:text-[56px] tw:max-[600px]:text-[44px] tw:font-extrabold tw:text-lime tw:leading-none'
export const bandLabel = 'tw:text-[15px] tw:text-cloud/80'
export const button = `tw:min-h-12 tw:inline-flex tw:items-center tw:gap-2.5 tw:px-5 tw:rounded-full tw:border-[1.5px] tw:border-solid tw:border-night tw:bg-transparent tw:text-night tw:font-bold tw:text-[15px] tw:cursor-pointer ${focus} ${lift}`
export const buttonDark = `tw:min-h-12 tw:inline-flex tw:items-center tw:gap-2.5 tw:pl-2 tw:pr-5 tw:rounded-full tw:border-[1.5px] tw:border-solid tw:border-night tw:bg-night tw:text-cloud tw:font-bold tw:text-[15px] tw:cursor-pointer ${focus} ${lift}`
export const robotChip =
  'tw:w-[34px] tw:h-[34px] tw:rounded-[17px] tw:bg-lime tw:grid tw:place-items-center'
export const faqList = 'tw:flex tw:flex-col tw:gap-2.5 tw:max-w-[820px]'
export const faqItem =
  'tw:border-[1.5px] tw:border-solid tw:border-night/16 tw:rounded-[22px] tw:px-5 tw:py-4'
export const faqQuestion = 'tw:cursor-pointer tw:text-[17px] tw:font-bold tw:min-h-7'
export const faqAnswer = 'tw:mt-2.5 tw:mb-0 tw:text-[15px] tw:leading-[1.55] tw:text-night/72'
export const tag =
  'tw:inline-flex tw:bg-lime tw:text-night tw:text-[13px] tw:font-extrabold tw:tracking-[1px] tw:px-3 tw:py-1.5 tw:rounded-full tw:mb-3'
// Staggered entrance: give each item one of these delays (0 / 80 / 160 / 240 ms).
export const enter = 'tw:motion-safe:animate-fade-up'
export const delays = [
  'tw:[animation-delay:0ms]',
  'tw:[animation-delay:80ms]',
  'tw:[animation-delay:160ms]',
  'tw:[animation-delay:240ms]',
  'tw:[animation-delay:320ms]',
]

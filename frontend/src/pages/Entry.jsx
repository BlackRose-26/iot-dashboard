import Scanner from './Scanner'

export function ScanGate({ message }) {
  return <Scanner message={message} />
}

// Opening or pasting a QR URL does not create an entry grant. The scanner API
// must report a detected code before the application requests entry.
export default function Entry() {
  return <Scanner />
}

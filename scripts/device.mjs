// npm wrapper for scripts/flash-device.py using the backend virtual environment.
// Examples: npm run device:selftest   npm run device:selftest -- --port COM5
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = join(
  root,
  "backend",
  ".venv",
  process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
);
if (!existsSync(python)) {
  console.error("[device] Complete the local backend setup first.");
  process.exit(1);
}
const child = spawn(
  python,
  [join(root, "scripts", "flash-device.py"), ...process.argv.slice(2)],
  { cwd: root, stdio: "inherit", windowsHide: true },
);
child.once("exit", (code) => process.exit(code ?? 1));
child.once("error", () => process.exit(1));

// npm wrapper for scripts/flash-device.py (or set-device-url.py with "url") using the backend venv.
// Examples: npm run device:selftest   npm run device:selftest -- --port COM5   npm run device:url
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
const urlMode = process.argv[2] === "url";
const script = urlMode ? "set-device-url.py" : "flash-device.py";
const child = spawn(
  python,
  [join(root, "scripts", script), ...process.argv.slice(urlMode ? 3 : 2)],
  { cwd: root, stdio: "inherit", windowsHide: true },
);
child.once("exit", (code) => process.exit(code ?? 1));
child.once("error", () => process.exit(1));

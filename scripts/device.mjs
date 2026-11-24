// npm wrapper for the device and database helpers, using the backend venv.
// Examples: npm run device:selftest -- --port COM5   npm run device:url   npm run db:backup
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
// "url" -> set-device-url.py, "db" -> db-backup.py, "purge" -> purge-student-ids.py, "check" -> event-check.py, otherwise flash-device.py.
const mode = { url: "set-device-url.py", db: "db-backup.py", purge: "purge-student-ids.py",
  check: "event-check.py",
}[
  process.argv[2]
];
const script = mode || "flash-device.py";
const subcommand = Boolean(mode);
const child = spawn(
  python,
  [join(root, "scripts", script), ...process.argv.slice(subcommand ? 3 : 2)],
  { cwd: root, stdio: "inherit", windowsHide: true },
);
child.once("exit", (code) => process.exit(code ?? 1));
child.once("error", () => process.exit(1));

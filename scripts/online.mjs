import { spawn, spawnSync } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  createWriteStream,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createConnection } from "node:net";
import { setTimeout as delay } from "node:timers/promises";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const backend = join(root, "backend");
const tools = join(root, ".tools", "free-online");
const python = join(
  backend,
  ".venv",
  process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
);
const tunnelExe =
  process.env.STACK_CLOUDFLARED ||
  join(tools, process.platform === "win32" ? "cloudflared.exe" : "cloudflared");
const children = [];
let stopping = false;
let backupsReady = false;
let backupRunning = false;
const backupMinutes = Number(process.env.STACK_BACKUP_MINUTES ?? 15);

// Encrypted database backup (scripts/db-backup.py). Never blocks the app; failures are reported.
function backupNow(label) {
  if (backupRunning) return;
  backupRunning = true;
  const child = spawn(
    python,
    ["scripts/db-backup.py", ...(label ? ["--label", label] : [])],
    { cwd: root, windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
  );
  let output = "";
  for (const stream of [child.stdout, child.stderr])
    stream.on("data", (chunk) => (output += chunk));
  child.once("exit", (code) => {
    backupRunning = false;
    const line = output.trim().split(/\r?\n/).pop() || "";
    if (code === 0) console.log(`[online] ${line}`);
    else
      console.error(
        `[online] Database backup failed: ${line} (retry with npm run db:backup)`,
      );
  });
  child.once("error", () => (backupRunning = false));
}

function occupied(port) {
  return new Promise((resolvePort) => {
    const socket = createConnection({ host: "127.0.0.1", port });
    socket.setTimeout(1500);
    const finish = (value) => {
      socket.destroy();
      resolvePort(value);
    };
    socket.once("connect", () => finish(true));
    socket.once("error", () => finish(false));
    socket.once("timeout", () => finish(false));
  });
}
// XAMPP MySQL is not a Windows service on the event laptop. Start it ourselves (detached, so
// it keeps running after Ctrl+C like a normal XAMPP start) and restart it if it stops.
const xampp = process.env.STACK_XAMPP_DIR || "C:\\xampp";
const mysqld = join(xampp, "mysql", "bin", process.platform === "win32" ? "mysqld.exe" : "mysqld");
let mysqlStartedAt = 0;
async function ensureMysql(reason) {
  if (await occupied(3306)) return true;
  if (!existsSync(mysqld)) return false;
  if (Date.now() - mysqlStartedAt < 60000) return false; // one start attempt per minute
  mysqlStartedAt = Date.now();
  console.log(`[online] ${reason}: starting XAMPP MySQL…`);
  const server = spawn(
    mysqld,
    [`--defaults-file=${join(xampp, "mysql", "bin", "my.ini")}`, "--standalone"],
    { cwd: join(xampp, "mysql"), detached: true, stdio: "ignore", windowsHide: true },
  );
  server.on("error", () => {});
  server.unref();
  for (let attempt = 0; attempt < 60; attempt++) {
    if (await occupied(3306)) {
      console.log("[online] MySQL is running.");
      return true;
    }
    await delay(500);
  }
  console.error("[online] MySQL did not start. Open the XAMPP Control Panel and start MySQL.");
  return false;
}
function watchMysql() {
  setInterval(async () => {
    if (stopping || (await occupied(3306))) return;
    console.error("[online] MySQL stopped. Players and the dashboard cannot save until it is back.");
    await ensureMysql("MySQL stopped");
  }, 15000).unref();
}
function start(command, args, options = {}) {
  const child = spawn(command, args, {
    cwd: root,
    windowsHide: true,
    stdio: "inherit",
    ...options,
  });
  children.push(child);
  return child;
}
function completed(child, label) {
  return new Promise((resolveExit, reject) => {
    child.once("error", () => reject(new Error(`Could not start ${label}.`)));
    child.once("exit", (code) =>
      code === 0
        ? resolveExit()
        : reject(new Error(`${label} stopped with an error.`)),
    );
  });
}
async function stop(code = 0) {
  if (stopping) return;
  stopping = true;
  if (backupsReady && backupMinutes > 0) {
    // Final backup while MySQL is still running (it is not one of our children).
    const final = spawnSync(
      python,
      ["scripts/db-backup.py", "--label", "shutdown"],
      { cwd: root, windowsHide: true, encoding: "utf8", timeout: 60000 },
    );
    const line = `${final.stdout || ""}${final.stderr || ""}`
      .trim()
      .split(/\r?\n/)
      .pop();
    console.log(
      final.status === 0
        ? `[online] ${line}`
        : `[online] Final backup failed: ${line}`,
    );
  }
  for (const child of children) {
    if (!child.pid || child.exitCode !== null || child.signalCode !== null)
      continue;
    if (process.platform === "win32") {
      await new Promise((done) => {
        const killer = spawn(
          "taskkill",
          ["/PID", String(child.pid), "/T", "/F"],
          { stdio: "ignore", windowsHide: true },
        );
        killer.once("exit", done);
        killer.once("error", done);
      });
    } else child.kill("SIGTERM");
  }
  process.exit(code);
}
process.once("SIGINT", () => void stop());
process.once("SIGTERM", () => void stop());

async function main() {
  if (!existsSync(python) || !existsSync(join(backend, ".env")))
    throw new Error("Complete the local backend setup first.");
  if (!(await ensureMysql("MySQL is not running")))
    throw new Error("Start MySQL in XAMPP, then run npm run online again.");
  if (await occupied(8000))
    throw new Error(
      "Port 8000 is already running. Stop its own terminal with Ctrl+C before starting online mode.",
    );
  if (!existsSync(tunnelExe))
    throw new Error(
      "Install the tunnel helper first: backend\\.venv\\Scripts\\python.exe scripts\\install-cloudflared.py",
    );
  const ollamaExe = join(
    process.env.LOCALAPPDATA || "",
    "Programs",
    "Ollama",
    "ollama.exe",
  );
  if (!(await occupied(11434)) && existsSync(ollamaExe)) {
    const modelServer = start(ollamaExe, ["serve"], {
      env: { ...process.env, OLLAMA_HOST: "127.0.0.1:11434" },
      stdio: "ignore",
    });
    modelServer.once("error", () =>
      console.log("[online] Open Ollama when you need Stack Intelligence."),
    );
    console.log("[online] Starting the installed local Ollama server.");
  }
  console.log("[online] Building the dashboard…");
  await completed(
    start(process.execPath, ["node_modules/vite/bin/vite.js", "build"], {
      cwd: join(root, "frontend"),
    }),
    "frontend build",
  );
  mkdirSync(tools, { recursive: true });
  const log = createWriteStream(join(tools, "tunnel.log"), { flags: "w" });
  const tunnel = start(
    tunnelExe,
    [
      "tunnel",
      "--url",
      "http://127.0.0.1:8000",
      "--protocol",
      "http2",
      "--no-autoupdate",
    ],
    { stdio: ["ignore", "pipe", "pipe"] },
  );
  const origin = await new Promise((resolveOrigin, reject) => {
    const timeout = setTimeout(
      () =>
        reject(
          new Error(
            "The HTTPS tunnel did not start. See .tools/free-online/tunnel.log.",
          ),
        ),
      60000,
    );
    let text = "";
    const consume = (chunk) => {
      log.write(chunk);
      text = (text + chunk.toString()).slice(-16000);
      const match = text.match(/https:\/\/[a-z0-9-]+\.trycloudflare\.com\b/);
      if (match) {
        clearTimeout(timeout);
        resolveOrigin(match[0]);
      }
    };
    tunnel.stdout.on("data", consume);
    tunnel.stderr.on("data", consume);
    tunnel.once("error", () => {
      clearTimeout(timeout);
      reject(new Error("Could not start cloudflared."));
    });
    tunnel.once("exit", () => {
      clearTimeout(timeout);
      reject(
        new Error(
          "The HTTPS tunnel stopped. See .tools/free-online/tunnel.log.",
        ),
      );
    });
  });
  const api = start(
    python,
    [
      "-m",
      "uvicorn",
      "app.main:app",
      "--app-dir",
      "backend",
      "--host",
      "127.0.0.1",
      "--port",
      "8000",
      "--workers",
      "1",
      "--no-access-log",
      "--ws-max-size",
      "1024",
      "--ws-max-queue",
      "4",
    ],
    {
      env: {
        ...process.env,
        STACK_PUBLIC_URL: origin,
        STACK_COOKIE_SECURE: "true",
        STACK_ENV: "production",
        STACK_SIMULATOR_ENABLED: "false",
        STACK_FRONTEND_DIST: join(root, "frontend", "dist"),
      },
    },
  );
  for (const child of [api, tunnel]) {
    child.once("exit", () => {
      if (!stopping) {
        console.error("[online] A required service stopped.");
        void stop(1);
      }
    });
    child.once("error", () => {
      if (!stopping) void stop(1);
    });
  }
  let ready = false;
  for (let attempt = 0; attempt < 60; attempt++) {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/health", {
        signal: AbortSignal.timeout(2000),
      });
      if (response.ok) {
        ready = true;
        break;
      }
    } catch {}
    await delay(500);
  }
  if (!ready)
    throw new Error(
      "Backend/database readiness failed; run the documented database setup.",
    );
  writeFileSync(join(tools, "current-url.txt"), origin + "\n");
  watchMysql();
  if (backupMinutes > 0) {
    backupsReady = true;
    backupNow();
    setInterval(backupNow, backupMinutes * 60000).unref();
    console.log(
      `[online] Encrypted database backups every ${backupMinutes} min and on Ctrl+C (outside the project folder).`,
    );
  }
  console.log(
    `\n[online] Admin: ${origin}/admin/login\n[online] Player scanner: ${origin}/scan`,
  );
  console.log(
    "[online] Keep this terminal and MySQL running. Ctrl+C stops the app and tunnel. The address changes on the next run.",
  );
  const device = process.argv.includes("--device");
  if (!device && !process.argv.includes("--firmware")) {
    // New tunnel address -> tell the USB-connected cabinet. No compile or reflash.
    try {
      await completed(
        start(python, ["scripts/set-device-url.py", "--url", origin, "--if-present"]),
        "cabinet address update",
      );
    } catch {
      console.error(
        "[online] Dashboard is online, but the cabinet did not take the new address. Close any serial monitor and run: npm run device:url",
      );
    }
  }
  if (device || process.argv.includes("--firmware")) {
    if (device)
      console.log(
        "[online] Building hotspot firmware and uploading it to the USB-connected ESP32 (NVS journal preserved)…",
      );
    try {
      await completed(
        start(python, [
          "scripts/prepare-online-firmware.py",
          "--url",
          origin,
          ...(device ? ["--device"] : []),
        ]),
        "private firmware preparation",
      );
      if (device)
        console.log(
          "[online] Cabinet flashed. Wait for a fresh heartbeat on the Machines page before calling a player.",
        );
    } catch {
      console.error(
        `[online] Dashboard remains online. Firmware preparation needs attention; retry scripts/prepare-online-firmware.py --url ${origin}${device ? " --device" : ""}.`,
      );
    }
  }
}
main().catch((error) => {
  console.error(`[online] ${error.message}`);
  void stop(1);
});

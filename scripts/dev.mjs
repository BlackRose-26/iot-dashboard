import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { createConnection } from "node:net";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { setTimeout as delay } from "node:timers/promises";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const backend = join(root, "backend");
const frontend = join(root, "frontend");
const apiUrl = "http://127.0.0.1:8000";
const backendOnly = process.argv.includes("--backend-only");
const owned = [];
let stopping = false;
let backendProcess;

function portInUse(port) {
  return new Promise((resolvePort) => {
    const socket = createConnection({ host: "127.0.0.1", port });
    const finish = (used) => {
      socket.destroy();
      resolvePort(used);
    };
    socket.setTimeout(1200, () => finish(false));
    socket.once("connect", () => finish(true));
    socket.once("error", () => finish(false));
  });
}

async function health() {
  try {
    const response = await fetch(`${apiUrl}/api/health`, {
      signal: AbortSignal.timeout(1500),
    });
    const body = await response.json().catch(() => ({}));
    return {
      reachable: true,
      ready:
        response.ok &&
        body.status === "ok" &&
        body.application === "stack-moko-baby",
    };
  } catch {
    return { reachable: false, ready: false };
  }
}

function start(command, args, cwd, name) {
  const child = spawn(command, args, {
    cwd,
    stdio: "inherit",
    windowsHide: true,
  });
  owned.push(child);
  child.once("error", (error) => {
    if (!stopping) {
      console.error(
        `[dev] Could not start ${name} (${error.code || "process error"}).`,
      );
      void stop(1);
    }
  });
  child.once("exit", (code, signal) => {
    if (!stopping) {
      console.error(
        `[dev] ${name} stopped${code ? ` with exit code ${code}` : ""}.`,
      );
      void stop(signal === "SIGINT" || code === 0 ? 0 : 1);
    }
  });
  return child;
}

async function stop(code) {
  if (stopping) return;
  stopping = true;
  await Promise.all(
    owned.map(
      (child) =>
        new Promise((done) => {
          if (
            !child.pid ||
            child.exitCode !== null ||
            child.signalCode !== null
          )
            return done();
          if (process.platform === "win32") {
            // Stop only process trees started by this launcher, including Uvicorn's reloader.
            const killer = spawn(
              "taskkill",
              ["/PID", String(child.pid), "/T", "/F"],
              { stdio: "ignore", windowsHide: true },
            );
            killer.once("error", () => {
              child.kill();
              done();
            });
            killer.once("exit", done);
          } else {
            child.once("exit", done);
            child.kill("SIGTERM");
            setTimeout(() => {
              if (child.exitCode === null) child.kill("SIGKILL");
              done();
            }, 3000).unref();
          }
        }),
    ),
  );
  process.exit(code);
}

process.once("SIGINT", () => void stop(0));
process.once("SIGTERM", () => void stop(0));

async function main() {
  if (!backendOnly && (await portInUse(5173))) {
    throw new Error(
      "Port 5173 is already in use. Keep the existing frontend, or stop it with Ctrl+C before running npm run dev again.",
    );
  }
  if (
    !backendOnly &&
    !existsSync(join(frontend, "node_modules/vite/bin/vite.js"))
  ) {
    throw new Error(
      "Frontend dependencies are missing. Run npm --prefix frontend ci from the project root.",
    );
  }
  if (
    !backendOnly &&
    process.env.STACK_API_TARGET &&
    process.env.STACK_API_TARGET.replace(/\/$/, "") !== apiUrl
  ) {
    throw new Error(
      "The combined launcher uses the local API on port 8000. For a custom STACK_API_TARGET, use npm run dev:frontend.",
    );
  }

  const existing = await portInUse(8000);
  if (existing) {
    if (!(await health()).ready) {
      throw new Error(
        "Port 8000 is occupied, but the current Stack Moko Baby API and database are not ready. Start MySQL in XAMPP. Stop an old backend with Ctrl+C and retry; do not reset the database.",
      );
    }
    console.log(
      "[dev] Reusing the running Stack Moko Baby backend. Its original terminal must stay open.",
    );
  } else {
    if (!existsSync(join(backend, ".env"))) {
      throw new Error(
        "Backend configuration is missing. Follow docs/local-setup.md for the one-time database setup.",
      );
    }
    const python = [
      join(
        backend,
        ".venv",
        process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
      ),
      join(
        root,
        ".tools/backend-venv",
        process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
      ),
    ].find(existsSync);
    if (!python)
      throw new Error(
        "Backend environment is missing. Follow docs/local-setup.md to create backend/.venv and install requirements.txt.",
      );
    console.log(
      "[dev] Starting FastAPI on port 8000. Keep XAMPP MySQL running.",
    );
    backendProcess = start(
      python,
      [
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--reload",
        "--no-access-log",
      ],
      backend,
      "Backend",
    );
    const deadline = Date.now() + 30000;
    let ready = false;
    while (!stopping && Date.now() < deadline) {
      if (backendProcess.exitCode !== null) return;
      if ((await health()).ready) {
        ready = true;
        break;
      }
      await delay(500);
    }
    if (stopping) return;
    if (!ready)
      throw new Error(
        "The backend/database did not become ready. Start MySQL in XAMPP, then run npm run dev again. If MySQL is already running, check the backend terminal error and docs/local-setup.md. Existing data and credentials have not been changed.",
      );
  }

  console.log("[dev] Backend and XAMPP database are ready.");
  if (backendOnly) {
    console.log(
      "[dev] API: http://127.0.0.1:8000 · Ctrl+C stops only servers this launcher started.",
    );
    return;
  }
  console.log("[dev] Starting React. Open http://localhost:5173/admin/login");
  console.log(
    "[dev] Keep this terminal open. Ctrl+C stops both owned servers; XAMPP is left running.",
  );
  start(
    process.execPath,
    [
      "node_modules/vite/bin/vite.js",
      "--host",
      "0.0.0.0",
      "--port",
      "5173",
      "--strictPort",
    ],
    frontend,
    "Frontend",
  );
}

try {
  await main();
} catch (error) {
  console.error(`\n[dev] ${error.message}\n`);
  await stop(1);
}

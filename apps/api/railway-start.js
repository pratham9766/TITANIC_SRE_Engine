const { spawn } = require("node:child_process");
require("dotenv").config();

const PORT = process.env.PORT || 3000;
const python = process.env.PYTHON_BIN || "python";

const child = spawn(
  python,
  ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", String(PORT)],
  { stdio: "inherit" }
);

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 0);
});

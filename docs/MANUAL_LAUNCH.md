# TITANIC AI SRE Command Center - Manual Launch Guide

This guide details how to manually set up, launch, and verify both the **FastAPI Backend** and the **Frontend Dashboard** of the TITANIC Reliability Operating System.

---

## 🛠️ Prerequisites
Ensure you have the following installed on your system:
- **Python 3.10+** (Python 3.12 is verified)
- **Node.js 18+** & **npm** (Node v22 / npm v11 is verified) — *Optional, only needed for the Node/Vite build option.*

---

## 🐍 Part 1: Starting the Backend (FastAPI)

Follow these steps from the root of your workspace:

### 1. Navigate to the API Directory
```powershell
cd apps/api
```

### 2. Run the Setup Script
This script creates a Python virtual environment (`.venv`), installs all required Python packages, and creates a local `.env` file from the example:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_backend.ps1
```

### 3. Activate the Virtual Environment
- **On Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **On Windows (Command Prompt):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **On macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 4. Start the Uvicorn Dev Server
Launch the API server on port `8000`:
```powershell
uvicorn app.main:app --reload --port 8000
```
- **Verification:** Open your browser and navigate to [http://localhost:8000/health](http://localhost:8000/health). You should see:
  ```json
  {"status": "ok", "service": "titanic-api"}
  ```
- **API Documentation:** You can view the interactive Swagger docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 💻 Part 2: Starting the Frontend Dashboard

We support two ways to launch the frontend. **Option A** is recommended if you have Node.js installed. **Option B** is a simple no-build alternative that runs instantly using Python.

### 🌟 Option A: React/Vite Dev Mode (Recommended)
This mode provides hot-reloading and modern bundler features.

1. **Navigate to the web directory:**
   ```powershell
   cd apps/web
   ```
2. **Install Node.js dependencies:**
   ```powershell
   npm install
   ```
3. **Run the Vite Dev Server:**
   ```powershell
   npm run dev
   ```
4. **Access the UI:**
   Open your browser and navigate to [http://localhost:5173](http://localhost:5173).

---

### 🐍 Option B: Python No-Build Static Server (Instant Fallback)
If you don't want to install Node.js dependencies, you can instantly run the vanilla dashboard using Python's built-in HTTP server.

1. **Navigate to the workspace root directory.**
2. **Run Python HTTP Server:**
   Serve the `apps/web` folder on port `4173`:
   ```powershell
   python -m http.server 4173 -d apps/web
   ```
3. **Access the UI:**
   Open your browser and navigate to [http://localhost:4173](http://localhost:4173).

---

## 🧪 Part 3: Troubleshooting

### CORS or Port Issues
- The FastAPI backend is configured to accept CORS requests originating from `http://localhost:4173` and `http://127.0.0.1:4173` by default.
- If you run the frontend using Vite (Option A) on port `5173`, ensure that the API backend's CORS settings in `apps/api/app/main.py` allow `http://localhost:5173`.

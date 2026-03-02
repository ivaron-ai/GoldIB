# Stop-Hook for Loop 1
# Checks if:
# 1. docker-compose.yml exists at repo root
# 2. src/main.py exists at repo root
# 3. pytest passes for tests/test_infra.py at repo root

Write-Host 'Running Stop-Hook for Loop 1...'

# Resolve repo root (two levels up from this job directory)
$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\'))
Write-Host "Repo root: $RepoRoot"

# 1. Check required files at repo root
if (-not (Test-Path (Join-Path $RepoRoot 'docker-compose.yml'))) { Write-Error 'Missing docker-compose.yml at repo root'; exit 1 }
if (-not (Test-Path (Join-Path $RepoRoot 'src\main.py'))) { Write-Error 'Missing src/main.py at repo root'; exit 1 }
if (-not (Test-Path (Join-Path $RepoRoot 'tests\test_infra.py'))) { Write-Error 'Missing tests/test_infra.py at repo root'; exit 1 }

Write-Host 'All required files present. Running pytest...'

# 2. Locate Python executable
$PythonExe = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    try {
        $ver = & $candidate --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $ver -match 'Python') {
            $PythonExe = $candidate
            Write-Host "Found Python: $ver ($PythonExe)"
            break
        }
    } catch {}
}

# Also check for venv at repo root
$VenvPython = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not $PythonExe -and (Test-Path $VenvPython)) {
    $PythonExe = $VenvPython
    Write-Host "Using venv Python: $VenvPython"
}

if (-not $PythonExe) {
    Write-Error 'Python not found. Please install Python 3.11+ and ensure it is on PATH.'
    Write-Host 'Tip: Install from https://www.python.org/downloads/ (add to PATH) or use: winget install Python.Python.3.11'
    exit 1
}

# 3. Run pytest from repo root
Push-Location $RepoRoot
try {
    # Install deps into venv if not already done
    if (-not (Test-Path (Join-Path $RepoRoot '.venv'))) {
        Write-Host 'Creating virtual environment...'
        & $PythonExe -m venv .venv
        & (Join-Path $RepoRoot '.venv\Scripts\python.exe') -m pip install -q fastapi uvicorn redis psycopg2-binary sqlalchemy structlog python-dotenv httpx pytest pytest-asyncio
    }
    $pytest = Join-Path $RepoRoot '.venv\Scripts\pytest.exe'
    if (Test-Path $pytest) {
        & $pytest tests/test_infra.py -v
    } else {
        & $PythonExe -m pytest tests/test_infra.py -v
    }
    $TestExit = $LASTEXITCODE
} catch {
    Write-Error "pytest failed to run: $_"
    $TestExit = 1
} finally {
    Pop-Location
}

if ($TestExit -ne 0) { Write-Error 'pytest tests failed'; exit 1 }

Write-Host 'All checks passed.'
exit 0

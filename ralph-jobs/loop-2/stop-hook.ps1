# Stop-Hook for Loop 2
# Verifies: Web UI, Portfolio Engine, AssetActor, AI Brain, Cloud stubs, and tests

Write-Host 'Running Stop-Hook for Loop 2...'

$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\'))
Write-Host "Repo root: $RepoRoot"

$errors = @()

# --- Phase A: Web UI ---
$requiredUI = @('ui\index.html', 'ui\style.css')
foreach ($f in $requiredUI) {
    if (-not (Test-Path (Join-Path $RepoRoot $f))) { $errors += "Missing $f" }
}

# --- Phase B: Portfolio Engine ---
$requiredPortfolio = @(
    'src\orchestrator\__init__.py',
    'src\orchestrator\portfolio\__init__.py',
    'src\orchestrator\portfolio\discovery_agent.py',
    'src\orchestrator\portfolio\risk_allocator.py',
    'src\orchestrator\portfolio\esoteric_screener.py'
)
foreach ($f in $requiredPortfolio) {
    if (-not (Test-Path (Join-Path $RepoRoot $f))) { $errors += "Missing $f" }
}

# --- Phase C: AssetActor ---
$requiredActors = @(
    'src\actors\__init__.py',
    'src\actors\asset_actor.py',
    'src\actors\execution_engine.py',
    'src\shared\__init__.py',
    'src\shared\models\__init__.py',
    'src\shared\models\trading_profile.py',
    'src\shared\models\prophecy_data.py'
)
foreach ($f in $requiredActors) {
    if (-not (Test-Path (Join-Path $RepoRoot $f))) { $errors += "Missing $f" }
}

# --- Phase D: AI Brain ---
$requiredAI = @(
    'src\actors\ai\__init__.py',
    'src\actors\ai\lstm_predictor.py',
    'src\actors\ai\rl_trade_manager.py',
    'src\actors\ai\online_learner.py'
)
foreach ($f in $requiredAI) {
    if (-not (Test-Path (Join-Path $RepoRoot $f))) { $errors += "Missing $f" }
}

# --- Phase E: Cloud Providers ---
$requiredCloud = @(
    'src\orchestrator\cloud_deploy\__init__.py',
    'src\orchestrator\cloud_deploy\base_provider.py',
    'src\orchestrator\cloud_deploy\local_provider.py',
    'src\orchestrator\cloud_deploy\do_provider.py',
    'src\orchestrator\cloud_deploy\aws_provider.py',
    'src\orchestrator\cloud_deploy\azure_provider.py',
    'src\orchestrator\cluster_manager.py'
)
foreach ($f in $requiredCloud) {
    if (-not (Test-Path (Join-Path $RepoRoot $f))) { $errors += "Missing $f" }
}

# --- Phase F: Tests ---
if (-not (Test-Path (Join-Path $RepoRoot 'tests\test_loop2.py'))) {
    $errors += "Missing tests\test_loop2.py"
}

# Report missing files
if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing files:" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}

Write-Host "All required files present." -ForegroundColor Green

# --- Run pytest ---
$PythonExe = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    try {
        $ver = & $candidate --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $ver -match 'Python') {
            $PythonExe = $candidate; break
        }
    } catch {}
}
$VenvPython = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not $PythonExe -and (Test-Path $VenvPython)) { $PythonExe = $VenvPython }
if (-not $PythonExe) {
    Write-Error 'Python not found. Install Python 3.11+ or run: winget install Python.Python.3.11'
    exit 1
}

Push-Location $RepoRoot
try {
    $pytest = Join-Path $RepoRoot '.venv\Scripts\pytest.exe'

    Write-Host "Running Loop 1 regression tests..."
    if (Test-Path $pytest) {
        & $pytest tests/test_infra.py -q
    } else {
        & $PythonExe -m pytest tests/test_infra.py -q
    }
    if ($LASTEXITCODE -ne 0) { Write-Error 'Loop 1 regression tests failed'; exit 1 }

    Write-Host "Running Loop 2 tests..."
    if (Test-Path $pytest) {
        & $pytest tests/test_loop2.py -v
    } else {
        & $PythonExe -m pytest tests/test_loop2.py -v
    }
    $TestExit = $LASTEXITCODE
} catch {
    Write-Error "pytest failed: $_"
    $TestExit = 1
} finally {
    Pop-Location
}

if ($TestExit -ne 0) { Write-Error 'Loop 2 tests failed'; exit 1 }

Write-Host ""
Write-Host "All Loop 2 checks passed." -ForegroundColor Green
exit 0

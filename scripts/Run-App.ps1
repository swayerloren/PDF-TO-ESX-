$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\\Scripts\\python.exe"

if (Test-Path $venvPython) {
    & $venvPython "$repoRoot\\run_app.py"
    exit $LASTEXITCODE
}

& py -3 "$repoRoot\\run_app.py"

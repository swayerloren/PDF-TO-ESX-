$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$specPath = Join-Path $repoRoot "PDF-TO-ESX-Agent.spec"
$distRoot = Join-Path $repoRoot "dist\PDF-TO-ESX-Agent"
$exePath = Join-Path $distRoot "PDF-TO-ESX-Agent.exe"
$buildRoot = Join-Path $repoRoot "build\pyinstaller"
$internalRoot = Join-Path $distRoot "_internal"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    & py -3 -m venv (Join-Path $repoRoot ".venv")
}

Write-Host "Installing build dependencies..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $repoRoot "requirements-build.txt")

if (Test-Path $buildRoot) {
    Remove-Item -LiteralPath $buildRoot -Recurse -Force
}

if (Test-Path $distRoot) {
    Remove-Item -LiteralPath $distRoot -Recurse -Force
}

Write-Host "Building Windows executable..."
Push-Location $repoRoot
try {
    & $venvPython -m PyInstaller `
        --noconfirm `
        --clean `
        --distpath dist `
        --workpath build\pyinstaller `
        $specPath
}
finally {
    Pop-Location
}

if (-not (Test-Path $exePath)) {
    throw "Expected executable was not produced: $exePath"
}

if (Test-Path $internalRoot) {
    Get-ChildItem -LiteralPath $internalRoot -Directory |
        Where-Object { $_.Name -like "*.dist-info" -or $_.Name -eq "__pycache__" } |
        Remove-Item -Recurse -Force
}

if (Test-Path $buildRoot) {
    Remove-Item -LiteralPath $buildRoot -Recurse -Force
}

Write-Host ""
Write-Host "Build completed successfully."
Write-Host "Executable path:"
Write-Host $exePath

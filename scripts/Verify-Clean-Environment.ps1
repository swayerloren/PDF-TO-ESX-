$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$tempRoot = Join-Path $env:TEMP "pdf-to-esx-agent-clean-check"
$venvRoot = Join-Path $tempRoot "venv"
$python = Join-Path $venvRoot "Scripts\\python.exe"

if (Test-Path $tempRoot) {
    Remove-Item -Recurse -Force $tempRoot
}

& py -3 -m venv $venvRoot
& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $repoRoot "requirements.txt")

Push-Location $repoRoot
try {
    & $python -m compileall src run_app.py
    & $python -m unittest discover -s tests -v
    @'
import sys
from pathlib import Path

repo_root = Path.cwd()
sys.path.insert(0, str(repo_root / "src"))

from pdf_to_esx_agent.core.conversion_service import ConversionService
from pdf_to_esx_agent.core.logging import configure_logging
from pdf_to_esx_agent.core.settings import load_settings
from pdf_to_esx_agent.ui.main_window import MainWindow

settings = load_settings()
logger = configure_logging(settings)
service = ConversionService(settings=settings, logger=logger.getChild("clean_check.conversion"))
window = MainWindow(settings=settings, conversion_service=service, logger=logger.getChild("clean_check.ui"))
window._root.update_idletasks()
window._root.destroy()
print("ui-startup-ok")
'@ | & $python -
}
finally {
    Pop-Location
}

if (Test-Path $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
}

Write-Host "Clean-environment verification completed successfully."

param([int]$Port = 0)
$ErrorActionPreference = 'Stop'
$viewerScript = Join-Path $PSScriptRoot 'serve_ui.py'
$runtimePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $runtimePython) {
    $viewerPython = $runtimePython
} else {
    $viewerPython = (Get-Command python -ErrorAction Stop).Source
}
& $viewerPython $viewerScript --port $Port --open
exit $LASTEXITCODE

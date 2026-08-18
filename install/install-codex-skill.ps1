param(
    [string]$Repo = "https://github.com/akim-kaneyev/1c-erp-diagnostics.git",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$SkillName = "one-c-erp-diagnostics"
$TargetRoot = Join-Path $HOME ".agents\skills"
$Target = Join-Path $TargetRoot $SkillName
$Temp = Join-Path ([System.IO.Path]::GetTempPath()) ("1c-erp-diagnostics-" + [Guid]::NewGuid().ToString("N"))

Write-Host "Installing $SkillName to $Target"
New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

git clone --depth 1 --branch $Branch $Repo $Temp
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }

$Source = Join-Path $Temp "skills\one-c-erp-diagnostics"
if (-not (Test-Path (Join-Path $Source "SKILL.md"))) {
    throw "Portable skill not found at $Source"
}

if (Test-Path $Target) {
    Remove-Item -Recurse -Force $Target
}
Copy-Item -Recurse -Force $Source $Target
Remove-Item -Recurse -Force $Temp

Write-Host "Installed: $Target"
Write-Host "Restart Codex, then invoke: `$one-c-erp-diagnostics <task>"

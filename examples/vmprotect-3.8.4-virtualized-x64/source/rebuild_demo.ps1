param([string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$caseSource = Split-Path -Parent $PSScriptRoot
$projectRoot = Split-Path -Parent (Split-Path -Parent $caseSource)
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $projectRoot 'runtime-artifacts\vmp-native-demo'
}
$outputRoot = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $outputRoot) {
    throw "Output directory already exists; choose a fresh -OutputDirectory: $outputRoot"
}

# The recorded LLVM wheel and native build were validated with Python 3.11 x64.
& python -c "import sys,struct; sys.exit(0 if sys.platform == 'win32' and sys.version_info[:2] == (3,11) and struct.calcsize('P') == 8 else 1)"
if ($LASTEXITCODE -ne 0) { throw 'This demo requires Windows x64 and Python 3.11 x64 on PATH' }
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
if (-not (Test-Path -LiteralPath $vswhere)) { throw 'Install Visual Studio C++ x64 build tools and a Windows SDK first' }
$installation = & $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $installation) { throw 'Visual Studio C++ x64 build tools were not found' }

New-Item -ItemType Directory -Path (Join-Path $outputRoot 'source') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $outputRoot 'recovered\native') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $outputRoot 'evidence') -Force | Out-Null
foreach ($name in @('compile_recovered.py', 'link_recovered.ps1', 'recovered_harness.cpp', 'validate_behavior.py')) {
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination (Join-Path $outputRoot 'source')
}
Copy-Item -LiteralPath (Join-Path $caseSource 'recovered\recovered.ll') -Destination (Join-Path $outputRoot 'recovered\recovered.ll')

& python -m venv (Join-Path $outputRoot '.venv')
if ($LASTEXITCODE -ne 0) { throw 'Failed to create the isolated Python environment' }
$demoPython = Join-Path $outputRoot '.venv\Scripts\python.exe'
& $demoPython -m pip install 'llvmlite==0.50.0'
if ($LASTEXITCODE -ne 0) { throw 'Failed to install the pinned LLVM binding' }
& $demoPython (Join-Path $outputRoot 'source\compile_recovered.py') (Join-Path $outputRoot 'recovered\recovered.ll') (Join-Path $outputRoot 'recovered\native')
if ($LASTEXITCODE -ne 0) { throw 'Recovered IR compilation failed' }
& (Join-Path $outputRoot 'source\link_recovered.ps1')

# Validate a renamed copy alone, independent of the source/build directories.
$isolated = Join-Path $outputRoot 'isolated'
New-Item -ItemType Directory -Path $isolated | Out-Null
$executable = Join-Path $outputRoot 'recovered\native\reu-recovered.exe'
$independent = Join-Path $isolated 'independent.exe'
Copy-Item -LiteralPath $executable -Destination $independent
Push-Location $isolated
try {
    & $demoPython (Join-Path $outputRoot 'source\validate_behavior.py') $independent --output (Join-Path $outputRoot 'evidence\demo-behavior.json')
    if ($LASTEXITCODE -ne 0) { throw 'Rebuilt harness failed behavior validation' }
} finally { Pop-Location }

$identities = foreach ($name in @('reu-recovered.dll', 'reu-recovered.exe')) {
    $artifact = Join-Path $outputRoot "recovered\native\$name"
    [ordered]@{ file = $artifact; sha256 = (Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash.ToLowerInvariant() }
}
[ordered]@{
    source = $caseSource
    output = $outputRoot
    python = $demoPython
    ir_sha256 = (Get-FileHash -LiteralPath (Join-Path $outputRoot 'recovered\recovered.ll') -Algorithm SHA256).Hash.ToLowerInvariant()
    configuration = 'Windows x64; Python 3.11; llvmlite 0.50.0; MSVC /O2 /Brepro; isolated EXE behavior checks'
    artifacts = @($identities)
    scope = 'Rebuilds the published recovered IR and source-built CLI harness. Does not unpack or devirtualize a new target, replay a trace, or compare with the protected program.'
} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputRoot 'evidence\demo-build.json') -Encoding utf8
Write-Output "Demo rebuilt; 45 behavior checks passed. EXE: $executable"

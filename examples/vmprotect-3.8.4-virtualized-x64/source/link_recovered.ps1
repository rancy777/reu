$ErrorActionPreference = 'Stop'
$caseRoot = Split-Path -Parent $PSScriptRoot
foreach ($folderName in @('original', 'protected', 'recovered', 'evidence')) {
    $folderPath = Join-Path $caseRoot $folderName
    if (-not (Test-Path -LiteralPath $folderPath -PathType Container)) {
        New-Item -ItemType Directory -Path $folderPath | Out-Null
    }
}
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
$installation = & $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $installation) { throw 'MSVC x64 toolchain not found' }
$devcmd = Join-Path $installation 'Common7\Tools\VsDevCmd.bat'
$environmentScript = Join-Path $caseRoot 'original\build-environment.cmd'
@('@echo off', ('call "{0}" -arch=x64 -host_arch=x64 >nul' -f $devcmd),
  'if errorlevel 1 exit /b 1', 'set') | Set-Content -LiteralPath $environmentScript -Encoding ascii
$environment = & $env:ComSpec /d /c $environmentScript
if ($LASTEXITCODE -ne 0) { throw 'Failed to initialize the MSVC environment' }
foreach ($line in $environment) {
    if ($line -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') }
}

$nativeDir = Join-Path $caseRoot 'recovered\native'
Push-Location $nativeDir
try {
 & link.exe /nologo /DLL /NOENTRY /NODEFAULTLIB /MACHINE:X64 /DYNAMICBASE /NXCOMPAT /Brepro /EXPORT:ReuRecoveredTransform /OUT:reu-recovered.dll /IMPLIB:reu-recovered.lib recovered.obj
 if ($LASTEXITCODE -ne 0) { throw 'Recovered DLL link failed' }
 & cl.exe /nologo /W4 /WX /O2 /GS- /GR- /utf-8 /Brepro /c (Join-Path $PSScriptRoot 'recovered_harness.cpp') /Fo:harness.obj
 if ($LASTEXITCODE -ne 0) { throw 'Harness compile failed' }
 & link.exe /nologo /Brepro /NODEFAULTLIB /ENTRY:entry /SUBSYSTEM:CONSOLE /MACHINE:X64 /DYNAMICBASE /NXCOMPAT /OPT:REF /OPT:ICF /OUT:reu-recovered.exe harness.obj recovered.obj kernel32.lib user32.lib
 if ($LASTEXITCODE -ne 0) { throw 'Recovered EXE link failed' }
} finally { Pop-Location }

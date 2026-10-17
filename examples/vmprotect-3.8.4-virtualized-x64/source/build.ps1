param([Parameter(Mandatory=$true)][string]$SdkDirectory)
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
$output = Join-Path $caseRoot 'original\reu-challenge.exe'
if (Test-Path -LiteralPath $output) { throw 'Refusing to overwrite the original benchmark binary' }
Push-Location (Join-Path $caseRoot 'original')
try {
    $compileOutput = & cl.exe /nologo /W4 /WX /O2 /GS- /GR- /utf-8 /Brepro /I $SdkDirectory /c (Join-Path $PSScriptRoot 'challenge.cpp') /Fo:challenge.obj 2>&1
    $compileExit = $LASTEXITCODE
    $compileOutput | Set-Content -LiteralPath (Join-Path $caseRoot 'evidence\compile.log')
    if ($compileExit -ne 0) { throw 'C++ compilation failed; see compile.log' }
    $linkOutput = & link.exe /nologo /Brepro /NODEFAULTLIB /ENTRY:entry /SUBSYSTEM:CONSOLE /MACHINE:X64 /DYNAMICBASE /NXCOMPAT /OPT:REF /OPT:ICF /OUT:reu-challenge.exe challenge.obj (Join-Path $SdkDirectory "VMProtectSDK64.lib") kernel32.lib user32.lib 2>&1
    $linkExit = $LASTEXITCODE
    $linkOutput | Add-Content -LiteralPath (Join-Path $caseRoot 'evidence\compile.log')
    if ($linkExit -ne 0) { throw 'Link failed; see compile.log' }
    Copy-Item -LiteralPath (Join-Path $SdkDirectory "VMProtectSDK64.dll") -Destination (Join-Path $caseRoot "original\VMProtectSDK64.dll")
    [ordered]@{
        source = Join-Path $PSScriptRoot 'challenge.cpp'
        compiler = (Get-Command cl.exe).Source
        compiler_version = (Get-Item -LiteralPath (Get-Command cl.exe).Source).VersionInfo.FileVersion
        windows_sdk = $env:WindowsSDKVersion.TrimEnd('\')
        source_sha256 = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'challenge.cpp') -Algorithm SHA256).Hash.ToLowerInvariant()
        branch = $null
        head = $null
        baseline = 'Local directory D:\Reu; no Git repository'
        configuration = 'Release x64, MSVC, no CRT, ASLR + NX, deterministic link'
        output = $output
        sha256 = (Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant()
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $caseRoot 'evidence\build.json') -Encoding utf8
} finally { Pop-Location }
Write-Output $output

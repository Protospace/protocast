@echo off
SET PowerShellScriptPath="\\ps\netlogon\protocast\protocast.ps1"
powershell.exe -ExecutionPolicy Bypass -File "%PowerShellScriptPath%" %*
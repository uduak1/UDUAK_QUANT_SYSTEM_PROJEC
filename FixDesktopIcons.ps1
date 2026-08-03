Write-Host "Configuring desktop icon settings..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "AutoArrange" -Value 0 -ErrorAction SilentlyContinue
Write-Host "Restarting Windows Explorer..." -ForegroundColor Cyan
Stop-Process -Name "explorer" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
if (!(Get-Process -Name "explorer" -ErrorAction SilentlyContinue)) { Start-Process "$env:windir\explorer.exe" }
Write-Host "Done!" -ForegroundColor Green

# 设置控制台标题
$host.ui.RawUI.WindowTitle = "ePubViewer 服务启动器"

Write-Host "正在启动 ePubViewer 服务..." -ForegroundColor Green

# 启动后端服务
$backendProcess = Start-Process -FilePath ".\dist\main\main.exe" -PassThru

# 启动前端服务（使用 Python 的 http.server）
$frontendProcess = Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$PSScriptRoot'; python -m http.server 8000`"" -PassThru

Write-Host "`n服务已启动！" -ForegroundColor Green
Write-Host "前端地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "后端地址: http://localhost:8001" -ForegroundColor Cyan
Write-Host "`n按 Ctrl+C 停止所有服务..." -ForegroundColor Yellow

try {
    Wait-Process -Id $backendProcess.Id
}
finally {
    # 清理进程
    if ($null -ne $backendProcess) { Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue }
    if ($null -ne $frontendProcess) { Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue }
} 
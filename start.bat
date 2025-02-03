@echo off
echo 正在启动 ChapterAI 服务...

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 正在检查依赖...
pip install -r requirements.txt >nul 2>&1

REM 启动后端服务
echo 正在启动后端服务...
start /b python api/main.py

REM 等待后端服务启动
timeout /t 2 /nobreak >nul

REM 启动前端服务
echo 正在启动前端服务...
start /b python -m http.server 8000

REM 等待前端服务启动
timeout /t 2 /nobreak >nul

REM 打开浏览器
echo 正在打开浏览器...
start http://localhost:8000

echo ChapterAI 服务已启动！
echo 按任意键停止服务...
pause >nul

REM 结束进程
taskkill /f /im python.exe >nul 2>&1
echo 服务已停止 
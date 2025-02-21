import subprocess
import webbrowser
import time
import os
import signal
import sys
import psutil
from rich.console import Console
from rich.panel import Panel

console = Console()

def kill_process_on_port(port):
    """终止指定端口上运行的进程"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    console.print(f"[yellow]终止端口 {port} 上的进程 {proc.pid}[/yellow]")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def start_services():
    """启动所有服务"""
    try:
        # 确保端口未被占用
        kill_process_on_port(8000)
        kill_process_on_port(8001)

        console.print(Panel("正在启动 ChapterAI 服务...", style="bold blue"))

        # 启动后端服务
        backend_path = os.path.join(os.path.dirname(__file__), "api", "main.py")
        console.print("[green]启动后端服务...[/green]")
        backend_process = subprocess.Popen(
            [sys.executable, backend_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 启动前端服务器
        console.print("[green]启动前端服务器...[/green]")
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 等待服务启动
        time.sleep(2)

        # 检查服务是否成功启动
        if backend_process.poll() is not None or frontend_process.poll() is not None:
            raise Exception("服务启动失败")

        console.print("[green]所有服务启动成功！[/green]")
        console.print(Panel.fit(
            "后端服务: http://localhost:8001\n前端服务: http://localhost:8000",
            title="服务地址",
            style="bold green"
        ))

        # 打开浏览器
        webbrowser.open('http://localhost:8000')
        
        return backend_process, frontend_process

    except Exception as e:
        console.print(f"[red]启动服务时发生错误: {str(e)}[/red]")
        sys.exit(1)

def main():
    try:
        backend_process, frontend_process = start_services()
        
        console.print("\n[cyan]按 Ctrl+C 停止服务...[/cyan]")
        
        # 等待用户按Ctrl+C
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]正在关闭服务...[/yellow]")
        # 优雅关闭服务
        backend_process.terminate()
        frontend_process.terminate()
        console.print("[green]服务已关闭[/green]")
        sys.exit(0)

if __name__ == '__main__':
    main() 
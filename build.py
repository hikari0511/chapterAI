import os
import shutil
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

# 安装rich的异常处理
install()

console = Console()

def run_command(command, error_message):
    """运行命令并检查结果"""
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        console.print(result.stdout)
        if result.stderr:
            console.print(f"[yellow]警告: {result.stderr}[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]错误: {error_message}[/red]")
        console.print(f"[red]命令: {' '.join(command)}[/red]")
        console.print(f"[red]错误输出: {e.stderr}[/red]")
        raise

def ensure_directory(path):
    """确保目录存在，如果存在则清空"""
    console.print(f"[blue]处理目录: {path}[/blue]")
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            console.print(f"[green]已清空目录: {path}[/green]")
        except Exception as e:
            console.print(f"[red]清空目录失败: {path}[/red]")
            console.print(f"[red]错误: {str(e)}[/red]")
            raise
    try:
        os.makedirs(path)
        console.print(f"[green]已创建目录: {path}[/green]")
    except Exception as e:
        console.print(f"[red]创建目录失败: {path}[/red]")
        console.print(f"[red]错误: {str(e)}[/red]")
        raise

def create_dist_directory():
    """创建并清理dist目录"""
    console.print("[blue]正在创建发布目录结构...[/blue]")
    ensure_directory("dist")
    ensure_directory("dist/frontend")
    console.print("[green]发布目录结构创建完成[/green]")

def install_dependencies():
    """安装所有依赖"""
    console.print(Panel("正在安装依赖...", style="bold blue"))
    run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "安装依赖失败"
    )
    console.print("[green]依赖安装完成[/green]")

def build_backend():
    """打包后端服务"""
    console.print(Panel("正在打包后端服务...", style="bold blue"))
    try:
        # 清理之前的构建文件
        for path in ["build", "dist/backend.exe", "backend.spec"]:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                console.print(f"[green]已清理: {path}[/green]")
        
        # 使用更简单的打包命令
        run_command(
            [
                "pyinstaller",
                "--name=backend",
                "--onefile",
                "--distpath=dist",
                "--workpath=build",
                "--specpath=.",
                "api/main.py"
            ],
            "打包后端服务失败"
        )
        
        console.print("[green]后端服务打包完成[/green]")
            
    except Exception as e:
        console.print(f"[red]后端打包失败: {str(e)}[/red]")
        raise

def build_launcher():
    """打包启动器"""
    console.print(Panel("正在打包启动器...", style="bold blue"))
    try:
        # 清理之前的构建文件
        if os.path.exists("start.spec"):
            os.remove("start.spec")
        
        run_command(
            [
                "pyinstaller",
                "--name=start",
                "--clean",
                "-F",
                "launcher.py"
            ],
            "打包启动器失败"
        )
        
        # 移动生成的exe文件
        if os.path.exists("dist/start.exe"):
            shutil.move("dist/start.exe", "dist/")
            console.print("[green]启动器打包完成[/green]")
        else:
            raise FileNotFoundError("未找到生成的start.exe文件")
            
    except Exception as e:
        console.print(f"[red]启动器打包失败: {str(e)}[/red]")
        raise

def copy_frontend_files():
    """复制前端文件"""
    console.print(Panel("正在复制前端文件...", style="bold blue"))
    frontend_files = ["index.html", "script.js", "style.css", "sw.js", "icon.ico", "icon.png"]
    for file in frontend_files:
        try:
            if os.path.exists(file):
                shutil.copy2(file, "dist/frontend/")
                console.print(f"[green]已复制: {file}[/green]")
            else:
                console.print(f"[yellow]警告: 未找到文件 {file}[/yellow]")
        except Exception as e:
            console.print(f"[red]复制文件失败 {file}: {str(e)}[/red]")
            raise

def copy_config_files():
    """复制配置文件"""
    console.print(Panel("正在复制配置文件...", style="bold blue"))
    try:
        if os.path.exists("api/.env"):
            shutil.copy2("api/.env", "dist/")
            console.print("[green]已复制: .env[/green]")
        else:
            console.print("[yellow]警告: 未找到.env文件[/yellow]")
            
        if os.path.exists("README.md"):
            shutil.copy2("README.md", "dist/")
            console.print("[green]已复制: README.md[/green]")
        else:
            console.print("[yellow]警告: 未找到README.md文件[/yellow]")
    except Exception as e:
        console.print(f"[red]复制配置文件失败: {str(e)}[/red]")
        raise

def create_release_package():
    """创建发布包"""
    console.print(Panel("正在创建发布包...", style="bold blue"))
    try:
        # 检查必要文件
        required_files = [
            ("dist/backend.exe", "后端服务"),
            ("dist/start.exe", "启动器"),
            ("dist/frontend", "前端文件"),
            ("dist/.env", "配置文件")
        ]
        
        for file_path, description in required_files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"缺少必要文件: {description} ({file_path})")
        
        # 创建zip文件
        if os.path.exists("ChapterAI.zip"):
            os.remove("ChapterAI.zip")
        
        shutil.make_archive("ChapterAI", "zip", "dist")
        console.print("[green]发布包创建完成[/green]")
        
    except Exception as e:
        console.print(f"[red]创建发布包失败: {str(e)}[/red]")
        raise

def main():
    try:
        console.print(Panel("开始构建 ChapterAI 发布包", style="bold blue"))
        
        # 执行构建步骤
        create_dist_directory()
        install_dependencies()
        build_backend()
        build_launcher()
        copy_frontend_files()
        copy_config_files()
        create_release_package()
        
        console.print(Panel("构建完成！\n发布包已保存为: ChapterAI.zip", style="bold green"))
        
    except Exception as e:
        console.print(Panel(f"构建失败！\n错误: {str(e)}", style="bold red"))
        sys.exit(1)

if __name__ == "__main__":
    main() 
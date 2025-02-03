# ChapterAI - epub章节分析助手

ChapterAI 是一个epub文件分章节分析工具，它能够帮助用户快速理解和提炼文章的核心内容。通过先进的AI技术，ChapterAI可以自动分析文章结构，提取关键观点，并生成清晰的可视化图表。

## 项目引用

本项目的前端界面基于 [ePubViewer](https://github.com/pgaskin/ePubViewer) 项目进行修改和适配。感谢原作者的开源贡献。

## 功能特点

- 🚀 快速分析：快速完成文章内容分析
- 📊 可视化展示：自动生成思维导图和流程图
- 🎯 核心观点提取：准确识别文章重点
- 💡 智能总结：生成结构化的内容概述
- 🔄 支持deepseek AI模型：兼容DeepSeek和SiliconFlow API

## 系统要求

- Windows 10 或更高版本
- Python 3.8 或更高版本
- 浏览器（推荐使用 Chrome 或 Edge）

## 安装说明

### 方法一：使用发布包（推荐）

1. 从 [Releases](https://github.com/hikari0511/chapterAI/releases) 页面下载最新的`ChapterAI.zip`
2. 将压缩包解压到任意目录
3. 进入解压后的目录
4. 编辑`api/.env`文件，配置您的API密钥（参见配置说明）
5. 双击运行`start.bat`即可启动服务

### 方法二：从源码安装

1. 克隆或下载本仓库：
   ```bash
   git clone https://github.com/yourusername/chapterAI.git
   cd chapterAI
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 编辑配置：
   ```bash
   cd api
   # 编辑.env文件，填入您的API密钥
   ```

## 使用方法

1. 双击运行 `start.bat`
2. 等待服务启动，浏览器会自动打开到 http://localhost:8000
3. 将文章内容粘贴到输入框
4. 点击"分析"按钮
5. 等待分析完成，查看结果
6. 按任意键停止服务

## 配置说明

在`api/.env`文件中，您可以配置以下选项：

```ini
# API提供商选择 (deepseek/siliconflow)
API_PROVIDER=deepseek

# DeepSeek API配置
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# SiliconFlow API配置
SILICONFLOW_API_KEY=your_key_here
SILICONFLOW_BASE_URL=https://api.siliconflow.com/v1
SILICONFLOW_MODEL=silicon-chat
```
硅基流动API获取地址：https://cloud.siliconflow.cn/i/k6Zl8Oeo

## 项目结构

```
chapterAI/
├── api/                 # 后端代码
│   ├── main.py         # 主服务器代码
│   ├── config.py       # 配置管理
│   └── .env           # 环境变量
├── frontend/           # 前端静态文件
│   ├── index.html     # 主页面
│   ├── script.js      # 前端逻辑
│   └── style.css      # 样式表
├── start.bat          # 启动脚本
└── requirements.txt   # 项目依赖
```

## 常见问题

1. **Q: 如何切换API提供商？**  
   A: 在`.env`文件中修改`API_PROVIDER`的值。

2. **Q: 启动时报端口占用错误？**  
   A: 确保8000和8001端口未被其他程序占用。可以在命令提示符中运行：
   ```bash
   netstat -ano | findstr :8000
   netstat -ano | findstr :8001
   ```
   然后使用任务管理器结束占用端口的进程。

3. **Q: 如何查看服务日志？**  
   A: 服务启动时会在命令提示符窗口显示日志信息。

4. **Q: Python未安装或版本不正确？**  
   A: 从[Python官网](https://www.python.org/downloads/)下载并安装Python 3.8或更高版本。安装时请勾选"Add Python to PATH"选项。


## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [ePubViewer](https://github.com/pgaskin/ePubViewer) - 提供了优秀的前端界面基础
- [3mintop](https://3min.top/) - 为页面布局提供了灵感

import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# API Provider Selection
API_PROVIDER = os.getenv('API_PROVIDER', 'deepseek')

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

# Silicon Flow API Configuration
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY')
SILICONFLOW_BASE_URL = os.getenv('SILICONFLOW_BASE_URL', 'https://api.siliconflow.cn/v1')
SILICONFLOW_MODEL = os.getenv('SILICONFLOW_MODEL', 'deepseek-ai/DeepSeek-V3')

# API Common Settings
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4000))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))

# CORS配置
ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    # 添加其他允许的域名
] 
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
from config import (
    DEEPSEEK_API_KEY, SILICONFLOW_API_KEY,
    DEEPSEEK_BASE_URL, SILICONFLOW_BASE_URL,
    DEEPSEEK_MODEL, SILICONFLOW_MODEL,
    API_PROVIDER, ALLOWED_ORIGINS, 
    MAX_TOKENS, TEMPERATURE
)

app = FastAPI()

# 配置CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChapterContent(BaseModel):
    content: str
    chapter_title: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
    error_type: Optional[str] = None

@app.options("/api/summarize")
async def options_route():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        },
    )

def get_ai_client():
    """根据配置返回相应的AI客户端"""
    if API_PROVIDER == "deepseek":
        return OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        ), DEEPSEEK_MODEL
    elif API_PROVIDER == "siliconflow":
        return OpenAI(
            api_key=SILICONFLOW_API_KEY,
            base_url=SILICONFLOW_BASE_URL
        ), SILICONFLOW_MODEL
    else:
        raise ValueError(f"不支持的API提供商: {API_PROVIDER}")

# 获取AI客户端
client, model = get_ai_client()

@app.post("/api/summarize", response_model=dict, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def summarize_chapter(chapter: ChapterContent):
    print(f"收到章节总结请求 (使用 {API_PROVIDER} API)")
    print(f"章节标题: {chapter.chapter_title}")
    print(f"章节内容长度: {len(chapter.content)}")

    if not chapter.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="章节内容不能为空",
            headers={"X-Error-Type": "EMPTY_CONTENT"}
        )

    try:
        chapter_title = f"《{chapter.chapter_title}》" if chapter.chapter_title else "本章"
        print(f"正在调用 {API_PROVIDER} API 进行总结...")
        
        # 获取最新的客户端实例
        current_client, current_model = get_ai_client()
        
        system_content = """你是一个专业的文章分析助手，你能够准确地找到文章的重点，同时又不遗漏原文的细节，你的讲述富有故事性。请使用 Markdown 格式按照以下结构对{}内容进行分析：

## 总体概述

用2-3句话概括本章的主要内容和中心思想。

## 核心观点

针对每个核心观点，请按以下结构分析，把重点放在原文的支撑依据上，观点之间避免重复：

### 观点 1：[观点标题]
- **核心内容**：清晰说明观点的具体内容
- **支撑依据**：如果有相关的案例、故事或个人经历，请详细描述，体现原文的故事性，请务必包含故事的起因经过结果和人物，人物需要包含该人物身份和姓名的介绍。并引用发人深省的原文语句作为支撑。如果作者对某概念做了解释，请详细描述该概念的定义和解释。
- **论证分析**：解释这些例证如何支持该观点
- **可视化**：根据观点内容的性质，使用以下一种或多种 Mermaid 图形进行可视化：

1. 流程图(graph TD): 用于表示步骤或决策过程
2. 思维导图(mindmap): 用于表示概念层级关系
3. 饼图(pie): 用于表示数据占比或分布情况
4. 状态图(stateDiagram-v2): 用于表示状态转换或并行处理

注意：
1. 使用中文描述节点和关系
2. 图形逻辑清晰，层次分明
3. 避免过于复杂的图形结构
4. 确保每个图形都有明确的起点和终点
5. 必须使用三个反引号加 mermaid 标记来包裹图形代码"""

        response = current_client.chat.completions.create(
            model=current_model,
            messages=[
                {
                    "role": "system",
                    "content": system_content.format(chapter_title)
                },
                {
                    "role": "user",
                    "content": f"请分析以下内容：\n\n{chapter.content}"
                }
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        print(f"{API_PROVIDER} API 调用完成")
        
        return JSONResponse(
            content={"summary": response.choices[0].message.content},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "86400",
            }
        )
    except Exception as e:
        error_msg = str(e)
        error_type = "AI_SERVICE_ERROR"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        if "Insufficient Balance" in error_msg:
            error_msg = f"{API_PROVIDER} API 服务余额不足，请联系管理员充值"
            error_type = "INSUFFICIENT_BALANCE"
            status_code = status.HTTP_402_PAYMENT_REQUIRED
            
        print(f"发生错误: {error_msg}")
        raise HTTPException(
            status_code=status_code,
            detail=error_msg,
            headers={
                "X-Error-Type": error_type,
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "86400",
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from app.core.tools import find_product, add_to_cart_tool, auto_order_tool
from app.core.rag import search_knowledge
import os

def chat_with_qwen(message: str, user_id: int = None):
    def make_tools(uid):
        return [
            Tool(name="find_product",
                 func=lambda kw: str(find_product(kw)),
                 description="根据关键词查找商品，输入为关键词字符串"),
            Tool(name="add_to_cart",
                 func=lambda inp: add_to_cart_tool(uid, int(inp.strip())),
                 description="将商品加入购物车，输入为商品ID（整数）"),
            Tool(name="auto_order",
                 func=lambda inp: auto_order_tool(uid, int(inp.strip())),
                 description="自动创建订单并支付，输入为地址ID（整数）"),
        ]

    # 检索知识库，将相关内容作为上下文注入
    knowledge_results = search_knowledge(message)
    if knowledge_results:
        context = "\n".join(f"- {k}" for k in knowledge_results)
        message = f"【参考知识库内容】\n{context}\n\n【用户问题】\n{message}"

    llm = ChatOpenAI(
        model="qwen-plus",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    tools = make_tools(user_id)
    agent = create_react_agent(llm, tools)

    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    return result["messages"][-1].content
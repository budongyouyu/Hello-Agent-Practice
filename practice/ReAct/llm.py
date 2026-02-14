import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict,List

""" 加载环境变量 """
load_dotenv()

""" LLM客户端类 """
class HelloAgentLLM():

    def __init__(self, model:str = None, apikey: str = None, base_url: str = None, timeout: int = None):
        self.model = model or os.getenv('LLM_MODEL_ID')
        apikey = apikey or os.getenv('LLM_API_KEY')
        base_url = base_url or os.getenv('LLM_BASE_URL')
        timeout = timeout or os.getenv('LLM_TIMEOUT')

        if not all([self.model, apikey, base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apikey, base_url=base_url, timeout=timeout)

    def think(self, message: List[Dict[str, str]], tempature: float = 0) -> str:
        print(f"正在调用{self.model}")
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = message,
                temperature=tempature,
                stream=True,
            )
            print(f"调用{self.model}成功")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                collected_content.append(content)
                print("\n")
                return "".join(collected_content)
        except Exception as e:
            print(f"调用{self.model}时发生错误：{e}")
            return None

# --- 客户端使用示例 ---
if __name__ == '__main__':
    try:
        llmClient = HelloAgentLLM()
        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writesPython code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]
        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        print(responseText)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)
    except ValueError as e:
            print(e)
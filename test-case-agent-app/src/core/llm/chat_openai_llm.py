from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class ChatLLM:
    def __init__(self, model_name, llm_base_url, llm_api_key, temperature=0.7):
        self.chat = ChatOpenAI(
            model_name=model_name,
            openai_api_base=llm_base_url,
            openai_api_key=llm_api_key,
            temperature=temperature
        )
    
    async def get_response(self, system_message: str, user_message: str) -> str:
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message)
        ]
        response = await self.chat(messages)
        return response.content

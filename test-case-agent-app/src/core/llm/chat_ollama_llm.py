from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class ChatLLM:
    def __init__(self, model_name):
        self.llm = ChatOllama(
            model=model_name
        )
    
    def get_chat_model(self):
        return self.llm
    
    async def get_response(self, system_message: str, user_message: str) -> str:
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message)
        ]
        response = await self.chat.ainvoke(messages)
        return response.content

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

class ChatLLM:
    def __init__(self, model_name, llm_api_key, temperature=0.7):
        self.chat = ChatGroq(
            model=model_name,
            groq_api_key=llm_api_key,
            temperature=temperature
        )
    
    async def get_response(self, system_message: str, user_message: str) -> str:
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message)
        ]
        response = await self.chat.ainvoke(messages)
        return response.content

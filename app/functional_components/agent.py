from typing import Any

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_openai import ChatOpenAI

from .rag_pipeline import RAGMultiModalModelPipeline
from .constants import RAG_TOOL_DESCRIPTION, RAG_TOOL_NAME
from .schemas import RAGPipelineInputSchema


class Agent:
    def __init__(
            self,
            llm: ChatOpenAI,
            rag_pipeline: RAGMultiModalModelPipeline,
            system_prompt: str
    ):
        self._llm = llm
        self.rag_pipeline = rag_pipeline
        self._system_prompt = system_prompt
        self._agent_executor = None
        self.store = dict()

    @property
    def tools(self) -> list:
        return [
            self.rag_pipeline.chain.as_tool(
                name=RAG_TOOL_NAME,
                description=RAG_TOOL_DESCRIPTION,
                args_schema=RAGPipelineInputSchema
            )
        ]

    @staticmethod
    def build_prompt(system_prompt: str) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(messages=[
            SystemMessagePromptTemplate.from_template(template=system_prompt),
            HumanMessagePromptTemplate.from_template(template="{query}"),
            MessagesPlaceholder("agent_scratchpad", optional=True)
        ])

    def get_session_history(self, session_id: str | None) -> BaseChatMessageHistory:
        if not session_id:
            return ChatMessageHistory()
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def build_agent(self) -> None:
        prompt = self.build_prompt(self._system_prompt)
        agent = create_tool_calling_agent(llm=self._llm, tools=self.tools, prompt=prompt)
        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools)

        self._agent_executor = RunnableWithMessageHistory(
            agent_executor,
            self.get_session_history,
            input_messages_key="query",
            history_messages_key="chat_history",
            output_messages_key="output",
        )

    async def reply(self, message: dict[str, Any]) -> str:
        return await self._agent_executor.ainvoke(
            message,
            config={
                "configurable": {"session_id": message.get("session_id", None)},
            }
        )

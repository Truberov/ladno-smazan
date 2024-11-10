from operator import itemgetter
from typing import Any

from byaldi import RAGMultiModalModel
from byaldi.objects import Result
from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, Runnable
from langchain_openai import ChatOpenAI

from .settings import Settings
from .constants import ID_MAP


class RAGMultiModalModelPipeline:
    chain: Runnable = None

    def __init__(
            self,
            retriever: RAGMultiModalModel,
            llm: ChatOpenAI,
            system_prompt: str,
            settings: Settings,
    ):
        self._retriever = retriever
        self._llm = llm
        self._system_prompt = system_prompt
        self._settings = settings

    @staticmethod
    def format_context(document: Result) -> str:
        return document.base64

    async def get_messages(self, _input_data: dict[str, Any]) -> list[BaseMessage]:
        query = _input_data['query']
        image_url = f"data:image/jpeg;base64,{self.format_context(_input_data["context"][0])}"

        return [
            SystemMessage(content=self._system_prompt),
            SystemMessage(content="Next message is human question"),
            HumanMessage(content=query),
            SystemMessage(content="Next message is document knowledge base"),
            HumanMessage(content=[
                {"type": "image_url", "image_url": {"url": image_url}}
            ]),
        ]

    async def reply(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self.chain.ainvoke(data)

    async def get_retriever_result(self, query: str) -> list[Result]:
        _results = self._retriever.search(k=self._settings.retriever_top_k, query=query)
        for _result in _results:
            _result.doc_id = ID_MAP.get(str(_result.doc_id))

        return _results

    def build_chain(self) -> None:
        generation_chain = RunnableLambda(self.get_messages) | self._llm | StrOutputParser()
        retriever_chain = itemgetter("query") | RunnableLambda(self.get_retriever_result)

        self.chain = RunnablePassthrough().assign(context=retriever_chain).assign(answer=generation_chain)

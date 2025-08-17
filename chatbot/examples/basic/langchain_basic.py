# import getpass
# import os

# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "sk-HecyDPgFCKdgjIK5qkdbFQXrAWJbETWcKtlFcnZoJCxoNQuL"
# os.environ["OPENAI_API_BASE"] = "https://api.moonshot.cn/v1"
# os.environ['http_proxy']="http://127.0.0.1:9328"
# os.environ['https_proxy']="http://127.0.0.1:9328"

# from langchain_openai import ChatOpenj

# model = ChatOpenAI(model="kimi-k2-0711-previewgpt-p4")

# <!--IMPORTS:[{"imported": "HumanMessage", "source": "langchain_core.messages", "docs": "https://python.langchain.com/api_reference/core/messages/langchain_core.messages.human.HumanMessage.html", "title": "Build a Simple LLM Application with LCEL"}, {"imported": "SystemMessage", "source": "langchain_core.messages", "docs": "https://python.langchain.com/api_reference/core/messages/langchain_core.messages.system.SystemMessage.html", "title": "Build a Simple LLM Application with LCEL"}]-->
# from langchain_core.messages import HumanMessage, SystemMessage

# messages = [
#     SystemMessage(content="Translate the following from English into Italian"),
#     HumanMessage(content="hi!"),
# ]

# model.invoke(messages)
import os
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain.schema import HumanMessage, SystemMessage
os.environ["MOONSHOT_API_KEY"] = 'sk-aFQzgnbOCKRqOpEkYiqFlbAWgkFSU8TOsVFQRK2FTPLKQ2dX'
chat = MoonshotChat(
    model="kimi-latest",
    temperature=0.8,
    max_tokens=20,)
messages = [
    # SystemMessage(content="你是一个很棒的智能助手"),
    # HumanMessage(content="请给我的花店起个名,多输出几个结果，直接输出名字，不要输出多余的语句")
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]
response = chat.invoke(messages)
print(response)
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
# 连接
client = OpenAI(
    api_key = 'sk-HecyDPgFCKdgjIK5qkdbFQXrAWJbETWcKtlFcnZoJCxoNQuL',
    base_url = 'https://api.moonshot.cn/v1',
)
# prompt
response =  client.chat.completions.create(
    model="moonshot-v1-8k", # 模型名
    messages=[
        {"role": "system", "content": "You are a creative AI."},
        {"role": "user", "content": "请给我的花店起个名,多输出几个结果，直接输出名字，不要输出多余的语句"},
    ], # prompt要求
    temperature=0.8, # 随机度
    max_tokens=20, # 最大输出token数
    #这个的意思是将结果截取到这个token数，并不是response只有这些token数
)
# 输出
# print(response.choices[0].message.content)

parser = StrOutputParser()
parser.invoke(response.choices[0].message.content)
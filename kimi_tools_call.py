from typing import *
import json
from openai import OpenAI
import os
import json
from diophila import OpenAlex
openalex = OpenAlex()
client = OpenAI(
    api_key="sk-106i1MhEY7PtQtNMYPwOly1pf2LuvTgxseX3XvF9pKrhoB0D", # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)
 
tools = [
	{
		"type": "function", # 约定的字段 type，目前支持 function 作为值
		"function": { 
			"name": "get_weather", 
			"description": """ 
				获取当前天气
				当你的知识无法回答用户提出的问题，或用户请求你进行联网搜索时，调用此工具。
			""",
			"parameters": { # 使用 parameters 字段来定义函数接收的参数
				"type": "object",
				"required": ["city"], # 使用 required 字段告诉 Kimi 大模型哪
				"properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather information for.",
                    },
                },
			}
		}
	},
    {
		"type": "function", 
		"function": { 
			"name": "get_paper", 
			"description": """ 
				通过openAlex进行检索文献,当用户请求你进行文献查找时，调用此工具。
			""",
			"parameters": { # 使用 parameters 字段来定义函数接收的参数
				"type": "object",
				"required": ["search","filters"], # 使用 required 字段告诉 Kimi 大模型哪
				"properties": {
                    "search": {
                        "type": "string",
                        "description": "结合上下文，用户要查找的论文的主题",
                    },
                    "filters": {
                        "type": "dict",
                        "description": """结合上下文，用户要查找的文献的筛选条件，只有以下这些过滤条件：abstract.search,alternate_host_venues.id,alternate_host_venues.license,alternate_host_venues.version,author.id,author.orcid,authorships.author.id,authorships.author.orcid,authorships.institutions.country_code,authorships.institutions.id,authorships.institutions.ror,authorships.institutions.type,cited_by,cited_by_count,cites,concept.id,concepts.id,concepts.wikidata,display_name,display_name.search,doi,from_created_date,from_publication_date,from_updated_date,has_doi,has_oa_accepted_or_published_version,has_oa_submitted_version,host_venue.id,host_venue.issn,host_venue.publisher,ids.mag,ids.openalex,ids.pmcid,ids.pmid,institution.id,institutions.country_code,institutions.id,institutions.ror,institutions.type,is_oa,is_paratext,is_retracted,journal.id,mag,oa_status,open_access.is_oa,open_access.oa_status,openalex,openalex_id,pmcid,pmid,publication_date,publication_year,raw_affiliation_string.search,referenced_works,related_to,title.search,to_publication_date,type.例如：{"is_oa": "true"，"type":"review"}"""
                    }
                },
			}
		}
	},
]
 
openalex = OpenAlex()
def get_paper(search):
    # print(search)
    grouped_concepts_list = openalex.get_list_of_works(search=search["search"],pages=[i for i in range(1, 2)],filters=search["filters"],sort={"relevance_score":"desc",})
    concepts_list = list(grouped_concepts_list)
    title, doi = [], []
    for id in concepts_list[0]["results"]:
        title.append(id["title"])
        doi.append(id["doi"])
    save = {"title":title, "doi":doi}
    return save
 
MAX_CALLS = 30  # 设置最大函数调用次数
num_calls = 0  # 初始化调用计数器

messages = [
    {"role": "system",
     "content": "你是一个文献搜索助手，返回用户查找的文献的名称与doi号"},
    {"role": "user", "content": "使用openAlex查找有关carbon material的2024年的文章"}  # 在提问中要求 Kimi 大模型联网搜索
]
 
finish_reason = None
 
tool_map = {
    "get_paper": get_paper,
}
while finish_reason is None or finish_reason == "tool_calls":
    if num_calls >= MAX_CALLS:  # 超过最大调用次数时候终止
        break

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        tool_choice="auto",
        temperature=0.3,
        tools=tools,
    )
    print(completion.choices[0].model_dump_json(indent=4))
    choice = completion.choices[0]
    
    finish_reason = choice.finish_reason
    if finish_reason == "tool_calls": # <-- 判断当前返回内容是否包含 tool_calls
        messages.append(choice.message) # <-- 我们将 Kimi 大模型返回给我们的 assistant 消息也添加到上下文中，以便于下次请求时 Kimi 大模型能理解
        for tool_call in choice.message.tool_calls: # <-- tool_calls 可能是多个，因此我们使用循环逐个执行
            tool_call_name = tool_call.function.name
            tool_call_arguments = json.loads(tool_call.function.arguments) # <-- arguments 是序列化后的 JSON Object，我们需要使用 json.loads 反序列化一下
            tool_function = tool_map[tool_call_name] # <-- 通过 tool_map 快速找到需要执行哪个函数
            tool_result = tool_function(tool_call_arguments)
 
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call_name,
                "content": json.dumps(tool_result), # <-- 我们约定使用字符串格式向 Kimi 大模型提交工具调用结果，因此在这里使用 json.dumps 将执行结果序列化成字符串
            })
            messages.append({"role": "user", "content": "请按相关性进行排序"} )
    num_calls += 1

print(choice.message.content) # <-- 在这里，我们才将模型生成的回复返回给用户

print(messages)

completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.3,
        tools=tools,
    )
print(completion.choices[0].model_dump_json(indent=4))
choice = completion.choices[0]

print(choice.message.content)

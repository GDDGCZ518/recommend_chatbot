
'''
api密钥:
sk-106i1MhEY7PtQtNMYPwOly1pf2LuvTgxseX3XvF9pKrhoB0D
'''

from openai import OpenAI
import json

# 创建客户端实例 
client = OpenAI(
    api_key = "sk-106i1MhEY7PtQtNMYPwOly1pf2LuvTgxseX3XvF9pKrhoB0D",
    base_url = "https://api.moonshot.cn/v1",
)

json_file_path = './tmp/meta analysis/meta analysis2013.json'
with open(json_file_path, 'r', encoding='utf-8') as file:
    json_file = json.load(file)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_delivery_date",
            "description": "Get the delivery date for a customer's order. Call this whenever you need to know the delivery date, for example when a customer asks 'Where is my package'",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID."
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    }
]

# messages = [
#         {"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."},
#         {"role": "user", "content": "Hi, can you tell me the delivery date for my order?"},
#         {"role": "assistant", "content": "Hi there! I can help with that. Can you please provide your order ID?"},
#         {"role": "user", "content": "i think it is order_12345"},
#         response['choices'][0]['message'],
#         function_call_result_message
#     ]
messages = []
messages.append({"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."})
messages.append({"role": "user", "content": "Hi, can you tell me the delivery date for my order?"})
messages.append({"role": "assistant", "content": " Can you please provide your order ID?"})
messages.append({"role": "user", "content": "i think it is order_12345"})
messages1 = messages
# 发送聊天完成请求 
completion = client.chat.completions.create(
    model = "moonshot-v1-8k",
    # tools = json_file,
    tools = tools,
    tool_choice = "auto",
    # tool_choice = "required",
    # messages = [
    #     {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    #     {"role": "user", "content": "请给出该年关于这条检索的推荐结果"}
    # ],
    messages=messages1,
    temperature = 0.3,
)
# print(completion)
print(completion.choices[0].message.content)




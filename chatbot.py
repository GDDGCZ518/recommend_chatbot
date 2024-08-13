import requests
import json
import os

# # 通过Moonshot AI API生成文本，即kimi生成文本，文档：https://platform.moonshot.cn/docs/api-reference#%E8%AF%B7%E6%B1%82%E5%86%85%E5%AE%B9
# def kimi_chat(user_message):
#     MOONSHOT_API_KEY = os.getenv('MOONSHOT_API_KEY')

#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {MOONSHOT_API_KEY}',
#     }

#     data = {
#         "model": "moonshot-v1-32k",      # moonshot-v1-8k,moonshot-v1-32k,moonshot-v1-128k
#         "messages": [
#             # {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
#             {"role": "user", "content": user_message}
#         ],
#         "temperature": 0.5,
#     }

#     response = requests.post('https://api.moonshot.cn/v1/chat/completions', headers=headers, data=json.dumps(data))
#     response_json = response.json()
#     # 提取出你需要的部分
#     assistant_message = response_json['choices'][0]['message']['content']

#     return assistant_message


# # 调用函数
# if __name__ == '__main__':
#     print(kimi_chat('你能干吗？')) 

'''
api密钥:
sk-106i1MhEY7PtQtNMYPwOly1pf2LuvTgxseX3XvF9pKrhoB0D
'''



# from openai import OpenAI

# # 创建客户端实例 
# client = OpenAI(
#     api_key = "sk-106i1MhEY7PtQtNMYPwOly1pf2LuvTgxseX3XvF9pKrhoB0D",
#     base_url = "https://api.moonshot.cn/v1",
# )
 
# # 发送聊天完成请求 
# completion = client.chat.completions.create(
#     model = "moonshot-v1-8k",
#     messages = [
#         {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
#         {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
#     ],
#     temperature = 0.3,
# )

# # 打印生成的消息内容 
# print(completion.choices[0].message.content)

from diophila import OpenAlex

openalex = OpenAlex()

# random_author = openalex.get_random_author()
# random_author['id']
# print(random_author)

# specific_work = openalex.get_single_work("https://doi.org/10.1364/PRJ.433188") 
# print(specific_work['display_name'])

# specific_author = openalex.get_single_author('https://doi.org/10.1364/PRJ.433188')
# print(specific_author)

# concept_groups = openalex.get_groups_of_concepts(
#     group_by='category',
#     filters={'status': 'active'},
#     search='机器学习',
#     sort={'name': 'asc'}
# )

# grouped_institutions = openalex.get_groups_of_institutions("type")
# print(grouped_institutions)
# for group in grouped_institutions['group_by']:
#     print(group['key'])

search_name = 'solar battery'
filters = {"is_oa": "true",
           "type": "review",
           "publication_year": 2013,
           }
grouped_concepts_list = openalex.get_list_of_works(search=search_name,pages=[1,20],filters=filters)

# 收集生成器中的所有数据
concepts_list = list(grouped_concepts_list)

# 保存的文件名
save_file_name = search_name + '.json'

# 将数据转换为JSON格式并保存到文件
with open(save_file_name, 'w', encoding='utf-8') as f:
    json.dump(concepts_list, f, ensure_ascii=False, indent=4)


# 迭代生成器
# for concept in grouped_concepts_list:
#     print(concept)

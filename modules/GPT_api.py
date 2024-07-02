from openai import OpenAI
import os



def GPT_generation(pdf_text):

    # 设置API密钥
    c_key = 'sk-proj-q4BSmJAdKjBDAhm6xtBST3BlbkFJxey686dvUm4P0MMb8l91'

    #连接api
    client = OpenAI(api_key=c_key)

    #导入提问句
    base_dir = os.path.dirname(os.path.abspath(__file__))
    instruction_path = os.path.join(base_dir, '../instruction.txt')
    with open(instruction_path, 'r') as instruction_file:
        instructions = instruction_file.read()

    #创建会话
    client = OpenAI(api_key=c_key)

    #完成会话信息
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": instructions},
        {"role": "user", "content": pdf_text}
      ]
    )

    #返回生成结果
    return response.choices[0].message.content



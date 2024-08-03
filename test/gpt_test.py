from openai import OpenAI
import pandas as pd


# Read data from CSV file
df = pd.read_csv('./data.csv')

# Extract 'Answer' and 'Evidence' columns as lists
answer_list = df['Answer'].tolist()
evidence_list = df['Evidence'].tolist()

# Function to get similarity score using GPT
def GPT_STS(text):

    # Set API key
    c_key = 'sk-proj-q4BSmJAdKjBDAhm6xtBST3BlbkFJxey686dvUm4P0MMb8l91'

    # Connect to OpenAI API
    client = OpenAI(api_key=c_key)

    # Instructions for the GPT model
    instructions = "I will input two paragraphs of text.(Separate with/) Please help me analyze whether the semantics of the two ends of the text are similar, and only provide me with a floating point number from 0 to 4(0,1,2,3,4, and 0 is not similar, 4 is very similar) to represent its similarity."

    # Create a session with the API
    client = OpenAI(api_key=c_key)

    # Complete the session with the given text
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ]
    )

    # Return the generated result
    return response.choices[0].message.content

# Iterate through the answer and evidence lists, compute similarity, and print it
df = pd.read_csv('data.csv')

# 计算每一对answer和evidence的相似度
similarity_scores = []
for idx, row in df.iterrows():
    answer = row['Answer']
    evidence = row['Evidence']
    similarity = GPT_STS(answer + "/" + evidence)
    similarity_scores.append(similarity)
    print(similarity)

df['Result'] = similarity_scores

df.to_csv('gpt_results.csv', index=False)

print("完成匹配，并将结果保存到gpt_results.csv中")
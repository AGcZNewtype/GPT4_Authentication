import pandas as pd
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

# Load data
df = pd.read_csv('./train.csv')

# Ensure the column name matches the actual column name in the CSV file
label_column = 'Label'

# Split dataset
train_df, test_df = train_test_split(df, test_size=0.2)

# Load pre-trained Sentence-BERT model
model_name = 'bert-base-nli-mean-tokens'
model = SentenceTransformer(model_name)

# Define custom dataset class
class STSDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        return self.encodings[idx], self.labels[idx]

    def __len__(self):
        return len(self.labels)

# Create dataset
train_encodings = list(zip(train_df['Answer'].astype(str).tolist(), train_df['Evidence'].astype(str).tolist()))
test_encodings = list(zip(test_df['Answer'].astype(str).tolist(), test_df['Evidence'].astype(str).tolist()))

train_dataset = STSDataset(train_encodings, train_df[label_column].tolist())
test_dataset = STSDataset(test_encodings, test_df[label_column].tolist())

# Train and evaluate the model (this will be unsupervised so we don't use a Trainer)
def calculate_similarity(model, dataset):
    similarities = []
    for idx, (answer, evidence) in enumerate(dataset):
        try:
            embedding1 = model.encode(answer, convert_to_tensor=True)
            embedding2 = model.encode(evidence, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
            similarities.append(similarity)
        except Exception as e:
            print(f"Error processing index {idx}: {e}")
            print(f"Answer: {answer}")
            print(f"Evidence: {evidence}")
            similarities.append(0.0)  # Assign a default similarity score in case of error
    return similarities

train_similarities = calculate_similarity(model, train_dataset)
test_similarities = calculate_similarity(model, test_dataset)

# Define function to convert similarity score to label
def convert_to_label(score):
    if 0 <= score < 0.2:
        return 0
    elif 0.2 <= score < 0.4:
        return 1
    elif 0.4 <= score < 0.6:
        return 2
    elif 0.6 <= score < 0.8:
        return 3
    elif 0.8 <= score <= 1:
        return 4
    else:
        return None  # Handle unexpected scores

# Convert similarities to labels
train_labels = [convert_to_label(score) for score in train_similarities]
test_labels = [convert_to_label(score) for score in test_similarities]

# Calculate accuracy for evaluation
train_accuracy = np.mean(np.array(train_labels) == np.array(train_df[label_column]))
test_accuracy = np.mean(np.array(test_labels) == np.array(test_df[label_column]))

print(f"Train Accuracy: {train_accuracy}")
print(f"Test Accuracy: {test_accuracy}")

# Method to predict similarity score
def predict_similarity(answer, evidence):
    model.eval()
    embedding1 = model.encode(answer, convert_to_tensor=True)
    embedding2 = model.encode(evidence, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
    label = convert_to_label(similarity)
    return label

# Test with data.csv
df = pd.read_csv('data.csv')
similarity_scores = []
for idx, row in df.iterrows():
    answer = row['Answer']
    evidence = row['Evidence']
    similarity = predict_similarity(answer, evidence)
    similarity_scores.append(similarity)

# Add similarity results to a new column
df['Bert result label'] = similarity_scores

df.to_csv('bert_results.csv', index=False)
print("Results saved to bert_results.csv")






################无预训练模型######################################################
# import pandas as pd
# from sentence_transformers import SentenceTransformer, util
#
# class BertModelWrapper:
#     def __init__(self):
#         # 加载Sentence-BERT模型
#         self.sentence_model = SentenceTransformer('bert-base-nli-mean-tokens')
#
#     def cosine_similarity(self, embedding1, embedding2):
#         # 计算余弦相似度
#         return util.pytorch_cos_sim(embedding1, embedding2)
#
#     def sentence_match(self, sen1, sen2):
#         # 生成句子嵌入
#         embedding1 = self.sentence_model.encode([sen1], convert_to_tensor=True)
#         embedding2 = self.sentence_model.encode([sen2], convert_to_tensor=True)
#
#         # 计算余弦相似度
#         similarity = self.cosine_similarity(embedding1, embedding2).item()
#
#         return similarity

# # 初始化模型包装器
# # wrapper = BertModelWrapper()
#
# # 加载CSV文件
# df = pd.read_csv('data.csv')
#
# # 计算每一对answer和evidence的相似度
# similarity_scores = []
# for idx, row in df.iterrows():
#     answer = row['Answer']
#     evidence = row['Evidence']
#     similarity = wrapper.sentence_match(answer, evidence)
#     similarity_scores.append(similarity)
#
# # 将相似度结果添加到新的列中
# df['Result'] = similarity_scores

# 定义一个函数将BERT结果转换为0-4的规格
# def convert_to_label(score):
#     if 0 <= score < 0.2:
#         return 0
#     elif 0.2 <= score < 0.4:
#         return 1
#     elif 0.4 <= score < 0.6:
#         return 2
#     elif 0.6 <= score < 0.8:
#         return 3
#     elif 0.8 <= score <= 1:
#         return 4
#     else:
#         return None  # 处理意外的分数
#
# # 将Bert result列中的数据转换为新的标签
# df['Bert result label'] = df['Result'].apply(convert_to_label)
#
# # 保存修改后的CSV文件
# df.to_csv('bert_results.csv', index=False)
#
# print("转换完成，并将结果保存到bert_results.csv中")
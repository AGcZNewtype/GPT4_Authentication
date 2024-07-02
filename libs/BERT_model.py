import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer, util
from torch.utils.tensorboard import SummaryWriter


class BertModelWrapper:
    def __init__(self):
        # # 初始化TensorBoard
        # self.writer = SummaryWriter('runs/sentence_similarity')

        # 初始化BERT模型和分词器
        self.model_name = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertModel.from_pretrained(self.model_name)

        # 使用SentenceTransformer进行句子嵌入
        self.sentence_model = SentenceTransformer('bert-base-nli-mean-tokens')

    def get_sentence_embedding(self, sentence):
        # 将句子分词并转换为模型输入格式
        inputs = self.tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # 获取[CLS]标记的嵌入向量
        embedding = outputs.last_hidden_state[:, 0, :].squeeze()
        return embedding

    def cosine_similarity(self, embedding1, embedding2):
        # 计算余弦相似度
        return util.pytorch_cos_sim(embedding1, embedding2)

    def sentence_match(self, sen1, sen2):
        # 输入句子
        sentence1 = sen1
        sentence2 = sen2

        # 使用SentenceTransformer获取句子嵌入
        embedding1 = self.sentence_model.encode([sentence1], convert_to_tensor=True)
        embedding2 = self.sentence_model.encode([sentence2], convert_to_tensor=True)

        # 计算余弦相似度
        similarity = self.cosine_similarity(embedding1, embedding2)

        # # 将结果写入TensorBoard
        # self.writer.add_text('Sentence 1', sentence1, 0)
        # self.writer.add_text('Sentence 2', sentence2, 0)
        # self.writer.add_scalar('Cosine Similarity', similarity.item(), 0)
        #
        # # 可视化句子嵌入
        # self.writer.add_embedding(embedding1, metadata=[sentence1], global_step=0, tag='sentence1')
        # self.writer.add_embedding(embedding2, metadata=[sentence2], global_step=0, tag='sentence2')

        # print(f"Sentence 1: {sentence1}")
        # print(f"Sentence 2: {sentence2}")
        # print(f"Cosine Similarity: {similarity.item():.4f}")
        return float(similarity)

        # # 关闭TensorBoard
        # self.writer.close()
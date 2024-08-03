from sentence_transformers import SentenceTransformer, util
import torch

class BertModelWrapper:
    def __init__(self):
        # Load Sentence-BERT model
        self.sentence_model = SentenceTransformer('bert-base-nli-mean-tokens')

    def cosine_similarity(self, embedding1, embedding2):
        # Calculate cosine similarity
        return util.pytorch_cos_sim(embedding1, embedding2)

    def sentence_match(self, sen1, sen2):
        # Input sentences
        sentence1 = sen1
        sentence2 = sen2

        # Generate sentence embeddings
        embedding1 = self.sentence_model.encode([sentence1], convert_to_tensor=True)
        embedding2 = self.sentence_model.encode([sentence2], convert_to_tensor=True)

        # Calculate cosine similarity
        similarity = self.cosine_similarity(embedding1, embedding2).item()

        return similarity

# # Test example
# wrapper = BertModelWrapper()
# sample_answer = "Reinforcement learning from human feedback (RLHF) is used."
# sample_evidence = "The study uses supervised learning with human feedback to fine-tune GPT-3."
# similarity_score = wrapper.sentence_match(sample_answer, sample_evidence)
# print(f'Similarity score: {similarity_score}')






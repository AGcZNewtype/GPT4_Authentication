import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer, util
from torch.utils.tensorboard import SummaryWriter

class BertModelWrapper:
    def __init__(self):
        ## Initialize TensorBoard (test only)
        # self.writer = SummaryWriter('runs/sentence_similarity')

        # Initialize default BERT model and tokenizer
        self.model_name = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)

        # Use SentenceTransformer for sentence embeddings
        self.sentence_model = SentenceTransformer('bert-base-nli-mean-tokens')

        # Load the BERT model
        self.model = BertModel.from_pretrained(self.model_name)

        # Use SentenceTransformer for sentence embeddings
        self.sentence_model = SentenceTransformer('bert-base-nli-mean-tokens')

        ## Alternatively, load a pre-trained BERT model (test only)
        # self.model_name = 'bert-base-uncased'
        # self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        # trained_model_path = './test/saved_model'
        # self.model = BertModel.from_pretrained(trained_model_path)
        # self.sentence_model = SentenceTransformer('bert-base-nli-mean-tokens')

    def get_sentence_embedding(self, sentence):
        # Tokenize the sentence and convert to model input format
        inputs = self.tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the embedding of the [CLS] token
        embedding = outputs.last_hidden_state[:, 0, :].squeeze()
        return embedding

    def cosine_similarity(self, embedding1, embedding2):
        # Calculate cosine similarity
        return util.pytorch_cos_sim(embedding1, embedding2)

    def sentence_match(self, sen1, sen2):
        # Input sentences
        sentence1 = sen1
        sentence2 = sen2

        # Use SentenceTransformer to get sentence embeddings
        embedding1 = self.sentence_model.encode([sentence1], convert_to_tensor=True)
        embedding2 = self.sentence_model.encode([sentence2], convert_to_tensor=True)

        # Calculate cosine similarity
        similarity = self.cosine_similarity(embedding1, embedding2)

        ## Write results to TensorBoard (test only)
        # self.writer.add_text('Sentence 1', sentence1, 0)
        # self.writer.add_text('Sentence 2', sentence2, 0)
        # self.writer.add_scalar('Cosine Similarity', similarity.item(), 0)
        #
        ## Visualize sentence embeddings (test only)
        # self.writer.add_embedding(embedding1, metadata=[sentence1], global_step=0, tag='sentence1')
        # self.writer.add_embedding(embedding2, metadata=[sentence2], global_step=0, tag='sentence2')

        # print(f"Sentence 1: {sentence1}")
        # print(f"Sentence 2: {sentence2}")
        # print(f"Cosine Similarity: {similarity.item():.4f}")
        return float(similarity)

        # Close TensorBoard (commented out as not being used in this example)
        # self.writer.close()

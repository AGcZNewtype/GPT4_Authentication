import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
import torch
import numpy as np
from sklearn.metrics import mean_squared_error
from torch.utils.tensorboard import SummaryWriter

# Load data
df = pd.read_csv('./data.csv')
print()

# Ensure the column name matches the actual column name in the CSV file
label_column = 'Label'

# Split dataset
train_df, test_df = train_test_split(df, test_size=0.2)

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=1)  # STS task is typically a regression problem

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Data preprocessing function
def preprocess_function(examples):
    # Output data list to check data
    # for answer, evidence, label in zip(examples['Answer'], examples['Evidence'], examples[label_column]):
    #     print(f"Answer: {answer}, Evidence: {evidence}, Label: {label}")
    return tokenizer(examples['Answer'].tolist(), examples['Evidence'].tolist(), truncation=True, padding='max_length',
                     max_length=128)

# Process training and testing sets
train_encodings = preprocess_function(train_df)
test_encodings = preprocess_function(test_df)

# Custom dataset class for STS
class STSDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

    def __len__(self):
        return len(self.labels)


train_dataset = STSDataset(train_encodings, train_df[label_column].tolist())
test_dataset = STSDataset(test_encodings, test_df[label_column].tolist())

# Define training parameters
training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy='epoch',  # Use eval_strategy instead of evaluation_strategy
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',  # For TensorBoard
    logging_steps=10,
    save_total_limit=2,
    save_steps=500,
)

# Compute evaluation metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.squeeze()

    # Remove non-finite values
    finite_indices = np.isfinite(predictions) & np.isfinite(labels)
    predictions = predictions[finite_indices]
    labels = labels[finite_indices]

    return {'mse': mean_squared_error(labels, predictions)}

# Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

# Start training
trainer.train()

# Evaluate model on test set
results = trainer.evaluate()
print(results)

# Save model and tokenizer
save_directory = './saved_model'
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

# TensorBoard logging
writer = SummaryWriter('../logs')
for epoch in range(training_args.num_train_epochs):
    train_result = trainer.evaluate(eval_dataset=train_dataset)
    test_result = trainer.evaluate(eval_dataset=test_dataset)
    writer.add_scalar('Loss/train', train_result['eval_loss'], epoch)
    writer.add_scalar('Loss/test', test_result['eval_loss'], epoch)
    writer.add_scalar('MSE/train', train_result['eval_mse'], epoch)
    writer.add_scalar('MSE/test', test_result['eval_mse'], epoch)
writer.close()

# Method to predict similarity score
def predict_similarity(answer, evidence):
    model.eval()
    tokenized_sample = tokenizer(answer, evidence, truncation=True, padding='max_length', max_length=128,
                                 return_tensors="pt")
    tokenized_sample = {k: v.to(device) for k, v in tokenized_sample.items()}
    with torch.no_grad():
        outputs = model(**tokenized_sample)
        similarity_score = outputs.logits.squeeze().item()
    return similarity_score

# Test
sample_answer = "OpenCV was used to change the color of eyes and mouth"
sample_evidence = "OpenCV"
similarity_score = predict_similarity(sample_answer, sample_evidence)
print(f'Similarity score: {similarity_score}')

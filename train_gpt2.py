import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# Загружаем GPT-2 и токенизатор
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Загружаем наши данные
train_file = "motivations.txt"

def load_dataset(file_path, tokenizer):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128
    )

dataset = load_dataset(train_file, tokenizer)

# Подготавливаем данные для обучения
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Настройки обучения
training_args = TrainingArguments(
    output_dir="./gpt2-motivator",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=2,
    prediction_loss_only=True,
    logging_steps=100
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator
)

# Запуск обучения
trainer.train()

# Сохранение обученной модели
trainer.save_model("./gpt2-motivator")
tokenizer.save_pretrained("./gpt2-motivator")

print("✅ Обучение завершено! Модель сохранена в ./gpt2-motivator")

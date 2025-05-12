import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = "./results"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)


def split_text_by_sentences(text, max_chars=600):
    text = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'(?<=[.!?؟]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def translate_long_text(text, chunk_size=300, batch_size=6):  # Adjusted batch size and chunk size
    # Split the text into chunks
    chunks = split_text_by_sentences(text, max_chars=chunk_size)
    translated_chunks = []

    print(f"\nTotal chunks to translate: {len(chunks)}")

    # chunks in batches
    for i in range(0, len(chunks), batch_size):
        # Get the current batch of chunks
        batch_chunks = chunks[i:i+batch_size]

        # Tokenize the batch
        inputs = tokenizer(batch_chunks, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)

        try:
            # Generate translation for the batch
            output_ids = model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=1024,
                num_beams=5,  # Consider experimenting with num_beams
                no_repeat_ngram_size=3,
                early_stopping=True,
                do_sample=False
            )

            # Decode the translated output and store
            for output in output_ids:
                translated_text = tokenizer.decode(output, skip_special_tokens=True)
                translated_chunks.append(translated_text)

            print(f"Translated batch {i // batch_size + 1} ({len(batch_chunks)} chunks)")

        except Exception as e:
            print(f"Error in batch {i // batch_size + 1}: {e}")
            continue

    # Join
    final_translation = " ".join(translated_chunks)
    final_translation = re.sub(r'\s+', ' ', final_translation).strip()

    return final_translation

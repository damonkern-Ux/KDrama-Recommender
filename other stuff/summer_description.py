from transformers import T5Tokenizer, T5ForConditionalGeneration
import mysql.connector as mysql
from os import system

system("cls")


def summarizer(text):
    # Load tokenizer + model
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    # T5 expects a task prefix
    input_text = "summarize: " + text
    # Tokenize
    input_ids = tokenizer.encode(
        input_text, return_tensors="pt", max_length=512, truncation=True
    )
    # Generate summary
    summary_ids = model.generate(
        input_ids,
        max_length=500,  # maximum words in summary
        min_length=10,  # minimum words in summary
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
    )
    # Decode
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


connection = mysql.connect(host="localhost", user="root", password="system")
cursor = connection.cursor()
cursor.execute("use dramas;")
cursor.execute("SELECT drama_name,description FROM drama_table;")
for record in cursor.fetchall():
    summary = summarizer(record[1])
    print(record[0],'\n',summary)
    print()

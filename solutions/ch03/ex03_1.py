import tiktoken

enc = tiktoken.get_encoding("o200k_base")
samples = {
    "English": "Please restart the database server after the backup completes.",
    "Filipino": "Pakisimulang muli ang database server pagkatapos makumpleto ang backup.",
    "Python": "if backup.status == 'done':\n    db.restart(force=False)",
}
for name, text in samples.items():
    n = len(enc.encode(text))
    print(f"{name:9} {n:3} tokens  {n / len(text):.2f} tokens/char")

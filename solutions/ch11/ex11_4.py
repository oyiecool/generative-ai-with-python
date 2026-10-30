# uv add jiwer
import jiwer

reference = Path("data/call_reference.txt").read_text()
for name, hyp in {"local": local_text, "hosted": hosted_text}.items():
    print(name, "WER:", round(jiwer.wer(reference.lower(), hyp.lower()), 3))

terms = ["kubernetes", "ORA-01555", "failover", "VLAN"]
for t in terms:
    print(t, t.lower() in local_text.lower(), t.lower() in hosted_text.lower())

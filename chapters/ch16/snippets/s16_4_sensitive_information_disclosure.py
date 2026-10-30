# uv add presidio-analyzer presidio-anonymizer && python -m spacy download en_core_web_lg
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="PH_TIN",                          # example custom identifier
    patterns=[Pattern("tin", r"\b\d{3}-\d{3}-\d{3}(-\d{3,5})?\b", 0.6)],
))
anonymizer = AnonymizerEngine()


def redact(text: str) -> str:
    results = analyzer.analyze(text=text, language="en")
    return anonymizer.anonymize(text=text, analyzer_results=results).text


print(redact("Call Maria Santos at +63 917 555 0123 or maria@example.ph. TIN 123-456-789-000."))

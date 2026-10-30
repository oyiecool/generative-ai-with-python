# tests/test_policy_assistant.py
import pytest
import yaml

from aikit.rag import answer

CASES = yaml.safe_load(open("evals/policy_assistant.yaml"))


@pytest.mark.llm                                   # opt-in marker: costs money
@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_case(case, index, llm):
    r = answer(case["question"], index=index, llm=llm, user_groups=["staff"])
    exp = case["expect"]

    assert r["answerable"] == exp["answerable"]
    text = r["answer"].lower()
    for phrase in exp.get("must_mention", []):
        assert phrase.lower() in text, f"missing {phrase!r}"
    for phrase in exp.get("must_not_mention", []):
        assert phrase.lower() not in text, f"leaked {phrase!r}"
    cited = {s["file"] for s in r["sources"]}
    for f in exp.get("must_cite", []):
        assert f in cited, f"did not cite {f}"

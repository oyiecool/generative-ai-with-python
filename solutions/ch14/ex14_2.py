# uv add scikit-learn
from sklearn.metrics import cohen_kappa_score

human = [5, 4, 2, 5, 3, ...]          # colleague's faithfulness scores for 20 answers
judge = [5, 4, 3, 5, 1, ...]          # judge's scores for the same answers
exact = sum(h == j for h, j in zip(human, judge)) / len(human)
within_one = sum(abs(h - j) <= 1 for h, j in zip(human, judge)) / len(human)
kappa = cohen_kappa_score(human, judge, weights="quadratic")
print(f"exact {exact:.0%}, within one {within_one:.0%}, weighted kappa {kappa:.2f}")

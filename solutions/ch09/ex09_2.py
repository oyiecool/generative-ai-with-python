answerable = [...]        # questions the KB answers
unanswerable = [...]      # five questions it cannot answer

top = lambda q: idx.search(q, k=1)[0].score
a_scores = sorted(top(q) for q in answerable)
u_scores = sorted(top(q) for q in unanswerable)
print("answerable min:", a_scores[0], "unanswerable max:", u_scores[-1])
threshold = (a_scores[0] + u_scores[-1]) / 2

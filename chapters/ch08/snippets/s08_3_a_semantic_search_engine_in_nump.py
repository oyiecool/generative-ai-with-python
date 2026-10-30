from aikit.embed import LocalEmbedder
from aikit.vectorindex import VectorIndex

idx = VectorIndex(LocalEmbedder())
idx.add(
    ["kb1", "kb2", "kb3"],
    ["To reset MFA, open the identity portal and choose 'Re-register device'.",
     "Disk alerts fire at 85% usage on /var; rotate logs with logrotate -f.",
     "Expense claims must be filed within 30 days with receipts attached."],
    [{"team": "identity"}, {"team": "ops"}, {"team": "finance"}],
)
for h in idx.search("my authenticator app stopped working on my new phone", k=2):
    print(f"{h.score:.2f}  {h.id}  {h.text}")

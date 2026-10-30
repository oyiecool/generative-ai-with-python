import os
from datetime import datetime

state = Path("data/ingest_state.json")
if state.exists():
    updated = datetime.fromtimestamp(os.path.getmtime(state)).strftime("%d %b %Y, %H:%M")
    st.info(f"Knowledge base last updated {updated}.")
else:
    st.warning("Knowledge base has not been built yet.")

# apps/policy_chat.py     (uv add streamlit httpx)
import httpx
import streamlit as st

API = st.secrets.get("api_url", "http://localhost:8000")
st.set_page_config(page_title="Policy Assistant", page_icon="📘")
st.title("Policy Assistant")
st.caption("Answers come only from approved IT policies. Always check the cited source.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if question := st.chat_input("Ask about an IT policy"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching policies…"):
            r = httpx.post(f"{API}/v1/ask", json={"question": question},
                           headers={"Authorization": f"Bearer {st.session_state.get('token', '')}"},
                           timeout=60).json()
        st.markdown(r["answer"])
        for s in r["sources"]:
            st.markdown(f"- [{s['n']}] **{s['file']}** — {s['section']}")
        c1, c2 = st.columns(2)
        if c1.button("👍 Helpful", key=r["trace_id"] + "u"):
            httpx.post(f"{API}/v1/feedback", json={"trace_id": r["trace_id"], "score": 1})
        if c2.button("👎 Wrong", key=r["trace_id"] + "d"):
            httpx.post(f"{API}/v1/feedback", json={"trace_id": r["trace_id"], "score": -1})
    st.session_state.messages.append({"role": "assistant", "content": r["answer"]})

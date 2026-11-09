import streamlit as st, os
import core, llm

st.set_page_config(page_title="Nyaya Saathi", page_icon="⚖️")
st.title("⚖️ Nyaya Saathi: free legal first-aid (India)")
st.caption("Deposits · refunds · unpaid salary · bounced cheques · online fraud · notices received.  I am an AI, not a lawyer. Replies in English / हिन्दी / Hinglish.")
with st.sidebar:
    st.subheader("Model (swappable)")
    prov = st.selectbox("Provider", ["offline", "gemini", "anthropic", "openai"], index=["offline", "gemini", "anthropic", "openai"].index(os.getenv("LLM_PROVIDER", "offline")))
    os.environ["LLM_PROVIDER"] = prov
    if prov != "offline":
        os.environ["LLM_API_KEY"] = st.text_input("API key", type="password", value=os.getenv("LLM_API_KEY", ""))
        os.environ["LLM_MODEL"] = st.text_input("Model", value=os.getenv("LLM_MODEL", llm.DEFAULTS.get(prov, "")))
        if prov == "openai": os.environ["LLM_BASE_URL"] = st.text_input("Base URL (OpenAI-compatible)", value=os.getenv("LLM_BASE_URL", llm.BASES["openai"]))
    st.markdown("**Covers:** the six areas above.  \n**Does not cover:** family, criminal defence, property/builder, inheritance, tax, immigration → I refer you.")
    st.markdown("Free legal aid: **NALSA 15100**")
    if st.button("Reset chat"): st.session_state.clear(); st.rerun()

st.session_state.setdefault("msgs", [])   # user messages only; we re-analyse the whole story each turn
st.session_state.setdefault("log", [])
for role, content in st.session_state.log:
    st.chat_message(role).markdown(content)

typed = st.chat_input("Tell me what happened, in your own words…")
if typed:
    st.session_state.msgs.append(typed); st.session_state.log.append(("user", typed)); st.chat_message("user").markdown(typed)
    story = "\n".join(st.session_state.msgs)
    with st.spinner("Checking verified sources…"):
        r = llm.respond(story)
    a = r["analysis"]
    with st.chat_message("assistant"):
        st.markdown(r["answer"])
        if r["removed"]: st.warning(f"{len(r['removed'])} statement(s) were removed because they cited law outside my verified sources.")
        with st.expander("Case file (what I understood)"):
            st.json(r.get("case") or {"category": a["category"], "amount_rs": a["facts"]["amount_rs"], "language": a["lang"], "sources_used": a["kb_ids"]})
        if r.get("notice"):
            with st.expander("📄 Draft notice (edit & get it checked)"): st.code(r["notice"], language=None)
        c = a["category"]
        if c in core.OTHERS and not a["flags"]:
            with st.expander("🎭 Practise: play the other side"):
                st.markdown("Copy this prompt into any chat model (or use it with your chosen provider):")
                st.code(core.ROLEPLAY_PROMPT.format(case=story[:300], other=core.OTHERS[c]), language=None)
        st.caption(f"mode: {r['mode']}  ·  sources: {', '.join(a['kb_ids'])}")
    st.session_state.log.append(("assistant", r["answer"]))

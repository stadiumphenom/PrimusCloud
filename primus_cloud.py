
import streamlit as st
import requests
import json

st.set_page_config(page_title="Primus Cloud Console", layout="wide")
st.title("🌐 Primus Cloud Console")
st.markdown("Type commands to your local LLM node. If mirrored, ShadowLink can execute them.")

# Default settings
default_llm_url = "http://localhost:11434/api/generate"
default_shadowlink_url = "http://localhost:5000/task"

with st.sidebar:
    st.header("⚙️ Settings")
    llm_url = st.text_input("LLM Endpoint", default_llm_url)
    shadowlink_url = st.text_input("ShadowLink API", default_shadowlink_url)
    mirror = st.checkbox("Mirror to ShadowLink", value=False)

st.subheader("🧠 Command Input")
user_input = st.text_area("Speak to Primus", height=200)

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please type something.")
    else:
        with st.spinner("Calling local LLM..."):
            payload = {
                "model": "llama2",
                "prompt": user_input,
                "stream": False
            }
            try:
                r = requests.post(llm_url, json=payload)
                llm_reply = r.json().get("response", "No response.")
                st.success("LLM Response:")
                st.code(llm_reply)

                if mirror:
                    with st.spinner("Mirroring to ShadowLink..."):
                        task = {
                            "name": "cloud_llm_task",
                            "action": "echo",
                            "content": llm_reply,
                            "autorun": True
                        }
                        mirror_resp = requests.post(shadowlink_url, json=task)
                        if mirror_resp.status_code == 200:
                            st.info("✅ Sent to ShadowLink.")
                        else:
                            st.error(f"Failed to mirror task: {mirror_resp.status_code}")
            except Exception as e:
                st.error(f"Error connecting to local LLM: {e}")

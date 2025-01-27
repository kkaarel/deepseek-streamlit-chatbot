
#Original code on how a chat can be developed can be found from here:https://github.com/streamlit/llm-examples/blob/main/Chatbot.py
#Deepseek documentation can be found from here:https://api-docs.deepseek.com/

from openai import OpenAI
import streamlit as st

with st.sidebar:
    #If you work locally you can add the api key in to secrets.toml file 
    if "api_key" in st.secrets:
        deepseek_api_key = st.secrets["api_key"]
    else:
        deepseek_api_key = st.text_input("Deepseek API Key", key="chatbot_api_key", type="password")
    
    model = st.selectbox(
        "Choose a model",
        options=["deepseek-chat"],
        index=0
    )
    st.markdown("App doesn't store any data, neither your api key ")
    st.markdown("[Get a Deepseek API key 	:rocket: ](https://platform.deepseek.com/)")
    st.markdown("[More about models :sparkle: ](https://api-docs.deepseek.com/)")
    st.markdown("[Contact the developer :email: ](https://www.linkedin.com/in/korvemaa/)")
    st.markdown("[Github :computer: ](https://github.com/kkaarel)")
    st.markdown("[Privacy notes](https://chat.deepseek.com/downloads/DeepSeek%20Privacy%20Policy.html)")

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Deepseek")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not deepseek_api_key:
        st.info("Please add your Deepseek API key to continue.")
        st.stop()
    client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

    st.session_state.messages.append({"role": "user", "content": prompt})

    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=8000, 
        stream=False
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
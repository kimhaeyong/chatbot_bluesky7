import streamlit as st
from openai import OpenAI

st.title("💬 나만의 챗봇")

openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
if not openai_api_key:
    openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("API 키를 입력해주세요.", icon="🔒")
    st.stop()

client = OpenAI(api_key=openai_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.header("⚙️ 설정")
model = st.sidebar.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
temperature = st.sidebar.slider("창의성", 0.0, 1.5, 0.7)

if st.button("🧹 대화 초기화"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=temperature,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"⚠️ 오류 발생: {e}")

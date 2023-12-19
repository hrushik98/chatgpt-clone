from openai import OpenAI
import streamlit as st

st.title("ChatGPT clone")
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""
api_key = st.text_input("Enter your api key", type = "password")
if api_key == "":
    pass
else:
    st.session_state.openai_api_key = api_key
client = OpenAI(api_key=st.session_state['openai_api_key'])



if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Define the model options
models = ["GPT 3.5", "GPT 3.5 16K", "GPT 4", "GPT 4 Turbo", "GPT 4 32K"]

# Create the dropdown menu
model_choice = st.selectbox("Select model", models)

# Use the selected model
if model_choice == "GPT 3.5":
    st.session_state["openai_model"] = "gpt-3.5-turbo"
elif model_choice == "GPT 3.5 16K":
    st.session_state["openai_model"] = "gpt-3.5-16K"
elif model_choice == "GPT 4":
    st.session_state["openai_model"] = "gpt-4"
elif model_choice == "GPT 4 Turbo":
    st.session_state["openai_model"] = "gpt-4-turbo"
elif model_choice == "GPT 4 32K":
    st.session_state["openai_model"] = "gpt-4-32K"

st.write(f"Using {st.session_state['openai_model']}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except:
        st.warning("Please enter a valid API key")
st.download_button(
        "Download chat",
        "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages
            ]
        ),
        "chat.txt",
    )

import streamlit as st
import asyncio
import websockets
import json


async def retrieve_bot_response(text):
    async with websockets.connect(
        "ws://fastapi_server:8000/api/v1/chat/tools"
    ) as websocket:
        message_data = {"message": text}
        json_data = json.dumps(message_data)

        await websocket.send(json_data)
        counter = 0
        with st.empty():
            stream_data = ""
            try:
                while True:
                    counter += 1
                    response = await asyncio.wait_for(websocket.recv(), timeout=20)
                    response = json.loads(response)

                    if "error" in response:
                        stream_data = response["error"]
                        break

                    if response["sender"] == "bot":
                        stream_data = (
                            response["message"]["body"][0]["items"][0]["text"]
                            if counter != 2
                            else ""
                        )
                        st.markdown(stream_data)

                    if response["type"] == "end":
                        break
                st.markdown(stream_data)
            except asyncio.TimeoutError:
                st.warning("Connection timed out. Closing the connection.")

        return stream_data


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = asyncio.new_event_loop().run_until_complete(
            retrieve_bot_response(prompt)
        )

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

import streamlit as st
from openai import OpenAI

st.title("HUBX User Creation Bot")

# Initialize chat history
founder_object =  {
    "funding_stage": "",
    "num_funding_rounds": 0,
    "last_equity_funding_type": "",
    "last_equity_funding_total": 0,
    "categories": [],
    "Industries":[],
    "description": "",
    "founders": [],
    "name": "",
    "founded_organizations": []
  }
client = OpenAI(api_key=st.secrets["api_key"])

investor_object ={
        "name": "",
        "location": "",
        "country": "",
        "previous_investments": [
            {
                "name": "",
                "field": [
                ],
                "funding_round": "",
                "description": ""
            },
        ],
        "total_funding_amount": 0,
        "description": "",
        "Funding Stage": [],
        "Industries": []
    }
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"system",
            "content": f"You are a bot helping make the user object. For the founders, the objects looks like  {founder_object} and for the investor and advisory firms the objects looks like {investor_object}. Go through each field and ask questions to fill the fields with relevant data. If the field is filled with relevant data then skip it. Once all the fields are done add a <DONE> tag to the response and return the JSON object. Make sure to Go through the entire object. Be Casua, encouraging and Give examples wherever necessary. Make Sure All your questions are relevant to the fields asked and do not add any extra questions."
        },
        {
          "role":"assistant",
          "content":"Hey, This is HUBX User Creation bot. You can ask me questions about HUBX if required. I'll need some information from you: Are you a Founder, investor or advisory"
        }]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    
    if message["role"] != "system":
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=st.session_state.messages
).choices[0].message.content  
    print("response ", response)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

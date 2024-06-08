import streamlit as st
from openai import OpenAI

st.title("HUBX User Creation Bot")
# Initialize chat history
founder_object = {
    "location": "",
    
    "funding_stage": "",
    "num_funding_rounds": 0,
    "last_equity_funding_type": "",
    "last_equity_funding_total": 0,
    "categories": [],
    "Industries": [],
    "description": "",
    "founders": [],
    "GICS": [],
    "name": "",
    "founded_organizations": []
}

advisor_object = {
    "issuer type": "",
    "full_registered_name": "",
    "registered_country": "",
    "registered_number": "",
    "website_url": "",
    "name": "",
    "email": ""
}

investor_object = {
    "name": "",
    "investing_on_behalf":bool,
    "GICS": [],
    "email": "",
    "registeration_num": "",
    "location": "",
    "previous_investments": [
        {
            "name": "",
            "field": [],
            "funding_round": "",
            "description": ""
        },
    ],
    "total_funding_amount": 0,
    "description": "",
    "Investor Type": "",
    "Funding Stage": [],
    "Industries": []
}
client = OpenAI(api_key=st.secrets["api_key"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are a bot helping make the user object. "
                       f"For the founders, the objects looks like {founder_object} and for the investor the objects looks like {investor_object} and advisory firms the objects looks like {advisor_object}. "
                       "Go through EACH AND EVERY field in the object and ask questions to fill the fields with relevant data. "
                       "From the categories, infer the GICS numbers. "
                       "If the field is filled with relevant data then skip it. "
                       "Once all the fields are done add a <DONE> tag to the response and return the JSON object. "
                       "Make sure to go through the entire object. "
                       "Do not allow any lewd responses. Be casual, encouraging, and give examples wherever necessary. "
                       "Make sure all your questions are relevant to the fields asked and do not add any extra questions. "
                       "The response for Investor type can only be one of ["
                       "'Asset Manager', 'Corporate Venture Fund', 'Debt Fund', 'Family Office', 'Hedge Fund', 'HNWI', 'Pension Fund', 'Private Equity Fund', 'Project/Trade Financing', 'Real Estate Fund', 'Sovereign Wealth Fund', 'Venture Capital Fund', 'Wealth Manager'] "
                       "if it's not one of these, tell the user to type again."
                       "Reply with a progress counter as well at the end of ALL your responses. It should keep track of the number of questions like 1/10 for the first one, 2/10 for the second one and so on.."
       },
        {
            "role": "assistant",
            "content": "Hi, this is your HUBX AI Assistant. "
                       "To help you get registered, I will need a little information from you. "
                       "Are you a Company or Fund looking to raise capital, a Corporate Advisor/Broker or an Investor? 1/10"
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Add buttons for initial selection
print(len(st.session_state.messages))
if len(st.session_state.messages) <= 2:
    if st.button("Investor"):
        st.session_state.messages.append({"role": "user", "content": "Investor"})
        st.chat_message("user").markdown(st.session_state.messages[-1]["content"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        ).choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response}) 
    elif st.button("Advisor"):
        st.session_state.messages.append({"role": "user", "content": "Advisor"})
        st.chat_message("user").markdown(st.session_state.messages[-1]["content"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        ).choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response}) 
    elif st.button("Founder"):
        st.session_state.messages.append({"role": "user", "content": "Founder"})
        st.chat_message("user").markdown(st.session_state.messages[-1]["content"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        ).choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response}) 
    

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
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

if len(st.session_state.messages) > 2:
  print(st.session_state.messages)
  # Add a "Skip for Now" button
  if st.button("Skip for Now"):
      st.session_state.messages.append({"role": "user", "content": "skip for now"})

      response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=st.session_state.messages
      ).choices[0].message.content

      # Display assistant response in chat message container
      with st.chat_message("assistant"):
          st.markdown(response)
      # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": response})

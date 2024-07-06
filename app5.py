import streamlit as st
import toml
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_google_genai import ChatGoogleGenerativeAI

# Giving the tab name of model
st.set_page_config("IrfanLLM")

# Page title
st.title('Irfan Large Language Model')

# page discription
st.write('This is a large language model that can be used for asking questions such as chatbot, using the google.gemini api. We are happy to see you there! ')
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'input' not in st.session_state:
    st.session_state['input'] = ""

# Adding The api key
with open('config.toml') as config_file:
    config =  toml.load(config_file)
    api_key = config['api']['key']

# Asking for the model from user
model = st.sidebar.selectbox("Please Select your desired model! ", ["gemini-1.5-flash",'gemini-1.5-pro', 'gemini-1.0-pro'])

# Asking the customer for token
token = st.sidebar.number_input("Please enter the number of tokens you want to generate", min_value=100, max_value=20000)
# Making the model if API is here

if api_key:
    llm = ChatGoogleGenerativeAI(temperature=0.9, model=model, google_api_key=api_key, max_output_tokens=token)
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k =50)
    conversation = ConversationChain(llm= llm, memory = st.session_state.entity_memory, prompt = ENTITY_MEMORY_CONVERSATION_TEMPLATE)
else:
    st.error('There is not API found! ')

# Asking the user to input text
user_input = st.text_input('You! ', st.session_state['input'], placeholder="Hi, there! I am your AI assistant how may I help you today! ")

# saving the session in st.session_state
if user_input:
    llm_output = conversation.run(input = user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(llm_output)

with st.expander('conversation'):
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        st.info(st.session_state['past'][i])
        st.success(st.session_state['generated'][i])

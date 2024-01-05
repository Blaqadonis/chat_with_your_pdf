import json
import os 
import streamlit as st
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader, PyPDFLoader
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from google.colab import userdata
from copy import deepcopy
from tempfile import NamedTemporaryFile

@st.cache_resource
def create_datastax_connection():
  cloud_config = {'secure_connect_bundle': 'secure-connect-pdf-qa1.zip'}
  CLIENT_ID = os.getenv('ASTRA_DB_CLIENTID') 
  CLIENT_SECRET = os.getenv('ASTRA_DB_SECRET') 
  auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
  cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
  session = cluster.connect()
  return session

def main():
  index_placeholder = None
  st.set_page_config(page_title = "Smart PDF Bot")

  if "conversation" not in st.session_state:
    st.session_state.conversation = None
  if "activate_chat" not in st.session_state:
    st.session_state.activate_chat = False

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = message['avatar']):
      st.markdown(message["content"])

  session = create_datastax_connection()

  openai_api_key = os.getenv('OPENAI_API_KEY')
  llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
  openai_embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

  table_name = "pdf_qa1_table"
  keyspace = "pdf_qa1_name"

  index_creator = VectorstoreIndexCreator(
    vectorstore_cls = Cassandra,
    embedding = openai_embeddings,
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap = 30
    ),

    vectorstore_kwargs={
        'session': session,
        'keyspace': keyspace,
        'table_name': table_name
    }
    )
  
  with st.side_bar:
    st.subheader('Upload yor PDF file')
    docs = st.file_uploader('⬆️Upload your PDF and click to process',
                            accept_multiple_files = False,
                            type = ['pdf'])
    if st.button('Process'):
      with NamedTemporaryFile(dir='', suffix='.pdf') as f:
        f.write(docs.getbuffer())
        with st.spinner('Processing'):
          loader = PyPDFLoader(f.name)
          pages = loader.load_and_split()
          pdf_index = index_creator.from_loaders([loader])
          # index_placeholder = deepcopy(pdf_index)
          if "pdf_index" not in st.session_state:
            st.session_state.pdf_index = pdf_index
          st.session_state.activate_chat = True

if st.session_state.activate_chat == True:
  if prompt := st.chat_input("Ask your question here"):
    with st.chat_message("user", avatar = '🅱🅻🅰🆀'):
      st.markdown(prompt)
    st.session_state.messages.append({"role": "user",
                                      "avatar": '🅱🅻🅰🆀',
                                      "content": prompt})
    
    index_placeholder = st.session_state.pdf_index
    pdf_response = index_placeholder.query_with_sources(prompt, llm = llm)
    cleaned_response = pdf_response["answer"]
    with st.chat_message("assistant", avatar = '🅱🅻🅰🆀'):
      st.markdown(cleaned_response)
    st.session_state.messages.append({"role": "assistant",
                                      "avatar" : '🅱🅻🅰🆀',
                                      "content": cleaned_response})
    
  else:
    st.markdown(
      'Upload your PDFs to chat'
    )

if __name__ == '__main__':
  main()
    




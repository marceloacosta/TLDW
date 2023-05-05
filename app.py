import streamlit as st
from streamlit_player import st_player
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
import os
from dotenv import load_dotenv
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader





persist_directory = 'db'




# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar API keys aquí
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")



# Cargar el modelo de OpenAI
llm = ChatOpenAI(model='gpt-3.5-turbo',temperature=0, openai_api_key=OPENAI_API_KEY,max_tokens= 2000)
chain = load_qa_chain(llm, chain_type="stuff")

class CustomDocument:
    def __init__(self, page_content):
        self.page_content = page_content
        self.metadata = {}



def load_unstructured_text(text):
    return [CustomDocument(page_content=text)]




# Funciones de la aplicación original

def get_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

def get_transcript(url):
    video_id = get_video_id(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=['es', 'en'])
        return transcript
    except Exception as e:
        print(f"Error: {e}")
        return None
# Function to get the video title using the YouTube Data API
def get_video_title(video_id):
    try:
        youtube = build("youtube", "v3", credentials=None, developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()

        if response["items"]:
            return response["items"][0]["snippet"]["title"]
        else:
            return None
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# Función para procesar la transcripción y buscar respuestas a preguntas

def chroma_exists(video_id):
    return os.path.exists(os.path.join(persist_directory, f"{video_id}.chroma"))

def load_or_create_chroma(video_id, texts):
    chroma_path = os.path.join(persist_directory, f"{video_id}.chroma")
    if chroma_exists(video_id):
        db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
    else:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
        db.persist()
    return db




def process_transcript_and_search(video_id, transcript, question):  # Add video_id parameter here
    data = "\n".join([entry["text"] for entry in transcript])
    loaded_data = load_unstructured_text(data)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(loaded_data)

    db = load_or_create_chroma(video_id, texts)

    docs = db.similarity_search(question, include_metadata=True)
    answer = chain.run(input_documents=docs, question=question)

    return answer



def main():
    st.title("Preguntale a Youtube")
    st.write("Ingresa la URL del video de YouTube y haz preguntas sobre su contenido.")

    url = st.text_input("URL del video de YouTube")
    video_id = get_video_id(url)
    
    if video_id:
        video_title = get_video_title(video_id)
        
        if video_title:
            st.write(f"Video: {video_title}")
        
        st_player(f"https://www.youtube.com/watch?v={video_id}")

    question = st.text_input("Ingresa tu pregunta")

    transcript = None

    if st.button("Obtener respuesta"):
        transcript = get_transcript(url)

    if transcript:
        video_id = get_video_id(url)
        answer = process_transcript_and_search(video_id, transcript, question)  # Add video_id here
        st.write(f"Respuesta: {answer}")
        
    elif url:
        st.write("Transcripción no encontrada o no se pudo recuperar.")

if __name__ == "__main__":
    main()

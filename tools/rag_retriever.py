import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

DB_DIR = "vector_db/chroma_db"
KB_DIR = "knowledge_base"

def load_environment():
    load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("ERRO: GEMINI_API_KEY não encontrada no .env!")

def build_vector_store():
    """Lê os PDFs, quebra em chunks e salva no ChromaDB em lotes."""
    load_environment()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    print(f"Lendo PDFs da pasta {KB_DIR}...")
    documents = []
    
    if not os.path.exists(KB_DIR):
        print(f"A pasta {KB_DIR} não existe. Crie a pasta e coloque seus PDFs.")
        return
        
    for file in os.listdir(KB_DIR):
        if file.endswith('.pdf'):
            print(f"Processando: {file}")
            loader = PyPDFLoader(os.path.join(KB_DIR, file))
            documents.extend(loader.load())
            
    if not documents:
        print("Nenhum PDF encontrado na pasta knowledge_base.")
        return
        
    # POP 01: Fragmentar os artigos priorizando blocos coerentes de parágrafos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Total de fragmentos (chunks) gerados: {len(chunks)}")
    
    print("Inicializando Embeddings (isso pode levar alguns minutos)...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    
    print("Construindo banco vetorial em lotes para evitar Rate Limiting (429)...")
    vectorstore = Chroma(
        collection_name="quimica_inclusiva",
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    
    # 25 chunks por lote para ser extremamente conservador com Rate Limits gratuitos
    batch_size = 25 
    total_batches = (len(chunks) // batch_size) + 1
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        lote_atual = i//batch_size + 1
        sucesso = False
        tentativas = 0
        
        while not sucesso and tentativas < 5:
            try:
                print(f"Indexando lote {lote_atual} de {total_batches} no banco vetorial...")
                vectorstore.add_documents(batch)
                sucesso = True
                time.sleep(2) # Dorme normal entre lotes ok
            except Exception as e:
                tentativas += 1
                if "429" in str(e) or "Quota exceeded" in str(e):
                    tempo_espera = 60 * tentativas
                    print(f"Limites da API (429) excedidos. O Google pede calma. Dormindo {tempo_espera}s antes de tentar o lote {lote_atual} novamente...")
                    time.sleep(tempo_espera)
                else:
                    print(f"Erro desconhecido: {e}")
                    raise e
        
    print("Banco de dados RAG construído com sucesso!")

def retrieve_context(query, k=4):
    """POP 01: Recupera o contexto da base para guiar o Agente."""
    load_environment()
    api_key = os.environ.get("GEMINI_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    
    if not os.path.exists(DB_DIR):
        print("ERRO: Banco vetorial não encontrado. Rode 'python tools/rag_retriever.py --build'")
        return ""
        
    vectorstore = Chroma(
        collection_name="quimica_inclusiva",
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    
    context = "\n\n".join([d.page_content for d in docs])
    return context

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        build_vector_store()
    else:
        print("Para construir a base, use: python tools/rag_retriever.py --build")

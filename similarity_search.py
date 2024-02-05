
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from loomie_core.connections import set_postgres_conn_vector

def process_doc(docs):
  final=[]
  for doc in docs:
    final.append(str(doc.metadata['source']))
  return final

def fetch_similar_records(question):
    embeddings = OpenAIEmbeddings()
    store = PGVector(
        collection_name= "sql_embeddings_new",
        connection_string=set_postgres_conn_vector()
        embedding_function=embeddings,
      )
    retriever = store.as_retriever(search_kwargs={"k": 2})
    docs = retriever.get_relevant_documents(str(question))
    return(process_doc(docs))
    
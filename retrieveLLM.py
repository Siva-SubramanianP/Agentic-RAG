from langchain_cohere import CohereRerank
from groq import Groq
from langchain_core.documents import Document as LCDocument
import chromadb
from chromadb.utils import embedding_functions
# from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "DEMO"
CHROMA_PATH = "./demo_CBD"

async def retrievefromLLM(question):

    ef = embedding_functions.DefaultEmbeddingFunction()

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    client_groq = Groq(api_key="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")

    query = question
    results = collection.query(
        query_texts=[query],
        n_results=10
    )
    # for doc, dist in zip(
    #         results["documents"][0],
    #         results["distances"][0]):
        
    #     print("Distance :", round(dist, 4))
    #     print("Similarity :", round(1 - dist, 4))
    #     print(doc)
    #     print("=" * 60)   

    contexts = results["documents"][0]


    langchain_docs = [
        LCDocument(page_content=chunk)
        for chunk in contexts
    ]

    COHERE_API_KEY = "BdoUvcZvPrWc8hHwsu3jcqQJPAtQrdU9FlFTg7bU"

    reranker = CohereRerank(
        cohere_api_key=COHERE_API_KEY,
        model="rerank-v3.5",
        top_n=3
    )

    reranked_docs = reranker.compress_documents(
        documents=langchain_docs,
        query=query
    )

    # print("\nTop Chunks After Reranking:\n")

    # for i, doc in enumerate(reranked_docs, 1):
    #     print(f"Rank {i}")
    #     print(doc.page_content)
    #     print("=" * 120)

    # Build context text
    #context = "\n\n".join(contexts)

    context = "\n\n".join(
        [doc.page_content for doc in reranked_docs]
    )

    # print("Retrieved Context:")
    # print(context)
    # print("=" * 120)

    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    # print("\n\nFinal Answer:\n")
    # print(response.choices[0].message.content)



    # 2. Print the exact token metrics
    # print("\nToken Usage Details:")
    # print(f"Prompt (Input) Tokens: {response.usage.prompt_tokens}")
    # print(f"Completion (Output) Tokens: {response.usage.completion_tokens}")
    # print(f"Total Tokens: {response.usage.total_tokens}")

    return response.choices[0].message.content

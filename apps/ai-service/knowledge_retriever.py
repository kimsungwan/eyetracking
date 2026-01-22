import chromadb
from chromadb.utils import embedding_functions

# Configuration
DB_DIR = "knowledge_db"
COLLECTION_NAME = "marketing_concepts"

def retrieve_knowledge(query_text: str, n_results: int = 3) -> list:
    """
    Queries the ChromaDB vector store for marketing concepts relevant to the input text.
    Returns a list of dictionaries containing the concept, definition, and advice.
    """
    try:
        client = chromadb.PersistentClient(path=DB_DIR)
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # Use get_or_create to avoid errors if called before ingestion (though ingestion should be done)
        collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)
        
        if collection.count() == 0:
            return []
            
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Format results
        knowledge_items = []
        if results['metadatas'] and len(results['metadatas']) > 0:
            for i, metadata in enumerate(results['metadatas'][0]):
                knowledge_items.append({
                    "concept": metadata['concept'],
                    "definition": metadata['definition'],
                    "advice": metadata['advice'],
                    "relevance_score": results['distances'][0][i] if results['distances'] else 0
                })
                
        return knowledge_items
        
    except Exception as e:
        print(f"Error in knowledge retrieval: {str(e)}")
        return []

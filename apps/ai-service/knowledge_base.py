import os
import json
import chromadb
from chromadb.utils import embedding_functions

# Configuration
KNOWLEDGE_FILE = "knowledge_data/knowledge.json"
DB_DIR = "knowledge_db"
COLLECTION_NAME = "marketing_concepts"

def load_knowledge():
    """Loads marketing concepts from JSON file."""
    if not os.path.exists(KNOWLEDGE_FILE):
        print(f"Error: Knowledge file not found at {KNOWLEDGE_FILE}")
        return []
    
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def setup_vector_db():
    """Initializes ChromaDB and ingests knowledge chunks."""
    print("Initializing Vector Database...")
    
    # Initialize Chroma Client (Persistent)
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Use a lightweight, high-performance embedding model
    # all-MiniLM-L6-v2 is standard for RAG
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Get or Create Collection
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)
    print(f"Collection '{COLLECTION_NAME}' loaded. Count: {collection.count()}")

    # Load Data
    data = load_knowledge()
    if not data:
        return

    # Check if data already exists to avoid duplicates (naive check)
    if collection.count() >= len(data):
        print("Data appears to be already ingested. Skipping.")
        return

    print(f"Ingesting {len(data)} knowledge chunks...")
    
    ids = []
    documents = []
    metadatas = []

    for item in data:
        # Construct a rich text representation for embedding
        # We want the vector to capture the concept, definition, triggers, and advice
        triggers = ", ".join(item.get('visual_triggers', item.get('trigger_context', [])))
        advice = "\n".join(item.get('actionable_advice', [item.get('advice_template', '')]))
        case_study = item.get('case_study', 'N/A')
        
        text_content = f"""
        Concept: {item['concept']}
        Category: {item.get('category', 'General')}
        Definition: {item['definition']}
        Triggers: {triggers}
        Advice: {advice}
        Case Study: {case_study}
        """
        
        ids.append(item['id'])
        documents.append(text_content.strip())
        metadatas.append({
            "concept": item['concept'],
            "definition": item['definition'],
            "advice": advice,
            "case_study": case_study
        })

    # Add to ChromaDB
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"Successfully ingested {len(ids)} items.")
    print(f"Total collection count: {collection.count()}")

def query_knowledge(query_text, n_results=3):
    """Queries the vector DB for relevant marketing concepts."""
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    return results

if __name__ == "__main__":
    setup_vector_db()
    
    # Test Query
    print("\n--- Test Query: 'User ignored the hero image' ---")
    test_results = query_knowledge("User ignored the hero image and looked at the text below")
    
    for i, doc in enumerate(test_results['documents'][0]):
        print(f"\nResult {i+1}:")
        print(doc)

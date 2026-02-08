# c:\daughter\knowledge_integrator.py

from typing import Any, Dict, List, Optional
import logging
import chromadb
import google.generativeai as genai

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KnowledgeIntegrator:
    """
    Handles Retrieval-Augmented Generation (RAG) by querying a knowledge base.

    Responsibilities:
    - Connects to the vector database (ChromaDB).
    - Uses the Gemini embedding model via a provided client.
    - Retrieves relevant documents based on a query.
    - Formats retrieved context for the PathwayGenerator.
    """

    def __init__(self, config: Dict[str, Any], gemini_client: Optional[Any] = None):
        """
        Initializes the KnowledgeIntegrator.

        Args:
            config: A dictionary containing configuration for the vector DB
                    (e.g., path, collection name) and embedding model name.
            gemini_client: An optional pre-configured Gemini API client instance
                           (used for embeddings). If None, embedding will fail.
                           Expected to be the configured 'genai' module or a specific client object.
        """
        self.config = config
        self.gemini_client = gemini_client # Store the client
        self.vector_db_client = None
        self.embedding_model_name = self.config.get("embedding_model_name", "models/embedding-001")
        self.collection = None # Represents the specific collection/index in the DB

        logging.info("Initializing KnowledgeIntegrator...")
        print("Initializing KnowledgeIntegrator...")
        self._initialize_vector_db()
        self._initialize_embedding_model()
        print("KnowledgeIntegrator initialized.")

    def _initialize_vector_db(self):
        """Sets up the connection to the ChromaDB vector database."""
        db_path = self.config.get("vector_db_path", "./chroma_db")
        collection_name = self.config.get("collection_name", "scim_kb")
        print(f"Connecting to ChromaDB at path: {db_path}, collection: {collection_name}")
        logging.info(f"Connecting to ChromaDB at path: {db_path}, collection: {collection_name}")
        try:
            # Using PersistentClient to store data on disk
            self.vector_db_client = chromadb.PersistentClient(path=db_path)
            # Get or create the collection.
            self.collection = self.vector_db_client.get_or_create_collection(name=collection_name)
            print("ChromaDB connection successful.")
            logging.info("ChromaDB connection successful.")
        except Exception as e:
            print(f"Error connecting to ChromaDB: {e}")
            logging.error(f"Error connecting to ChromaDB: {e}", exc_info=True)
            self.vector_db_client = None
            self.collection = None

    def _initialize_embedding_model(self):
        """Checks for the Gemini client needed for embeddings."""
        print(f"Configured to use Gemini embedding model: {self.embedding_model_name}")
        logging.info(f"Configured to use Gemini embedding model: {self.embedding_model_name}")
        if not self.gemini_client:
            print("Warning: Gemini client not provided during init. Embeddings will not function.")
            logging.warning("Gemini client not provided during KnowledgeIntegrator init. Embeddings will fail.")

    def retrieve(self, query_text: str, top_k: int = 3) -> List[str]:
        """
        Retrieves relevant context from the knowledge base using Gemini embeddings and ChromaDB.

        Args:
            query_text: The text to search for relevant information.
            top_k: The maximum number of documents to retrieve.

        Returns:
            A list of strings, where each string is a relevant document chunk. Returns empty list on errors.
        """
        print(f"Retrieving knowledge for query: '{query_text[:50]}...' (top_k={top_k})")
        logging.info(f"Retrieving knowledge for query: '{query_text[:50]}...' (top_k={top_k})")

        if not self.collection:
            print("Warning: Vector DB collection not available. Skipping retrieval.")
            logging.warning("Vector DB collection not available in retrieve().")
            return []
        if not self.gemini_client:
            print("Warning: Gemini client not available. Cannot generate embeddings. Skipping retrieval.")
            logging.warning("Gemini client not available in retrieve(). Cannot generate embeddings.")
            return []

        try:
            # 1. Generate embedding for the query using the provided Gemini client
            print(f"Generating embedding for query using {self.embedding_model_name}...")
            # Use the embed_content function from the configured genai module
            result = self.gemini_client.embed_content(
                model=self.embedding_model_name,
                content=query_text,
                task_type="retrieval_query" # Specify task type for potentially better embeddings
            )
            query_embedding = result['embedding']
            print("Embedding generated.")

            # 2. Query the vector database
            print(f"Querying ChromaDB collection '{self.collection.name}'...")
            results = self.collection.query(
                query_embeddings=[query_embedding], # Chroma expects a list of embeddings
                n_results=top_k,
                include=['documents'] # Only fetch the document text
            )
            print("Query successful.")

            # 3. Format results (ChromaDB returns results['documents'] as a list of lists)
            retrieved_docs = results.get('documents', [[]])[0]
            print(f"Retrieved {len(retrieved_docs)} documents from vector DB.")
            logging.info(f"Retrieved {len(retrieved_docs)} documents for query '{query_text[:50]}...'")
            return retrieved_docs

        except Exception as e:
            print(f"Error during knowledge retrieval: {e}")
            logging.error(f"Error during knowledge retrieval for query '{query_text[:50]}...': {e}", exc_info=True)
            return [] # Return empty list on error

# Example Usage (Conceptual - Run this from a main script after configuring Gemini)
if __name__ == '__main__':
    # --- In your main script, you would configure Gemini first ---
    # Example using python-dotenv:
    # import os
    # from dotenv import load_dotenv
    # load_dotenv() # Load GOOGLE_API_KEY from .env file
    # api_key = os.getenv("GOOGLE_API_KEY")
    # if not api_key:
    #     print("Error: GOOGLE_API_KEY not found in environment variables.")
    #     gemini_client_instance = None
    # else:
    #     try:
    #         genai.configure(api_key=api_key)
    #         print("Gemini client configured successfully.")
    #         gemini_client_instance = genai # Pass the configured module
    #     except Exception as e:
    #         print(f"Failed to configure Gemini: {e}")
    #         gemini_client_instance = None
    # --- End Gemini Config Example ---

    # Dummy config for KnowledgeIntegrator - replace with your actual settings
    rag_config = {
        "vector_db_path": "./chroma_db_test", # Path where ChromaDB stores its data
        "collection_name": "test_scim_collection",
        "embedding_model_name": "models/embedding-001" # Or your preferred Gemini embedding model
    }

    # !!! Replace 'None' with your actual configured 'gemini_client_instance' from above !!!
    configured_gemini_client = None
    # Example: configured_gemini_client = gemini_client_instance

    integrator = KnowledgeIntegrator(config=rag_config, gemini_client=configured_gemini_client)

    # --- Test Retrieval (only if integrator initialized properly) ---
    if integrator.collection and integrator.gemini_client:
        # Add a dummy document to Chroma for testing if the collection is empty
        # Note: Adding requires generating embeddings too!
        if integrator.collection.count() == 0:
             print("Adding dummy document to ChromaDB for testing...")
             try:
                 dummy_doc_text = "AI safety involves mitigating risks associated with artificial intelligence."
                 # Generate embedding for the dummy document
                 embedding_result = integrator.gemini_client.embed_content(
                     model=integrator.embedding_model_name,
                     content=dummy_doc_text,
                     task_type="retrieval_document" # Use document task type for storage
                 )
                 integrator.collection.add(
                     embeddings=[embedding_result['embedding']],
                     documents=[dummy_doc_text],
                     ids=["test_doc_safety_1"] # Provide unique IDs
                 )
                 print("Dummy document added.")
             except Exception as e:
                 print(f"Failed to add dummy document: {e}")
                 logging.error(f"Failed to add dummy document: {e}", exc_info=True)

        # Now perform a retrieval
        query = "What are the risks of AI?"
        context = integrator.retrieve(query, top_k=2)

        print("\n--- Retrieval Test ---")
        print(f"Query: {query}")
        print("Retrieved Context:")
        if context:
            for i, doc in enumerate(context):
                print(f"{i+1}. {doc}")
        else:
            print("No context retrieved (check warnings/errors above, ensure DB is populated).")
    else:
        print("\nSkipping retrieval example as KnowledgeIntegrator wasn't fully initialized (check Gemini client and ChromaDB connection).")


"""
Vector Storage Module for SCIM Veritas

This module provides vector database functionality for the SCIM-Veritas framework,
enabling semantic storage and retrieval of embeddings for various components.
"""

import logging
import os
import json
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import numpy as np

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

class VectorStore:
    """
    Vector database interface for SCIM-Veritas.
    
    Provides a unified interface for vector storage and retrieval,
    with support for multiple backend providers (ChromaDB, Pinecone).
    """
    
    def __init__(self, provider: str = "chroma", 
                collection_name: str = "scim_vectors",
                persist_directory: Optional[str] = None,
                api_key: Optional[str] = None,
                environment: Optional[str] = None):
        """
        Initialize the vector store.
        
        Args:
            provider: Vector database provider ("chroma" or "pinecone").
            collection_name: Name of the collection/index to use.
            persist_directory: Directory to persist ChromaDB data (if using ChromaDB).
            api_key: API key for Pinecone (if using Pinecone).
            environment: Environment for Pinecone (if using Pinecone).
        """
        self.logger = logging.getLogger("SCIM.VectorStore")
        self.provider = provider.lower()
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.index = None
        
        # Initialize the vector store
        if self.provider == "chroma":
            self._init_chroma(persist_directory)
        elif self.provider == "pinecone":
            self._init_pinecone(api_key, environment)
        else:
            raise ValueError(f"Unsupported vector store provider: {provider}")
    
    def _init_chroma(self, persist_directory: Optional[str] = None) -> None:
        """
        Initialize ChromaDB.
        
        Args:
            persist_directory: Directory to persist ChromaDB data.
        """
        if not CHROMA_AVAILABLE:
            self.logger.error("ChromaDB is not available. Please install it with 'pip install chromadb'.")
            raise ImportError("ChromaDB is not available")
        
        try:
            # Configure ChromaDB
            settings = Settings()
            
            if persist_directory:
                os.makedirs(persist_directory, exist_ok=True)
                self.client = chromadb.PersistentClient(path=persist_directory, settings=settings)
            else:
                self.client = chromadb.Client(settings)
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            
            self.logger.info(f"ChromaDB initialized with collection: {self.collection_name}")
        except Exception as e:
            self.logger.error(f"Error initializing ChromaDB: {e}")
            raise
    
    def _init_pinecone(self, api_key: Optional[str] = None, environment: Optional[str] = None) -> None:
        """
        Initialize Pinecone.
        
        Args:
            api_key: Pinecone API key.
            environment: Pinecone environment.
        """
        if not PINECONE_AVAILABLE:
            self.logger.error("Pinecone is not available. Please install it with 'pip install pinecone-client'.")
            raise ImportError("Pinecone is not available")
        
        try:
            # Check for API key
            if not api_key:
                api_key = os.environ.get("PINECONE_API_KEY")
                
            if not api_key:
                self.logger.error("Pinecone API key is required")
                raise ValueError("Pinecone API key is required")
            
            # Initialize Pinecone client
            self.client = Pinecone(api_key=api_key)
            
            # Check if index exists
            indexes = [index.name for index in self.client.list_indexes()]
            
            if self.collection_name not in indexes:
                # Create index
                self.client.create_index(
                    name=self.collection_name,
                    dimension=1536,  # Default dimension for OpenAI embeddings
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-west-2")
                )
            
            # Connect to index
            self.index = self.client.Index(self.collection_name)
            
            self.logger.info(f"Pinecone initialized with index: {self.collection_name}")
        except Exception as e:
            self.logger.error(f"Error initializing Pinecone: {e}")
            raise
    
    def add_vectors(self, vectors: List[List[float]], 
                   documents: List[str], 
                   metadata: List[Dict[str, Any]],
                   ids: Optional[List[str]] = None) -> List[str]:
        """
        Add vectors to the vector store.
        
        Args:
            vectors: List of embedding vectors.
            documents: List of documents corresponding to the vectors.
            metadata: List of metadata dictionaries for each vector.
            ids: Optional list of IDs for the vectors. If not provided, UUIDs will be generated.
            
        Returns:
            List of IDs for the added vectors.
        """
        if len(vectors) != len(documents) or len(vectors) != len(metadata):
            raise ValueError("vectors, documents, and metadata must have the same length")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
        elif len(ids) != len(vectors):
            raise ValueError("If provided, ids must have the same length as vectors")
        
        try:
            if self.provider == "chroma":
                return self._add_vectors_chroma(vectors, documents, metadata, ids)
            elif self.provider == "pinecone":
                return self._add_vectors_pinecone(vectors, documents, metadata, ids)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error adding vectors: {e}")
            raise
    
    def _add_vectors_chroma(self, vectors: List[List[float]], 
                           documents: List[str], 
                           metadata: List[Dict[str, Any]],
                           ids: List[str]) -> List[str]:
        """
        Add vectors to ChromaDB.
        
        Args:
            vectors: List of embedding vectors.
            documents: List of documents corresponding to the vectors.
            metadata: List of metadata dictionaries for each vector.
            ids: List of IDs for the vectors.
            
        Returns:
            List of IDs for the added vectors.
        """
        # Add embeddings to collection
        self.collection.add(
            embeddings=vectors,
            documents=documents,
            metadatas=metadata,
            ids=ids
        )
        
        return ids
    
    def _add_vectors_pinecone(self, vectors: List[List[float]], 
                             documents: List[str], 
                             metadata: List[Dict[str, Any]],
                             ids: List[str]) -> List[str]:
        """
        Add vectors to Pinecone.
        
        Args:
            vectors: List of embedding vectors.
            documents: List of documents corresponding to the vectors.
            metadata: List of metadata dictionaries for each vector.
            ids: List of IDs for the vectors.
            
        Returns:
            List of IDs for the added vectors.
        """
        # Prepare vectors for Pinecone
        pinecone_vectors = []
        
        for i in range(len(vectors)):
            # Add document to metadata
            meta = metadata[i].copy()
            meta["document"] = documents[i]
            
            pinecone_vectors.append({
                "id": ids[i],
                "values": vectors[i],
                "metadata": meta
            })
        
        # Upsert vectors in batches of 100
        batch_size = 100
        for i in range(0, len(pinecone_vectors), batch_size):
            batch = pinecone_vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)
        
        return ids
    
    def query_vectors(self, query_vector: List[float], 
                     top_k: int = 5, 
                     filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Query the vector store for similar vectors.
        
        Args:
            query_vector: The query embedding vector.
            top_k: Number of results to return.
            filter_metadata: Optional metadata filter.
            
        Returns:
            List of dictionaries containing the query results.
        """
        try:
            if self.provider == "chroma":
                return self._query_vectors_chroma(query_vector, top_k, filter_metadata)
            elif self.provider == "pinecone":
                return self._query_vectors_pinecone(query_vector, top_k, filter_metadata)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error querying vectors: {e}")
            raise
    
    def _query_vectors_chroma(self, query_vector: List[float], 
                             top_k: int = 5, 
                             filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Query ChromaDB for similar vectors.
        
        Args:
            query_vector: The query embedding vector.
            top_k: Number of results to return.
            filter_metadata: Optional metadata filter.
            
        Returns:
            List of dictionaries containing the query results.
        """
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
        
        return formatted_results
    
    def _query_vectors_pinecone(self, query_vector: List[float], 
                               top_k: int = 5, 
                               filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Query Pinecone for similar vectors.
        
        Args:
            query_vector: The query embedding vector.
            top_k: Number of results to return.
            filter_metadata: Optional metadata filter.
            
        Returns:
            List of dictionaries containing the query results.
        """
        # Query the index
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter_metadata
        )
        
        # Format results
        formatted_results = []
        
        for match in results["matches"]:
            document = match["metadata"].pop("document", "")
            
            formatted_results.append({
                "id": match["id"],
                "document": document,
                "metadata": match["metadata"],
                "distance": match["score"]
            })
        
        return formatted_results
    
    def delete_vectors(self, ids: List[str]) -> bool:
        """
        Delete vectors from the vector store.
        
        Args:
            ids: List of vector IDs to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "chroma":
                return self._delete_vectors_chroma(ids)
            elif self.provider == "pinecone":
                return self._delete_vectors_pinecone(ids)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error deleting vectors: {e}")
            return False
    
    def _delete_vectors_chroma(self, ids: List[str]) -> bool:
        """
        Delete vectors from ChromaDB.
        
        Args:
            ids: List of vector IDs to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.collection.delete(ids=ids)
            return True
        except Exception as e:
            self.logger.error(f"Error deleting vectors from ChromaDB: {e}")
            return False
    
    def _delete_vectors_pinecone(self, ids: List[str]) -> bool:
        """
        Delete vectors from Pinecone.
        
        Args:
            ids: List of vector IDs to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.index.delete(ids=ids)
            return True
        except Exception as e:
            self.logger.error(f"Error deleting vectors from Pinecone: {e}")
            return False
    
    def get_vector_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get a vector by ID.
        
        Args:
            id: The vector ID.
            
        Returns:
            Dictionary containing the vector data, or None if not found.
        """
        try:
            if self.provider == "chroma":
                return self._get_vector_by_id_chroma(id)
            elif self.provider == "pinecone":
                return self._get_vector_by_id_pinecone(id)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error getting vector by ID: {e}")
            return None
    
    def _get_vector_by_id_chroma(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get a vector by ID from ChromaDB.
        
        Args:
            id: The vector ID.
            
        Returns:
            Dictionary containing the vector data, or None if not found.
        """
        try:
            result = self.collection.get(ids=[id])
            
            if not result["ids"]:
                return None
            
            return {
                "id": result["ids"][0],
                "document": result["documents"][0],
                "metadata": result["metadatas"][0],
                "embedding": result["embeddings"][0] if "embeddings" in result else None
            }
        except Exception as e:
            self.logger.error(f"Error getting vector by ID from ChromaDB: {e}")
            return None
    
    def _get_vector_by_id_pinecone(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get a vector by ID from Pinecone.
        
        Args:
            id: The vector ID.
            
        Returns:
            Dictionary containing the vector data, or None if not found.
        """
        try:
            result = self.index.fetch(ids=[id])
            
            if not result["vectors"]:
                return None
            
            vector_data = result["vectors"][id]
            document = vector_data["metadata"].pop("document", "")
            
            return {
                "id": id,
                "document": document,
                "metadata": vector_data["metadata"],
                "embedding": vector_data["values"]
            }
        except Exception as e:
            self.logger.error(f"Error getting vector by ID from Pinecone: {e}")
            return None
    
    def update_metadata(self, id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata for a vector.
        
        Args:
            id: The vector ID.
            metadata: New metadata dictionary.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "chroma":
                return self._update_metadata_chroma(id, metadata)
            elif self.provider == "pinecone":
                return self._update_metadata_pinecone(id, metadata)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error updating metadata: {e}")
            return False
    
    def _update_metadata_chroma(self, id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata for a vector in ChromaDB.
        
        Args:
            id: The vector ID.
            metadata: New metadata dictionary.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Get current vector data
            vector_data = self._get_vector_by_id_chroma(id)
            
            if not vector_data:
                return False
            
            # Update with new metadata
            self.collection.update(
                ids=[id],
                metadatas=[metadata]
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating metadata in ChromaDB: {e}")
            return False
    
    def _update_metadata_pinecone(self, id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata for a vector in Pinecone.
        
        Args:
            id: The vector ID.
            metadata: New metadata dictionary.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Get current vector data
            vector_data = self._get_vector_by_id_pinecone(id)
            
            if not vector_data:
                return False
            
            # Add document to metadata
            metadata["document"] = vector_data["document"]
            
            # Update vector
            self.index.update(
                id=id,
                values=vector_data["embedding"],
                metadata=metadata
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating metadata in Pinecone: {e}")
            return False
    
    def count_vectors(self) -> int:
        """
        Count the number of vectors in the store.
        
        Returns:
            Number of vectors.
        """
        try:
            if self.provider == "chroma":
                return self._count_vectors_chroma()
            elif self.provider == "pinecone":
                return self._count_vectors_pinecone()
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error counting vectors: {e}")
            return 0
    
    def _count_vectors_chroma(self) -> int:
        """
        Count the number of vectors in ChromaDB.
        
        Returns:
            Number of vectors.
        """
        try:
            return self.collection.count()
        except Exception as e:
            self.logger.error(f"Error counting vectors in ChromaDB: {e}")
            return 0
    
    def _count_vectors_pinecone(self) -> int:
        """
        Count the number of vectors in Pinecone.
        
        Returns:
            Number of vectors.
        """
        try:
            stats = self.index.describe_index_stats()
            return stats["total_vector_count"]
        except Exception as e:
            self.logger.error(f"Error counting vectors in Pinecone: {e}")
            return 0
    
    def create_collection(self, collection_name: str) -> bool:
        """
        Create a new collection/index.
        
        Args:
            collection_name: Name of the collection to create.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "chroma":
                return self._create_collection_chroma(collection_name)
            elif self.provider == "pinecone":
                return self._create_collection_pinecone(collection_name)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error creating collection: {e}")
            return False
    
    def _create_collection_chroma(self, collection_name: str) -> bool:
        """
        Create a new collection in ChromaDB.
        
        Args:
            collection_name: Name of the collection to create.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.client.create_collection(name=collection_name)
            return True
        except Exception as e:
            self.logger.error(f"Error creating collection in ChromaDB: {e}")
            return False
    
    def _create_collection_pinecone(self, collection_name: str) -> bool:
        """
        Create a new index in Pinecone.
        
        Args:
            collection_name: Name of the index to create.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Check if index exists
            indexes = [index.name for index in self.client.list_indexes()]
            
            if collection_name in indexes:
                return True
            
            # Create index
            self.client.create_index(
                name=collection_name,
                dimension=1536,  # Default dimension for OpenAI embeddings
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-west-2")
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error creating index in Pinecone: {e}")
            return False
    
    def switch_collection(self, collection_name: str) -> bool:
        """
        Switch to a different collection/index.
        
        Args:
            collection_name: Name of the collection to switch to.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "chroma":
                return self._switch_collection_chroma(collection_name)
            elif self.provider == "pinecone":
                return self._switch_collection_pinecone(collection_name)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error switching collection: {e}")
            return False
    
    def _switch_collection_chroma(self, collection_name: str) -> bool:
        """
        Switch to a different collection in ChromaDB.
        
        Args:
            collection_name: Name of the collection to switch to.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.collection = self.client.get_or_create_collection(name=collection_name)
            self.collection_name = collection_name
            return True
        except Exception as e:
            self.logger.error(f"Error switching collection in ChromaDB: {e}")
            return False
    
    def _switch_collection_pinecone(self, collection_name: str) -> bool:
        """
        Switch to a different index in Pinecone.
        
        Args:
            collection_name: Name of the index to switch to.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Check if index exists
            indexes = [index.name for index in self.client.list_indexes()]
            
            if collection_name not in indexes:
                # Create index
                self.client.create_index(
                    name=collection_name,
                    dimension=1536,  # Default dimension for OpenAI embeddings
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-west-2")
                )
            
            # Connect to index
            self.index = self.client.Index(collection_name)
            self.collection_name = collection_name
            
            return True
        except Exception as e:
            self.logger.error(f"Error switching index in Pinecone: {e}")
            return False
    
    def list_collections(self) -> List[str]:
        """
        List available collections/indexes.
        
        Returns:
            List of collection/index names.
        """
        try:
            if self.provider == "chroma":
                return self._list_collections_chroma()
            elif self.provider == "pinecone":
                return self._list_collections_pinecone()
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error listing collections: {e}")
            return []
    
    def _list_collections_chroma(self) -> List[str]:
        """
        List available collections in ChromaDB.
        
        Returns:
            List of collection names.
        """
        try:
            return self.client.list_collections()
        except Exception as e:
            self.logger.error(f"Error listing collections in ChromaDB: {e}")
            return []
    
    def _list_collections_pinecone(self) -> List[str]:
        """
        List available indexes in Pinecone.
        
        Returns:
            List of index names.
        """
        try:
            return [index.name for index in self.client.list_indexes()]
        except Exception as e:
            self.logger.error(f"Error listing indexes in Pinecone: {e}")
            return []
    
    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection/index.
        
        Args:
            collection_name: Name of the collection to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "chroma":
                return self._delete_collection_chroma(collection_name)
            elif self.provider == "pinecone":
                return self._delete_collection_pinecone(collection_name)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error deleting collection: {e}")
            return False
    
    def _delete_collection_chroma(self, collection_name: str) -> bool:
        """
        Delete a collection in ChromaDB.
        
        Args:
            collection_name: Name of the collection to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.client.delete_collection(name=collection_name)
            
            # If we deleted the current collection, switch to a different one
            if collection_name == self.collection_name:
                collections = self.client.list_collections()
                if collections:
                    self.collection = self.client.get_collection(name=collections[0])
                    self.collection_name = collections[0]
                else:
                    self.collection = self.client.create_collection(name="default")
                    self.collection_name = "default"
            
            return True
        except Exception as e:
            self.logger.error(f"Error deleting collection in ChromaDB: {e}")
            return False
    
    def _delete_collection_pinecone(self, collection_name: str) -> bool:
        """
        Delete an index in Pinecone.
        
        Args:
            collection_name: Name of the index to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.client.delete_index(name=collection_name)
            
            # If we deleted the current index, switch to a different one
            if collection_name == self.collection_name:
                indexes = [index.name for index in self.client.list_indexes()]
                if indexes:
                    self.index = self.client.Index(indexes[0])
                    self.collection_name = indexes[0]
                else:
                    # Create a new default index
                    self.client.create_index(
                        name="default",
                        dimension=1536,
                        metric="cosine",
                        spec=ServerlessSpec(cloud="aws", region="us-west-2")
                    )
                    self.index = self.client.Index("default")
                    self.collection_name = "default"
            
            return True
        except Exception as e:
            self.logger.error(f"Error deleting index in Pinecone: {e}")
            return False
    
    def backup_collection(self, collection_name: str, backup_path: str) -> bool:
        """
        Backup a collection/index to a file.
        
        Args:
            collection_name: Name of the collection to backup.
            backup_path: Path to save the backup file.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "chroma":
                return self._backup_collection_chroma(collection_name, backup_path)
            elif self.provider == "pinecone":
                return self._backup_collection_pinecone(collection_name, backup_path)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error backing up collection: {e}")
            return False
    
    def _backup_collection_chroma(self, collection_name: str, backup_path: str) -> bool:
        """
        Backup a collection in ChromaDB to a file.
        
        Args:
            collection_name: Name of the collection to backup.
            backup_path: Path to save the backup file.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Get the collection
            collection = self.client.get_collection(name=collection_name)
            
            # Get all data
            data = collection.get()
            
            # Create backup directory if it doesn't exist
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Save to file
            with open(backup_path, 'w') as f:
                json.dump(data, f)
            
            return True
        except Exception as e:
            self.logger.error(f"Error backing up collection in ChromaDB: {e}")
            return False
    
    def _backup_collection_pinecone(self, collection_name: str, backup_path: str) -> bool:
        """
        Backup an index in Pinecone to a file.
        
        Args:
            collection_name: Name of the index to backup.
            backup_path: Path to save the backup file.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Connect to the index
            index = self.client.Index(collection_name)
            
            # Get all vector IDs
            stats = index.describe_index_stats()
            total_vectors = stats["total_vector_count"]
            
            # Fetch vectors in batches
            batch_size = 1000
            vectors = []
            
            # This is a simplified approach - in a real system, you would need
            # to implement pagination to handle large indexes
            if total_vectors > 0:
                # Query with a dummy vector to get all IDs
                dummy_vector = [0.0] * 1536
                results = index.query(
                    vector=dummy_vector,
                    top_k=min(10000, total_vectors),
                    include_metadata=True
                )
                
                # Get all IDs
                ids = [match["id"] for match in results["matches"]]
                
                # Fetch vectors in batches
                for i in range(0, len(ids), batch_size):
                    batch_ids = ids[i:i+batch_size]
                    batch_results = index.fetch(ids=batch_ids)
                    
                    for id, vector_data in batch_results["vectors"].items():
                        vectors.append({
                            "id": id,
                            "values": vector_data["values"],
                            "metadata": vector_data["metadata"]
                        })
            
            # Create backup directory if it doesn't exist
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Save to file
            with open(backup_path, 'w') as f:
                json.dump(vectors, f)
            
            return True
        except Exception as e:
            self.logger.error(f"Error backing up index in Pinecone: {e}")
            return False
    
    def restore_collection(self, backup_path: str, collection_name: Optional[str] = None) -> bool:
        """
        Restore a collection/index from a backup file.
        
        Args:
            backup_path: Path to the backup file.
            collection_name: Name of the collection to restore to. If None, uses the current collection.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Use current collection name if not specified
            if collection_name is None:
                collection_name = self.collection_name
            
            if self.provider == "chroma":
                return self._restore_collection_chroma(backup_path, collection_name)
            elif self.provider == "pinecone":
                return self._restore_collection_pinecone(backup_path, collection_name)
            else:
                raise ValueError(f"Unsupported vector store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error restoring collection: {e}")
            return False
    
    def _restore_collection_chroma(self, backup_path: str, collection_name: str) -> bool:
        """
        Restore a collection in ChromaDB from a backup file.
        
        Args:
            backup_path: Path to the backup file.
            collection_name: Name of the collection to restore to.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Load backup data
            with open(backup_path, 'r') as f:
                data = json.load(f)
            
            # Create or get collection
            collection = self.client.get_or_create_collection(name=collection_name)
            
            # Check if we have data to restore
            if not data["ids"]:
                return True
            
            # Add data to collection
            collection.add(
                ids=data["ids"],
                embeddings=data["embeddings"],
                metadatas=data["metadatas"],
                documents=data["documents"]
            )
            
            # Update current collection if restoring to current collection name
            if collection_name == self.collection_name:
                self.collection = collection
            
            return True
        except Exception as e:
            self.logger.error(f"Error restoring collection in ChromaDB: {e}")
            return False
    
    def _restore_collection_pinecone(self, backup_path: str, collection_name: str) -> bool:
        """
        Restore an index in Pinecone from a backup file.
        
        Args:
            backup_path: Path to the backup file.
            collection_name: Name of the index to restore to.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Load backup data
            with open(backup_path, 'r') as f:
                vectors = json.load(f)
            
            # Check if index exists
            indexes = [index.name for index in self.client.list_indexes()]
            
            if collection_name not in indexes:
                # Create index
                self.client.create_index(
                    name=collection_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-west-2")
                )
            
            # Connect to index
            index = self.client.Index(collection_name)
            
            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i+batch_size]
                index.upsert(vectors=batch)
            
            # Update current index if restoring to current collection name
            if collection_name == self.collection_name:
                self.index = index
            
            return True
        except Exception as e:
            self.logger.error(f"Error restoring index in Pinecone: {e}")
            return False
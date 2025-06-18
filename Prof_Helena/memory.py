import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_community.vectorstores.faiss import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

class ArtHistoryMemory:
    """
    Memory system for Professor Helena
    Manages chronological artwork database with vector search capabilities
    """
    
    def __init__(self, data_path: str = "data/art_history_docs"):
        self.data_path = data_path
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_store = None
        self.analysis_history = []
        
        # Ensure data directory exists
        os.makedirs(data_path, exist_ok=True)
        
        # Initialize or load existing vector store
        self._initialize_vector_store()
        
    def _initialize_vector_store(self):
        """Initialize vector store with art history documents"""
        vector_store_path = os.path.join(self.data_path, "vector_store")
        
        if os.path.exists(vector_store_path):
            # Load existing vector store
            self.vector_store = FAISS.load_local(
                vector_store_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # Create new vector store with initial art history knowledge
            initial_docs = self._create_initial_art_documents()
            if initial_docs:
                self.vector_store = FAISS.from_documents(initial_docs, self.embeddings)
                self.vector_store.save_local(vector_store_path)
            else:
                # Create empty vector store
                dummy_doc = Document(page_content="Art history knowledge base", metadata={})
                self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
    
    def _create_initial_art_documents(self) -> List[Document]:
        """Create initial art history documents for the knowledge base"""
        # This would typically load from files in your data directory
        # For now, we'll create some sample documents
        
        sample_art_knowledge = [
            {
                "content": "Renaissance art (14th-17th century) emphasized humanism, perspective, and classical themes. Key characteristics include realistic human figures, linear perspective, and chiaroscuro lighting techniques.",
                "metadata": {"period": "Renaissance", "century": "14th-17th", "movements": ["High Renaissance", "Early Renaissance"]}
            },
            {
                "content": "Baroque art (17th-18th century) featured dramatic lighting, intense emotions, and dynamic compositions. Artists like Caravaggio pioneered tenebrism, while Bernini excelled in sculptural movement.",
                "metadata": {"period": "Baroque", "century": "17th-18th", "techniques": ["tenebrism", "chiaroscuro"]}
            },
            {
                "content": "Impressionism (late 19th century) revolutionized art with loose brushwork, light studies, and outdoor painting. Monet, Renoir, and Degas captured fleeting moments and changing light conditions.",
                "metadata": {"period": "Impressionism", "century": "19th", "techniques": ["plein air", "broken color"]}
            },
            {
                "content": "Cubism (early 20th century) deconstructed forms into geometric shapes. Picasso and Braque developed analytical and synthetic cubism, fundamentally changing perspective representation.",
                "metadata": {"period": "Cubism", "century": "20th", "artists": ["Picasso", "Braque"]}
            },
            {
                "content": "Abstract Expressionism (mid-20th century) emphasized spontaneous, automatic, or subconscious creation. Artists like Pollock and Rothko explored pure abstraction and emotional expression.",
                "metadata": {"period": "Abstract Expressionism", "century": "20th", "techniques": ["action painting", "color field"]}
            }
        ]
        
        documents = []
        for item in sample_art_knowledge:
            doc = Document(
                page_content=item["content"],
                metadata=item["metadata"]
            )
            documents.append(doc)
        
        return documents
    
    def search_similar_artworks(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar artworks or relevant art historical information
        
        Args:
            query: Search query (artwork description, style, period, etc.)
            k: Number of results to return
            
        Returns:
            List of relevant documents with similarity scores
        """
        if not self.vector_store:
            return []
        
        try:
            # Perform similarity search
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
            
            results = []
            for doc, score in docs_with_scores:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score)
                })
            
            return results
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
    
    def store_analysis(self, artwork_info: Dict[str, Any], analysis: str, perspectives: List[Dict[str, Any]], visual_analysis: Optional[Dict[str, Any]] = None):
        """
        Store a completed analysis in memory
        
        Args:
            artwork_info: Information about the analyzed artwork
            analysis: The complete analysis text
            perspectives: Historical perspectives generated
        """
        analysis_record = {
        "timestamp": datetime.now().isoformat(),
        "artwork_info": artwork_info,
        "analysis": analysis,
        "perspectives": perspectives,
        "visual_analysis": visual_analysis  # Add this line
        }
        
        self.analysis_history.append(analysis_record)
        
        # Also add to vector store for future reference
        if self.vector_store:
            doc = Document(
                page_content=f"Analysis: {analysis}",
                metadata={
                    "type": "analysis",
                    "artwork": artwork_info.get("title", "Unknown"),
                    "timestamp": analysis_record["timestamp"]
                }
            )
            
            self.vector_store.add_documents([doc])
            
            # Save updated vector store
            vector_store_path = os.path.join(self.data_path, "vector_store")
            self.vector_store.save_local(vector_store_path)
    
    def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis history"""
        return self.analysis_history[-limit:]
    
    def add_art_document(self, content: str, metadata: Dict[str, Any]):
        """Add a new art history document to the knowledge base"""
        doc = Document(page_content=content, metadata=metadata)
        
        if self.vector_store:
            self.vector_store.add_documents([doc])
            # Save updated vector store
            vector_store_path = os.path.join(self.data_path, "vector_store")
            self.vector_store.save_local(vector_store_path)

import os
import ollama
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import json
from datetime import datetime

class TinyLlamaRAG:
    def __init__(self, model_name="tinyllama", embedding_model="all-MiniLM-L6-v2"):
        """
        Initialize RAG system with and FAISS
        
        Args:
            model_name: Ollama model name (tinyllama, gemma:2b, etc.)
            embedding_model: SentenceTransformer model for embeddings
        """
        print("🚀 Initializing TinyLlama RAG System...")
        
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(embedding_model)
        self.documents = []
        self.chunks = []
        self.chunk_metadata = []
        self.faiss_index = None
        
        print(f"✅ Using model: {model_name}")
        print(f"✅ Using embeddings: {embedding_model}")
    
    def load_documents_from_folder(self, folder_path="documents", chunk_size=500, overlap=50):
        """
        Load all .txt files from folder and split into chunks
        
        Args:
            folder_path: Path to folder containing .txt files
            chunk_size: Maximum words per chunk
            overlap: Words to overlap between chunks
        """
        print(f"\n📁 Loading documents from: {folder_path}")
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"❌ Created folder '{folder_path}' - Please add some .txt files!")
            return False
        
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        
        if not txt_files:
            print("❌ No .txt files found! Please add some text documents.")
            return False
        
        total_chunks = 0
        
        for filename in txt_files:
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.documents.append({
                    'filename': filename,
                    'content': content,
                    'length': len(content)
                })
                
                # Split into chunks with overlap
                file_chunks = self._split_into_chunks(content, chunk_size, overlap)
                
                # Add metadata for each chunk
                for i, chunk in enumerate(file_chunks):
                    self.chunks.append(chunk)
                    self.chunk_metadata.append({
                        'filename': filename,
                        'chunk_id': i,
                        'chunk_start': i * (chunk_size - overlap),
                        'chunk_length': len(chunk)
                    })
                
                total_chunks += len(file_chunks)
                print(f"   📄 {filename}: {len(file_chunks)} chunks")
                
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
        
        print(f"✅ Loaded {len(self.documents)} documents, {total_chunks} chunks total")
        return True
    
    def _split_into_chunks(self, text, chunk_size, overlap):
        """Split text into overlapping chunks by words"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)
            
            # Break if we've covered all words
            if i + chunk_size >= len(words):
                break
        
        return chunks
    
    def create_embeddings_and_index(self):
        """
        Create embeddings for all chunks and build FAISS index
        """
        if not self.chunks:
            print("❌ No chunks to embed! Load documents first.")
            return False
        
        print(f"\n🧮 Creating embeddings for {len(self.chunks)} chunks...")
        
        try:
            # Create embeddings
            embeddings = self.embedding_model.encode(
                self.chunks, 
                show_progress_bar=True,
                convert_to_numpy=True
            )
            
            print(f"✅ Embeddings shape: {embeddings.shape}")
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
            self.faiss_index.add(embeddings)
            
            print(f"✅ FAISS index created with {self.faiss_index.ntotal} vectors")
            return True
            
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
            return False
    
    def retrieve_relevant_chunks(self, query, top_k=3):
        """
        Retrieve most relevant chunks for a query using FAISS
        
        Args:
            query: Search query
            top_k: Number of chunks to retrieve
        
        Returns:
            List of relevant chunks with metadata
        """
        if self.faiss_index is None:
            print("❌ No FAISS index found! Create embeddings first.")
            return []
        
        try:
            # Embed the query
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search FAISS index
            scores, indices = self.faiss_index.search(query_embedding, top_k)
            
            # Gather results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1:  # Valid result
                    results.append({
                        'chunk': self.chunks[idx],
                        'metadata': self.chunk_metadata[idx],
                        'score': float(score),
                        'rank': i + 1
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Error retrieving chunks: {e}")
            return []
    
    def generate_rag_response(self, question, retrieved_chunks):
        """
        Generate response using TinyLlama with retrieved context
        
        Args:
            question: User's question
            retrieved_chunks: Relevant chunks from retrieval
        
        Returns:
            Generated response
        """
        if not retrieved_chunks:
            # Fallback to direct question
            prompt = f"Question: {question}\n\nPlease provide a helpful answer based on your knowledge:"
        else:
            # Build context from retrieved chunks
            context_parts = []
            for chunk in retrieved_chunks:
                context_parts.append(f"Source: {chunk['metadata']['filename']}")
                context_parts.append(f"Content: {chunk['chunk'][:500]}...")  # Limit chunk size
                context_parts.append("---")
            
            context = "\n".join(context_parts)
            
            # Create RAG prompt
            prompt = f"""Based on the following context information, please answer the question.

Context:
{context}

Question: {question}

Instructions:
- Use the provided context to answer the question
- If the context doesn't contain relevant information, say so
- Be specific and cite which sources support your answer
- Keep your answer concise but complete

Answer:"""

        try:
            # Generate response with TinyLlama
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.3,  # Lower temperature for factual responses
                    'top_p': 0.9,
                    'max_tokens': 500,
                    'stop': ['Question:', 'Context:']  # Stop tokens
                }
            )
            
            return response['response'].strip()
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return "Sorry, I encountered an error generating a response."
    
    def ask_question(self, question, top_k=3, show_sources=True):
        """
        Main method to ask a question and get RAG response
        
        Args:
            question: User's question
            top_k: Number of chunks to retrieve
            show_sources: Whether to show retrieved sources
        
        Returns:
            Response with sources
        """
        print(f"\n❓ Question: {question}")
        print("🔍 Searching for relevant information...")
        
        # Retrieve relevant chunks
        retrieved_chunks = self.retrieve_relevant_chunks(question, top_k)
        
        if show_sources and retrieved_chunks:
            print(f"📚 Found {len(retrieved_chunks)} relevant sources:")
            for chunk in retrieved_chunks:
                print(f"   📄 {chunk['metadata']['filename']} (score: {chunk['score']:.3f})")
        
        # Generate response
        print("🤖 Generating answer...")
        response = self.generate_rag_response(question, retrieved_chunks)
        
        return {
            'question': question,
            'answer': response,
            'sources': retrieved_chunks,
            'timestamp': datetime.now().isoformat()
        }
    
    def interactive_chat(self):
        """
        Start interactive chat session
        """
        print("\n💬 TinyLlama RAG Chat Started!")
        print("Ask questions about your documents. Type 'quit' to exit.")
        print("Commands: 'sources' = toggle source display, 'stats' = show statistics")
        
        show_sources = True
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🤖 RAG: Goodbye! 👋")
                    break
                
                elif user_input.lower() == 'sources':
                    show_sources = not show_sources
                    print(f"🔧 Source display: {'ON' if show_sources else 'OFF'}")
                    continue
                
                elif user_input.lower() == 'stats':
                    self._show_stats()
                    continue
                
                elif not user_input:
                    continue
                
                # Ask question
                result = self.ask_question(user_input, show_sources=show_sources)
                print(f"\n🤖 RAG: {result['answer']}")
                
                if show_sources and result['sources']:
                    print("\n📚 Sources used:")
                    for source in result['sources']:
                        print(f"   • {source['metadata']['filename']}")
                
            except KeyboardInterrupt:
                print("\n🤖 RAG: Goodbye! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_stats(self):
        """Show system statistics"""
        print(f"\n📊 RAG System Statistics:")
        print(f"   Documents loaded: {len(self.documents)}")
        print(f"   Total chunks: {len(self.chunks)}")
        print(f"   FAISS index size: {self.faiss_index.ntotal if self.faiss_index else 0}")
        print(f"   Model: {self.model_name}")

def main():
    """
    Main function to set up and run RAG system
    """
    print("🚀 TinyLlama RAG System")
    print("=" * 50)
    
    # Initialize RAG system
    rag = TinyLlamaRAG(model_name="tinyllama")  # Change to "gemma:2b" if preferred
    
    # Load documents
    if not rag.load_documents_from_folder("documents"):
        print("Please add .txt files to the 'documents' folder and run again!")
        return
    
    # Create embeddings and index
    if not rag.create_embeddings_and_index():
        print("Failed to create embeddings. Please check your setup.")
        return
    
    print("\n✅ RAG System Ready!")
    
    # Test with a sample question
    print("\n🧪 Testing with sample question...")
    sample_result = rag.ask_question("What is this document about?", show_sources=False)
    print(f"Sample answer: {sample_result['answer'][:200]}...")
    
    # Start interactive chat
    rag.interactive_chat()

if __name__ == "__main__":
    main()

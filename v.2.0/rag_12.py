import ollama
import os
from pathlib import Path

class SimpleRAG:
    def __init__(self):
        self.documents = {}
        self.load_documents()
    
    def load_documents(self):
        """Load text documents from a folder"""
        docs_folder = "rag_input"  # Create this folder and add .txt files
        
        if not os.path.exists(docs_folder):
            os.makedirs(docs_folder)
            print(f"Created {docs_folder} folder. Add some .txt files there!")
            return
        
        for file_path in Path(docs_folder).glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.documents[file_path.name] = content
        
        print(f"Loaded {len(self.documents)} documents")
    
    def search_documents(self, query):
        """Simple keyword-based search"""
        relevant_docs = []
        query_words = query.lower().split()
        
        for doc_name, content in self.documents.items():
            content_lower = content.lower()
            score = sum(1 for word in query_words if word in content_lower)
            
            if score > 2:
                relevant_docs.append((doc_name, content, score))
        
        # Sort by relevance score
        relevant_docs.sort(key=lambda x: x[2], reverse=True)
        return relevant_docs[:1]  # Return top 2 most relevant
    
    def answer_question(self, question):
        """Generate answer using retrieved documents"""
        relevant_docs = self.search_documents(question)
        
        if not relevant_docs:
            return "I couldn't find relevant information in the documents."
        
        # Prepare context from relevant documents
        context = ""
        for doc_name, content, score in relevant_docs:
            context += f"\nFrom {doc_name}:\n{content[:500]}...\n"
        
        rag_prompt = f"""
        Based on the following documents, answer this question: {question}
        
        Context from documents:
        {context}
        
        Instructions:
        - Only use information from the provided documents
        - If the answer isn't in the documents, say so
        - Cite which document(s) you're using
        - Be specific and accurate
        
        Answer:
        """
        
        response = ollama.generate(
            model='tinyllama',
            prompt=rag_prompt,
            options={'temperature': 0.3}  # Lower temperature for factual responses
        )
        
        return response['response']

def rag_demo():
    print("🔍 RAG Document Q&A System")
    print("Add .txt files to the 'documents' folder, then ask questions about them!")
    
    rag_system = SimpleRAG()
    
    while True:
        question = input("\n❓ Ask a question (or 'quit'): ")
        if question.lower() == 'quit':
            break
            
        answer = rag_system.answer_question(question)
        print(f"\n🤖 Answer: {answer}")

if __name__ == "__main__":
    rag_demo()

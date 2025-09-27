import os

class RAGController:
    def __init__(self):
        self.current_model = "tinyllama"
        self.documents = []
    
    def set_model(self, model_name):
        self.current_model = model_name
    
    def add_document(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.documents.append({
                'path': file_path,
                'name': os.path.basename(file_path),
                'content': content
            })
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def process_query(self, query):
        # Placeholder for RAG processing
        # TODO: Integrate with your FAISS RAG system
        
        if not self.documents:
            return "No documents loaded. Please upload some documents first."
        
        # Simple keyword search for now
        relevant_docs = []
        for doc in self.documents:
            if query.lower() in doc['content'].lower():
                relevant_docs.append(doc['name'])
        
        if relevant_docs:
            return f"Found information in: {', '.join(relevant_docs)}\n\nRAG Response: This is a placeholder response based on your query '{query}'"
        else:
            return f"No relevant information found for '{query}' in uploaded documents."

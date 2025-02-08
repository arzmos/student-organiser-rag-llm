from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Answering System</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .container {
            margin-top: 50px;
        }
        #question {
            height: 100px;
        }
        #response {
            margin-top: 20px;
            white-space: pre-wrap;
            background-color: #ffffff;
            border: 1px solid #ced4da;
            padding: 15px;
            border-radius: 5px;
        }
        .content-link {
            color: #007bff; /* Bootstrap primary color */
            text-decoration: none;
        }
        .content-link:hover {
            text-decoration: underline;
        }
        .sources {
            margin-top: 15px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Ask a Question</h1>
        <div class="form-group">
            <textarea id="question" class="form-control" placeholder="Enter your question here..."></textarea>
        </div>
        <button class="btn btn-primary btn-block" onclick="askQuestion()">Submit</button>
        <div id="response"></div>
        <div id="sources" class="sources"></div>
    </div>

    <script>
        async function askQuestion() {
            const question = document.getElementById('question').value;
            const responseDiv = document.getElementById('response');
            const sourcesDiv = document.getElementById('sources');
            
            responseDiv.innerHTML = 'Loading...';
            sourcesDiv.innerHTML = '';

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question }),
                });

                const data = await response.json();
                responseDiv.innerHTML = data.answer || 'No answer provided.';
                
                if (data.sources && data.sources.length > 0) {
                    sourcesDiv.innerHTML = '<h5>Sources:</h5>' + 
                        data.sources.map(source => 
                            `<p><a href="${source.url}" target="_blank" class="content-link">${source.title}</a></p>`
                        ).join('');
                }
            } catch (error) {
                responseDiv.innerHTML = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
'''

# Configure Gemini directly with API key
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

try:
    # Load the data
    with open('aggregated_data.json', 'r', encoding='utf-8') as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("aggregated_data.json not found. Please make sure it exists in the same directory as app.py")

# Prepare documents for TF-IDF
documents = [doc['content'] for doc in knowledge_base]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

def get_relevant_documents(query, top_k=3):
    # Transform the query
    query_vector = vectorizer.transform([query])
    
    # Calculate similarity
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]
    
    # Get top k most similar documents
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    relevant_docs = []
    for idx in top_indices:
        doc = knowledge_base[idx]
        relevant_docs.append({
            'content': doc['content'],
            'source': doc['source'],
            'title': doc['title']
        })
    
    return relevant_docs

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        question = data['question']
        
        # Get relevant documents
        relevant_docs = get_relevant_documents(question)
        
        # Prepare context for Gemini
        context = "Based on the following information:\n\n"
        for doc in relevant_docs:
            context += f"Document: {doc['content']}\n\n"
        
        prompt = f"""{context}
        
        Question: {question}
        
        Please provide a clear and concise answer based only on the information provided above. 
        If the information is not sufficient to answer the question, please say so."""
        
        # Generate response using Gemini
        response = model.generate_content(prompt)
        
        # Prepare sources information
        sources = []
        for doc in relevant_docs:
            if doc['source']:  # Only include if source URL exists
                sources.append({
                    'url': doc['source'],
                    'title': doc['title']
                })
        
        return jsonify({
            'answer': response.text,
            'sources': sources
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use the port specified by Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

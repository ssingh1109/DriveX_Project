<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Q&A Application</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        input, button { margin: 10px 0; }
        #response { margin-top: 20px; }
    </style>
</head>
<body>

    <h1>Document Q&A Application</h1>
    
    <!-- File upload form -->
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" name="file" id="file" accept=".xls,.xlsx" required />
        <button type="submit">Upload File</button>
    </form>
    
    <!-- Input field for asking questions -->
    <h2>Ask a Question</h2>
    <input type="text" id="question" placeholder="Enter your question here" />
    <button onclick="askQuestion()">Ask</button>
    
    <div id="response"></div>

    <script>
        let index, texts; // Global variables to store FAISS index and document texts after file upload

        // Handle file upload
        document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData();
            formData.append("file", document.getElementById('file').files[0]);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message); // Show success message
                } else {
                    alert(data.error); // Show error if any
                }
            })
            .catch(error => {
                console.error('Error uploading file:', error);
                alert('Failed to upload file.');
            });
        });

        // Handle asking a question
        function askQuestion() {
            const query = document.getElementById('question').value;
            if (!query) {
                alert('Please enter a question.');
                return;
            }

            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            })
            .then(response => response.json())
            .then(data => {
                if (data.answer) {
                    document.getElementById('response').innerText = "Answer: " + data.answer;
                } else {
                    document.getElementById('response').innerText = "Error: No answer found.";
                }
            })
            .catch(error => {
                console.error('Error asking question:', error);
                alert('Failed to get an answer.');
            });
        }
    </script>

</body>
</html>

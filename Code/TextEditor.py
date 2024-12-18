#Create the UI for the editor with custom HTML and JavaScript
import streamlit as st  
def text_editor(extracted_text):
# Define HTML for contenteditable div with JavaScript functions for formatting
    editor_html = f"""
    <div contenteditable="true" id="editor" style="border:1px solid #ccc; 
    width:95%; padding:10px; min-height:100px; margin-bottom: 10px; color: white; background-color: black;">
        
    </div>

    <br>
    <button style="color: white; background-color: #007bff; border: none; padding: 5px 10px; 
    cursor: pointer;" onclick="document.execCommand('bold', false, '');">Bold</button>
    <button style="color: white; background-color: #007bff; border: none; padding: 5px 10px; 
    cursor: pointer;" onclick="document.execCommand('italic', false, '');">Italic</button>
    <button style="color: white; background-color: #007bff; border: none; padding: 5px 10px; 
    cursor: pointer;" onclick="document.execCommand('underline', false, '');">Underline</button><br><br>
    <button style="color: white; background-color: #007bff; border: none; padding: 5px 10px; 
    cursor: pointer;" onclick="appendText('{extracted_text}');">Add Text</button>
    <br>
    <br>
    <br>
    <button style="color: white; background-color: #007bff; border: none; padding: 5px 10px; 
    cursor: pointer;" onclick="downloadContent()">Download as .html</button>

    <script>
        // Function to download the content of the editor as an HTML file
        function downloadContent() {{
            var content = document.getElementById('editor').innerHTML; // Get the HTML content
            var blob = new Blob([content], {{ type: 'text/html' }}); // Set type to 'text/html'
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'text_editor_output.html'; // Change the file extension to .html
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        // Function to append text
        function appendText(newText) {{
            var editor = document.getElementById('editor');
            editor.innerText += newText; // Append new text to the current content
            editor.focus(); // Set focus back to the editor
        }}

    </script>
    """

    # Embed the custom HTML into the Streamlit app
    st.components.v1.html(editor_html, height=500)
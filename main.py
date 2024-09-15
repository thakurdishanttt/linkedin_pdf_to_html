import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import openai
import os

import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set your OpenAI API key securely
openai.api_key = "sk-svcacct-RBat5Y6n4uTDNL03C7y-s8OK0bPWegb8KgrhrspA_bWh4fRY73mDJU-ZFK9T3BlbkFJbZQ8stps9eneBF-7Utao1uI_qXJjcBBkxqFhPyjrYOktx88twVQazSVf7PwA" # Better to set it as an environment variable  

# Function to extract text from the uploaded PDF file using OCR
def extract_text_from_pdf(pdf_path):
    try:
        # Add the path to your poppler installation
        poppler_path = r"C:\Users\thaku\Downloads\Release-24.07.0-0\poppler-24.07.0\Library\bin"  # Replace with your actual path to poppler's 'bin' folder
        images = convert_from_path(pdf_path, 500, poppler_path=poppler_path)  # Convert PDF pages to images
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)  # Extract text from each image
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None


# Function to process the extracted text using OpenAI API
def process_text_with_openai(text):
    try:
        # Define a system message to guide the model for structured resume output
        messages = [
            {"role": "system", "content": "You are a helpful assistant that structures resumes."},
            {"role": "user", "content": f"Convert the following resume text into a structured format with sections like 'Work Experience', 'Skills', 'Education', etc:\n\n{text}"}
        ]

        # Call the OpenAI API with the new chat-based completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use an available model like gpt-3.5-turbo
            messages=messages,
            temperature=0.5
        )

        structured_data = response['choices'][0]['message']['content'].strip()  # Extract structured data
        return structured_data
    except Exception as e:
        st.error(f"Error processing text with OpenAI: {e}")
        return None


# Function to generate HTML resume from structured data
# Function to generate HTML resume from structured data
def generate_html_resume(structured_data):
    html_content = """
    <html>
        <head>
            <title>Resume</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .section {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="resume">
                {structured_data}
            </div>
        </body>
    </html>
    """.format(structured_data=structured_data.replace("\n", "<br>"))  # Replace line breaks with HTML <br>
    return html_content



# Function to save the HTML resume to a local file
def save_html_to_file(html_content, file_name="resume.html"):
    try:
        with open(file_name, "w") as f:
            f.write(html_content)
        st.success(f"Resume saved locally as {file_name}")
    except Exception as e:
        st.error(f"Error saving HTML resume to file: {e}")

# Main function to run the Streamlit app
# Main function to run the Streamlit app
def main():
    st.title("LinkedIn PDF to HTML Resume Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a LinkedIn PDF", type="pdf")

    if pdf_file:
        try:
            # Save the uploaded PDF locally
            pdf_path = r"C:\Users\thaku\OneDrive - Graphic Era University\Desktop\python\Freelancing\Thakur Dishant __CV.pdf"  # Use a temporary file for uploading
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.read())

            # Extract text from the PDF using OCR
            text = extract_text_from_pdf(pdf_path)

            if text:
                st.write("### Extracted Text from PDF:")
                st.write(text)

                # Process the text with OpenAI to structure it into resume sections
                structured_data = process_text_with_openai(text)
                
                if structured_data:
                    st.write("### Structured Data from OpenAI:")
                    st.write(structured_data)

                    # Generate and display the HTML resume
                    html_resume = generate_html_resume(structured_data)
                    st.markdown(html_resume, unsafe_allow_html=True)

                    # Allow the user to download the generated HTML resume
                    st.download_button(
                        label="Download HTML Resume",
                        data=html_resume,
                        file_name="resume.html",
                        mime="text/html"
                    )

                    # Save the HTML resume locally
                    save_html_to_file(html_resume, file_name="local_resume.html")
                else:
                    st.error("Failed to generate structured data from OpenAI.")
            else:
                st.error("Failed to extract text from the uploaded PDF.")
        
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Call main function directly
main()

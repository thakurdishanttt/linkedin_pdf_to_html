# LinkedIn PDF to HTML Resume Converter

This project is a **Streamlit web application** that allows users to upload a LinkedIn PDF resume and converts it into a structured HTML format. The application uses **OCR (Optical Character Recognition)** to extract text from the PDF, processes the extracted text with **OpenAI GPT**, and generates a downloadable HTML resume.

## Features

- **PDF Upload**: Upload a LinkedIn PDF resume through the app.
- **OCR with Tesseract**: Extracts text from the PDF using Tesseract OCR.
- **OpenAI GPT Integration**: Processes the extracted text to structure it into sections like Work Experience, Skills, Education, etc.
- **HTML Resume Generation**: Generates a downloadable HTML version of the structured resume.
  
## How It Works

1. The user uploads a PDF resume.
2. The app uses **Tesseract OCR** to convert the PDF pages to text.
3. The extracted text is processed by **OpenAI GPT** to format it into structured resume sections.
4. The app generates and displays an HTML version of the resume.
5. The user can download the HTML resume.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/thakurdishanttt/linkedin_pdf_to_html.git
cd linkedin_pdf_to_html

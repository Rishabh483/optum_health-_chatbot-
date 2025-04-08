# optum_health-_chatbot-
# Optum India Website Chatbot

A simple retrieval-augmented generation (RAG) chatbot that scrapes content from the Optum India website and provides answers to user questions based on that content.

## Overview

This project creates an AI-powered chatbot that:
1. Scrapes the Optum India website (https://www.optum.in/)
2. Indexes the content using a vector database (FAISS)
3. Uses Google's Gemini LLM to provide accurate responses to user queries
4. Presents information through a clean, user-friendly Streamlit interface

## Features

- **Automated Web Scraping**: Discovers and extracts content from Optum India's website
- **Smart Indexing**: Uses vector embeddings to organize and retrieve relevant information
- **Natural Language Understanding**: Powered by Google Gemini AI model
- **Interactive UI**: Easy-to-use chat interface built with Streamlit
- **Contextual Responses**: Provides information directly from Optum's official content

## Installation

### Prerequisites
- Python 3.8 or higher
- Google API key for Gemini

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/optum-india-chatbot.git
   cd optum-india-chatbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv chatbot
   # On Windows
   chatbot\Scripts\activate
   # On Unix or MacOS
   source chatbot/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. In your web browser, the Streamlit interface will load (typically at http://localhost:8501)

3. Click the "Initialize Chatbot" button in the sidebar to begin scraping the Optum India website

4. Once initialization is complete, you can ask questions in the chat interface

## Example Questions

- "What services does Optum India provide?"
- "Who are Optum's clients in India?"
- "What is Optum's approach to healthcare?"
- "Tell me about career opportunities at Optum India"
- "Where are Optum India's offices located?"

## Project Structure

```
optum-india-chatbot/
├── app.py              # Main application file
├── requirements.txt    # Requir

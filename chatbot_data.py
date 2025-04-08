import os
import streamlit as st
import google.generativeai as genai
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()

# Set up Google API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="YOUR_API_KEY_HERE")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class OptumChatbot:
    def __init__(self):
        self.db = None
        self.base_url = "https://www.optum.in"
        self.urls_to_scrape = [
            "https://www.optum.in/",
            "https://www.optum.in/solutions/global-operations.html",
            "https://www.optum.in/solutions/global-employee-benefits.html",
            "https://www.optum.in/thought-leadership.html?tagid=optum3%3Aen%2Fthought-leadership-topics%2Fai-and-automation",
            "https://www.optum.in/thought-leadership.html?tagid=optum3%3Aen%2Fthought-leadership-topics%2Fdata-and-analytics",
            "https://www.optum.in/thought-leadership.html?tagid=optum3%3Aen%2Fthought-leadership-topics%2Femployee-wellness",
            "https://www.optum.in/thought-leadership.html?tagid=optum3%3Aen%2Fthought-leadership-topics%2Fhealthcare-operation",
            "https://www.optum.in/thought-leadership.html?tagid=optum3%3Aen%2Fthought-leadership-topics%2Ftechnology",
            "https://www.optum.in/about.html",
            "https://www.optum.in/about/careers.html",
            "https://www.optum.in/about/news.html",
            "https://www.optum.in/about/events.html",
            "https://www.optum.in/about/inclusion-diversity.html",
            "https://www.optum.in/about/social-commitment.html",
            "https://www.optum.in/contact-us.html"
                ]
        self.scraped_urls = set()

    def get_links(self, url):
        """Extract links from a webpage that belong to Optum India domain"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Process relative links
                if href.startswith('/'):
                    full_url = f"{self.base_url}{href}"
                    links.append(full_url)
                # Process absolute links that belong to the same domain
                elif href.startswith(self.base_url):
                    links.append(href)
                    
            return links
        except Exception as e:
            st.error(f"Error extracting links from {url}: {str(e)}")
            return []

    def scrape_page(self, url):
        """Scrape a single page"""
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            self.scraped_urls.add(url)
            return docs
        except Exception as e:
            st.error(f"Error scraping {url}: {str(e)}")
            return []

    def discover_and_scrape(self, max_pages=15):
        """Discover and scrape pages from Optum India website"""
        all_docs = []
        pages_scraped = 0
        
        # First, scrape our initial set of important pages
        for url in self.urls_to_scrape:
            if pages_scraped >= max_pages:
                break
                
            if url not in self.scraped_urls:
                st.info(f"Scraping: {url}")
                docs = self.scrape_page(url)
                all_docs.extend(docs)
                pages_scraped += 1
                
                # Discover new links
                new_links = self.get_links(url)
                for link in new_links:
                    if link not in self.urls_to_scrape and "optum.in" in link:
                        if not any(exclude in link for exclude in [".pdf", ".jpg", ".png", "mailto:", "#"]):
                            self.urls_to_scrape.append(link)
        
        # Second, scrape any additional pages we discovered up to max_pages
        for url in self.urls_to_scrape:
            if pages_scraped >= max_pages:
                break
                
            if url not in self.scraped_urls:
                st.info(f"Scraping: {url}")
                docs = self.scrape_page(url)
                all_docs.extend(docs)
                pages_scraped += 1
        
        return all_docs

    def clean_text(self, text):
        """Clean the text by removing unnecessary content"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove common website elements
        text = re.sub(r'cookie policy.*?privacy policy', '', text, flags=re.IGNORECASE|re.DOTALL)
        return text.strip()

    def process_documents(self, docs):
        """Process and split the documents"""
        # Clean the documents
        for doc in docs:
            doc.page_content = self.clean_text(doc.page_content)
            
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        return splits

    def build_vector_db(self, splits):
        """Build the FAISS vector database"""
        self.db = FAISS.from_documents(splits, embeddings)
        return self.db

    def initialize(self):
        """Initialize the chatbot by scraping and indexing the website"""
        with st.spinner("Scraping Optum India website..."):
            progress_bar = st.progress(0)
            
            # Scrape the website
            docs = self.discover_and_scrape(max_pages=15)
            progress_bar.progress(0.5)
            
            # Process and index the documents
            if docs:
                splits = self.process_documents(docs)
                self.db = self.build_vector_db(splits)
                progress_bar.progress(1.0)
                
                st.success(f"Successfully scraped and indexed {len(docs)} pages from Optum India's website")
                return True
            else:
                st.error("Failed to scrape any documents")
                return False

    def answer_question(self, question):
        """Answer a question about Optum India"""
        if not self.db:
            return "Please initialize the chatbot first by clicking the 'Initialize Chatbot' button."
        
        # Get relevant documents
        relevant_docs = self.db.similarity_search(question, k=4)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Generate the answer
        prompt = f"""
        You are a helpful assistant for Optum India. Answer the following question based on the information provided.
        If the information isn't available in the context, say you don't have that specific information.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        response = llm.invoke(prompt).content
        return response
    
    
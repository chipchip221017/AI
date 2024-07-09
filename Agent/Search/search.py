import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Set your AI agent's name and version
AGENT_NAME = "Search-Agent"
AGENT_VERSION = "1.0"

# Set the Google Search URL
GOOGLE_SEARCH_URL = "https://www.google.com/search?q="

# Load environment variables from the .env file
load_dotenv()

# Set the email sending details
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
RECIPIENTS = ["linh.pham@sai-digital.com","chipchip221017@gmail.com"]

def google_search(query):
    # Define the user-agent to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Use requests library to send a GET request to Google search
    url = f"{GOOGLE_SEARCH_URL}{query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all("div", {"class": "g"})

def generate_email_text(query):
    # Use local LLaMA model via Ollama API to generate an email text based on the query
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    return response_json['message']['content']

def send_emails(recipients, subject, body):
    # Use smtplib library to send emails to the recipients
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipients, msg.as_string())

def main():
    # Define the query to search Google for
    query = "what is the latest trend of AI for e-commerce?"

    # Search Google for the query
    results = google_search(query)

    # Extract text from search results (simplified for demonstration)
    search_summary = " ".join([result.text for result in results[:10]])

    print("Generating...")
    # Generate an email text based on the search results
    email_text = generate_email_text(search_summary)

    # Send emails to the recipients with the generated email text
    send_emails(RECIPIENTS, "AI in ecommerce", email_text)

if __name__ == "__main__":
    main()


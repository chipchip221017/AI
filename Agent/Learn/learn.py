import ollama
import http.client as http_client
import logging

# Enable HTTP connection debug output
http_client.HTTPConnection.debuglevel = 1

# Configure logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

try:
    with open('sensitive_data.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    print()

    # Debug
    if data:
        print("File loaded successfully.")
    else:
        print("File loading failed or file is empty.")
    print()

    # Set the prompt for the first agent
    prompt_01 = f'{data} ### from this text, extract 3 interesting lessons about Large Language Models (LLMs).'
    print("<agent-01> Prompt: " + "extract 3 interesting lessons about Large Language Models")
    print()

    print("<agent-01> Generating a response...")
    print()

    # Get a response from Agent 1 - Extractor
    response_01 = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt_01
        }
    ])

    # Set the prompt for the second agent
    prompt_02 = f"{response_01['message']['content']} ### Explain this to the user in a simple, clear and engaging way."
    print("<agent-02> Prompt: " + prompt_02)
    print()

    print("<agent-02> Generating a response...")

    # Get a response from Agent 2 - Teacher
    response_02 = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt_02
        }
    ])

    # Print the final response from the second agent
    print("<agent-02> Response: " + response_02['message']['content'])

except UnicodeDecodeError as e:
    print(f"Error reading file: {e}")

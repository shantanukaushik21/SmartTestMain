import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Print to verify the API key is loaded
print("API Key:", os.getenv("OPENAI_API_KEY"))  # Debugging step
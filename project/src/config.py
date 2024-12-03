import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API Configuration
GOOGLE_API_KEY = "AIzaSyA8vOdpaecoLB4TNqMBZeXtKW5PwnmjhfY"

# Streamlit Configuration
PAGE_TITLE = "Text Analysis Suite"
PAGE_ICON = "📊"
LAYOUT = "centered"

# Analysis Configuration
DEFAULT_NUM_TOPICS = 3
SUPPORTED_FILE_TYPES = ['pdf', 'txt', 'docx']
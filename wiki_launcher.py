import requests
import webbrowser
import os
import time
import datetime

# Configuration
HISTORY_FILE = "seen_pages.txt"
LOG_FILE = "activity_log.txt"
API_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0"

# Helper function to find the file paths (ensures it works with the .bat/.vbs launchers)
def get_file_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

def log_message(message):
    """Writes the message to the log file instead of the console."""
    path = get_file_path(LOG_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # We open in "a" (append) mode so we don't delete old logs
    try:
        with open(path, "a", encoding="utf-8") as f:
            # Writing format: [Timestamp] Message
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass # If logging fails, we don't want to crash the app

def load_history():
    path = get_file_path(HISTORY_FILE)
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_to_history(page_id):
    path = get_file_path(HISTORY_FILE)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{page_id}\n")

def get_unique_page():
    seen_ids = load_history()
    
    log_message("--- New Execution ---")
    log_message("Searching for a unique article...")
    
    attempts = 0
    max_retries = 10 

    while attempts < max_retries:
        try:
            r = requests.get(API_URL, headers={'User-Agent': 'UniqueWikiBot/1.0'})
            data = r.json()
            page = data['query']['random'][0]
            
            page_id = str(page['id'])
            title = page['title']
            
            if page_id not in seen_ids:
                log_message(f"Found unique article: {title}")
                save_to_history(page_id)
                
                url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                webbrowser.open(url)
                return
            else:
                log_message(f"Duplicate encountered: {title}. Retrying...")
                attempts += 1
                
        except Exception as e:
            log_message(f"Error: {e}")
            time.sleep(2)
            attempts += 1
    
    log_message("Failed to find a unique article after multiple attempts.")

if __name__ == "__main__":
    get_unique_page()
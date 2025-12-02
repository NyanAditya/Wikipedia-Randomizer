import requests
import webbrowser
import os
import time
import datetime
import sys
import ctypes.wintypes

# --- CONFIGURATION ---
FOLDER_NAME = "Random-Wiki-Logs"
HISTORY_FILE = "seen_pages.txt"
LOG_FILE = "activity_log.txt"
API_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0"

def get_documents_folder():
    """
    Robust way to find the 'My Documents' folder on Windows.
    This works even if you use OneDrive or have moved the folder.
    """
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default path

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    
    return buf.value

def get_storage_path(filename):
    """
    Returns the full path to a file inside 'Documents/Random-Wiki-Logs'.
    Creates the folder if it doesn't exist.
    """
    # 1. Find the Documents folder (Works for OneDrive too)
    docs_dir = get_documents_folder()
    
    # 2. Define the target folder: ...\Documents\Random-Wiki-Logs
    log_dir = os.path.join(docs_dir, FOLDER_NAME)
    
    # 3. Create it if it doesn't exist
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError:
            pass # Fail silently if we can't create it
            
    return os.path.join(log_dir, filename)

def log_message(message):
    path = get_storage_path(LOG_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass

def load_history():
    path = get_storage_path(HISTORY_FILE)
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_to_history(page_id):
    path = get_storage_path(HISTORY_FILE)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{page_id}\n")

def get_unique_page():
    # Attempt to create/locate the folder immediately for debugging
    # (This ensures the folder exists before we try to read history)
    get_storage_path(HISTORY_FILE) 

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
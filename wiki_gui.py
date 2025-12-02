import requests
import webbrowser
import os
import time
import datetime
import sys
import ctypes.wintypes
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from urllib.parse import unquote

# --- CONFIGURATION ---
FOLDER_NAME = "Random-Wiki-Logs"
HISTORY_FILE = "seen_pages.txt"
LOG_FILE = "activity_log.txt"
API_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0"

# Refined Categories List
CATEGORIES = [
    "Any (Totally Random)",
    "Natural_sciences",
    "Applied_sciences",
    "Modern_philosophy",
    "World_history",
    "Human_geography",
    "Computer_science",
    "Astronomy",
    "Cognitive_psychology",
    "Visual_arts",
    "Literature"
]

# --- FOLDER & PATH LOGIC ---
def get_documents_folder():
    CSIDL_PERSONAL = 5       
    SHGFP_TYPE_CURRENT = 0   
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def get_storage_path(filename):
    docs_dir = get_documents_folder()
    log_dir = os.path.join(docs_dir, FOLDER_NAME)
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError:
            pass 
    return os.path.join(log_dir, filename)

# --- LOGGING ---
def log_message(message):
    path = get_storage_path(LOG_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{full_msg}\n")
    except Exception:
        pass

    try:
        log_widget.after(0, update_gui_log, full_msg)
    except NameError:
        pass

def update_gui_log(message):
    log_widget.config(state=tk.NORMAL)
    log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)
    log_widget.config(state=tk.DISABLED)

# --- HISTORY & STATS LOGIC ---
def load_history():
    path = get_storage_path(HISTORY_FILE)
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_to_history(identifier):
    path = get_storage_path(HISTORY_FILE)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{identifier}\n")

def calculate_stats():
    """Calculates Total and Today's count."""
    # 1. Total Count (Lines in seen_pages.txt)
    total_count = len(load_history())

    # 2. Today's Count (Parse activity_log.txt)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    daily_count = 0
    
    log_path = get_storage_path(LOG_FILE)
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                for line in f:
                    # Look for lines that start with today's date AND contain "SUCCESS"
                    if line.startswith(f"[{today_str}") and "SUCCESS:" in line:
                        daily_count += 1
        except Exception:
            pass

    return total_count, daily_count

def refresh_dashboard():
    """Updates the GUI labels with new stats."""
    total, daily = calculate_stats()
    lbl_total_val.config(text=str(total))
    lbl_today_val.config(text=str(daily))

# --- FETCHING LOGIC ---
def get_random_from_api():
    r = requests.get(API_URL, headers={'User-Agent': 'UniqueWikiBot/4.0'})
    data = r.json()
    page = data['query']['random'][0]
    return page['title'], f"https://en.wikipedia.org/wiki/{page['title'].replace(' ', '_')}"

def get_random_from_category(category):
    base_url = f"https://en.wikipedia.org/wiki/Special:RandomInCategory/{category}"
    r = requests.get(base_url, headers={'User-Agent': 'UniqueWikiBot/4.0'})
    final_url = r.url
    if "/wiki/" not in final_url:
        raise Exception("Failed to resolve category URL")
    title_part = final_url.split("/wiki/")[-1]
    clean_title = unquote(title_part).replace("_", " ")
    return clean_title, final_url

def fetch_logic_thread(selected_category):
    main_button.config(state=tk.DISABLED, text="Searching...")
    
    seen_items = load_history()
    log_message(f"--- Search: {selected_category} ---")
    
    attempts = 0
    max_retries = 20 
    found_unique = False

    while attempts < max_retries:
        try:
            log_message(f"Attempt {attempts+1}...")
            
            if selected_category.startswith("Any"):
                title, url = get_random_from_api()
            else:
                title, url = get_random_from_category(selected_category)
            
            # Filter non-articles
            if title.startswith(("Category:", "File:", "Talk:", "Portal:", "Template:", "Help:")):
                log_message(f"Skipped non-article: '{title}'")
                attempts += 1
                continue 

            if title not in seen_items:
                log_message(f"SUCCESS: Found unique: '{title}'")
                save_to_history(title)
                webbrowser.open(url)
                found_unique = True
                break
            else:
                log_message(f"Duplicate: '{title}'. Retrying...")
                attempts += 1
                time.sleep(0.5)
                
        except Exception as e:
            log_message(f"Error: {e}")
            time.sleep(1)
            attempts += 1
    
    if not found_unique:
        log_message("FAILURE: Could not find unique article.")
        messagebox.showerror("Oops", "Couldn't find a clean article. Try again!")

    # Update stats on the main thread
    window.after(0, refresh_dashboard)
    main_button.config(state=tk.NORMAL, text="🎲 Roll Again")

def on_button_click():
    cat = category_combo.get()
    threading.Thread(target=fetch_logic_thread, args=(cat,), daemon=True).start()

# --- GUI SETUP ---
def create_gui():
    global log_widget, main_button, category_combo, window, lbl_total_val, lbl_today_val

    window = tk.Tk()
    window.title("Infinite Wiki 4.0 📊")
    window.geometry("500x520")

    # Header
    header_frame = tk.Frame(window, pady=10)
    header_frame.pack(fill=tk.X)
    
    lbl = tk.Label(header_frame, text="Select Topic:", font=("Segoe UI", 10))
    lbl.pack()

    category_combo = ttk.Combobox(header_frame, values=CATEGORIES, state="readonly", font=("Segoe UI", 11), width=30)
    category_combo.current(0)
    category_combo.pack(pady=5)

    # Dashboard Frame (Stats)
    stats_frame = tk.Frame(window, bg="#f0f0f0", pady=10)
    stats_frame.pack(fill=tk.X, padx=20, pady=5)

    # Total Count Widget
# The Random Wiki Button 🎲
**Your Gateway to Infinite, Non-Repeating Knowledge.**

Tired of the same old feed? Want to learn something weird, wonderful, or completely random? 

Meet your new favorite desktop companion. One click drops you into a random Wikipedia article. The best part? **It remembers where you've been, so you never see the same page twice.**

## ✨ Why You Need This
* **Zero Repeats:** A smart memory ensures every click is a fresh discovery.
* **Invisible Magic:** Runs silently in the background. No ugly code windows.
* **Instant Access:** Open it from your Desktop, Taskbar, or Start Menu.
* **History Log:** It secretly keeps a diary of your journey in `activity_log.txt`.

---

## 🚀 Quick Start (3 Steps)

### 1. The Ingredients
Make sure you have **Python** installed. You just need one tiny library to make the magic happen. Open your terminal and run:
```bash
pip install requests
````

### 2\. The Setup

Put these three files in a folder (e.g., `Documents\WikiButton`):

1.  `wiki_launcher.py` (The Brains)
2.  `RunWiki.bat` (The Engine)
3.  `Launch.vbs` (The Silencer)

### 3\. The Launch

Double-click **`Launch.vbs`**.
Boom. Your browser opens a fresh Wiki page. 🧠

-----

## ⚡ PRO MODE: Add to Start Menu (Windows)

Want to feel like a hacker? Add this to your Windows Search so you can just hit the `Windows Key` and type **"Random Wiki"** to launch it.

1.  **Create the Key:** Right-click `Launch.vbs` and choose **Create Shortcut**.
2.  **Rename It:** Name the new shortcut **"Random Wiki"** (or whatever you like\!).
3.  **Open the Gate:** Press `Windows Key + R` on your keyboard, type `shell:programs`, and hit Enter.
4.  **Drop It In:** Drag your new "Random Wiki" shortcut into that folder.

**That's it\!** Now press the Windows key, search for "Random Wiki," and pin it to your Start Menu or Taskbar. Knowledge is now one click away.

-----

## 🔧 Troubleshooting (Just in case)

  * **Nothing happened?** Check the `activity_log.txt` file in the folder. It will tell you what went wrong.
  * **Saw a black window?** You probably clicked the `.bat` file. Make sure you use the `.vbs` file (or the shortcut pointing to it) for the invisible experience.
  * **Python error?**
    * `"It says 'python is not recognized'..."` This means Python isn't in your system PATH.

      * **Easy Fix:** Reinstall Python and check the box that says "Add Python to PATH."

      * **Pro Fix:** Edit RunWiki.bat and replace python with the full path to your python.exe (e.g., C:\Python39\python.exe).
    * `"I want to use a specific Python version!"` You can! Just edit RunWiki.bat.

      * Change python to py -3.11 (to use the Python Launcher).

      * Or paste the direct path to your specific environment.

Happy Learning\! 🌍

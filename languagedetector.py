# ---------------- Libraries ----------------
import tkinter as tk
from tkinter import messagebox
import requests

# ---------------- Language Dictionary ----------------
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

# ---------------- Global History ----------------
history = []

# ---------------- Translation Function ----------------
def translate_text(text, src_lang, dest_lang):
    try:
        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "sl": src_lang,
            "tl": dest_lang,
            "dt": "t",
            "q": text
        }

        response = requests.get(url, params=params)
        result = response.json()

        translated = result[0][0][0]
        return translated

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", "Translation Failed!")
        return ""

# ---------------- GUI Window ----------------
def create_gui():
    window = tk.Tk()
    window.title("Advanced Language Translator")
    window.geometry("600x550")
    return window

# ---------------- GUI Components ----------------
def build_gui(window):
    global input_text, output_text, src_var, dest_var

    # Input
    tk.Label(window, text="Enter Text:", font=("Arial", 12)).pack(pady=5)
    input_text = tk.Text(window, height=5, width=50)
    input_text.pack(pady=5)

    # 🔹 SOURCE LANGUAGE
    tk.Label(window, text="From:", font=("Arial", 12)).pack()
    src_var = tk.StringVar(window)
    src_var.set("English")
    tk.OptionMenu(window, src_var, *LANGUAGES.keys()).pack(pady=5)

    # 🔹 TARGET LANGUAGE
    tk.Label(window, text="To:", font=("Arial", 12)).pack()
    dest_var = tk.StringVar(window)
    dest_var.set("Hindi")
    tk.OptionMenu(window, dest_var, *LANGUAGES.keys()).pack(pady=5)

    # 🔥 -------- FULL DYNAMIC SWAP --------
    def swap_languages():
        src = src_var.get()
        dest = dest_var.get()

        src_var.set(dest)
        dest_var.set(src)

    tk.Button(window, text="Swap Languages 🔄",
              command=swap_languages,
              bg="orange", fg="white").pack(pady=5)

    # -------- TRANSLATE BUTTON --------
    def on_translate():
        text = input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text!")
            return

        src_code = LANGUAGES[src_var.get()]
        dest_code = LANGUAGES[dest_var.get()]

        translated = translate_text(text, src_code, dest_code)

        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", translated)

        history.append((text, translated))

    tk.Button(window, text="Translate", command=on_translate,
              bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

    # Output
    tk.Label(window, text="Translated Text:", font=("Arial", 12)).pack(pady=5)
    output_text = tk.Text(window, height=5, width=50)
    output_text.pack(pady=5)

    # -------- HISTORY BUTTON --------
    def view_history():
        if not history:
            messagebox.showinfo("History", "No translations yet.")
            return

        hist_window = tk.Toplevel(window)
        hist_window.title("History")

        for i, (orig, trans) in enumerate(history, start=1):
            tk.Label(hist_window,
                     text=f"{i}. {orig} → {trans}",
                     wraplength=400,
                     justify="left").pack(pady=2)

    tk.Button(window, text="View History", command=view_history,
              bg="purple", fg="white").pack(pady=5)

    # -------- COPY BUTTON --------
    def copy_text():
        text = output_text.get("1.0", tk.END).strip()
        if text:
            window.clipboard_clear()
            window.clipboard_append(text)
            messagebox.showinfo("Copied", "Text copied!")

    tk.Button(window, text="Copy", command=copy_text,
              bg="blue", fg="white").pack(pady=5)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    window = create_gui()
    build_gui(window)
    window.mainloop()

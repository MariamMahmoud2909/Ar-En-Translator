from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from translator import *
import sys, os

sys.stdout.reconfigure(encoding='utf-8')

def on_translate():
    ar = input_box.get("1.0", tk.END).strip()
    if not ar:
        messagebox.showwarning("Empty input", "Please enter Arabic text.")
        return
    translate_btn.config(state="disabled")
    try:
        en = translate_long_text(ar, chunk_size=300, batch_size=6)
    except Exception as e:
        en = f"Error: {e}"
    finally:
        translate_btn.config(state="normal")

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, en)

    src_count.set(f"Source chars: {len(ar)}")
    tgt_count.set(f"Translated chars: {len(en)}")

def on_copy():
    text = output_box.get("1.0", tk.END)
    if text.strip():
        root.clipboard_clear()
        root.clipboard_append(text)
    else:
        messagebox.showwarning("Empty", "No translated text to copy.")

def on_open_file():
    path = filedialog.askopenfilename(title="Open text file",filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if path:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, data)
            # update source char count
            src_count.set(f"Source chars: {len(data)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

root = tk.Tk()
root.title("Arabic → English Translator")
root.geometry("900x450")
root.configure(bg="white")

ttk.Label(root, text="Arabic → English Translator", font=("Arial", 16, "bold"), foreground="#004080").pack(pady=8)

main = tk.Frame(root, bg="white")
main.pack(fill="both", expand=True, padx=10, pady=5)

left = tk.Frame(main, bg="white")
left.pack(side="left", fill="both", expand=True)

tk.Label(left, text="Arabic", font=("Arial", 12), fg="#004080", bg="white").pack(anchor="w")
input_box = tk.Text(left, height=8, bg="#f0f8ff", font=("Arial", 11), wrap="word")
input_box.pack(fill="both", expand=True)

src_count = tk.StringVar(value="Source chars: 0")
tk.Label(left, textvariable=src_count, font=("Arial", 10), fg="#333", bg="white").pack(anchor="e", pady=(2,0))

center = tk.Frame(main, bg="white")
center.pack(side="left", padx=10)

translate_btn = tk.Button(center, text="Translate Text", command=on_translate,font=("Arial", 11, "bold"), bg="#0066cc", fg="white", activebackground="#005bb5", padx=20, pady=10, relief="flat", cursor="hand2")
translate_btn.pack(pady=(0,10))

open_btn = tk.Button(center,text="Translate File",command=on_open_file,font=("Arial", 11, "bold"),bg="#0066cc", fg="white",relief="flat", cursor="hand2", padx=20, pady=10)
open_btn.pack(pady=(0,10))

right = tk.Frame(main, bg="white")
right.pack(side="left", fill="both", expand=True)

tk.Label(right, text="English", font=("Arial", 12), fg="#004080", bg="white").pack(anchor="w")
output_box = tk.Text(right, height=8, bg="#f0f8ff", font=("Arial", 11), wrap="word")
output_box.pack(fill="both", expand=True)

btn_copy = tk.Button(right, text="Copy Text", command=on_copy, bg="#0066cc", fg="white", relief="flat", cursor="hand2")
btn_copy.pack(anchor="ne", pady=(5,0))

tgt_count = tk.StringVar(value="Translated chars: 0")
tk.Label(right, textvariable=tgt_count, font=("Arial", 10), fg="#333", bg="white").pack(anchor="e", pady=(2,0))

root.mainloop()
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from openai import AzureOpenAI
import os

from dotenv import load_dotenv
load_dotenv()

class DocumentUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Uploader")
        
        self.text_display = tk.Text(root, wrap=tk.WORD, height=10)
        self.text_display.pack(expand=True, fill="both")
        
        self.summary_display = tk.Text(root, wrap=tk.WORD, height=5, bg="#f0f0f0")
        self.summary_display.pack(expand=True, fill="both")
        
        self.translation_display = tk.Text(root, wrap=tk.WORD, height=5, bg="#e0f7fa")
        self.translation_display.pack(expand=True, fill="both")
        
        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()
        
        self.summarize_button = tk.Button(root, text="Summarize", command=self.summarize_text)
        self.summarize_button.pack()
        
        self.translate_button = tk.Button(root, text="Translate", command=self.translate_text)
        self.translate_button.pack()
        
        self.language_var = tk.StringVar(value="en")
        self.language_dropdown = tk.OptionMenu(root, self.language_var, "en", "es", "fr")
        self.language_dropdown.pack()
        
        self.text_content = ""
        self.azure_client = AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), api_version=os.getenv("AZURE_OPENAI_API_VERSION"))
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
        if not file_path:
            return
        
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_content = file.read()
        elif file_path.endswith(".pdf"):
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                self.text_content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", self.text_content)
    
    def summarize_text(self):
        target_lang = self.language_var.get()

        if not self.text_content:
            messagebox.showerror("Error", "No content to summarize")
            return
        
        response = self.azure_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are an expert summarizer. Provide a concise summary of the given text in the selected lannguage {target_lang}"},
                {"role": "user", "content": self.text_content}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        self.summary_display.delete("1.0", tk.END)
        self.summary_display.insert("1.0", summary)
    
    def translate_text(self):
        target_lang = self.language_var.get()
        if not self.text_content:
            messagebox.showerror("Error", "No content to translate")
            return
        
        response = self.azure_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text into {target_lang}."},
                {"role": "user", "content": self.text_content}
            ],
            max_tokens=200
        )
        translation = response.choices[0].message.content.strip()
        self.translation_display.delete("1.0", tk.END)
        self.translation_display.insert("1.0", translation)

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentUploader(root)
    root.mainloop()
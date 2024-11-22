import os
import io
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
import json

# Créer le dossier de stockage si nécessaire
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

def convert_pdf_to_text():
    """
    Lit un PDF depuis le système local, extrait le texte et l'enregistre dans vault.txt.
    """
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text() + " "
            process_text_and_save(text)
            # Copier le fichier PDF dans storage
            save_to_storage(file_path)

def save_to_storage(file_path):
    """
    Copie un fichier dans le dossier de stockage.
    """
    filename = os.path.basename(file_path)
    destination = os.path.join(STORAGE_DIR, filename)
    with open(file_path, 'rb') as src_file, open(destination, 'wb') as dest_file:
        dest_file.write(src_file.read())
    print(f"Fichier {filename} copié dans {STORAGE_DIR}.")

def upload_txtfile():
    """
    Lit un fichier texte depuis le système local, nettoie le texte et l'ajoute à vault.txt.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as txt_file:
            text = txt_file.read()
            process_text_and_save(text)
            save_to_storage(file_path)

def upload_jsonfile():
    """
    Lit un fichier JSON depuis le système local, aplati les données et les ajoute à vault.txt.
    """
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            text = json.dumps(data, ensure_ascii=False)
            process_text_and_save(text)
            save_to_storage(file_path)

def process_text_and_save(text):
    """
    Divise le texte en chunks et les ajoute à vault.txt.
    :param text: Texte brut extrait d'un fichier.
    """
    # Normaliser le texte
    text = re.sub(r'\s+', ' ', text).strip()

    # Découper en phrases et chunks
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 pour l'espace
            current_chunk += (sentence + " ").strip()
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk)

    # Écrire les chunks dans vault.txt
    with open("vault.txt", "a", encoding="utf-8") as vault_file:
        for chunk in chunks:
            vault_file.write(chunk.strip() + "\n")
    print(f"Le texte a été ajouté à vault.txt avec chaque chunk sur une ligne.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Upload .pdf, .txt, or .json")

# Bouton pour télécharger un PDF
pdf_button = tk.Button(root, text="Upload PDF", command=convert_pdf_to_text)
pdf_button.pack(pady=10)

# Bouton pour télécharger un fichier texte
txt_button = tk.Button(root, text="Upload Text File", command=upload_txtfile)
txt_button.pack(pady=10)

# Bouton pour télécharger un fichier JSON
json_button = tk.Button(root, text="Upload JSON File", command=upload_jsonfile)
json_button.pack(pady=10)

# Lancer la boucle principale de l'application
root.mainloop()

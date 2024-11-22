# Local RAG with Ollama + Email RAG

### Installation

1. `git clone https://github.com/AllAboutAI-YT/easy-local-rag.git`
2. `cd dir`
3. `pip install -r requirements.txt`
4. Installez Ollama : [https://ollama.com/download](https://ollama.com/download)
5. `ollama pull llama3.2`

### Fonctionnalités
- Les fichiers sont **stockés localement** dans un dossier appelé `storage`.
- Aucun service S3 n'est utilisé pour éviter des coûts supplémentaires ou inattendus.
- Tous les fichiers (.pdf, .txt, .json) sont copiés localement après traitement.
- Le texte extrait est divisé en chunks et sauvegardé dans `vault.txt`.

### Lancement : 

6. `python upload.py`
7. `python localrag.py`

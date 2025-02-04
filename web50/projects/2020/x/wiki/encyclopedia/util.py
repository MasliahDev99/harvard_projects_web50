import re
import os,shutil
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def delete_entry(title):
    """
    Deletes an encyclopedia entry by its title. If no such
    entry exists.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
   


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    
def validate_markdown(content):
    """
    Valida si el contenido proporcionado es válido Markdown.
    Retorna True si es válido, lanza una excepción si no.
    """
    markdown = Markdown()
    try:
        markdown.convert(content)
        return True
    except Exception as e:
        raise ValueError("Invalid Markdown format")
    
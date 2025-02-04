# WIKI  Encyclopedia Project 1 - Harvard CS50's Web Programming with Python and JavaScript

This is a Django project that implements an online encyclopedia called "wiki". The application allows users to view, search, create, edit, and navigate encyclopedia entries written in Markdown.


## Features
- **Entry Page**: View the content of a specific encyclopedia entry.
- **Index Page**: List all available entries in the encyclopedia.
- **Search**: Allows searching for entries by title or content.
- **New Page**: Create new encyclopedia entries.
- **Edit Page**: Edit the content of existing entries.
- **Random Page**: Navigate to a random encyclopedia entry.
- **Markdown to HTML Conversion**: Converts Markdown content to HTML for display.


## Demonstration
Watch the demonstration video here: [Demo Video](https://youtu.be/e05CgtHqEmY)

## Installation

1. **Clone the repository**:
    ```bash
    git clone <REPOSITORY_URL>
    cd wiki
2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Start the development server:
    ```bash
    python manage.py runserver
    ```


## Usage
- Navigation: Use the sidebar to navigate between different features of the encyclopedia.
- Search: Use the search bar to find entries by title or content.
- Create/Edit Entries: Use the "New Page" and "Edit Page" features to create or modify entries.

## Project Structure
- `wiki/`: Main project directory.
- `wiki/encyclopedia/`: Application directory.
- `wiki/templates/`: HTML templates.
- `wiki/static/`: Static files (CSS, JavaScript).
- `wiki/entries/`: Markdown encyclopedia entries.
- `wiki/requirements.txt`: List of project dependencies.
- `wiki/manage.py`: Django management script. 


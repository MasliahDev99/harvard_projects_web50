
# Mundo Campero 

---
## Indice 
- [Description](#description)
- [Project Structure](#project-structure)
- [Project Preview](#project-preview)
- [Project Requirements](#project-requirements)
- [Use Cases](#use-cases)
- [Design Documentation](#design-documentation)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Next Steps](#next-steps)
- [Bugs Found and Fixed](#bugs-found-and-fixed)


## Description


### What is Mundo Campero?

Mundo campero is an comprehensive web application for managing sheep herds,designed to simplify agricultural activities related to sheep breeding and management. This project was developed as part of **CS50’s Web Programming with Python and JavaScript** at Harvard, tackling a challenge beyond the examples provided in the course.

The sheep managment is a part of the beginning of something bigger which aims to integrate agriculture activities into single application.

### Why Choose This Topic?

1.	Distinctiveness: The topic is unique and goes beyond the common projects typically seen in the course.
2.	Challenge: It presents significant technical challenges, such as dynamic data fetching through custom local APIs and designing a modern, responsive user interface.
3.	Personal Connection: My family’s involvement in the agricultural sector inspired me to create a practical and impactful tool for this field. 

### Distinctiveness and Complexity

### Why Mundo campero is distinctive?

Mundo Campero is distinctive because it combines:
   * A non-traditional theme (sheep herd management) with real-world applicability.
   * A complex backend that includes local APIs for efficient and dynamic data communication between the frontend and backend.


### Why is Mundo Campero Complex?

The project involves:
 *	Designing and consuming custom APIs for CRUD operations on sheep and sales records.
 *	Implementing a dashboard with dynamic graphs and statistics for data visualization.
 *	Developing a robust authentication system with role-based access control.
 *	Combining frontend and backend technologies to deliver a seamless experience.
---

## Project structure
[Back to Indice](#indice)
<details>
<summary>Click to view directory structure</summary>

```plaintext

.
├── Especificaciones.md
├── MundoCampero
│   ├── MundoCampero
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   ├── ganaderia
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms
│   │   │   ├── __init__.py
│   │   │   └── venta_forms.py
│   │   ├── media
│   │   │   ├── archivo_1.xlsx
│   │   │   ├── jr.png
│   │   │   └── pepitos.xlsx
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── static
│   │   │   └── ganaderia
│   │   │       ├── css
│   │   │       │   ├── ovinoHub.css
│   │   │       │   └── styles.css
│   │   │       ├── images
│   │   │       │   ├── eficiencia.jpg
│   │   │       │   ├── gc.png
│   │   │       │   ├── genealogia.jpg
│   │   │       │   └── reporte.jpg
│   │   │       └── js
│   │   │           ├── analisis_ovinos.js
│   │   │           ├── analisis_ventas.js
│   │   │           ├── dashboard.js
│   │   │           ├── ovejas.js
│   │   │           ├── ovinoHub.js
│   │   │           ├── planteletas.js
│   │   │           ├── tabla_ventas.js
│   │   │           └── ventas.js
│   │   ├── templates
│   │   │   └── ganaderia
│   │   │       ├── OvinoHub.html
│   │   │       ├── components
│   │   │       │   ├── botones_accion.html
│   │   │       │   ├── dashboard
│   │   │       │   │   ├── DatosOvinos.html
│   │   │       │   │   ├── DatosVentas.html
│   │   │       │   │   ├── ranking.html
│   │   │       │   │   ├── resumen_ovino.html
│   │   │       │   │   └── resumen_venta.html
│   │   │       │   ├── modals
│   │   │       │   │   ├── agregar_ovino.html
│   │   │       │   │   ├── agregar_venta.html
│   │   │       │   │   ├── descargas.html
│   │   │       │   │   ├── editar_ovino.html
│   │   │       │   │   └── eliminar_ovino.html
│   │   │       │   ├── navbar.html
│   │   │       │   ├── registro_ovino.html
│   │   │       │   └── registro_venta.html
│   │   │       ├── dashboard.html
│   │   │       ├── detalle.html
│   │   │       ├── detalleVenta.html
│   │   │       ├── index.html
│   │   │       ├── layout.html
│   │   │       ├── login.html
│   │   │       ├── main.html
│   │   │       ├── ovejas.html
│   │   │       ├── planteletas.html
│   │   │       ├── register.html
│   │   │       └── ventas.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   ├── utils_descargas.py
│   │   └── views.py
│   ├── manage.py
│   └── requirements.txt
├── README.md
├── directory_structure.txt
└── imagenes_proyecto
    ├── captura_index1.png
    ├── captura_index2.png
    ├── captura_index3.png
    ├── dashboard.png
    ├── dashboard1.png
    ├── detail.png
    ├── estructura_app1.png
    ├── estructura_app2.png
    ├── login.png
    ├── ovinoHub.png
    ├── ovinoHub2.png
    ├── registro.png
    ├── registro_ovino.png
    ├── registro_ovino1.png
    ├── registro_venta.png
    └── statstic.png



```
</details>






### Directory Overview

#### **Root-Level Files**
- **`utils.py`**: Contains utility functions used throughout the project to streamline operations or handle repetitive tasks.
- **`urls.py`**: Defines the URL routing for the application, mapping endpoints to their respective views.
- **`views.py`**: Houses the core logic for handling HTTP requests and responses.
- **`models.py`**: Defines the database models, outlining the structure of the application's data.
- **`admin.py`**: Configures how models are displayed and managed in the Django Admin interface.
- **`serializers.py`**: Converts complex data types (e.g., models) into JSON for API consumption and vice versa.
- **`signals.py`**: Manages Django signals for automating certain actions when specific events occur (e.g., saving a model).
- **`utils_descargas.py`**: Provides utility functions for handling file downloads and related operations.

---

#### **Template Structure**
- **`/templates/ganaderia/`**: Root folder for all HTML templates related to the "ganaderia" module.  
- **`/templates/ganaderia/components/`**: Contains reusable UI components to ensure modularity and reduce code repetition.
- **`/templates/ganaderia/components/modals/`**: Templates for modal dialogs used throughout the application.
- **`/templates/ganaderia/components/dashboard/`**: Specific components for the dashboard, such as widgets and statistics displays.

---


## Project Preview

### Application Screenshots

#### Home Page
![Home Page](./imagenes_proyecto/captura_index1.png)
![Home Page2](./imagenes_proyecto/captura_index2.png)
![Home Page3](./imagenes_proyecto/captura_index3.png)

### Ovino Hub
![ovino hub](./imagenes_proyecto/ovinoHub.png)
![ovino hub1](./imagenes_proyecto/ovinoHub2.png)

#### Dashboard
![Dashboard](./imagenes_proyecto/dashboard.png)

### Sheep managment
![sheep managment](./imagenes_proyecto/registro_ovino.png)
![sheep managment](./imagenes_proyecto/registro_ovino1.png)
![sheep detail](./imagenes_proyecto/detail.png)

### Sales
![sales1](./imagenes_proyecto/registro_venta.png)
![dashboard1](./imagenes_proyecto/dashboard1.png)
#### Statistic 
![Statistics Dashboard](./imagenes_proyecto/statstic.png)

### Video Tutorial
Watch the tutorial embedded in the [homepage](http://127.0.0.1:8000) or view it directly on [YouTube](https://youtube.com/embed/qXgDbXibWo8).

[Back to Indice](#indice)

---




## Project Requirements

### General Objectives
Develop an application capable of:  
- Managing detailed records of a sheep herd, including general data, genealogy, status, and transactions.  
- Providing valuable statistics and analysis for herd management.  
- Implementing a simple and accessible interface for users with varying levels of technical expertise.  

### Functional Requirements

1. **Sheep Management:**  
   - Record data such as breed, weight, gender, status (active, sold, deceased), and genealogy.  
   - Update the status of sheep, such as registering sales or deaths.  
   - Edit and delete existing records.  

2. **Sales Management:**  
   - Record individual, batch, or slaughterhouse sales.  
   - Register sale values and calculate transaction statistics.  

3. **Analytics and Statistics:**  
   - Display herd statistics (total number of sheep, status, predominant breeds, etc.).  
   - Generate graphs to facilitate data visualization.  

4. **Local API Consumption:**  
   - Create APIs to allow the frontend to dynamically fetch data from the backend efficiently.  

5. **Access and Authentication:**  
   - Implement a user registration and authentication system.  
   - Restrict access to certain functionalities based on user roles.  

6. **Usability:**  
   - Design a responsive, user-friendly interface.  

### Non-Functional Requirements

- **Scalability:** The system must be scalable to support a larger database in the future.  
- **Efficiency:** Minimize response times in API consumption.  
- **Security:** Protect user data using encryption and secure practices.  

[Back to Indice](#indice)

---

## Use Cases

### Use Case: Register a Sheep
1. **Primary Actor:** Registered user.  
2. **Main Flow:**  
   - The user accesses the sheep registration form.  
   - Enters required data (breed, weight, gender, status, etc.).  
   - Saves the record.  
3. **Expected Outcome:** The sheep is successfully registered and appears in the list of active sheep.  

### Use Case: Register a Sale
1. **Primary Actor:** Registered user.  
2. **Main Flow:**  
   - The user selects sheep to sell.  
   - Enters sale information (type of sale, value, date).  
   - Saves the record.  
3. **Expected Outcome:** The selected sheep are marked as "sold," and the sale is successfully recorded.  

### Use Case: Generate Statistics
1. **Primary Actor:** Registered user.  
2. **Main Flow:**  
   - The user accesses the analytics section.  
   - Views dynamically generated graphs and statistics.  
3. **Expected Outcome:** The user obtains valuable insights for herd management.  

[Back to Indice](#indice)
---

## Design Documentation

### Architecture Diagram

The application follows an **MVC** (Model-View-Controller) architecture:  

- **Frontend:** HTML, CSS, JavaScript, and Bootstrap.  
- **Backend:** Django + Django REST Framework to handle server logic and APIs.  
- **Database:** SQLite (for development) with plans to migrate to PostgreSQL.  

### Local APIs

- **Sheep Endpoint:**  
  - `GET /api/ovejas/`: Lists all sheep.  
 
  

- **Sales Endpoint:**  
  - `GET /api/ventas/`: Lists all recorded sales.  

[Back to Indice](#indice) 

---

## Technologies Used

## Technologies Used
[Back to Indice](#indice)

- **Backend:** Django + Django REST Framework + Python. 
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)   
-  **Frontend:** HTML, CSS, JavaScript, Bootstrap. 
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)  
- **Database:** SQLite (development), PostgreSQL (future).  
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) 
- **Development Tools:** VS Code, Git, and GitHub.  
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)  





---

## Installation

### Requirements
- Python 3.9+  
- Django 4.0+  
- Dependencies listed in `requirements.txt`.  

### Installation Steps:
1. Clone the repository:  
   ```bash
   git clone https://github.com/your_username/tu-ovino.git
   cd tu-ovino
2. Create a virtual enviroment:

    ```bash
    python3 -m venv  env
    source env/bin/activate  # On Windows: .\env\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
  
4. Apply migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrations

5. Start server:
    ```bash
    python3 manage.py runserver

6. Clean the database(optional):
   * Flush the database:
   ```bash
   python3 manage.py flush
   ```
   * This command will remove all data from the database.You will be prompted to confirm action.
   * Remove the database file:
   ```bash
      rm -rf db.sqlite3
   ```
   * This command delete the SQLite databse file
   * Clear migration files:
   ```bash
      find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
      find . -path "*/migrations/*.pyc" -delete
   ```
   These commands remove all migration files except for the `__init__.py` file.
   
 #### Access the application at http://127.0.0.1:8000.
[Back to Indice](#indice)


---

## Next steps

1.	Implement advanced analytics using language models (LLMs).
2.	Create a system for bulk sheep registration via Excel files.
3.	Add options to manage documents (vaccination records, life histories).
4.	Enhance data export features in Excel and PDF formats.
5.	Expand local API functionalities.

[Back to Indice](#indice)

## Bugs Found and Fixed

1. **Missing `RP` for Non-Pedigree Sheep**  
   When adding a sheep with a purity different from "pedigree," errors occurred because the `RP` field was not provided.

2. **Sales Registration for Sheep Without `RP`**  
   When registering a sale for a sheep without an `RP`, the following issues occurred:
   - Sheep without an `RP` couldn't be selected.
   - JavaScript failed to update the data properly.  

   **Fixes:**
   - Updated the local API to include the `ID` field, as all sheep have this field, while not all have an `RP`.
   - Modified the backend view to filter sheep by `ID` instead of `RP`.  
   Previously, filtering by `RP` caused errors when sheep without an `RP` were included in a sale. Using `ID` resolved this issue entirely.


[Back to Indice](#indice)


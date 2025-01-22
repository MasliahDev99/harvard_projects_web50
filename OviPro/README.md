# Mundo Campero 

---

## Description

### What is Mundo Campero?

Mundo campero is an comprehensive web application for managing sheep herds,designed to simplify agricultural activities related to sheep breeding and management. This project was developed as part of **CS50’s Web Programming with Python and JavaScript** at Harvard, tackling a challenge beyond the examples provided in the course.

The sheep managment is a part of the beginning of something bigger which aims to integrate agriculture activities into single application.

### Why Choose This Topic?

1. It’s a unique and challenging theme compared to common course projects.  
2. It presents technical challenges, such as integrating local APIs, dynamic data fetching, and a modern interface.  
3. My family has ties to the agricultural sector, which inspired me to create a practical and helpful tool for this field.  

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
Watch the tutorial embedded in the [homepage](http://127.0.0.1:8000) or view it directly on [YouTube](https://youtu.be/h0gDXW7UJfA).

---
## Project structure
![s1](./imagenes_proyecto/estructura_app1.png)
![s2](./imagenes_proyecto/estructura_app2.png)

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
 

---

## Technologies Used

- **Backend:** Django + Django REST Framework + Python.  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap.  
- **Database:** SQLite (development), PostgreSQL (future).  
- **Development Tools:** VS Code, Git, and GitHub.  

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
   python3 manage.py migrations

5. Start server:
    ```bash
    python3 manage.py runserver

 #### Access the application at http://127.0.0.1:8000.
---

## Next steps

1.	Implement advanced analytics using language models (LLMs).
2.	Create a system for bulk sheep registration via Excel files.
3.	Add options to manage documents (vaccination records, life histories).
4.	Enhance data export features in Excel and PDF formats.
5.	Expand local API functionalities.






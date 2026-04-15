# Delivery-App Reviews (iMeals)

> **College Project - Database I** > A web-based dashboard and system designed for storing, inserting, and creating valuable insights for a fictitious takeaway delivery app called **iMeals**. 

## 📖 About The Project

This project was developed to practice relational database modeling, complex SQL queries, and database transaction management. It serves as the backend and internal dashboard for a delivery app's review and rating system. 

Instead of a simple 5-star rating, this system allows administrators to register dynamic questions targeted at specific entities (the delivery driver, the restaurant, the app itself, or specific items in the order). Users can then evaluate their completed orders, and the system securely processes these complex, multi-target reviews using atomic database transactions.

## ✨ Key Features

* **Dynamic Review System:** Administrators can register specific evaluation questions aimed at different targets (`entregador`, `estabelecimento`, `aplicativo`, `item_do_pedido`).
* **Order Management:** View, list, and track the status of customer orders.
* **Atomic Transactions:** Review submissions are handled via strict Data Access Objects (DAOs) to ensure that if one part of a complex review fails to save, the entire transaction rolls back, preventing orphaned data.
* **Massive Data Seeding:** The project includes a robust suite of Python scripts utilizing the `Faker` library to populate the database with realistic data. It can generate thousands of fake customers, delivery drivers, restaurants (cafes, pizzerias, burger joints), and even simulate biased reviews to generate analytical insights.
* **MVC-inspired Architecture:** Clean separation of concerns using Models, Data Access Objects (DAOs), and Flask Routes.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** PostgreSQL (Interfacing via `psycopg`)
* **Frontend:** HTML5, CSS3 (Bootstrap), Jinja2 Templates, Custom SVGs
* **Data Generation:** `Faker` (for Python)

## 🗄️ Domain Entities (Models)
The PostgreSQL database is heavily normalized and interacts with the following Python models:
* **Users:** `Cliente` (Customer), `Entregador` (Delivery Person)
* **Commerce:** `Estabelecimento` (Restaurant), `Categoria` (Category), `Classe_produto` (Product Class), `Item`
* **Operations:** `Pedido` (Order), `Item_pedido` (Order Item)
* **Insights:** `Avaliacao` (Evaluation), `Pergunta` (Question), `Resposta` (Answer)

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.x and PostgreSQL installed on your machine.

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/delivery-app-reviews.git](https://github.com/yourusername/delivery-app-reviews.git)
cd delivery-app-reviews
```
### 2. Database Setup

Create a PostgreSQL database named `imeals`.
By default, the application connects to a local database using the URL inside `app/dao/base.py`:
`postgresql://postgres:yourpassword@localhost/imeals`

(Note: Make sure to update the DB_URL in `app/dao/base.py` with your actual local PostgreSQL credentials before running).

### 3. Install Dependencies

Install the required python packages (e.g., inside a virtual environment):

```bash
pip install flask psycopg faker
```

### 4. Populate the Database (Data Seeding)

To properly test the dashboard and insights, run the provided load scripts in the scripts/ directory to generate dummy data:

```bash
python scripts/carga_clientes.py
python scripts/carga_entregadores.py
python scripts/carga_estabelecimentos/carga_avaliacoes.py
# Run other scripts as needed (mass orders, biased evaluations, etc.)
```

### 5. Run the Application

Start the Flask development server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000/`

## Project Structure

```
├── app/
│   ├── dao/             # Data Access Objects (SQL queries and DB connection)
│   ├── models/          # Domain classes (Cliente, Pedido, Avaliacao, etc.)
│   ├── routes/          # Flask Blueprints (Controllers)
│   ├── static/          # SVG Icons, Bootstrap CSS
│   └── templates/       # HTML Jinja2 Templates
├── scripts/             # Data seeding scripts (Faker) for DB population
├── run.py               # Application entry point
└── README.md
```

## Author

Developed by Guilherme N Braga for the Database I course.

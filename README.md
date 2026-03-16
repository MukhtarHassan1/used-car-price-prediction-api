# FastAPI Product CRUD API

This project implements a **RESTful API using FastAPI** to manage product data with full CRUD functionality.

It demonstrates backend API development in Python using **FastAPI, Pydantic, and modular project architecture**.

---

## Project Overview

The API allows users to:

* Create new products
* Retrieve all products
* Update product details
* Delete products
* Filter and sort products
* Apply pagination

The system follows a **service-based architecture** separating business logic from API routes.

---

## Technologies Used

* Python
* FastAPI
* Pydantic
* REST API Design
* JSON Data Storage

---

## API Endpoints

### Get All Products

```
GET /products
```

Supports:

* filtering
* sorting
* pagination

---

### Create Product

```
POST /products
```

Example Request Body:

```
{
  "name": "Laptop",
  "price": 1200,
  "sku": "ABC123"
}
```

---

### Update Product

```
PUT /products/{id}
```

Updates an existing product.

---

### Delete Product

```
DELETE /products/{id}
```

Removes a product from the system.

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/fastapi-product-crud-api.git
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run the API Server

```
uvicorn app.main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Key Learning Outcomes

* Designing RESTful APIs with FastAPI
* Data validation using Pydantic
* Modular backend architecture
* Implementing CRUD operations
* Handling filtering, sorting, and pagination

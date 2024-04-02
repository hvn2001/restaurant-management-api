# Restaurant Management API

This is a Flask-based RESTful API for managing restaurant orders and analyzing revenue data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/hvn2001/restaurant-management-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd restaurant-management-api
    ```

3. Install dependencies:

## Usage

1. Move the validated CSV file to the data folder.

2. Run the Flask application:

    ```bash
    python app.py
    ```

3. Once the server is running, you can access the API endpoints.

## Endpoints

- `/api/orders`: Get all orders.
- `/api/orders/<order_id>`: Get details of a specific order.
- `/api/items/<n>`: Get top N items by revenue.
- `/api/daily-revenue`: Get daily revenue within a date range.
- `/api/monthly-revenue`: Get monthly revenue within a date range.

## Examples

### Get all orders

```bash
GET /api/orders
```
Response:

```bash
{
    "630": [
        ["Burger", 10.0],
        ["Fries", 5.0]
    ],
    "648": [
        ["Pizza", 15.0],
        ["Soda", 2.5]
    ]
}
```

### Get details of a specific order.

```bash
GET /api/orders/16118
```
Response:

```bash
[
  [
    "Plain Papadum",
    1.6
  ],
  [
    "King Prawn Balti",
    12.95
  ],
  [
    "Garlic Naan",
    2.95
  ],
  [
    "Mushroom Rice",
    3.95
  ],
  [
    "Paneer Tikka Masala",
    8.95
  ],
  [
    "Mango Chutney",
    0.5
  ]
]
```


### Get daily revenue within a date range.

```bash
GET /api/daily-revenue?from=2024-01-01&to=2024-01-31
```
Response:
```bash
{
    "2024-01-01": 150.0,
    "2024-01-02": 200.0,
    "2024-01-03": 180.0
}
```
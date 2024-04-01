from flask import Flask, jsonify, request
from flask_cors import CORS

import csv
from collections import defaultdict
import pandas as pd

app = Flask(__name__)
CORS(app)

QUANTITY = 'Quantity'
ORDER_NUMBER = 'Order Number'
PRODUCT_PRICE = 'Product Price'
ITEM_NAME = 'Item Name'
total = float(0)
items = defaultdict(float)
orders = defaultdict(list)
csv_file = "data/restaurant-1-orders.csv"

with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price_order = int(row[QUANTITY]) * float(row[PRODUCT_PRICE])
        items[row[ITEM_NAME]] = round(items[row[ITEM_NAME]] + price_order, 3)
        orders[int(row[ORDER_NUMBER])].append((row[ITEM_NAME], round(price_order, 3)))
        total += price_order

sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)

df = pd.read_csv(csv_file, parse_dates=['Order Date'], dayfirst=True)


@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    if order_id in orders:
        return jsonify(orders[order_id])
    else:
        return jsonify({"error": "Order not found"}), 404


@app.route('/api/items/<int:n>', methods=['GET'])
def get_top_items(n):
    items_list = sorted_items[:n]
    remain = total - sum(it[1] for it in items_list)
    items_list.append(("Remain", round(remain, 2)))
    return jsonify(items_list)


@app.route('/api/daily-revenue', methods=['GET'])
def get_daily_revenue():
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if not from_date or not to_date:
        return jsonify({"error": "Please provide 'from' and 'to' dates"}), 400

    try:
        filtered_data = df[(df['Order Date'] >= from_date) & (df['Order Date'] <= to_date)]
        filtered_data['Revenue'] = filtered_data['Quantity'] * filtered_data['Product Price']

        daily_revenue = filtered_data.groupby(filtered_data['Order Date'].dt.date)['Revenue'].sum()

        # Convert the index (date) to string for the dictionary
        daily_revenue_dict = daily_revenue.reset_index().set_index('Order Date').to_dict()['Revenue']
        # Convert date keys to strings
        daily_revenue_dict = {str(key): value for key, value in daily_revenue_dict.items()}
        return jsonify(daily_revenue_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/monthly-revenue', methods=['GET'])
def get_monthly_revenue():
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if not from_date or not to_date:
        return jsonify({"error": "Please provide 'from' and 'to' dates"}), 400

    try:
        filtered_data = df[(df['Order Date'] >= from_date) & (df['Order Date'] <= to_date)]
        monthly_revenue = filtered_data.groupby(filtered_data['Order Date'].dt.to_period("M"))['Product Price'].sum()

        # Convert the index (date) to string for the dictionary
        monthly_revenue_dict = monthly_revenue.reset_index().set_index('Order Date').to_dict()['Product Price']
        # Convert date keys to strings
        monthly_revenue_dict = {str(key): value for key, value in monthly_revenue_dict.items()}
        return jsonify(monthly_revenue_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

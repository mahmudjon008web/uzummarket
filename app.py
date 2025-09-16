import sqlite3
from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)
def create_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn

@app.route("/", methods=['GET'])
def home_view():
    return render_template("index.html")

@app.route("/products", methods=['GET'])
def product_view():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("select * from products")
    rows = cursor.fetchall()
    product = [dict(row) for row in rows]
    return jsonify(product)

@app.route("/", methods=["POST"])
def add_data():
    try:
        image_url = request.form['image_url']
        uzum_pay = request.form["uzum_pay"]
        pay = request.form["pay"]
        split_pay = request.form["split_pay"]
        title = request.form["title"]

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("insert into products (image_url, uzum_pay, pay, split_pay, title) values (?,?,?,?,?)", (image_url, uzum_pay, pay, split_pay, title))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Mahsulotlar muvaffaqiyatli qo'shildi"})

    except Exception as e: 
        return jsonify({"status": "error", "message": str(e)})

@app.route("/cards", methods=['GET'])
def cards_view():
    conn = create_connection()
    cursor = conn.cursor()
    return render_template("cards.html")


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def fetch_data(clients_limit, orders_limit, rma_limit):
    conn = sqlite3.connect("QuantigrationUpdates.db")
    cur = conn.cursor()

    if clients_limit > 0:
        cur.execute("SELECT * FROM Clients LIMIT ?", (clients_limit,))
        clients = cur.fetchall()
    else:
        clients = []

    if orders_limit > 0:
        cur.execute("SELECT * FROM Orders LIMIT ?", (orders_limit,))
        orders = cur.fetchall()
    else:
        orders = []

    if rma_limit > 0:
        cur.execute("SELECT * FROM RMA LIMIT ?", (rma_limit,))
        rma = cur.fetchall()
    else:
        rma = []

    conn.close()
    return clients, orders, rma

@app.route("/", methods=["GET"])
def index():
    clients_limit = request.args.get("clients_limit", default=0, type=int)
    orders_limit = request.args.get("orders_limit", default=0, type=int)
    rma_limit = request.args.get("rma_limit", default=0, type=int)

    clients, orders, rma = fetch_data(clients_limit, orders_limit, rma_limit)
    return render_template("index.html", clients=clients, orders=orders, rma=rma)

if __name__ == "__main__":
    app.run(debug=True)

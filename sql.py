import sqlite3
import csv

# Connect to (or create) the SQLite database
conn = sqlite3.connect("QuantigrationUpdates.db")
cur = conn.cursor()

# Step 1: Create tables (Clients first because others depend on it)
cur.executescript("""
DROP TABLE IF EXISTS RMA;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Clients;

CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    FirstName VARCHAR(25),
    LastName VARCHAR(25),
    Street VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    Telephone VARCHAR(15)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    ClientID INT,
    SKU VARCHAR(30),
    Description VARCHAR(60),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

CREATE TABLE RMA (
    RMAID INT PRIMARY KEY,
    OrderID INT,
    Step VARCHAR(60),
    Status VARCHAR(35),
    Reason VARCHAR(50),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
""")

# Step 2: Load data from CSVs
def load_csv_to_table(csv_filename, table_name, column_count):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        rows = [tuple(row) for row in reader]
        placeholders = ",".join(["?"] * column_count)
        cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)

# Adjust the file names and number of columns
load_csv_to_table("customers.csv", "Clients", 8)
load_csv_to_table("orders.csv", "Orders", 4)
load_csv_to_table("rma.csv", "RMA", 5)

conn.commit()

conn = sqlite3.connect("QuantigrationUpdates.db")
cur = conn.cursor()

cur.execute("SELECT * FROM Clients LIMIT 5;")
print("Clients sample data:", cur.fetchall())

cur.execute("SELECT * FROM Orders LIMIT 5;")
print("Orders sample data:", cur.fetchall())

cur.execute("SELECT * FROM RMA LIMIT 5;")
print("RMA sample data:", cur.fetchall())

conn.close()


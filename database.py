import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='products.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price TEXT,
                url TEXT,
                date_added DATETIME
            )
        ''')
        self.conn.commit()

    def add_product(self, name, price, url):
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO products (name, price, url, date_added)
            VALUES (?, ?, ?, ?)
        ''', (name, price, url, date_added))
        self.conn.commit()

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def get_product_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM products")
        return self.cursor.fetchone()[0]

    def search_products(self, query):
        self.cursor.execute('''
            SELECT * FROM products
            WHERE name LIKE ? OR price LIKE ? OR url LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        results = self.cursor.fetchall()
        return [{'id': r[0], 'name': r[1], 'price': r[2], 'url': r[3], 'date_added': r[4]} for r in results]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    product_count = db.get_product_count()
    print(f"Total number of items in the database: {product_count}")
    
    print("\nList of all items:")
    for product in db.get_all_products():
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, URL: {product[3]}, Date Added: {product[4]}")
    
    db.close()
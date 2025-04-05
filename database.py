import sqlite3
class DATABASE():
    def create_connection(self):
        return sqlite3.connect("products.db")

    def create_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT NOT NULL,
        part_number TEXT UNIQUE NOT NULL,
        size_mm INTEGER NOT NULL)"""
        )     
        conn.commit()
        conn.close()  

    def insert_product(self,name, color,part_number,size_mm):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO products (name, color, part_number, size_mm) VALUES (?,?,?,?) """
        , (name,color,part_number,size_mm)
        )
        conn.commit()
        conn.close()


    def fetch_products(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, color, part_number, size_mm FROM products")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_product(self,part_number):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE from products WHERE part_number = ?",
        (part_number,)
        )
        conn.commit()
        conn.close()

    def modify_product(self,part_number, new_name, new_color, new_size):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, color = ?, size_mm = ?
            WHERE part_number = ?
        """, (new_name, new_color, new_size, part_number))
        conn.commit()
        conn.close()


    


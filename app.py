from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

# Database connection parameters
DB_CONFIG = {
    "host": "lab44-sql.cxqmk4ysm6t6.eu-west-1.rds.amazonaws.com",
    "user": "admin",
    "password": "amalitech",
    "database": "delvindb",
}


# Function to get a database connection
def get_db_connection():
    connection = pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )
    return connection


@app.route("/")
def welcome():
    message = """The list of API's to use are:

  <h1> 1. Top Customers by Spending :  /top_customers<h1> <br> 
  <h1> 2. Monthly Sales Report (Only Shipped/Delivered) : /monthly_sales <h1><br>
  <h1> 3. Products Never Ordered : /products_never_ordered  <h1><br>
  <h1> 4. Average Order Value by Country : /avg_order_value_by_country <h1><br> 
  <h1> 5. Frequent Buyers (More Than One Order) : /frequent_buyers <h1><br>  """
    return f"<pre>{message}</pre>"


# API endpoint: Top Customers by Spending
@app.route("/top_customers", methods=["GET"])
def top_customers():
    query = """
    SELECT 
        c.customer_id,
        c.name,
        c.email,
        SUM(oi.quantity * oi.unit_price) AS total_spent
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    GROUP BY 
        c.customer_id, c.name, c.email
    ORDER BY 
        total_spent DESC;
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)


# API endpoint: Monthly Sales Report (Only Shipped/Delivered)
@app.route("/monthly_sales", methods=["GET"])
def monthly_sales():
    query = """
    SELECT 
        YEAR(o.order_date) AS year,
        MONTH(o.order_date) AS month,
        SUM(oi.quantity * oi.unit_price) AS total_sales
    FROM 
        orders o
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    WHERE 
        o.status IN ('Shipped', 'Delivered')
    GROUP BY 
        YEAR(o.order_date), MONTH(o.order_date)
    ORDER BY 
        year DESC, month DESC;
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)


# API endpoint: Products Never Ordered
@app.route("/products_never_ordered", methods=["GET"])
def products_never_ordered():
    query = """
    SELECT 
        p.product_id,
        p.name,
        p.category,
        p.price
    FROM 
        products p
    LEFT JOIN 
        order_items oi ON p.product_id = oi.product_id
    WHERE 
        oi.product_id IS NULL;
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)


# API endpoint: Average Order Value by Country
@app.route("/avg_order_value_by_country", methods=["GET"])
def avg_order_value_by_country():
    query = """
    SELECT 
        c.country,
        AVG(order_total) AS avg_order_value
    FROM (
        SELECT 
            o.order_id,
            SUM(oi.quantity * oi.unit_price) AS order_total,
            o.customer_id
        FROM 
            orders o
        JOIN 
            order_items oi ON o.order_id = oi.order_id
        GROUP BY 
            o.order_id, o.customer_id
    ) AS order_values
    JOIN 
        customers c ON order_values.customer_id = c.customer_id
    GROUP BY 
        c.country
    ORDER BY 
        avg_order_value DESC;
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)


# API endpoint: Frequent Buyers (More Than One Order)
@app.route("/frequent_buyers", methods=["GET"])
def frequent_buyers():
    query = """
    SELECT 
        c.customer_id,
        c.name,
        c.email,
        COUNT(o.order_id) AS order_count
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    GROUP BY 
        c.customer_id, c.name, c.email
    HAVING 
        COUNT(o.order_id) > 1
    ORDER BY 
        order_count DESC;
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

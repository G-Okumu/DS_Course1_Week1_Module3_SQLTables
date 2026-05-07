# main.py
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')


# Part 1: Join and Filter
def get_employees_in_boston(connection=conn):
    return pd.read_sql("""
        SELECT firstName, lastName, jobTitle 
        FROM employees e 
        JOIN offices o ON e.officeCode = o.officeCode 
        WHERE o.city = 'Boston';
    """, connection)


def get_offices_with_zero_employees(connection=conn):
    return pd.read_sql("""
        SELECT o.officeCode, o.city 
        FROM offices o 
        LEFT JOIN employees e ON o.officeCode = e.officeCode 
        WHERE e.employeeNumber IS NULL;
    """, connection)


# Part 2: Type of Join
def get_all_employees_with_office(connection=conn):
    return pd.read_sql("""
        SELECT e.firstName, e.lastName, o.city, o.state
        FROM employees e
        LEFT JOIN offices o ON e.officeCode = o.officeCode
        ORDER BY e.firstName, e.lastName;
    """, connection)


def get_customers_without_orders(connection=conn):
    return pd.read_sql("""
        SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
        FROM customers c
        LEFT JOIN orders o ON c.customerNumber = o.customerNumber
        WHERE o.orderNumber IS NULL
        ORDER BY c.contactLastName;
    """, connection)


# Part 3: Built-in Function
def get_customer_payments(connection=conn):
    return pd.read_sql("""
        SELECT c.contactFirstName, c.contactLastName, p.paymentDate, p.amount
        FROM customers c
        JOIN payments p ON c.customerNumber = p.customerNumber
        ORDER BY CAST(p.amount AS REAL) DESC;
    """, connection)


# Part 4: Joining and Grouping
def get_employees_with_high_credit(connection=conn):
    return pd.read_sql("""
        SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
        FROM employees e
        JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        GROUP BY e.employeeNumber
        HAVING AVG(c.creditLimit) > 90000
        ORDER BY num_customers DESC;
    """, connection)


def get_top_selling_products(connection=conn):
    return pd.read_sql("""
        SELECT p.productName, 
               COUNT(od.orderNumber) AS numorders,
               SUM(od.quantityOrdered) AS totalunits
        FROM products p
        JOIN orderdetails od ON p.productCode = od.productCode
        GROUP BY p.productName
        ORDER BY totalunits DESC;
    """, connection)


def get_product_customer_counts(connection=conn):
    return pd.read_sql("""
        SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
        FROM products p
        JOIN orderdetails od ON p.productCode = od.productCode
        JOIN orders o ON od.orderNumber = o.orderNumber
        GROUP BY p.productName
        ORDER BY numpurchasers DESC;
    """, connection)


def get_customers_per_office(connection=conn):
    return pd.read_sql("""
        SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
        FROM offices o
        LEFT JOIN employees e ON o.officeCode = e.officeCode
        LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        GROUP BY o.officeCode;
    """, connection)


# Part 6: Subquery
def get_employees_selling_low_products(connection=conn):
    return pd.read_sql("""
        WITH low_sales AS (
            SELECT p.productCode
            FROM products p
            JOIN orderdetails od ON p.productCode = od.productCode
            JOIN orders o ON od.orderNumber = o.orderNumber
            GROUP BY p.productCode
            HAVING COUNT(DISTINCT o.customerNumber) < 20
        )
        SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
        FROM employees e
        JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        JOIN orders ord ON c.customerNumber = ord.customerNumber
        JOIN orderdetails od ON ord.orderNumber = od.orderNumber
        JOIN low_sales ls ON od.productCode = ls.productCode
        JOIN offices o ON e.officeCode = o.officeCode
        ORDER BY e.lastName;
    """, connection)


# Close the connection function
def close_connection(connection=conn):
    connection.close()

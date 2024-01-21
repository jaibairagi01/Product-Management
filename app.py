from flask import Flask, jsonify,request
import mysql.connector as sql
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def get_db_connection():
    return sql.connect(host="localhost", user="root", passwd="", database='Products')

@app.route('/products', methods=['GET'])
def get_all_products():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        products = cursor.fetchall()
        cursor.close()
        connection.close()

        for i in range(0,len(products)):
            data={
            'PID':None,
            'Pname':None,
            'Price':None,
            'Quantity':None,
            }
            data['PID']=products[i][0]
            data['Pname']=products[i][1]
            data['Price']=products[i][2]
            data['Quantity']=products[i][3]
            products[i]=data
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Product WHERE PID = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if product:
            return jsonify({'product': product})
        else:
            return jsonify({'message': 'Product not found'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/products/add', methods=['POST'])
def add_product():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        product_data = request.get_json()
        pname = product_data.get('Pname')
        price = product_data.get('Price')
        quantity = product_data.get('quantity')

        query = "INSERT INTO Product (Pname, Price, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (pname, price, quantity))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Product added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "DELETE FROM Product WHERE PID = %s"
        cursor.execute(query, (product_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        product_data = request.get_json()
        pname = product_data.get('Pname')
        price = product_data.get('Price')
        quantity = product_data.get('quantity')

        query = "UPDATE Product SET Pname = %s, Price = %s, quantity = %s WHERE PID = %s"
        cursor.execute(query, (pname, price, quantity, product_id))
        connection.commit()

        cursor.close()
        connection.close()
  
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)


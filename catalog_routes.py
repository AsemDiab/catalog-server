from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

class QueryBuilder:
    def __init__(self, table_name):
        self.table_name = table_name
    def retrive_data(self,condition=None,orderBy=None,appearedCol=None,isAsc=True):
        query="SELECT "
        if appearedCol !=None:
            for col in appearedCol:
                query+=col+","
            query=query[:-1]
        else:
            query+="*"
        query+=" FROM "+self.table_name
        if condition !=None:
            query+=" WHERE "
            for key in condition:
                query+=key+"="+ ("'" if type(condition[key])==str else "")+ str(condition[key])+("'" if type(condition[key])==str else "")+" AND "
            query=query[:-5]
        if orderBy !=None:
            query+=" ORDER BY "+orderBy+ (" ASC" if isAsc else " DESC")
        return query
    def update_stock(self,condition,new_stock):
        query = f"UPDATE {self.table_name} SET  stock = {new_stock} "
        if condition !=None:
            query+=" WHERE "
            for key in condition:
                query+=key+"="+ ("'" if type(condition[key])==str else "")+ str(condition[key])+("'" if type(condition[key])==str else "")+" AND "
            query=query[:-5]
        

        return query
    def update_price(self,condition,new_price):
        query = f"UPDATE {self.table_name} SET price = {new_price} "
        if condition !=None:
            query+=" WHERE "
            for key in condition:
                query+=key+"="+ ("'" if type(condition[key])==str else "")+ str(condition[key])+("'" if type(condition[key])==str else "")+" AND "
            query=query[:-5]
        
        return query
    def delete_data(self,condition):
        query = f"DELETE FROM {self.table_name}"
        if condition !=None:
            query+=" WHERE "
            for key in condition:
                query+=key+"="+ ("'" if type(condition[key])==str else "")+ str(condition[key])+("'" if type(condition[key])==str else "")+" AND "
            query=query[:-5]
        
        return query


# Database connection function
def connect_db():
    conn = sqlite3.connect('database/Book_DB.db')
    # conn.row_factory = sqlite3.Row  # This allows dict-like access to the rows
    return conn

@app.route('/books')
def get_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(QueryBuilder("book_table").retrive_data())
    rows = cursor.fetchall()
    data=cursor.execute(QueryBuilder("book_table").retrive_data()) 
    keys=[]
    for column in data.description: 
        keys.append(column[0])
    conn.close()
    
    items = [dict(zip(keys, row)) for row in rows]
    return jsonify(items), 200
# Query by subject
@app.route('/search/<subject>', methods=['GET'])
def query_by_subject(subject):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(QueryBuilder("book_table").retrive_data(condition={"topic":subject}))
    rows = cursor.fetchall()
    data=cursor.execute(QueryBuilder("book_table").retrive_data()) 
    keys=[]
    for column in data.description: 
        keys.append(column[0])
    conn.close()
    
    items = [dict(zip(keys, row)) for row in rows]
    conn.close()
    
    return jsonify(items), 200

# Query by item number
@app.route('/info/<int:Book_ID>', methods=['GET'])
def query_by_item(Book_ID):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(QueryBuilder("book_table").retrive_data(condition={"Book_ID":Book_ID}))
    row = cursor.fetchone()
    data=cursor.execute(QueryBuilder("book_table").retrive_data()) 
    keys=[]
    for column in data.description: 
        keys.append(column[0])
    conn.close()
        
    if row:
        item = dict(zip(keys, row))
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

# Update item (price or stock)
@app.route('/items/<int:Book_ID>', methods=['PUT'])
def update_item(Book_ID):
    data = request.json
    new_price = data.get('price')
    new_stock = data.get('stock')
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if the item exists
    print("befote query")
    cursor.execute(QueryBuilder("book_table").retrive_data({"Book_ID":Book_ID}))
    row = cursor.fetchone()
    print("after query")
    if not row:
        conn.close()
        return jsonify({'error': 'Item not found'}), 404
    
    # Update item details
    if new_price:
        cursor.execute(QueryBuilder("book_table").update_price({"Book_ID":Book_ID},new_price))
    if new_stock:
        cursor.execute(QueryBuilder("book_table").update_stock({"Book_ID":Book_ID},new_stock))
    print("The update done")
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item updated successfully'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

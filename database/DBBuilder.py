import sqlite3


conn=sqlite3.connect("Book_DB.db")

cursor=conn.cursor()

cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS book_table (
            Book_ID INTEGER PRIMARY KEY , 
            name TEXT NOT NULL,
            topic TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL
    );
    ''')

books_list = [
        { "Book_ID": 1, "name":"How to get a good grade in DOS in 40 minutes a day","topic":"distributed systems","stock":10, "price":29.99 },
        { "Book_ID": 2, "name":"RPCs for Noobs","topic":"distributed systems","stock":15, "price":29.99 },
        { "Book_ID": 3, "name":"Xen and the Art of Surviving Undergraduate School.","topic":" undergraduate school","stock":5, "price":29.99 },
        { "Book_ID": 4, "name":"Cooking for the Impatient Undergrad","topic":" undergraduate school","stock":50, "price":29.99 }
    ]

insert = ('''
            INSERT INTO book_table(Book_ID,name,topic,stock,price)
            VALUES(?,?,?,?,?)
        ''')
for book in books_list:
        conn.execute(insert,([book["Book_ID"],book["name"],book["topic"],book["stock"],book["price"]]))
    

conn.commit()


res=cursor.execute("SELECT * From book_table")

for row in res:
        print(row[0])

conn.close()
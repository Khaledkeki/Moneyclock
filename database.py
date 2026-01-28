import psycopg2
from psycopg2 import Error

def data():
    try:
        connection = psycopg2.connect(user = "postgres", password="Dontell_1", host="127.0.0.1", port = "5432", database = "Moneyclock")

        cursor = connection.cursor()
        print("postgresSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT VERSION();")
        record = cursor.fetchone()
        print("You are connected to -", record, "\n")
        return connection 

    except (Exception, Error) as error:
        print("Error while connecting to postgresSQL", error)
    




def table_budget():
    try:
        connection = data()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BUDGET (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100),
                    item_name VARCHAR(100),
                    price INTEGER,
                    hours_needed INTEGER
                       
                    )
                    """)
    
        connection.commit()
        cursor.close()
        connection.close()
        print("Table created succesfully")
    except Exception as e:
        print("Error creating table:", e)

def table_users():
    try:
        connection = data()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE,
                    password VARCHAR(100),
                    hourly_wage INTEGER  )
                """)
        connection.commit()
        cursor.close()
        connection.close()
        print("Table created succesfully")
    except Exception as e:
        print("Errpr creating table:", e)


def create_user(email, password, hourly_wage):
    try:
        connection = data()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (email, password, hourly_wage)
            VALUES (%s, %s, %s)
                                    
        """,(email, password, hourly_wage))

        connection.commit()
        cursor.close()
        connection.close()
        print("User created successfully")
    except Exception as e:
        print("Erorr creating user:", e)

def get_user(email):
    connection = data()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()


    cursor.close()
    connection.close()
    return user

def save_calculation(user_id, item_name, price, hours_needed):
    connection = data()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO BUDGET (user_id, item_name, price, hours_needed)
        VALUES(%s, %s, %s, %s)
                   
                     """, (user_id, item_name, price, hours_needed))
    
    connection.commit()
    cursor.close()
    connection.close()

def get_history(user_id):
    connection = data()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM BUDGET WHERE user_id = %s", (user_id,))
    user = cursor.fetchall()

    cursor.close()
    connection.close()
    return user

def add_purchased_colum():
    connection = data()
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE budget ADD COLUMN purchased BOOLEAN DEFAULT FALSE")

    connection.commit()
    cursor.close()
    connection.close()
    print("column added succesfully")

def update_purchased(id, purchased):
    connection = data()
    cursor = connection.cursor()

    cursor.execute("UPDATE budget SET purchased = %s WHERE id = %s", (purchased, id))

    connection.commit()
    cursor.close()
    connection.close()

def get_summary(user_id):
    connection = data()
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(hours_needed) FROM budget WHERE user_id = %s AND purchased = TRUE", (user_id,))
    spent = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(hours_needed) FROM budget WHERE user_id = %s AND purchased = FALSE",(user_id,))
    saved = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    return {"hours_spent": spent, "hours_saved": saved}


    









   

    






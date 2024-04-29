from mysql.connector.pooling import MySQLConnectionPool

dbConfig = {
    "user": "root",
    "password": ".1Zhuzhaoyuyxlm",
    "host": "localhost",
    "database": "edu_assistant",
    "raise_on_warnings": True
}

# create a connection pool
pool = MySQLConnectionPool(pool_name="mydb_pool", pool_size=10, **dbConfig)


class ConnectionManager:
    def __enter__(self):
        self.conn = pool.get_connection()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()


def executeQuery(query, data=None, operation="SELECT", dictionary=False, size=0):
    result = None
    try:
        with ConnectionManager() as conn:
            if dictionary:
                cursor = conn.cursor(dictionary=True)
            else:
                cursor = conn.cursor()
                # print(f"Executing query: {query}")
                # print(f"Data: {data}")
            if operation == "COMMIT":
                cursor.execute(query, data)
                conn.commit()
                # Get the ID of the last inserted row
                result = cursor.lastrowid
            if operation == "COMMIT_MANY":
                cursor.executemany(query, data)
                conn.commit()
                # Get the ID of the last inserted row
                result = cursor.lastrowid
            elif operation == "SELECT":
                cursor.execute(query, data)
                if size == 0:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchmany(size=size)
            cursor.close()
    except Exception as e:
        print(f"An error occurred while executing the query: {query}")
    return result


def addUser(data):
    query = """
    INSERT INTO user (email, first_name, last_name, password, avatar) 
    VALUES (%s, %s, %s, %s, %s)
    """
    newId = executeQuery(query, data, operation="COMMIT")
    return newId


def getUserByEmail(email):
    query = "SELECT * FROM user WHERE email = %s"
    result = executeQuery(query, (email,), dictionary=True)
    if result is None:
        return None
    elif len(result) == 0:
        return False
    else:
        return result[0]


if __name__ == '__main__':
    print(getUserByEmail("linglingwu@gmail.com"))
    print(getUserByEmail("123"))

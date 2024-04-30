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
        print(f"An error occurred while executing the query: {query}\nError: {e}")
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


def addRecord(data):
    query = """
    INSERT INTO records (user_id, name, type) 
    VALUES (%s, %s, %s)
    """
    newId = executeQuery(query, data, operation="COMMIT")
    return newId


def getRecords(userId):
    query = "SELECT * FROM records WHERE user_id = %s"
    result = executeQuery(query, (userId,), dictionary=True)
    return result


def getRecord(recordId):
    query = "SELECT * FROM records WHERE id = %s"
    result = executeQuery(query, (recordId,), dictionary=True)
    return result


def addFileRecord(data):
    query = """
    INSERT INTO file_record (record_id, path)
    VALUES (%s, %s)
    """
    newId = executeQuery(query, data, operation="COMMIT")
    return newId


def addTextRecord(data):
    query = """
    INSERT INTO text_record (record_id, content)
    VALUES (%s, %s)
    """
    newId = executeQuery(query, data, operation="COMMIT")
    return newId


def deleteRecord(recordId):
    query = "DELETE FROM records WHERE id = %s"
    executeQuery(query, (recordId,), operation="COMMIT")
    return True


def deleteFileRecord(recordId):
    query = "DELETE FROM file_record WHERE record_id = %s"
    executeQuery(query, (recordId,), operation="COMMIT")
    return True


def deleteTextRecord(recordId):
    query = "DELETE FROM text_record WHERE record_id = %s"
    executeQuery(query, (recordId,), operation="COMMIT")
    return True


def getTextRecord(recordId):
    query = "SELECT * FROM text_record WHERE record_id = %s"
    result = executeQuery(query, (recordId,), dictionary=True)
    return result


def deleteDetection(textId):
    query = "DELETE FROM detection WHERE text_id = %s"
    executeQuery(query, (textId,), operation="COMMIT")
    return True


def getFileRecord(recordId):
    query = "SELECT * FROM file_record WHERE record_id = %s"
    result = executeQuery(query, (recordId,), dictionary=True)
    return result


if __name__ == '__main__':
    print(getUserByEmail("linglingwu@gmail.com"))
    print(getUserByEmail("123"))

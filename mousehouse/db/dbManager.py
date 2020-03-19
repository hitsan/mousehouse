import mysql.connector
from utils import logger as lg

def dbSetup():
    dbLogger = lg.getLogger(__name__, True)
    timeOut = 0

    dbLogger.info("Start the connection of the mousehouse DB.")
    while timeOut < 5:
        timeOut += 1
        try:
            conn = mysql.connector.connect(
                    host='localhost',
                    port='3306',
                    user='mousehouse',
                    password='mousehouse',
                    database='msDB'
                    )
        except:
            if timeOut >= 5:
                dbLogger.error("Time out. Check the settings MySQL and mousehouse DB.")
                exit(0)
            dbLogger.error("Can not Access Data Base. Try again")
    conn.ping(reconnect=True)
    cur = conn.cursor(buffered=True)

    cur.execute("""CREATE TABLE IF NOT EXISTS msDB.machines(
            id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
            ip VARBINARY(4) NOT NULL UNIQUE,
            Status BOOL,
            macAdrr varchar(20) UNIQUE
            )""")
    dbLogger.info("Success the connetion of the mousehou DB")

    cur.execute("show columns from machines")

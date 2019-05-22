import random
import MySQLdb
import config


def commercial_text():
    conn = MySQLdb.connect(host=config.host, port=config.port, user=config.user, passwd=config.passwd, db=config.db)
    conn.set_character_set('utf8')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM commercial")
    rows = cursor.fetchall()

    row = rows[random.randrange(0, len(rows))]
    while row[2] == 0:
        row = rows[random.randrange(0, len(rows))]

    cursor.execute("UPDATE commercial SET counter = %s WHERE id = %s", (row[2]-1, row[0]))
    conn.commit()
    conn.close()

    commercial = "\n" + row[1]

    return commercial


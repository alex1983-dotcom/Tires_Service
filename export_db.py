import sqlite3

def export_db(old_db_path, new_db_path):
    conn = sqlite3.connect(old_db_path)
    with open(new_db_path, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    print("Экспорт завершен")

if __name__ == "__main__":
    old_db_path = 'db.sqlite3'
    new_db_path = 'new_db.sqlite3'
    export_db(old_db_path, new_db_path)

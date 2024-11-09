import os

def change_permissions(file_path):
    os.chmod(file_path, 0o777)
    print(f"Permissions for {file_path} have been changed to 777")

if __name__ == "__main__":
    change_permissions("db.sqlite3")

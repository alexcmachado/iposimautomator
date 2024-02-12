import json
import os

from cryptography.fernet import Fernet


def save_credentials(credentials_file_path, key, password, filename, output_dir, user):
    credentials = {
        "user": user,
        "password": password,
        "filename": filename,
        "output_dir": output_dir,
    }
    json_string = json.dumps(credentials)
    json_bytes_string = json_string.encode()
    encrypted_json_bytes_string = key.encrypt(json_bytes_string)
    with open(credentials_file_path, "wb") as credentials_file:
        credentials_file.write(encrypted_json_bytes_string)


def get_key(key_file_path):
    try:
        os.mkdir(f"{os.getenv('APPDATA')}/Iposim Automator")
    except FileExistsError:
        pass

    try:
        with open(key_file_path, "rb") as file:
            fernet_obj = Fernet(file.read())
        return fernet_obj
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_file_path, "wb") as file:
            file.write(key)
        fernet_obj = Fernet(key)
        return fernet_obj


def load_credentials(credentials_file_path, key, password, filename, output_dir, user):
    try:
        with open(credentials_file_path, "rb") as credentials_file:
            encrypted_json_bytes_string = credentials_file.read()
            decrypted_json_bytes_string = key.decrypt(encrypted_json_bytes_string)
            credentials = json.loads(decrypted_json_bytes_string)
        user.set(credentials["user"])
        password.set(credentials["password"])
        filename.set(credentials["filename"])
        output_dir.set(credentials["output_dir"])
    except FileNotFoundError:
        pass

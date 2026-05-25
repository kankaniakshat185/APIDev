from pwdlib import PasswordHash

def Hash(password: str):
    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(password)
    return hashed_password
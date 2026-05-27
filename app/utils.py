from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def Hash(password: str):
    hashed_password = password_hash.hash(password)
    return hashed_password

def verify(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
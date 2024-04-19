from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HASHING IS TO BE DONE LATER

def hash (password:str):
    return password

def verify (plain_pass, hashed_pass):
    return plain_pass == hashed_pass
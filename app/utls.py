from passlib.context import CryptContext
pwb_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwb_context.hash(password)
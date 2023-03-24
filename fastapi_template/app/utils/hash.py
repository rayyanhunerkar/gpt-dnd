from passlib.context import CryptContext

pwt_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwt_cxt.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwt_cxt.verify(password, hashed_password)

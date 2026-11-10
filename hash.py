import hashlib

def hash_password(password):
    hashPass = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hashPass
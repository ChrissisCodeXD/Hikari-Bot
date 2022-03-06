import hashlib
import time
def generate_id() -> str:
    return hashlib.md5(f"{time.time()}".encode()).hexdigest()
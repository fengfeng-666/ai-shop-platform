from app.core.security import verify_password, hash_password

hashed = hash_password("111111")
print("hash:", hashed)
print("verify:", verify_password("111111", hashed))
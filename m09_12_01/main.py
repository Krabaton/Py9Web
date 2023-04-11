from jose import jwt, JWTError


secret = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'

payload = {'sub': 'example@test.com', 'username': 'denis', 'role': 'moderator'}

token = jwt.encode(payload, secret, algorithm=jwt.ALGORITHMS.HS512)
print(token)

try:
    r = jwt.decode(token, secret, algorithms=[jwt.ALGORITHMS.HS512, jwt.ALGORITHMS.HS256])
    print(r)
except JWTError as e:
    print(e)

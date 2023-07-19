from jose import jwt


secret = "0b69c4486093953c50403bd4c7c2ba3b1007c630059f6783700bd946bf1bed32"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYXZpZmVybG8iLCJleHAiOjE2ODk3NzA3MDl9.2ULw1fqk0g9mA01J9s2UpytJsSDzd2ZRom2cxOqflFE"


username = jwt.decode(token, secret, algorithms = ["HS256"]).get("sub")

print(username)



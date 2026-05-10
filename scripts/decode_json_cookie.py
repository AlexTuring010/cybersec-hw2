import base64
data = "eyJhZG1pbiI6MCwidGljayI6NywidXNlciI6IkFsZXhUdXJpbmcifQ"
decoded = base64.urlsafe_b64decode(data + '==')
print(decoded.decode())

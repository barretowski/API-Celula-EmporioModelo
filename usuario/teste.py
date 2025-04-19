with open(".env", "rb") as f:
    content = f.read()
    content_str = content.decode("utf-8")  # Convertendo para string
    print(content_str)

from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

print("Conexão:", db_url)

# Testar conexão
import psycopg2

try:
    conn = psycopg2.connect(db_url)
    print("✅ Conexão com sucesso!")
    conn.close()
except Exception as e:
    print("❌ Erro na conexão:", repr(e))

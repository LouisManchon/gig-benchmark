import mysql.connector

# --- Connexion à MySQL ---
db = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="1234" 
)

cursor = db.cursor()

# --- Créer la base ---
cursor.execute("CREATE DATABASE IF NOT EXISTS cotes_db")
cursor.execute("USE cotes_db")

# --- Créer la table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS cotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_name VARCHAR(255),
    bookmaker VARCHAR(100),
    cote_1 VARCHAR(10),
    cote_N VARCHAR(10),
    cote_2 VARCHAR(10)
)
""")

print("✅ Base et table créées avec succès !")

db.commit()
cursor.close()
db.close()

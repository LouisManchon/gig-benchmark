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
CREATE TABLE IF NOT EXISTS odds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_name VARCHAR(255),
    match_date DATETIME,
    bookmaker VARCHAR(100),
    cote_1 FLOAT,
    cote_N FLOAT,
    cote_2 FLOAT,
    trj FLOAT,
    league VARCHAR(25),
    sport VARCHAR(25),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

print("✅ Base et table créées avec succès !")

db.commit()
cursor.close()
db.close()

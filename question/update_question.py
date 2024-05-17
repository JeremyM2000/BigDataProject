import json
import mysql.connector
from mysql.connector import errorcode

# Charger les données JSON
with open('questions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Connexion à la base de données MySQL
config = {
  'user': 'your_username',
  'password': 'your_password',
  'host': 'localhost',
  'database': 'your_database'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Créer la table si elle n'existe pas
    create_table_query = """
    CREATE TABLE IF NOT EXISTS questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(255),
        question TEXT,
        option1 VARCHAR(255),
        option2 VARCHAR(255),
        option3 VARCHAR(255),
        option4 VARCHAR(255),
        correct_answer VARCHAR(255),
        UNIQUE KEY unique_question (question)
    )
    """
    cursor.execute(create_table_query)
    
    # Préparer la requête d'insertion avec IGNORE pour éviter les doublons
    insert_question_query = """
    INSERT IGNORE INTO questions (category, question, option1, option2, option3, option4, correct_answer)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Insérer les questions
    for q in data['questions']:
        cursor.execute(insert_question_query, (
            q['category'],
            q['question'],
            q['options'][0],
            q['options'][1],
            q['options'][2],
            q['options'][3],
            q['correct_answer']
        ))
        
    # Valider les changements
    conn.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erreur de connexion : Vérifiez votre nom d'utilisateur et mot de passe")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Erreur de connexion : La base de données n'existe pas")
    else:
        print(err)
finally:
    cursor.close()
    conn.close()

print("Les questions ont été ajoutées avec succès.")

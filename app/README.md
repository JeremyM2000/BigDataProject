# Set en run app

## Base de donnée

- Installer un mysql 
- Créer une base de données
- Modifier la config du projet en fonction de la base de données 
    - dans `app/config.py`:
        - db_user
        - db_password
        - db_host
        - db_name
- Créer les tables :
    - Les tbales sont définits dans les moèdle `app/models`.
    - Dans un terminal depuis `app`run :
        - `flask db migrate` initialiser la migration.
        - `flask db upgrade` appliquer la migration à la base de données.
        - Normalement on voit un message avec le nom des nouvelles tables.

- Seed la tables __questions__ :
    - Il faut run le script `app/seed/seed_questions.py`

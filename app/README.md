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
        - Si `app/migrations`existe il faut le supprimer
        - `python -m flask db init` initialiser les migrations.
            ```bash
            python3.12 -m flask db init                                               
            Creating directory '/Users/servanpelle/Desktop/BigDataProject/app/migrations'
            ...  done
            Creating directory
            '/Users/servanpelle/Desktop/BigDataProject/app/migrations/versions' ...  done
            Generating
            /Users/servanpelle/Desktop/BigDataProject/app/migrations/script.py.mako ...  done
            Generating /Users/servanpelle/Desktop/BigDataProject/app/migrations/env.py ...  done
            Generating /Users/servanpelle/Desktop/BigDataProject/app/migrations/README ...  done
            Generating /Users/servanpelle/Desktop/BigDataProject/app/migrations/alembic.ini ...  done
            Please edit configuration/connection/logging settings in '/Users/servanpelle/Desktop/BigDataProject app/migrations/alembic.ini' before proceeding.
            ```
        - `python -m flask db migrate` créer la migration.
            ```bash
            python3.12 -m flask db migrate                                            
            INFO  [alembic.runtime.migration] Context impl MySQLImpl.
            INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
            INFO  [alembic.autogenerate.compare] Detected added table 'asked_questions'
            INFO  [alembic.autogenerate.compare] Detected added table 'questions'
            INFO  [alembic.autogenerate.compare] Detected added table 'users'
            Generating /Users/servanpelle/Desktop/BigDataProject/app/migrations/versions/4a0376f93578_.py ...  done
            ```
        - `python -m flask db upgrade` appliquer la migration à la base de données.
            ```bash
            python3.12 -m flask db upgrade                                            
            INFO  [alembic.runtime.migration] Context impl MySQLImpl.
            INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
            INFO  [alembic.runtime.migration] Running upgrade  -> 4a0376f93578, empty message
            ```
        - Normalement on voit un message avec le nom des nouvelles tables.

- Seed la tables __questions__ :
    - Dans un terminal et dans `app` : 
        - Il faut run le script `app/seed/seed_questions.py`
        - `python3.12 seed_questions.py`

## Run app

- Dans un terminal et dans `app` : 
    - `python app.py`
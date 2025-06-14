from flask_bcrypt import Bcrypt
from .models import db, User

bcrypt = Bcrypt()

def createAdminUser():
    adminCheck = User.query.filter_by(username="admin").first()

    if adminCheck:
        print("Admin user already exists.")
        return
    
    try:
        print("Creating admin user.")

        password_hash = bcrypt.generate_password_hash('changeme').decode('utf-8')

        createAdmin = User(
            username='admin',
            email='admin@example.com',
            password=password_hash,
            is_active=True,
            theme=False,
            first_login=True
        )

        db.session.add(createAdmin)
        db.session.commit()
        print("Admin user has successfully been created:")
        print("Username: admin")
        print("Password: changeme")

    except Exception as e:
        db.session.rollback()
        print(f"Error creating admin user: {e}")
from nico_webapp import create_app, db
from nico_webapp.models import Image, User

app = create_app()
app.app_context().push()


def create_all():
    db.drop_all()
    db.create_all()
    db.session.commit()


def create_admin():
    create_all()
    admin = User(username='dex', password='123')
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    create_all()
    create_admin()

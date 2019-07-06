from nico_webapp import create_app, db
from nico_webapp.models import Image

app = create_app()
app.app_context().push()


def create_all():
    db.drop_all()
    db.create_all()
    db.session.commit()


def create_images():
    image1 = Image(image_file='dex_in_tree.jpg', title='test title', description='test description')
    image2 = Image(image_file='tut_and_tabla.jpg', title='test title', description='test description')
    image3 = Image(image_file='dex_in_tree.jpg', title='test title', description='test description')
    image4 = Image(image_file='dex_in_tree.jpg', title='test title', description='test description')
    image5 = Image(image_file='tut_and_tabla.jpg', title='test title', description='test description')
    image6 = Image(image_file='tut_and_tabla.jpg', title='test title', description='test description')
    db.session.add(image1)
    db.session.add(image2)
    db.session.add(image3)
    db.session.add(image4)
    db.session.add(image5)
    db.session.add(image6)
    db.session.commit()


if __name__ == '__main__':
    pass
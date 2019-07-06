from nico_webapp import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(60), nullable=True, unique=True)
    description = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"Image(' {self.image_file}', '{self.title}')"

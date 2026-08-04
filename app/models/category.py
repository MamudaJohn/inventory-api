from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    parent_category_id = db.Column(
        db.Integer, 
        db.ForeignKey("categories.id", ondelete="RESTRICT"), 
        nullable=True
        )

    subcategories = db.relationship("Category", backref=db.backref("parent", remote_side=[id]))

    def __repr__(self):
        return f"Category {self.name}"




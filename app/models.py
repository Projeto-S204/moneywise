from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'receita' ou 'despesa'
    icon = db.Column(db.String(50))
    fixed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Category {self.name} ({self.type})>"

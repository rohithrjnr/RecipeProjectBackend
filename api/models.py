# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    steps = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(250))

    
    comments = db.relationship('Comment', backref='recipe', lazy=True)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': self.ingredients,
            'steps': self.steps,
            'category': self.category,
            'image_url': self.image_url,
            'comments': [comment.serialize() for comment in self.comments],
            'ratings': [rating.serialize() for rating in self.ratings]
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    content = db.Column(db.String(500), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'content': self.content
        }


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    rating = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'rating': self.rating
        }

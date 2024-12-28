# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Recipe, Comment, Rating

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()



@app.route('/recipes', methods=['GET'])
def get_recipes():
    category = request.args.get('category')
    if category:
        recipes = Recipe.query.filter_by(category=category).all()
    else:
        recipes = Recipe.query.all()
    return jsonify([recipe.serialize() for recipe in recipes])


@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    new_recipe = Recipe(
        title=data['title'],
        description=data['description'],
        ingredients=data['ingredients'],
        steps=data['steps'],
        category=data['category'],
        image_url=data.get('image_url', '')
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.serialize()), 201


@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify(recipe.serialize())


@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()
    recipe.title = data.get('title', recipe.title)
    recipe.description = data.get('description', recipe.description)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.steps = data.get('steps', recipe.steps)
    recipe.category = data.get('category', recipe.category)
    recipe.image_url = data.get('image_url', recipe.image_url)
    
    db.session.commit()
    return jsonify(recipe.serialize())


@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully'}), 200


@app.route('/recipes/<int:id>/comments', methods=['POST'])
def add_comment(id):
    data = request.get_json()
    new_comment = Comment(
        recipe_id=id,
        content=data['content']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment.serialize()), 201


@app.route('/recipes/<int:id>/ratings', methods=['POST'])
def add_rating(id):
    data = request.get_json()
    new_rating = Rating(
        recipe_id=id,
        rating=data['rating']
    )
    db.session.add(new_rating)
    db.session.commit()
    return jsonify(new_rating.serialize()), 201


if __name__ == '__main__':
    app.run(debug=True)

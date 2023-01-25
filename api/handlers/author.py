from api import app, db, request, auth
from api.models.author import AuthorModel
from api.schemas.author import author_schema, authors_schema
from api.models.quote import QuoteModel

@app.route('/authors', methods=["GET"])
def get_authors():
    authors = AuthorModel.query.all()
    return authors_schema.dump(authors), 200


@app.route('/authors/<int:author_id>', methods=["GET"])
def get_author_by_id(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        return f"Author id={author_id} not found", 404

    return author_schema.dump(author), 200


@app.route('/authors', methods=["POST"])
@auth.login_required
def create_author():
    print("user = ", auth.current_user())
    author_data = request.json
    author = AuthorModel(**author_data)
    db.session.add(author)
    db.session.commit()
    return author_schema.dump(author), 201


@app.route('/authors/<int:author_id>', methods=["PUT"])
@auth.login_required
def edit_author(author_id):
    print("user = ", auth.current_user())
    author_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404
    for key, value in author_data.items():
        setattr(author, key, value)
    db.session.commit()
    return author_schema.dump(author), 200


@app.route('/authors/<int:author_id>', methods=["DELETE"])
@auth.login_required
def delete_author(author_id):
    print("user = ", auth.current_user())
    author = AuthorModel.query.get(author_id)
    if author is None:
        return f"author with id={author_id} not found", 404
# если есть цитаты у автора то автор будет удален а цитаты нет
# в место айди автора появится значение нулл в колонке автора
    db.session.delete(author)
    db.session.commit()
    return {"massege": f"author with id={author_id} has deleted"}, 200

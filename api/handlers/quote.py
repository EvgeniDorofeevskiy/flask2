from flask import jsonify
from api import app, db, request, multi_auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import  quotes_schema, quote_schema

@app.route('/quotes', methods=["GET"])  # Если запрос приходит по url: /quotes
def quotes():
    quotes = QuoteModel.query.all()
    return quotes_schema.dump(quotes)  # Возвращаем ВСЕ цитаты


@app.route('/quotes/<int:quote_id>', methods=["GET"])
def get_quotes_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is not None:  # Если запрос приходит по url: /authors/<int:author_id>/quotes
        # Возвращаем все цитаты автора
        return quote_schema.dump(quote), 200
    return {"Error": "Quote with id={quote_id} not found"}, 404


@app.route('/authors/<int:author_id>/quotes', methods=["GET"])
def get_quotes_by_author_id(author_id):
    # Если запрос приходит по url: /quotes/<int:quote_id>
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404
    quotes = author.quotes.all()
    return quotes_schema.dump(quotes), 200

@app.route('/authors/<int:author_id>/quotes', methods=["POST"])
@multi_auth.login_required
def create_quote(author_id):
    print("user = ", multi_auth.current_user())
    quote_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404

    quote = QuoteModel(author, **quote_data)
    db.session.add(quote)
    db.session.commit()
    return jsonify(quote_schema.dump(quotes)), 201


@app.route('/quotes/<int:quote_id>', methods=["PUT"])
@multi_auth.login_required
def edit_quote(quote_id):
    print("user = ", multi_auth.current_user())
    quote_data = request.json
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        return {"Error": f"Quote id={quote_id} not found"}, 404
    for key, value in  quote_data.items():
        setattr(quote, key, value)
    db.session.commit()
    return quote_schema.dump(quote), 200


@app.route('/quotes/<int:quote_id>', methods=["DELETE"])
@multi_auth.login_required
def delete_quote(quote_id):
    print("user = ", multi_auth.current_user())
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        return f"quote with id={quote_id} not found", 404
# если есть цитаты у автора то автор будет удален а цитаты нет
# в место айди автора появится значение нулл в колонке автора
    db.session.delete(quote)
    db.session.commit()
    return {"massege": f"quote with id={quote_id} has deleted"}, 200

from api import app, db, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema

@app.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return {"Erorr": f"User with id={user_id}not found"}, 404
    return user_schema.dump(user), 200


@app.route("/users")
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.post("/users")
@multi_auth.login_required
def create_user():
    print("user = ", multi_auth.current_user())
    user_data = request.json
    user = UserModel(**user_data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@app.delete("/users/<int:user_id>")
@multi_auth.login_required
def delete_user(user_id):
    print("user = ", multi_auth.current_user())
    user = UserModel.query.get(user_id)
    if user is None:
        return f"quote with id={user_id} not found", 404
# если есть цитаты у автора то автор будет удален а цитаты нет
# в место айди автора появится значение нулл в колонке автора
    db.session.delete(user)
    db.session.commit()
    return {"massege": f"quote with id={user_id} has deleted"}, 200
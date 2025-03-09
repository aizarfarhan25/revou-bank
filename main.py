from flask import Flask, jsonify, request, render_template
import copy

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# dummy_users = {
#     "users": {
#         "aizar@gmail.com": {
#             "password": "pass1234",
#             "first_name": "Aizar",
#             "last_name": "Farhan",
#             "email": "aizar@gmail.com",
#             "balance": 1000000

#         }
#     }
# }

dummy_users = {
    "users": {
        "coco@gmail.com": {
            "password": "pass1234",
            "first_name": "Nata",
            "last_name": "Decoco",
            "full_name": "Nata Decoco",
            "email": "coco@gmail.com",
        },
        "aizar@gmail.com": {
            "password": "pass1234",
            "first_name": "Aizar",
            "last_name": "Farhan",
            "full_name": "Aizar Farhan",
            "email": "aizar@gmail.com",
        },
    }
}


def all_user_repository() -> dict:
    return copy.deepcopy(dummy_users)


def create_user_repository(email: str, user_data: dict):
    dummy_users["users"][email] = user_data


def get_all_users():
    users = all_user_repository()["users"]
    formatted_responses = []
    for email, user_data in users.items():
        user_data.pop("password")
        user_data.pop("first_name")
        user_data.pop("last_name")
        formatted_responses.append(user_data)
    return formatted_responses


def create_users(data_masuk: dict):
    email = data_masuk.get("email")
    password = data_masuk.get("password")
    first_name = data_masuk.get("first_name")
    last_name = data_masuk.get("last_name")
    full_name = f"{first_name} {last_name}"
    if not email:
        return jsonify(
            {"data": {"message": "Email is required"}, "success": False}
        ), 400
    if not password:
        return jsonify(
            {"data": {"message": "Password is required"}, "success": False}
        ), 400
    if not first_name:
        return jsonify(
            {"data": {"message": "First Name is required"}, "success": False}
        ), 400
    if not last_name:
        return jsonify(
            {"data": {"message": "Last Name is required"}, "success": False}
        ), 400
    data_masuk["full_name"] = full_name
    create_user_repository(data_masuk.get("email"), data_masuk)
    return jsonify(
        {"data": {"message": f"{email} is registered"}, "success": True}
    ), 201


@app.route("/")
def index():
    return render_template("index.html", **dummy_users)


@app.route("/account")
def account_api():
    try:
        raise Exception("This is an exception")
    except Exception as e:
        return jsonify({"data": {"message": "account error"}, "success": False}), 400
    return jsonify({"data": {"apiKey": "ajshdkasgas2351sdfs"}, "success": True}), 200


@app.route("/users", methods=["GET", "POST", "PUT", "DELETE"])
def user_api():
    print("=" * 10, "METHOD -> ", request.method, "=" * 10)
    match request.method.lower():
        case "get":
            response = get_all_users()
            return jsonify({"data": response, "success": True}), 200
        case "post":
            return create_users(request.json)
        case "put":
            pass
        case "delete":
            pass

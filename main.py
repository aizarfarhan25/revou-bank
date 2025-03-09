import uuid

from flask import Flask, render_template, jsonify, request

from auth.login import login_required
from models.user import dummy_users
from router.auth import auth_router
from router.user import user_router

app = Flask(__name__)
app.register_blueprint(user_router)
app.register_blueprint(auth_router)


@app.before_request
def before_request():
    print("BEFORE REQUEST")
    print(request.method)


@app.after_request
def after_request(response):
    request_id = str(uuid.uuid4())
    response.headers["X-Request-ID"] = request_id
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/account", methods=["GET"])
@login_required
def account():
    print("ROUTE /account")
    user = getattr(request, "user", None)
    print(user)
    return jsonify({"data": {}, "success": True}), 200


@app.route("/")
def index():
    # return render_template("index.html", users=dummy_users["users"])
    return render_template("index.html", **dummy_users)


# @app.route("/account")
# def account_api():
#     try:
#         raise Exception("This is an exception")
#     except Exception as e:
#         return jsonify({"data": {"message": "account error"}, "success": False}), 400
#     return jsonify({"data": {"apiKey": "ajshdkasgas2351sdfs"}, "success": True}), 200

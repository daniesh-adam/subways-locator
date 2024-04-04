from flask import render_template, request, flash, redirect, current_app, abort, jsonify


from app.utils.database import get_all
from app.query_handler import QueryHandler


query_handler = QueryHandler(
    "sqlite:///" + current_app.config["DB_PATH"],
    current_app.config["FIREWORKS_API_KEY"]
)


@current_app.route("/", methods=["GET", "POST"])
@current_app.route("/index", methods=["GET", "POST"])
def main():

    if request.method == "POST":

        if "user-prompt" in request.form:
            user_prompt = request.form["user-prompt"]

            prompt_response = query_handler.get_response(
                question=user_prompt)

            return render_template("index.html", user_prompt=user_prompt,
                                   prompt_response=prompt_response)

    return render_template("index.html")


@current_app.route("/get-data", methods=["GET"])
def get_data():

    data = get_all(db_path=current_app.config["DB_PATH"], table_name="subway")
    return jsonify(data)

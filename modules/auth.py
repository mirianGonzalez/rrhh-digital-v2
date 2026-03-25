from flask import Blueprint, render_template, request, redirect, session
from database import get_db
import hashlib

auth_bp = Blueprint("auth", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = hash_password(request.form["password"])
        db = get_db()
        user = db.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND password=?",
            (usuario, password)
        ).fetchone()

        if user:
            session["usuario"] = usuario
            session["rol"] = user["rol"]
            return redirect("/panel_rrhh")  # lleva al panel
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
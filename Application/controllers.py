from functools import wraps
from flask import abort, redirect, render_template, request, session, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Info
from .database import db
from key_generator import aadhar_key, pan_key, driving_key, voter_key


def current_user():
    return User.query.get(session.get("user_id")) if session.get("user_id") else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user or user.type != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def owner_or_admin(user_id):
    user = current_user()
    if not user or (user.id != user_id and user.type != "admin"):
        abort(403)


@app.route("/")
def index():
    user = current_user()
    if user:
        return redirect(url_for("admin_dash") if user.type == "admin" else url_for("user_dashboard", user_id=user.id))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("admin_dash") if user.type == "admin" else url_for("user_dashboard", user_id=user.id))
        return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if len(username) < 3 or len(password) < 8 or not email:
            return render_template("Register.html", error="Username, email and an 8+ character password are required.")
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return render_template("Register.html", error="Username or email already registered.")
        db.session.add(User(username=username, email=email, password=generate_password_hash(password), type="general"))
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("Register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin")
@admin_required
def admin_dash():
    this_user = User.query.filter_by(type="admin").first()
    all_info = Info.query.order_by(Info.id.desc()).all()
    users = User.query.count()
    requests = Info.query.filter_by(attribute_name="Status", attribute_value="requested").count()
    generated = Info.query.filter_by(attribute_name="Status", attribute_value="generated").count()
    return render_template("admin_dashboard.html", this_user=this_user, all_info=all_info, users=users, requests=requests, generated=generated)


@app.route("/home/<int:user_id>")
@login_required
def user_dashboard(user_id):
    owner_or_admin(user_id)
    this_user = User.query.get_or_404(user_id)
    return render_template("user_dashboard.html", this_user=this_user)


@app.route("/request_card/<int:user_id>", methods=["GET", "POST"])
@login_required
def request_cards(user_id):
    owner_or_admin(user_id)
    if request.method == "POST":
        card = request.form.get("selectedcard", "").lower()
        if card not in {"aadhar", "pan", "driving", "voterid"}:
            abort(400)
        return redirect(url_for("card_details", card=card, user_id=user_id))
    return render_template("select.html", user_id=user_id)


@app.route("/request/<card>/<int:user_id>", methods=["GET", "POST"])
@login_required
def card_details(card, user_id):
    owner_or_admin(user_id)
    if card not in {"aadhar", "pan", "driving", "voterid"}:
        abort(404)
    this_user = User.query.get_or_404(user_id)
    if request.method == "POST":
        field_map = {
            "aadhar": ["Aadhar_name", "father_name", "gender", "dob", "Address"],
            "pan": ["pan_name", "father_name", "dob"],
            "driving": ["driving_license_name", "father_name", "dob", "Address", "pincode"],
            "voterid": ["voter_id_name", "ward_name", "gender", "dob"],
        }
        for name in field_map[card]:
            value = request.form.get(name, "").strip()
            if value:
                db.session.add(Info(attribute_name=name, attribute_value=value[:2000], card_name=card, user_id=user_id))
        db.session.add(Info(attribute_name="Status", attribute_value="requested", card_name=card, user_id=user_id))
        db.session.commit()
        return render_template("user_dashboard.html", this_user=this_user)
    template = {"aadhar": "Aadhar.html", "pan": "pan-card.html", "driving": "driving-license.html", "voterid": "voter-id.html"}[card]
    return render_template(template, user_id=user_id)


@app.route("/update_status/<card>/<int:user_id>", methods=["GET", "POST"])
@admin_required
def update_status(card, user_id):
    details = Info.query.filter_by(user_id=user_id, card_name=card).all()
    detail = Info.query.filter_by(user_id=user_id, card_name=card, attribute_name="Status").first_or_404()
    if request.method == "POST":
        status = request.form.get("status", "")
        if status not in {"requested", "under_verification", "verified", "rejected", "generated"}:
            abort(400)
        detail.attribute_value = status
        db.session.commit()
        return redirect(url_for("admin_dash"))
    return render_template("update_status.html", user_id=user_id, card=card, details=details)


@app.post("/generate/<card>/<int:user_id>")
@admin_required
def generate(card, user_id):
    detail = Info.query.filter_by(card_name=card, user_id=user_id, attribute_name="Status").first_or_404()
    detail.attribute_value = "generated"
    generator = {"aadhar": aadhar_key, "pan": pan_key, "driving": driving_key, "voterid": voter_key}.get(card)
    if not generator:
        abort(404)
    db.session.add(Info(card_name=card, user_id=user_id, attribute_name="key", attribute_value=str(generator())))
    db.session.commit()
    return redirect(url_for("admin_dash"))


@app.route("/view/<card>/<int:user_id>")
@login_required
def view_card(card, user_id):
    owner_or_admin(int(user_id))
    details = Info.query.filter_by(user_id=int(user_id), card_name=card).all()
    template = {"aadhar": "view_aadhar.html", "pan": "view_pan.html", "voterid": "view_voterid.html", "driving": "view_driving.html"}.get(card)
    if not template:
        abort(404)
    return render_template(template, details=details)


@app.route("/results")
@admin_required
def search():
    search_word = request.args.get("search", "").strip()
    key = request.args.get("key")
    if key == "user":
        results = User.query.filter(User.username.ilike(f"%{search_word}%")).all()
    else:
        results = Info.query.filter(Info.attribute_name == "Status", Info.card_name == (search_word.lower() if search_word else "")).all()
    return render_template("results.html", results=results, key=key)


@app.route("/summary")
@admin_required
def summary():
    cards = ["aadhar", "pan", "driving", "voterid"]
    statuses = ["requested", "under_verification", "verified", "generated"]
    matrix = {(card, status): Info.query.filter_by(attribute_name="Status", card_name=card, attribute_value=status).count() for card in cards for status in statuses}
    return render_template("summary.html", cards=cards, statuses=statuses, matrix=matrix)

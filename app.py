from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

from database import db, Complaint
from ai.predict import analyze_complaint


app = Flask(__name__)

# =========================================================
# APP CONFIGURATION
# =========================================================

app.secret_key = "resolveai-secret-key-change-this"

# Admin credentials - DEMO VERSION
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///duoverse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Create database tables
with app.app_context():
    db.create_all()


# =========================================================
# ADMIN AUTHENTICATION
# =========================================================

def admin_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return view_function(*args, **kwargs)

    return wrapped_view


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# SUBMIT COMPLAINT
# =========================================================

@app.route("/submit", methods=["POST"])
def submit_complaint():

    name = request.form["name"]
    email = request.form["email"]
    complaint_text = request.form["complaint"]

    # AI ANALYSIS
    result = analyze_complaint(complaint_text)

    # Create complaint record
    complaint = Complaint(
        name=name,
        email=email,
        complaint_text=complaint_text,
        category=result["category"],
        priority=result["priority"],
        priority_score=result["score"],
        department=result["department"],
        status="Submitted"
    )

    # Save to database
    db.session.add(complaint)
    db.session.commit()

    # Show AI result
    return render_template(
        "result.html",
        name=name,
        email=email,
        complaint=complaint_text,
        result=result
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    # If already logged in
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )

    return render_template("admin_login.html")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
@admin_required
def admin_dashboard():

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    # -----------------------------
    # BASIC STATISTICS
    # -----------------------------

    total_complaints = Complaint.query.count()

    high_priority = Complaint.query.filter(
        Complaint.priority.in_(["HIGH", "CRITICAL"])
    ).count()

    pending_complaints = Complaint.query.filter(
        Complaint.status.in_(["Submitted", "Pending"])
    ).count()

    resolved_complaints = Complaint.query.filter_by(
        status="Resolved"
    ).count()


    # -----------------------------
    # CATEGORY ANALYTICS
    # -----------------------------

    category_data = {}

    for complaint in complaints:

        category = complaint.category or "General"

        category_data[category] = (
            category_data.get(category, 0) + 1
        )


    # -----------------------------
    # PRIORITY ANALYTICS
    # -----------------------------

    priority_data = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for complaint in complaints:

        priority = complaint.priority

        if priority in priority_data:
            priority_data[priority] += 1


    # -----------------------------
    # DEPARTMENT ANALYTICS
    # -----------------------------

    department_data = {}

    for complaint in complaints:

        department = complaint.department or "Administration"

        department_data[department] = (
            department_data.get(department, 0) + 1
        )


    # -----------------------------
    # STATUS ANALYTICS
    # -----------------------------

    status_data = {}

    for complaint in complaints:

        status = complaint.status or "Submitted"

        status_data[status] = (
            status_data.get(status, 0) + 1
        )


    return render_template(
        "admin.html",

        complaints=complaints,

        total_complaints=total_complaints,

        high_priority=high_priority,

        pending_complaints=pending_complaints,

        resolved_complaints=resolved_complaints,

        category_data=category_data,

        priority_data=priority_data,

        department_data=department_data,

        status_data=status_data
    )

# =========================================================
# UPDATE COMPLAINT STATUS
# =========================================================

@app.route("/admin/update/<int:complaint_id>", methods=["POST"])
@admin_required
def update_status(complaint_id):

    complaint = Complaint.query.get_or_404(complaint_id)

    complaint.status = request.form["status"]

    db.session.commit()

    return redirect(url_for("admin_dashboard"))


# =========================================================
# DELETE COMPLAINT
# =========================================================

@app.route("/admin/delete/<int:complaint_id>", methods=["POST"])
@admin_required
def delete_complaint(complaint_id):

    complaint = Complaint.query.get_or_404(complaint_id)

    db.session.delete(complaint)

    db.session.commit()

    return redirect(url_for("admin_dashboard"))


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin_login"))

@app.route("/admin/complaint/<int:complaint_id>")
@admin_required
def complaint_details(complaint_id):

    complaint = Complaint.query.get_or_404(complaint_id)

    return render_template(
        "complaint_details.html",
        complaint=complaint
    )

# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)

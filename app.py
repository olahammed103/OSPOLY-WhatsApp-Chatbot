from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ospoly_chatbot.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-in-production")

db = SQLAlchemy(app)

# ---------------------- Models ----------------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class QA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False, unique=True)
    answer = db.Column(db.Text, nullable=False)

# ---------------------- Seed Data ----------------------
SEED_QA = [
    ("How do I apply for admission into OSPOLY?","You can apply by visiting the OSPOLY admission portal, filling the online application form, and paying the required fee."),
    ("What are the admission requirements for ND and HND programmes?","ND requires five O’level credits including English and Mathematics. HND requires ND with at least Lower Credit with one year industrial training or Pass grade with two year industrial training"),
    ("When is the OSPOLY admission form closing?","The closing date is usually announced on the school website. Please check regularly for updates."),
    ("How much is the application fee?","The application fee varies by programme. ND is usually ₦2,000 while HND is ₦20,000."),
    ("Can I apply for HND with a pass in ND?","No, a minimum of Lower Credit is required. However, some programmes may consider a Pass with two year industrial training experience."),
    ("How can I check my admission status?","You can check your admission status on the OSPOLY portal using your application number."),
    ("Is there a direct entry option into HND programmes?","No, HND applicants must have completed an ND programme."),
    ("Do you accept candidates who did not choose OSPOLY in JAMB?","Yes, but you must do a change of institution on the JAMB portal."),
    ("What documents are required for screening?","You will need your O’level results, ND certificate (for HND), JAMB result slip, birth certificate, and state of origin certificate."),
    ("How do I print my admission letter?","Login to the OSPOLY portal, go to Admission Status, and print your admission letter."),
    ("How much is the school fees for ND students?","The school fees for ND students is between ₦95,000 and ₦117,500 depending on the department."),
    ("What is the school fees for HND students?","The school fees for HND students is between ₦100,000 and ₦117,500 depending on the department."),
    ("Can I pay my fees in installments?","Yes, students are allowed to pay in two installments."),
    ("How do I generate payment invoice online?","Login to the OSPOLY portal, click on ‘Payments’, and generate your invoice."),
    ("What happens if I don’t pay school fees on time?","You may not be allowed to register courses or sit for examinations."),
    ("Is there a penalty for late payment?","Yes, a late payment fee is applied after the deadline."),
    ("How do I confirm my payment after making it online?","Login to the portal and check your payment status. You can also print your payment receipt."),
    ("What are the available courses in OSPOLY?","OSPOLY offers ND and HND courses in Engineering, Sciences, Business, Arts, and Communication Studies."),
    ("How do I check my exam timetable?","Exam timetables are available on the student portal and departmental notice boards."),
    ("When will the semester exams start?","The exam dates are usually announced by the school and uploaded on the portal."),
    ("How do I access the academic calendar?","The academic calendar can be downloaded from the OSPOLY portal or collected at the academic office."),
    ("What is the grading system in OSPOLY?","Grades are based on GPA system: A=4.00, B=3.00, C=2.00, D=1.00, F=0.00."),
    ("How many semesters are there in a session?","There are two semesters in each academic session."),
    ("How do I apply for a change of course?","You can apply at the registrar’s office with valid reasons and supporting documents."),
    ("How can I check my results online?","Login to the OSPOLY portal, navigate to ‘Results’, and select the semester to view your results."),
    ("What should I do if I forget my portal password?","Click on ‘Forgot Password’ on the portal and follow the reset instructions."),
    ("How do I register my courses on the portal?","Login to your student portal, go to Course Registration, select courses, and submit."),
    ("What happens if I miss course registration?","You may not be allowed to take exams for unregistered courses."),
    ("How do I correct errors in my portal profile?","Visit the ICT center or contact support through the portal."),
    ("Can I access my portal on my phone?","Yes, the portal is mobile-friendly and can be accessed on any smartphone."),
    ("How do I retrieve my portal login details?","Visit the ICT center with proof of identity to recover your login details."),
    ("Does OSPOLY provide hostel accommodation?","Yes, hostel accommodation is available for students."),
    ("How do I apply for a hostel bed space?","Login to the student portal and apply under Accommodation."),
    ("What is the hostel fee?","Hostel fees range from ₦15,000 to ₦25,000 depending on the type of room."),
    ("Are there separate hostels for male and female students?","Yes, there are separate hostels for male and female students."),
    ("Can I stay off-campus as a student?","Yes, students are allowed to live off-campus."),
    ("Is there a student union in OSPOLY?","Yes, OSPOLY has a Student Union Government (SUG)."),
    ("How do I get an ID card?","You can get your student ID card after completing registration and payment."),
    ("Does OSPOLY have a medical centre?","Yes, the school has a medical centre that attends to students and staff."),
    ("What clubs and associations are available?","There are academic, religious, cultural, and social clubs available for students."),
    ("How do I report issues like missing grades or harassment?","You should report such issues to your Head of Department or the Dean of Students."),
    ("How do I get an exam clearance slip?","You can obtain it from the portal after completing registration and paying necessary fees."),
    ("What happens if I miss an exam?","You may have to carry over the course unless you have a valid reason approved by the school."),
    ("Can I apply for a carryover in a failed course?","Yes, you will automatically retake failed courses in the next session."),
    ("What is the process for final year clearance?","Final year clearance is done at the bursary, library, department, and student affairs before graduation."),
    ("Where is OSPOLY located?","OSPOLY is located in Iree, Osun State, Nigeria."),
    ("What are the official contact numbers of OSPOLY?","The official contact numbers are available on the school’s website."),
    ("How do I reach the ICT helpdesk?","You can visit the ICT center within the campus or contact them via the portal."),
    ("When does the new academic session start?","The new academic session usually starts in October/November."),
    ("Does OSPOLY accept part-time students?","Yes, OSPOLY offers part-time and daily part-time programmes."),
]

def seed_db():
    # Create default admin if none
    if Admin.query.count() == 0:
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Created default admin: username='admin', password='admin123'")

    # Seed QAs if empty
    if QA.query.count() == 0:
        for q, a in SEED_QA:
            db.session.add(QA(question=q.strip(), answer=a.strip()))
        db.session.commit()
        app.logger.info("Seeded initial Q&A items.")

with app.app_context():
    db.create_all()

# ---------------------- Helpers ----------------------
def is_logged_in():
    return session.get("admin_user") is not None

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            flash("Please log in as admin.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper

# ---------------------- Routes ----------------------
@app.route("/")
def index():
    all_qas = QA.query.order_by(QA.id.asc()).all()
    return render_template("index.html", qas=all_qas)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"answer": "Please enter a question."})
    # Exact match first
    qa = QA.query.filter(QA.question.ilike(question)).first()
    if not qa:
        # fallback: naive contains search picking the first match
        qa = QA.query.filter(QA.question.ilike(f"%{question}%")).first()
    if qa:
        return jsonify({"answer": qa.answer})
    return jsonify({"answer": "Sorry, I couldn't find an answer. Please try a different question or contact the ICT helpdesk."})

# -------- Admin Auth --------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session["admin_user"] = admin.username
            flash("Welcome admin!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_user", None)
    flash("Logged out.", "info")
    return redirect(url_for("admin_login"))

# -------- Admin CRUD --------
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()
        if question and answer:
            if QA.query.filter(QA.question.ilike(question)).first():
                flash("A QA with this exact question already exists.", "warning")
            else:
                db.session.add(QA(question=question, answer=answer))
                db.session.commit()
                flash("Q&A added.", "success")
        else:
            flash("Both question and answer are required.", "warning")
        return redirect(url_for("admin_dashboard"))
    qas = QA.query.order_by(QA.id.asc()).all()
    return render_template("admin_dashboard.html", qas=qas)

@app.route("/admin/edit/<int:qa_id>", methods=["GET", "POST"])
@login_required
def admin_edit(qa_id):
    qa = QA.query.get_or_404(qa_id)
    if request.method == "POST":
        qa.question = request.form.get("question", "").strip()
        qa.answer = request.form.get("answer", "").strip()
        db.session.commit()
        flash("Q&A updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_qa.html", qa=qa)

@app.route("/admin/delete/<int:qa_id>", methods=["POST"])
@login_required
def admin_delete(qa_id):
    qa = QA.query.get_or_404(qa_id)
    db.session.delete(qa)
    db.session.commit()
    flash("Q&A deleted.", "info")
    return redirect(url_for("admin_dashboard"))

# ---------------------- CLI init ----------------------
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database and seed with defaults."""
    db.create_all()
    seed_db()
    print("Database initialized and seeded.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash
)

import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)

app.secret_key = "biswo-software-secret-key"

DATABASE = "database.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =====================================================
# INITIALIZE DATABASE
# =====================================================

def init_db():

    db = get_db()

    # Users table
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Contact enquiries table
    db.execute("""
        CREATE TABLE IF NOT EXISTS contact_enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            service TEXT,
            budget TEXT,
            message TEXT,
            consent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
    db.close()


# =====================================================
# AI CHATBOT
# =====================================================

def chatbot_response(message):

    message = message.lower().strip()

    if not message:
        return "Please enter your question."


    # =================================================
    # GREETING
    # =================================================

    if any(word in message for word in [
        "hello",
        "hi",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return (
            "Hello! 👋 Welcome to BISWO Software. "
            "I am your team assistant. "
            "How can I help you today?"
        )


    # =================================================
    # ABOUT BISWO
    # =================================================

    if any(keyword in message for keyword in [
        "about biswo",
        "who are you",
        "what is biswo",
        "tell me about biswo",
        "biswo software"
    ]):
        return (
            "BISWO Software is a software development company "
            "focused on web development, mobile applications, "
            "UI/UX design, AI solutions, cloud deployment and "
            "technical support."
        )


    # =================================================
    # BUSINESS / E-COMMERCE
    # =================================================

    if any(keyword in message for keyword in [
        "business",
        "ecommerce",
        "e-commerce",
        "shopping",
        "online store",
        "shop"
    ]):
        return (
            "BISWO Software provides business and e-commerce "
            "website solutions, including online stores, "
            "product catalogues, shopping features and "
            "custom business systems."
        )


    # =================================================
    # HOTEL / RESTAURANT
    # =================================================

    if any(keyword in message for keyword in [
        "hotel",
        "restaurant",
        "food",
        "booking system"
    ]):
        return (
            "BISWO Software can help create modern hotel and "
            "restaurant websites with menus, booking systems, "
            "online services and responsive designs."
        )


    # =================================================
    # HOSPITAL / MEDICAL
    # =================================================

    if any(keyword in message for keyword in [
        "hospital",
        "medical",
        "healthcare",
        "clinic"
    ]):
        return (
            "BISWO Software can develop healthcare and hospital "
            "websites with modern interfaces and useful online "
            "features."
        )


    # =================================================
    # GOVERNMENT
    # =================================================

    if any(keyword in message for keyword in [
        "government",
        "govt",
        "public service"
    ]):
        return (
            "BISWO Software can develop information and service "
            "websites for organizations and public-facing services."
        )


    # =================================================
    # AI
    # =================================================

    if (
        "artificial intelligence" in message
        or " ai " in f" {message} "
        or message == "ai"
    ):
        return (
            "BISWO Software can develop AI-powered website "
            "features, chatbots, automation systems and "
            "AI integrations based on project requirements."
        )


    # =================================================
    # SOFTWARE DEVELOPMENT
    # =================================================

    if any(keyword in message for keyword in [
        "software development",
        "software developer",
        "custom software",
        "application software"
    ]):
        return (
            "BISWO Software provides customized software "
            "development solutions designed around specific "
            "business and project requirements."
        )


    # =================================================
    # WEB DEVELOPMENT
    # =================================================

    if any(keyword in message for keyword in [
        "website",
        "web site",
        "websites",
        "web development",
        "web design"
    ]):
        return (
            "BISWO Software can create modern, responsive "
            "websites based on your requirements, including "
            "business websites, e-commerce websites and "
            "custom web applications."
        )


    # =================================================
    # MOBILE APP
    # =================================================

    if any(keyword in message for keyword in [
        "mobile app",
        "mobile application",
        "android app",
        "ios app",
        "app development"
    ]):
        return (
            "BISWO Software provides mobile application "
            "development solutions for modern digital products."
        )


    # =================================================
    # UI / UX
    # =================================================

    if any(keyword in message for keyword in [
        "ui ux",
        "ui/ux",
        "ui design",
        "ux design",
        "user interface",
        "user experience"
    ]):
        return (
            "Our UI/UX service focuses on clean interfaces, "
            "user-friendly experiences, responsive layouts, "
            "wireframes and prototypes."
        )


    # =================================================
    # CLOUD
    # =================================================

    if any(keyword in message for keyword in [
        "cloud",
        "deployment",
        "server",
        "hosting"
    ]):
        return (
            "BISWO Software provides cloud and deployment "
            "services including application deployment, "
            "server configuration, deployment automation "
            "and maintenance."
        )


    # =================================================
    # MAINTENANCE / SUPPORT
    # =================================================

    if any(keyword in message for keyword in [
        "maintenance",
        "support",
        "technical support",
        "bug fixing",
        "website update"
    ]):
        return (
            "BISWO Software provides website maintenance, "
            "bug fixing, performance improvements, updates "
            "and technical support."
        )


    # =================================================
    # SERVICES
    # =================================================

    if "service" in message or "services" in message:

        return (
            "Our main services include:\n"
            "• Web Development\n"
            "• Mobile App Development\n"
            "• UI/UX Design\n"
            "• AI & Automation\n"
            "• Cloud & Deployment\n"
            "• Maintenance & Support"
        )


    # =================================================
    # CONTACT
    # =================================================

    if any(keyword in message for keyword in [
        "contact",
        "contact us",
        "reach you",
        "talk to team"
    ]):
        return (
            "You can contact BISWO Software through our "
            "Contact Us page. You can also submit your "
            "project requirements through the contact form."
        )


    # =================================================
    # LOCATION
    # =================================================

    if any(keyword in message for keyword in [
        "location",
        "address",
        "where are you",
        "where is biswo",
        "office"
    ]):
        return (
            "You can find BISWO Software location information "
            "on our Location page."
        )


    # =================================================
    # CAREERS
    # =================================================

    if any(keyword in message for keyword in [
        "career",
        "careers",
        "job",
        "jobs",
        "vacancy",
        "work with you"
    ]):
        return (
            "Please visit our Careers page to learn about "
            "opportunities and future openings at BISWO Software."
        )


    # =================================================
    # PRICING
    # =================================================

    if any(keyword in message for keyword in [
        "price",
        "pricing",
        "cost",
        "how much",
        "budget"
    ]):
        return (
            "Project pricing depends on the required features, "
            "technology, design and development scope. "
            "Please contact BISWO Software with your requirements "
            "for a project discussion."
        )


    # =================================================
    # THANKS
    # =================================================

    if any(word in message for word in [
        "thank",
        "thanks",
        "thank you"
    ]):
        return "You're welcome! 😊"


    # =================================================
    # GOODBYE
    # =================================================

    if any(word in message for word in [
        "bye",
        "goodbye",
        "see you"
    ]):
        return "Goodbye! 👋 Take care."


    # =================================================
    # DEFAULT
    # =================================================

    return (
        "I can help with information about BISWO Software, "
        "our services, web development, mobile apps, UI/UX, "
        "AI solutions, cloud deployment, maintenance, "
        "careers and contact information."
    )


# =====================================================
# HOME
# =====================================================

@app.route("/")
def index():
    return render_template("index.html")


# =====================================================
# HOME ALIAS
# =====================================================
# This prevents BuildError if an older template still
# contains url_for('home').

@app.route("/home")
def home():
    return redirect(url_for("index"))


# =====================================================
# ABOUT
# =====================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =====================================================
# SERVICES
# =====================================================

@app.route("/services")
def services():
    return render_template("services.html")


# =====================================================
# WEB DEVELOPMENT
# =====================================================

@app.route("/services/web-development")
def web_development():
    return render_template("web-development.html")


# =====================================================
# MOBILE APP DEVELOPMENT
# =====================================================

@app.route("/services/mobile-app-development")
def mobile_app_development():
    return render_template("mobile-app-development.html")


# =====================================================
# UI / UX DESIGN
# =====================================================

@app.route("/services/ui-ux-design")
def ui_ux_design():
    return render_template("ui-ux-design.html")


# =====================================================
# AI & AUTOMATION
# =====================================================

@app.route("/services/ai-automation")
def ai_automation():
    return render_template("ai-automation.html")


# =====================================================
# CLOUD & DEPLOYMENT
# =====================================================

@app.route("/services/cloud-deployment")
def cloud_deployment():
    return render_template("cloud-deployment.html")


# =====================================================
# MAINTENANCE & SUPPORT
# =====================================================

@app.route("/services/maintenance-support")
def maintenance_support():
    return render_template("maintenance-support.html")


# =====================================================
# AI CHATBOT PAGE
# =====================================================

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


# =====================================================
# AI CHAT API
# =====================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    response = chatbot_response(message)

    return jsonify({
        "response": response
    })


# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember")

        if not email or not password:

            flash(
                "Please enter your email and password.",
                "error"
            )

            return redirect(url_for("login"))

        db = get_db()

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        db.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            if remember:
                session.permanent = True
            else:
                session.permanent = False

            flash(
                "Login successful!",
                "success"
            )

            return redirect(url_for("index"))

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(url_for("login"))

    return render_template("login.html")


# =====================================================
# REGISTER
# =====================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            flash(
                "Please fill in all required fields.",
                "error"
            )

            return redirect(url_for("register"))

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(url_for("register"))

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        db = get_db()

        try:

            db.execute(
                """
                INSERT INTO users (
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    password_hash
                )
            )

            db.commit()

        except sqlite3.IntegrityError:

            db.close()

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(url_for("register"))

        db.close()

        flash(
            "Account created successfully. Please login.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("register.html")


# =====================================================
# FORGOT PASSWORD
# =====================================================

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        if not email:

            flash(
                "Please enter your email address.",
                "error"
            )

            return redirect(url_for("forgot_password"))

        # Password reset email/token system can be added later.
        # For now, return a generic message.

        flash(
            "If an account exists for this email, "
            "password reset instructions can be sent.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("forgot-password.html")


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("login"))


# =====================================================
# SUPPORT
# =====================================================

@app.route("/support")
def support():
    return render_template("support.html")


# =====================================================
# CONTACT
# =====================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        service = request.form.get(
            "service",
            ""
        ).strip()

        budget = request.form.get(
            "budget",
            ""
        ).strip()

        message = request.form.get(
            "message",
            ""
        ).strip()

        consent = request.form.get(
            "consent",
            ""
        )

        if not name or not email or not message:

            flash(
                "Please fill in the required fields.",
                "error"
            )

            return redirect(url_for("contact"))

        db = get_db()

        db.execute(
            """
            INSERT INTO contact_enquiries (
                name,
                email,
                phone,
                service,
                budget,
                message,
                consent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                phone,
                service,
                budget,
                message,
                consent
            )
        )

        db.commit()
        db.close()

        flash(
            "Thank you! Your project enquiry has been submitted.",
            "success"
        )

        return redirect(url_for("contact"))

    return render_template("contact.html")


# =====================================================
# LOCATION
# =====================================================

@app.route("/location")
def location():
    return render_template("location.html")


# =====================================================
# BLOGS
# =====================================================

@app.route("/blogs")
def blogs():
    return render_template("blogs.html")


# =====================================================
# CAREERS
# =====================================================

@app.route("/careers")
def careers():
    return render_template("careers.html")


# =====================================================
# AWARDS
# =====================================================

@app.route("/awards")
def awards():
    return render_template("awards.html")


# =====================================================
# MEDIA
# =====================================================

@app.route("/media")
def media():
    return render_template("media.html")


# =====================================================
# FEEDBACK
# =====================================================

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


# =====================================================
# BRAND COLLABORATION
# =====================================================

@app.route("/brand-collaboration")
def brand_collaboration():
    return render_template("brand_collaboration.html")


# =====================================================
# 404 ERROR
# =====================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# =====================================================
# START APPLICATION
# =====================================================

# Initialize database when Flask starts.
# This also works when using "flask run".

init_db()


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )




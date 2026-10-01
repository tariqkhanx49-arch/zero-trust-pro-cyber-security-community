from flask import Flask,render_template,request,redirect,url_for,session,flash,abort
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash,generate_password_hash
from pathlib import Path
app=Flask(__name__); app.secret_key="ztp-local-demo-secret"
UPLOAD=Path("static/uploads"); UPLOAD.mkdir(parents=True,exist_ok=True)
USERNAME="Tariq"; PASSWORD="ZTP0123"
courses=[
{"name":"Cloud Fundamentals","short":"CF","progress":95,"status":"Almost Complete","description":"Cloud concepts, service models, virtualization, IAM, cloud networking, storage and cloud security.","modules":["Cloud Concepts","IaaS / PaaS / SaaS","Cloud Networking","Identity & Access","Cloud Security"]},
{"name":"Cyber Security Fundamental","short":"CS","progress":100,"status":"Completed","description":"Core cybersecurity concepts covering threats, vulnerabilities, controls, risk, authentication and security operations.","modules":["Security Principles","Threats & Vulnerabilities","Authentication","Risk Management","Security Operations"]},
{"name":"Networking","short":"NW","progress":89,"status":"In Progress","description":"OSI/TCP-IP, IPv4, subnetting, switching, routing, DNS and network troubleshooting.","modules":["OSI & TCP/IP","IPv4 & Subnetting","Switching","Routing","Network Troubleshooting"]},
{"name":"Blue Team / SOC","short":"SOC","progress":90,"status":"In Progress","description":"Defensive security and SOC operations including monitoring, alert triage, logs, incident response and threat detection.","modules":["SOC Fundamentals","Log Analysis","Alert Triage","Incident Response","Threat Detection"]}]
def logged(): return session.get("logged_in") is True
def allowed(f): return f and "." in f and f.rsplit(".",1)[1].lower() in {"png","jpg","jpeg","webp"}
@app.route("/")
def home(): return redirect(url_for("dashboard")) if logged() else render_template("login.html")
@app.post("/login")
def login():
    if request.form.get("username")==USERNAME and request.form.get("password")==PASSWORD:
        session.clear(); session.update(logged_in=True,username=USERNAME); return redirect(url_for("dashboard"))
    flash("Invalid username or password."); return redirect(url_for("home"))
@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("home"))
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",courses=courses) if logged() else redirect(url_for("home"))
@app.route("/course/<int:i>")
def course(i):
    if not logged(): return redirect(url_for("home"))
    if i<0 or i>=len(courses): return redirect(url_for("dashboard"))
    return render_template("course.html",course=courses[i],course_id=i)
@app.route("/profile")
def profile():
    if not logged(): return redirect(url_for("home"))
    logo=next(iter(UPLOAD.glob("logo.*")),None); student=next(iter(UPLOAD.glob("student.*")),None)
    return render_template("profile.html",courses=courses,logo_url=url_for("static",filename=f"uploads/{logo.name}") if logo else None,student_url=url_for("static",filename=f"uploads/{student.name}") if student else None)
@app.post("/profile/upload")
def upload():
    if not logged(): return redirect(url_for("home"))
    kind=request.form.get("asset_type"); f=request.files.get("file")
    if kind not in {"logo","student"} or not f or not allowed(f.filename): flash("Choose a PNG, JPG, JPEG or WEBP image."); return redirect(url_for("profile"))
    ext=f.filename.rsplit(".",1)[1].lower()
    for old in UPLOAD.glob(f"{kind}.*"): old.unlink(missing_ok=True)
    f.save(UPLOAD/secure_filename(f"{kind}.{ext}")); flash("Image uploaded successfully."); return redirect(url_for("profile"))
if __name__=="__main__": app.run(debug=False,host="127.0.0.1",port=5000)

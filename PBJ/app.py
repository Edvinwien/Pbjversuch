from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors 
from twilio.rest import Client
import re
import os


app = Flask(__name__)
app.secret_key = 'dein_geheimer_schlüssel'  # Ändere dies auf einen zufälligen, sicheren Schlüssel


account_sid = 'AC6fa1be1ed8099720c12436a95f92eeaf'
auth_token = ''
client = Client(account_sid, auth_token)


def getHostnameViaEnv():
    if "MYSQL_HOST" in os.environ:
        return os.environ['MYSQL_HOST']
    else:
        return "127.0.0.1"

app.config['MYSQL_HOST'] = getHostnameViaEnv()  # 'db' ist der Name des DB-Services im Docker-Setup
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root_password'
app.config['MYSQL_DB'] = 'user_system'

mysql = MySQL(app)


# Setze einen geheimen Schlüssel, um Sessions zu ermöglichen


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    mesage = ""
    if request.method == "POST" and "email" in request.form and "password" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user["password"], password):
            session["loggedin"] = True
            session["userid"] = user["userid"]
            session["name"] = user["name"]
            session["email"] = user["email"]
            mesage = "Login abgeschlossen"
            return render_template("impressum.html", mesage=mesage)
        else:
            mesage = "Richtige Email oder Paswort verwenden"
    return render_template("login.html", mesage=mesage)


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("userid", None)
    session.pop("email", None)
    return redirect(url_for("login"))
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    mesage = ""
    if request.method == "POST" and "name" in request.form and "password" in request.form and "email" in request.form:
        userName = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        account = cursor.fetchone()
        if account:
            mesage = "Account already exists"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            mesage = "Invalid email address"
        elif not userName or not password or not email:
            mesage = "Bitte alle Felder füllen"
        else:
            password_hash = generate_password_hash(password)
            cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (userName, email, password_hash,))
            mysql.connection.commit()
            mesage = "Erfolgreich Regestriert"
    elif request.method == "POST":
        mesage = "Bitte alle Felder füllen"
    return render_template("register.html", mesage=mesage)


@app.route('/patienthinzu', methods=['GET', 'POST']) 
def patient_hinzufuegen():
    if "loggedin" in session:
        message = ""
        if request.method == "POST":
            name = request.form.get("name")
            age = request.form.get("age")
            email = request.form.get("email")
            address = request.form.get("address")
            telefonnummer = request.form.get("telefonnummer")
            
            if name and age and email and address and telefonnummer:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                    "INSERT INTO patients (name, age, email, address, telefonnummer, userid) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, age, email, address, telefonnummer, session["userid"]),
                )
                mysql.connection.commit()
                message = "Patient erfolgreich hinzugefügt!"
            else:
                message = "Bitte alle Felder ausfüllen!"
        return render_template("patienthinzu.html", message=message)   
    return redirect(url_for('login'))


@app.route("/patiensuche", methods=["GET", "POST"])
def patienten_liste():
    if "loggedin" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session["userid"]

        # Löschanfrage behandeln
        if request.method == "POST" and "delete" in request.form:
            patient_id = request.form.get("patient_id")
            if patient_id:
                # Lösche den Patienten aus der Datenbank
                delete_query = "DELETE FROM user_system.patients WHERE id = %s AND userid = %s"
                cursor.execute(delete_query, (patient_id, user_id))
                mysql.connection.commit()
        
        # Suchanfrage oder Standardanzeige
        if request.method == "POST" and "search" in request.form:
            search_query = request.form.get('search', '')
            if search_query:
                query = "SELECT * FROM user_system.patients WHERE name LIKE %s AND userid = %s"
                cursor.execute(query, ("%" + search_query + "%", user_id))
            else:
                cursor.execute("SELECT * FROM user_system.patients WHERE userid = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM user_system.patients WHERE userid = %s", (user_id,))

        patients = cursor.fetchall()

        return render_template("patiensuche.html", patients=patients, search_query=request.form.get('search', ''))
    return redirect(url_for("login"))


@app.route("/main")
def Main():
    return render_template("Main.html")

@app.route("/patienthinzu")
def patient_hinzu():
    return render_template("patienthinzu.html")

@app.route("/andern", methods=["GET", "POST"])
def andern():
    if "loggedin" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session["userid"]
        selected_patient = None

        # Wenn es sich um einen GET-Request handelt und die `patient_id` in der URL übergeben wird
        if request.method == "GET":
            patient_id = request.args.get("patient_id")  # Holen des `patient_id`-Werts aus der URL
            if patient_id:
                cursor.execute(
                    "SELECT * FROM user_system.patients WHERE userid = %s AND id = %s",
                    (user_id, patient_id),
                )
                selected_patient = cursor.fetchone()  # Wähle den entsprechenden Patienten

        if request.method == "POST":
            action = request.form["action"]

            if action == "select":
                patient_id = request.form["patient_id"]
                cursor.execute(
                    "SELECT * FROM user_system.patients WHERE userid = %s AND id = %s",
                    (user_id, patient_id),
                )
                selected_patient = cursor.fetchone()

            elif action == "update":
                patient_id = request.form["id"]
                name = request.form["name"]
                age = request.form["age"]
                email = request.form["email"]
                address = request.form["address"]
                symptome = request.form["symptome"]
                medikamente = request.form["medikamente"]
                telefonnummer = request.form["telefonnummer"]

                cursor.execute(
                    """
                    UPDATE patients 
                    SET name = %s, age = %s, email = %s, address = %s, symptome = %s, medikamente = %s, telefonnummer = %s 
                    WHERE id = %s
                    """,
                    (name, age, email, address, symptome, medikamente, telefonnummer, patient_id),
                )
                mysql.connection.commit()

                # Nach dem Update zur Patientensuche umleiten
                return redirect(url_for("patienten_liste"))

        # Lade alle Patienten für die Übersicht
        cursor.execute("SELECT * FROM user_system.patients WHERE userid = %s", (user_id,))
        patients = cursor.fetchall()

        return render_template("andern.html", patients=patients, selected_patient=selected_patient)

    return redirect(url_for("login"))


@app.route("/Medikamentesuchen", methods=["GET", "POST"])
def medikamente_suchen():
    if "loggedin" in session:
        message = ""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Medikament löschen
        if request.method == "POST" and "delete_id" in request.form:
            delete_id = request.form["delete_id"]
            cursor.execute("DELETE FROM m_medikamente WHERE m_id = %s", (delete_id,))
            mysql.connection.commit()
            message = "Medikament erfolgreich gelöscht!"

        # Medikament hinzufügen
        if request.method == "POST" and not "delete_id" in request.form:
            m_name = request.form.get("m_name")
            m_hersteller = request.form.get("m_hersteller")
            m_dosis = request.form.get("m_dosis")

            if m_name and m_hersteller and m_dosis:
                cursor.execute(
                    "INSERT INTO m_medikamente (m_name, m_hersteller, m_dosis) VALUES(%s, %s, %s)",
                    (m_name, m_hersteller, m_dosis),
                )
                mysql.connection.commit()
                message = "Medikament erfolgreich hinzugefügt!"
            else:
                message = "Bitte alle Felder ausfüllen!"

        # Medikamentensuche
        if request.method == "POST" and "search" in request.form:
            search_query = request.form.get("search", "")
            query = "SELECT * FROM m_medikamente WHERE m_name LIKE %s"
            cursor.execute(query, ("%" + search_query + "%",))
        else:
            cursor.execute("SELECT * FROM m_medikamente")

        m_medikamente = cursor.fetchall()
        return render_template("Medikamentesuchen.html", m_medikamente=m_medikamente, message=message)
    return redirect(url_for("login"))


from datetime import datetime, timedelta
from pytz import timezone, utc

@app.route("/sms", methods=["GET", "POST"])
def sms():
    if "loggedin" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Medikamenten-Daten immer abrufen
    cursor.execute("SELECT m_id, m_name FROM m_medikamente")
    medikamente = cursor.fetchall()

    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        medikament_id = request.form.get("medikament")  # Geänderte Variable
        sms_dates = request.form.getlist("sms_dates[]")
        sms_times = request.form.getlist("sms_times[]")

        if patient_id:
            cursor.execute("SELECT telefonnummer FROM patients WHERE id = %s", (patient_id,))
            patient = cursor.fetchone()
            if patient:
                telefonnummer = patient['telefonnummer']
            else:
                return "Patient nicht gefunden.", 404
        else:
            return "Keine Patient-ID angegeben.", 400

        # Überprüfen, ob die Telefonnummer ein gültiges internationales Format hat
        if not re.match(r"^\+\d{10,15}$", telefonnummer):
            return "Ungültige Telefonnummer. Bitte im internationalen Format eingeben (z. B. +4915123456789).", 400

        # SMS-Zeitplan validieren
        if not sms_dates or not sms_times or len(sms_dates) != len(sms_times):
            return "Ungültiger SMS-Zeitplan. Bitte überprüfen Sie die Daten.", 400

        # Lokale Zeitzone (z. B. Europa/Berlin)
        local_tz = timezone("Europe/Berlin")

        # Medikamentenname aus der Datenbank abrufen
        cursor.execute("SELECT m_name FROM m_medikamente WHERE m_id = %s", (medikament_id,))
        medikament_row = cursor.fetchone()
        if not medikament_row:
            return "Ungültige Medikamenten-ID.", 400
        medikament = medikament_row["m_name"]

        # SMS planen
        for date, time in zip(sms_dates, sms_times):
            local_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            local_dt_with_tz = local_tz.localize(local_dt)
            send_at_utc = local_dt_with_tz.astimezone(utc)

            sms_body = (
                f"Erinnerung: Bitte nehmen Sie Ihr Medikament '{medikament}' "
                f"entsprechend dem Zeitplan: {date} um {time}."
            )

            try:
                message = client.messages.create(
                    messaging_service_sid="MG4dd2c7fa5a663a3f9f56203495e59392",
                    schedule_type="fixed",
                    send_at=send_at_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    from_="+16282096510",
                    body=sms_body,
                    to=telefonnummer
                )
                print(f"SMS gesendet: {message.sid}")
            except Exception as sms_error:
                print(f"Fehler beim Senden der SMS: {sms_error}")
                return f"Fehler beim Senden der SMS: {sms_error}", 500

        # Nach erfolgreichem Planen zur Patientensuche weiterleiten
        return render_template("Main.html")

    return render_template("sms.html", medikamente=medikamente)



@app.route("/impressum")
def impressum():
    return render_template("impressum.html") 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


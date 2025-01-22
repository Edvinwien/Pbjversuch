import unittest
from app import app, mysql  # Flask-App und MySQL-Instanz importieren

class TestApp(unittest.TestCase):
    def setUp(self):
        # Flask-Anwendung für Tests vorbereiten
        self.app = app.test_client()
        self.app.testing = True

        # Datenbankverbindung herstellen
        cursor = mysql.connection.cursor()

        # Tabellen erstellen und Testdaten hinzufügen
        self.create_tables(cursor)
        self.insert_test_data(cursor)

    def tearDown(self):
        # Datenbank zurücksetzen
        cursor = mysql.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS patients;")
        cursor.execute("DROP TABLE IF EXISTS m_medikamente;")
        cursor.execute("DROP TABLE IF EXISTS user;")
        mysql.connection.commit()

    def create_tables(self, cursor):
        # Tabellen erstellen
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            userid INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS m_medikamente (
            m_id INT AUTO_INCREMENT PRIMARY KEY,
            m_name VARCHAR(255),
            m_hersteller VARCHAR(255),
            m_dosis VARCHAR(255)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            email VARCHAR(255),
            address VARCHAR(255),
            telefonnummer VARCHAR(20),
            symptome TEXT,
            medikamente TEXT,
            userid INT,
            FOREIGN KEY (userid) REFERENCES user(userid)
        );
        """)
        mysql.connection.commit()

    def insert_test_data(self, cursor):
        # Beispielbenutzer einfügen
        cursor.execute("""
        INSERT INTO user (name, email, password) 
        VALUES ('TestUser', 'testuser@example.com', 'password123');
        """)

        # Beispielmedikamente einfügen
        cursor.execute("""
        INSERT INTO m_medikamente (m_name, m_hersteller, m_dosis) 
        VALUES ('Aspirin', 'Bayer', '100mg');
        """)

        # Beispielpatienten einfügen
        cursor.execute("""
        INSERT INTO patients (name, age, email, address, telefonnummer, symptome, medikamente, userid)
        VALUES ('Max Mustermann', 30, 'max@example.com', 'Musterstr. 1', '+123456789', 'Fieber', 'Aspirin', 1);
        """)
        mysql.connection.commit()

    def test_register_user(self):
        response = self.app.post('/register', data=dict(
            name='New User', email='newuser@example.com', password='securepassword'
        ))
        self.assertIn(b'Erfolgreich Registriert', response.data)

    def test_login_user(self):
        response = self.app.post('/login', data=dict(
            email='testuser@example.com', password='password123'
        ))
        self.assertIn(b'Login abgeschlossen', response.data)

    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(
            email='wronguser@example.com', password='wrongpassword'
        ))
        self.assertIn(b'Richtige Email oder Passwort verwenden', response.data)

    def test_add_patient(self):
        # Logge den Testbenutzer ein
        self.app.post('/login', data=dict(
            email='testuser@example.com', password='password123'
        ))

        response = self.app.post('/patienthinzu', data=dict(
            name='Anna Schmidt', age=40, email='anna@example.com',
            address='Schmidtstr. 5', telefonnummer='+987654321'
        ))
        self.assertIn('Patient erfolgreich hinzugefügt!', response.data)

    def test_sms_sending(self):
        # Logge den Testbenutzer ein
        self.app.post('/login', data=dict(
            email='testuser@example.com', password='password123'
        ))

        response = self.app.post('/sms', data=dict(
            patient_id=1, medikament=1,
            sms_dates=['2025-01-20'], sms_times=['08:00']
        ))
        self.assertIn(b'SMS erfolgreich geplant!', response.data)


if __name__ == '__main__':
    unittest.main()

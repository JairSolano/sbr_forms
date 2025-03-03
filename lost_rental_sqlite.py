from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Function to create a database and tables
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    # Create submissions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            account TEXT,
            job TEXT,
            equipment TEXT,
            osr TEXT,
            reason TEXT
        )
    ''')
    # Create competitors table
    c.execute('''
        CREATE TABLE IF NOT EXISTS competitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            account TEXT,
            competitor TEXT,
            equipment TEXT,
            job TEXT,
            address TEXT,
            date TEXT,
            osr TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the input from the form
    company = request.form.get('company')
    account = request.form.get('account')
    job = request.form.get('job')
    eqp = request.form.get('equipment')
    osr = request.form.get('osr')
    reason = request.form.get('reason')

    # Insert data into the submissions database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO submissions (company, account, job, equipment, osr, reason)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (company, account, job, eqp, osr, reason))
    conn.commit()
    conn.close()

    return render_template('lost.html')

@app.route('/lost')
def lost():
    return render_template('lost.html')  # Ensure this template exists

@app.route('/contendor', methods=['POST'])
def contendor():
    # Get the input from the form
    company = request.form.get('customer')
    account = request.form.get('account')
    competitor = request.form.get('competitor')
    eqp = request.form.get('equipment')
    job = request.form.get('job')
    address = request.form.get('address')
    date = request.form.get('date on job')
    osr = request.form.get('submitted by')

    # Insert data into the competitors database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO competitors (company, account, competitor, equipment, job, address, date, osr)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company, account, competitor, eqp, job, address, date, osr))
    conn.commit()
    conn.close()

    return render_template('opps.html')  # This will render the opps.html template

@app.route('/opps')
def opps():
    return render_template('opps.html')  # Ensure this template exists

@app.route('/submissions')
def view_submissions():
    # Connect to the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Query to retrieve all submissions
    c.execute('SELECT * FROM submissions')
    submissions = c.fetchall()
    
    conn.close()

    return render_template('submissions.html', submissions=submissions)

@app.route('/competitors_list')
def view_competitors():
    # Connect to the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Query to retrieve all competitors
    c.execute('SELECT * FROM competitors')
    competitors = c.fetchall()
    
    conn.close()

    return render_template('compsubs.html', competitors=competitors)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
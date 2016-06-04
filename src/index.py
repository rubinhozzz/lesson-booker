from flask import Flask, render_template, request, jsonify
import sqlite3

application = Flask(__name__)

@application.route("/")
def index():
    return render_template('index.html')

@application.route('/_do_booking')
def do_booking():
    ok = True
    start = request.args.get('start')
    end = request.args.get('end')
    full_name = request.args.get('full_name')
    phone_number = request.args.get('phone_number')
    email = request.args.get('email')
    conn = sqlite3.connect('booking.db')
    c = conn.cursor()
    params = (start, end, full_name, phone_number, email)
    try:
        c.execute(
            """
            INSERT INTO booking(start, end, full_name, phone_number, email, active)
            VALUES(?, ?, ?, ?, ?, 0)
            """, params)
    except sqlite3.Error as e:
        ok = False
        print "An error occurred:", e.args[0]
    conn.commit()
    conn.close()
    return jsonify(result=ok)

@application.route('/_get_events')
def get_events():
    ok = True
    date = request.args.get('date')
    conn = sqlite3.connect(application.config['DATABASE_PATH'])
    c = conn.cursor()
    params = (date,)
    x = []
    try:
        c.execute("SELECT * FROM booking WHERE strftime('%Y-%m-%d', start)=?", params)
        x = c.fetchall()
    except sqlite3.Error as e:
        #ok = False
        ok = "An error occurred: %s" % (e.args[0],)
    conn.commit()
    conn.close()
    return jsonify(result=ok, source=x)

if __name__ == "__main__":
    application.config['DEBUG'] = True
    application.config['DATABASE_PATH'] = 'booking.db'
    application.run()
else:
    application.config['DEBUG'] = False
    application.config['DATABASE_PATH'] = '/home/rubinhozzz/webapps/rodolfonavarrete_booker/htdocs/booking.db'

#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import Response

from datetime import datetime

from schedule import Schedule

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return 'Welcome'

@app.route("/create-appointment")
def get_create_appointment():
    return render_template('schedule.html')

@app.route('/create-appointment', methods=['POST'])
def create_appointment():
    print('fdsfadsf')
    # 'doctor', 'Strange'), ('apptdate', '2023-08-24'), ('starttime', '09:11'), ('endtime', '10:33')
    app.logger.info(request.form)
    doctor = request.form.get('doctor')
    apptdate = request.form.get('apptdate')
    starttime = request.form.get('starttime')
    endtime = request.form.get('endtime')

    if doctor == 'Strange':
        success = sched_strange.create_appointment(apptdate, starttime, endtime)
        print(f'Strange appt: {success}, {sched_strange.schedule}')
    else:
        success = sched_who.create_appointment(apptdate, starttime, endtime)
        print(f'Who appt: {success}, {sched_who.schedule}')

    if success:
        return 'Successfully created appointment', 200
    else:
        return 'Did not create appointment', 400

@app.route('/get-appointments', methods=['POST'])
def get_appointments():
    doctor = request.form.get('doctor')
    apptdate = request.form.get('apptdate')
    starttime = request.form.get('starttime')
    endtime = request.form.get('endtime')

    if doctor == 'Strange':
        appts = sched_strange.get_appointments(apptdate, starttime, endtime)
    else:
        appts = sched_strange.get_appointments(apptdate, starttime, endtime)
    return appts

@app.route('/get-first-appointment', methods=['POST'])
def get_first_appointment():
    doctor = request.form.get('doctor')
    apptdate = request.form.get('apptdate')
    starttime = request.form.get('starttime')

    if doctor == 'Strange':
        appt = sched_strange.get_first_appointment(apptdate, starttime)
    else:
        appt = sched_strange.get_first_appointment(apptdate, starttime)
    return appt
    

@app.route('/get-schedules')
def get_schedules():
    return render_template('result.html', data={'Strange': sched_strange.schedule, 'Who': sched_who.schedule})

if __name__ == '__main__':
    sched_strange = Schedule('Strange', 9, 5)
    sched_who = Schedule('Who', 8, 4)
    app.run(host='0.0.0.0', port=5000, debug=True)


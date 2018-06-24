from flask import Flask, redirect, url_for, request, jsonify, session, render_template
from com.auth.authenticate import DatabaseOperations
import os
from datetime import timedelta
from flask_ask import Ask, statement
from com.helpers.Session_handlers import Session
import com.smart_device.Devices as Devices
from com.smart_device.database_helper import RaspberryDevices
import logging

app = Flask(__name__)
ask = Ask(app, '/')
logger = logging.getLogger()
database = DatabaseOperations()


@app.route('/login')
def auth():
    if request.args:
        user = request.args.get('user_name')
        key = request.args.get('password')
        if database.validate_user(user_name=user, key=key):
            if database.get_user_data(user)['status'] == 'ACTIVE':
                session['user'] = user
                session['logged'] = True
                session['role'] = database.get_user_data(session['user'])['role']
                database.update_last_login(user)
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=60)
                return redirect(url_for('success', name=user))
            message = database.get_user_data(user)['status'] + " user"
            return redirect(url_for('home', message=message))
    return redirect(url_for('home', message='Failed login'))


@app.route('/<message>')
def home(message):
    if session and message:
        return jsonify({'message': message})
    return 'Hello human!'


@app.route('/success/<name>')
def success(name):
    if session:
        if session['user']:
            return jsonify({'logged_in': name, 'details': str(url_for('user_data'))})
    return redirect(url_for('home', message='Please login first'))


@app.route('/details')
def user_data():
    if session:
        user_details = database.get_user_data(session['user'])
        current_session = Session(session)
        if current_session.is_admin():
            user_details.pop('key', None)
        return jsonify(user_details)
    return redirect(url_for('home', message='Please login'))


@app.route('/create/<user_name>')
def create_user(user_name):
    if session:
        current_session = Session(session)
        if current_session.is_admin():
            return jsonify(database.create_user(user_name))
        return redirect(url_for('home', message='Only admin users can access this function!'))
    return redirect(url_for('home', message='Please login first!'))


@app.route('/kill')
def kill():
    current_session = Session(session)
    current_session.destroy_session(['user', 'role', 'logged'])
    return redirect(url_for('home', message='Killed session successfully!'))


@app.route('/details/<username>')
def fetch_user(username):
    if session:
        current_session = Session(session)
        if current_session.is_admin():
            user_details = database.get_user_data(username)
            if len(user_details) > 0:
                return jsonify(user_details)
            return redirect(url_for('home', message='No such user present'))
        return redirect(url_for('home', message='Only admin users can access this function!'))
    return redirect(url_for('home', message='Please login first!'))


@ask.intent('HelloIntent')
def hello(first_name):
    text = render_template('hello', firstname=first_name)
    return statement(text).simple_card('Hello', text)


@app.route('/device/set', methods=['POST'])
def set_device():
    current_session = Session(session)
    if current_session.is_valid_session():
        if request.method == 'POST':
            data = request.get_json()
            device = data['device']
            status = data['status']
            user = session['user']
            if status == RaspberryDevices.Status.ON.value:
                Devices.home.switch_on(device, user)
            elif status == RaspberryDevices.Status.OFF.value:
                Devices.home.switch_off(device, user)
            return jsonify(Devices.home.current_status(device))
    return jsonify({'Message': 'Please login'})

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0')

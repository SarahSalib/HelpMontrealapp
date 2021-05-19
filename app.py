import csv
import os

import bcrypt
from flask import Flask, render_template, url_for, redirect, session, flash
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager
from flask_mail import Mail, Message

from forms import SponsorForm, EventForm, SignupForm, LoginForm, ForgetPassword, ResetPassword

app = Flask(__name__)
app.secret_key = 'Jesus'

app.config['MAIL_DEBUG'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT_TLS'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEB'] = False
app.config['MAIL_USERNAME'] = 'sarah.salib.ss@gmail.com'
app.config['MAIL_PASSWORD'] = 'Sarah@111'
app.config['MAIL_DEFAULT_SENDER'] = ('Help Montreal', 'help.Montreal.2020@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ACSII_ATTACHMENTS'] = False
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, email):
        self.id = email


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def find_use(email):
    with open('data/Sign UP.csv')as f:
        for user in csv.reader(f):
            if len(user) == 0:
                continue
            elif email == user[4]:
                session['email'] = user[4]
                session['password'] = user[2]
                session['last'] = user[1]
                session['phone'] = user[7]
                session['first'] = user[0]
                return True
    return False


@app.route('/')
def homepage():
    return render_template('home page.html', username=session.get('first', '.......'))


@app.route('/helpday')
def helpday():
    return render_template('help day.html', username=session.get('first', '.......'))


@app.route('/homeservice')
def homeservice():
    return render_template('home service.html', username=session.get('first', '.......'))


@app.route('/signup', methods=['Get', 'Post'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = find_use(form.email.data)
        session['first'] = '.......'
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            with open('data/Sign UP.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([form.first.data, form.last.data, password.decode(), form.sex.data,
                                 form.email.data, form.uni.data, form.study.data, form.phone.data])
            return redirect(url_for('login'))
        else:
            flash('This Email already exist,enter another Email or login in ')
    return render_template('student-signup.html', form=form, username=session.get('first', '.......'))


@app.route('/login', methods=('Get', 'Post'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_use(form.email.data)
        if user and bcrypt.checkpw(form.password.data.encode(), session.get('password').encode()):
            login_user(User(form.email.data))
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password!')
    return render_template('login.html', form=form, username=session.get('first', '.......'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect('/')


@app.route('/sponsors', methods=['GET', 'POST'])
def sponsors_form():
    form = SponsorForm()
    if form.validate_on_submit():
        session['institution'] = form.name.data
        msg = Message('HELP MONTREAL',
                      recipients=[form.email.data])
        msg.html = '<b>Dear Mrs/Mr ' + '<br/><br/>We are so grateful that <b>' + session.get(
            'institution') + '</b> institution wants to be part of sponsors <br/>One of our staff will contact you ' \
                             'soon <br/><br/>Best Regards,<br/>HELP MONTREAL team'
        mail.send(msg)
        with open('data/sponsors.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([form.name.data, form.field.data, form.email.data, form.phone.data,
                             form.address.data, form.why.data])
        return redirect(url_for('sponsor1_redirect'))
    return render_template('sponsors.html', form=form, username=session.get('first', '.......'))


@app.route('/sponsor_redirect')
def sponsor1_redirect():
    return render_template('sponsers message.html', username=session.get('first', '.......'))


@app.route('/ineedhelp')
def i_need_help():
    return render_template('I need help.html', username=session.get('first', '.......'))


@app.route('/icanhelp')
def i_can_help():
    return render_template('I can help.html', username=session.get('first', '.......'))


@app.route('/event', methods=['Get', 'Post'])
@login_required
def event():
    form = EventForm()
    if form.validate_on_submit():
        with open('data/Event.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['EVENT', session.get('first') + ' ' + session.get('last'), session.get('email'), session.get('phone'),
                 form.occasion.data, form.date.data, form.time.data,
                 form.address.data + ", " + form.city.data + ', ' + form.postal.data,
                 form.info.data, form.duty.data, form.duration.data,
                 form.start.data, form.end.data])
        return redirect(url_for('event_message'))
    return render_template('event.html', form=form, username=session.get('first', '.......'))


@app.route('/eventMessage')
def event_message():
    return render_template('event message.html', username=session.get('first', '.......'))


@app.route('/weekly')
@login_required
def check_schedule():
    prefix = '/static/'
    with open('data/Sechedule.csv') as f:
        schedule = list(csv.reader(f))
    return render_template('weekly schedule.html', schedule=schedule, prefix=prefix,
                           username=session.get('first', '.......'))


@app.route('/event_request')
@login_required
def event_request():
    info = [' ', 'Name', 'Email', 'Phone ', 'Occasion', 'Date', 'Time', 'Address', 'Event information', 'Helper duties',
            'Help duration', 'Start time ', 'End time ']
    prefix = '/static/'
    with open('data/Event.csv') as f:
        reader = csv.reader(f)
        all = []
        for row in reader:
            if len(row) == 0:
                continue
            else:
                event_info = [(info[1], row[1]), (info[2], row[2]),
                              (info[3], row[3]), (info[4], row[4]), (info[5], row[5]),
                              (info[6], row[6]), (info[7], row[7]), (info[8], row[8]),
                              (info[9], row[9]), (info[10], row[10] + " hours"), (info[11], row[11]),
                              (info[12], row[12])]
                all.append(event_info)
        return render_template('event request.html', event_info=event_info, all=all,
                               username=session.get('first', '.......'), prefix=prefix)


@app.route('/forget', methods=['Get', 'Post'])
def forget_password():
    form = ForgetPassword()
    user = find_use(form.email.data)
    if form.validate_on_submit():
        if user:
            return redirect(url_for('reset_password'))
        else:
            flash('This email does not exist, Please Check your Email or Sign Up ')
    return render_template('forget password.html', form=form, username='.......')


@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    form = ResetPassword()
    email = session.get('email')
    session['first'] = '.......'
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(form.password.data.encode(), salt)
        forget(email, password)
        session.clear()
        return redirect(url_for('login'))
    return render_template('rest password.html', form=form, username='.......')


def forget(email, password):
    with open('data/Sign UP.csv') as R, open('data/temp.csv', 'w')as f:
        reader = csv.reader(R)
        writer = csv.writer(f)
        for user in reader:
            if len(user) == 0:
                continue
            elif email == user[4]:
                user[2] = password.decode()
                row = user
                writer.writerow(row)
            else:
                writer.writerow(user)
    os.remove('data/Sign UP.csv')
    os.rename('data/temp.csv', 'data/Sign UP.csv')


if __name__ == '__main__':
    app.run(debug=True)

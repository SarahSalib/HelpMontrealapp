
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField, TimeField
from wtforms import DecimalField, PasswordField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length, Regexp, NumberRange, EqualTo, ValidationError


class SponsorForm(FlaskForm):
    name = StringField('Institution Name:', validators=[InputRequired(), Length(4, 64)])
    field = StringField('Business Field:', validators=[InputRequired(), Length(4, 64)])
    email = EmailField('Email:', validators=[InputRequired(), Email()])
    phone = StringField('Phone Number:', validators=[InputRequired()])
    address = TextAreaField('Address:', validators=[InputRequired()], render_kw={'rows': 3})
    why = TextAreaField('Please tell us, Why do you want to join our sponsors?', validators=[InputRequired()],
                        render_kw={'rows': 3})
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    occasion = SelectField('What is the occasion?',
                           validators=[InputRequired()],
                           choices=[('Birthday', 'Birthday'),
                                    ('Baby Shower', 'Baby Shower'),
                                    ('Fund raising', 'Fund raising'),
                                    ('Party', 'Party'), ('Proposal', 'Proposal')])
    date = DateField('Event Date',validators=[InputRequired()])
    time = TimeField('Event Time',validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    postal = StringField('Postal Code', validators=[InputRequired()])
    info = TextAreaField('Please tell us more about your event', validators=[InputRequired()],
                         render_kw={'rows': 3})
    duty = TextAreaField('Please tell us more about our helper duties', validators=[InputRequired()],
                         render_kw={'rows': 3})
    duration = DecimalField('Estimated help time needed in hours',validators=[InputRequired()])
    start = TimeField('Help Start',validators=[InputRequired()])
    end = TimeField('Help End',validators=[InputRequired()])
    submit = SubmitField('Help Me',validators=[InputRequired()])


class SignupForm(FlaskForm):
    first = StringField('First Name', validators=[InputRequired(),
                                                  Regexp('([A-Za-z][a-zA-Z]*)'), Length(3, 10)])
    last = StringField('Last name', validators=[InputRequired(),
                                                Regexp('([A-Za-z][a-zA-Z]*)'), Length(3, 10)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     EqualTo('confirm', message='Password must much'),
                                                     Regexp('^([a-zA-Z0-9@*#]{8,16})$',
                                                            message='Password must be between 8 and 16 character long '
                                                                    'contain upper and lower case letters ,digits and '
                                                                    'special character')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    email = EmailField('Your Email', validators=[InputRequired(), Email()])
    uni = SelectField('Please select you university',
                      validators=[InputRequired()],
                      choices=[('Concordia University', 'Concordia University'),
                               ('École de Technologie Supérieure', 'École de Technologie Supérieure'),
                               ('École Polytechnique de Montréal', ' École Polytechnique de Montréal'),
                               ('McGill University', 'McGill University'),
                               ('Université de Montréal', 'Université de Montréal'),
                               ('University of Québec in Montréal', 'University of Québec in Montréal')])
    study = StringField('Field of study', validators=[InputRequired(),
                                                      Regexp('([A-Za-z][a-zA-Z]*)'), Length(8, 25)])
    phone = StringField('Phone Number:', validators=[InputRequired(),
                                                     Regexp('^[\\(]{0,1}([0-9]){3}[\\)]{0,1}[ ]?([^0-1]){1}([0-9]){'
                                                            '2}[ ]?[-]?[ ]?([0-9]){4}[ ]*((x){0,1}([0-9]){1,5}){0,'
                                                            '1}$', message='it should be 10 digits long')])
    sex = RadioField('sex', validators=[InputRequired()],
                     choices=[('Male', 'Male'), ('Female', 'Female')],
                     render_kw={'required': True})
    sign = SubmitField('Sign UP')


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField('login')


class ForgetPassword(FlaskForm):
    email = EmailField('email', validators=[InputRequired(), Email()])
    sign = SubmitField('Submit Request')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(),
                                                     EqualTo('confirm', message='Password must much'),
                                                     Regexp('^([a-zA-Z0-9@*#_]{8,16})$',
                                                            message='Password must be between 8 and 16 character long '
                                                                    'contain upper and lower case letters ,digits and '
                                                                    'special character')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    sign = SubmitField('Reset Password')
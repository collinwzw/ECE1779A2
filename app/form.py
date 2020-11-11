from flask import session, flash, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField,validators, IntegerField
from wtforms.validators import DataRequired,number_range, data_required




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ConfigForm(FlaskForm):
    max_worker = IntegerField('Max Worker Size',validators=[DataRequired(),number_range(max=10,min=1,message='Please input int 1-10')])
    min_worker = IntegerField('Max Worker Size',
                              validators=[DataRequired(), number_range(max=10, min=1, message='Please input int 1-10')])
    cooling_time = IntegerField('Cooling Time',validators=[DataRequired(),number_range(max=1000, min=1, message='Please input int 1-10')])
    cpu_up_threshold = IntegerField('CPU Upper Threshold', [validators.NumberRange(min=1, max=100, message="Please input int 1-100")])
    cpu_down_threshold = IntegerField('CPU Down Threshold', [validators.NumberRange(min=0, max=99, message="Please input int 0-99")])
    upper_ratio = FloatField('ratio_expand', validators=[DataRequired(),number_range(max=10,min=1,message='Please input float 1-10')])
    lower_ratio = FloatField('ratio_shrink', validators=[DataRequired(),number_range(max=1,min=0,message='Please input float 0-1')])
    submit = SubmitField('Save Config')
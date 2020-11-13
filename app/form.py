from flask import session, flash, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField,validators, IntegerField, SelectField
from wtforms.validators import DataRequired,number_range




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ConfigForm(FlaskForm):
    max_worker = SelectField('Max Worker Size',choices=[1,2,3,4,5,6,7,8], validators=[DataRequired()])
    min_worker = SelectField('Min Worker Size',choices=[1,2,3,4,5,6,7,8], validators=[DataRequired()])
    cooling_time = FloatField('Cooling Time',validators=[DataRequired(),number_range(max=1000, min=1, message='Please input int 1-1000')])
    cpu_up_threshold = FloatField('CPU Upper Threshold', [validators.NumberRange(min=1, max=100, message="Please input int 1-100")])
    cpu_down_threshold = FloatField('CPU Down Threshold', [validators.NumberRange(min=0, max=100, message="Please input int 0-99")])
    extend_ratio = FloatField('ratio_extend', validators=[DataRequired(),number_range(max=10,min=1,message='Please input float 1-10')])
    shrink_ratio = FloatField('ratio_shrink', validators=[DataRequired(),number_range(max=1,min=0,message='Please input float 0-1')])
    submit = SubmitField('Save Config')
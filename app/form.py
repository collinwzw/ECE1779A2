from flask import session, flash, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField,validators
from wtforms.validators import DataRequired,Email, EqualTo, length




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ConfigForm(FlaskForm):
    max_worker = FloatField('Max Worker Size',
                                  [validators.NumberRange(min=0, max=8, message="Please input int 1-8)")],
                                  render_kw={'readonly': ''})
    min_worker = FloatField('Min Worker Size',
                                    [validators.NumberRange(min=1, max=8, message="Please input int 1-8")],
                                    render_kw={'readonly': ''})
    cpu_up_threshold = FloatField('CPU Upper Threshold', [validators.NumberRange(min=0, max=99, message="Please input int 1-100")], render_kw={'readonly': ''})
    cpu_down_threshold = FloatField('CPU Down Threshold', [validators.NumberRange(min=0, max=99, message="Please input int 1-100")], render_kw={'readonly': ''})
    upper_ratio = FloatField('ratio_expand', [validators.NumberRange(min=1, max=10, message="Please number 1-10")], render_kw={'readonly': ''})
    lower_ratio = FloatField('ratio_shrink', [validators.NumberRange(min=1, max=10, message="Please input number 1-10")], render_kw={'readonly': ''})
    submit = SubmitField('Save Config')
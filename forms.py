#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,
                            SelectField, SelectMultipleField, TextAreaField,
                            RadioField, IntegerField, DecimalField, SubmitField)
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, NumberRange




class LoginForm(FlaskForm):
    username = StringField('用户名：', validators=[Length(min=2, max=25),DataRequired()], render_kw={'class':'easyui-textbox'})
    password = PasswordField('密　码：', validators=[Length(min=6, max=25),DataRequired()], render_kw={'class':'easyui-passwordbox'})
    #date = DateField('日期', validators=[DataRequired()], render_kw={'class':'easyui-datebox'})
    remember_me = BooleanField('记住我',default=False, render_kw={'class':'easyui-switchbutton','data-options':"onText:'Yes',offText:'No'"})
    submit = SubmitField('登　陆')
    
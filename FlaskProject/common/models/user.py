# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, info='primary key')
    nickname = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='username')
    login_name = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, unique=True, server_default=db.FetchedValue(), info='loginname')
    login_pwd = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='loginpassword')
    login_salt = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='salt')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='status 0 is invalid 1 is valid')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='last login time')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='create time')

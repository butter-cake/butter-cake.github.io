from flask_app.configs.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9.-]+\.[a-zA-Z]+$')

class User:
    DB = 'loginAndValidation'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def CreateUser(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s)
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @staticmethod
    def validate_user(new_user):
        is_valid = True
        if len(new_user['first_name']) < 2:
            flash('First name must be longer than 2 letters')
            is_valid = False
        if len(new_user['last_name']) < 2:
            flash('Last name must be longer than 2 letters')
            is_valid = False

        if not EMAIL_REGEX.match(new_user['email']):
            flash('Enter a correct email')
            is_valid = False
        if len(new_user['password']) < 8:
            flash('Password has to be longer than 8 letters')
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash('Passwords do not match')
            is_valid = False
        return is_valid

    
    @classmethod
    def GetUserById(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(user_id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def GetUserByEmail(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

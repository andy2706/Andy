import time
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)
api = Api(app)

#db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="cdlvw2002",db="test")
db = MySQLdb.connect(host="145.24.222.206",user="testuser",passwd="1234",db="database1")

cursor = db.cursor()

class CheckIfRegistered(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser() 
            parser.add_argument('IBAN', required=True)
            args = parser.parse_args()
            try:
                iban = str(args.get('IBAN'))
                query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
                cursor.execute(query)
                db.commit()
                data = cursor.fetchall()
                data = data[0]
                if data[7] == 1:
                    return{'data': 'Blocked'}, 434
                else:
                    return{'data': 'OK'}, 208
            except:
                return{'data': 'Not registered'}, 433
        except:
            return{'data': 'JSON error'}, 432
    pass

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        parser.add_argument('pincode', required=True)
        args = parser.parse_args()
        try:
            iban = str(args.get('IBAN'))
            pincode = str(args.get('pincode'))
            query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
            cursor.execute(query)
            db.commit()
            data = cursor.fetchall()
            data = data[0]
            pogingen = data[6]
            email = data[4]
            newpogingen = pogingen - 1
            query = f"UPDATE `database1`.`account` SET `Pogingen` = '{newpogingen}' WHERE (`Rekeningnummer` = '{iban}');"
            cursor.execute(query)
            db.commit()
            print(newpogingen)
            if data[5] == pincode:
                query = f"UPDATE `database1`.`account` SET `Ingelogd` = '1' WHERE (`Rekeningnummer` = '{iban}');"
                cursor.execute(query)
                db.commit()
                query = f"UPDATE `database1`.`account` SET `Pogingen` = '3' WHERE (`Rekeningnummer` = '{iban}');"
                cursor.execute(query)
                db.commit()
                return{'data': email}, 208
            if newpogingen <= 0:
                query = f"UPDATE `database1`.`account` SET `Blokeer status` = '1' WHERE (`Rekeningnummer` = '{iban}');"
                cursor.execute(query)
                db.commit()
                return{'data': 'Blocked'}, 434
            if data[7] == 1:
                return{'data': 'Blocked'}, 434
            else:
                return{'data': 'Pincode Wrong'}, 435
        except:
            return{'data': 'JSON error'}, 432
    pass



class CheckBalance(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            iban = str(args.get('IBAN'))
            query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
            cursor.execute(query)
            db.commit()
            data = cursor.fetchall()
            data = data[0]
            saldo = float(data[2])
            if data[8] == 0:
                return{'data': "not logged in"}, 436
            else:
                return int(saldo), 209
        except:
            return {'error': 'JSON error'}, 432
    pass

class GetEmail(Resource):
   def post(self):
       parser = reqparse.RequestParser() 
       parser.add_argument('IBAN', required=True)
       args = parser.parse_args()
       try:
           iban = str(args.get('IBAN'))
           query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
           cursor.execute(query)
           db.commit()
           data = cursor.fetchall()
           data = data[0]
           email = str(data[4])
           return{'data': email}, 208
       except:
           return {'error': 'email not found'}, 432
   pass


class Withdraw(Resource): 
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        parser.add_argument('amount', required=True)
        args = parser.parse_args()
        try:
            iban = str(args.get('IBAN'))
            amount = int(args.get('amount'))
            query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
            cursor.execute(query)
            db.commit()
            data = cursor.fetchall()
            data = data[0]
            currentAmount = int(data[2])
            newAmount = currentAmount - amount
            if data[8] == 0:
                return{'data': "not logged in"}, 436
            elif newAmount <= 0:
                return {'data': "onvoldoende saldo"}, 437
            else:
                query = f"UPDATE `database1`.`account` SET `Saldo` = '{newAmount}' WHERE (`Rekeningnummer` = '{iban}');"
                cursor.execute(query)
                db.commit()
                return {'data' : newAmount}, 208 
        except:
            return {'error': 'invalid input'}, 432 
    pass

class Logout(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            iban = str(args.get('IBAN'))
            query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
            cursor.execute(query)
            db.commit()
            data = cursor.fetchall()
            data = data[0]
            if data[8] == 1:
                query = f"UPDATE `database1`.`account` SET `Ingelogd` = '0' WHERE (`Rekeningnummer` = '{iban}');"
                cursor.execute(query)
                db.commit()
                return{'data': 'OK'}, 208 
            else:
                return{'data': 'Not logged in'}, 436          
        except:
            return{'data': 'JSON error'}, 432
    pass

class CheckAttempts(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            iban = str(args.get('IBAN'))
            query = f"SELECT * FROM `database1`.`account` WHERE Rekeningnummer ='{iban}';"
            cursor.execute(query)
            db.commit()
            data = cursor.fetchall()
            data = data[0]
            attempts = float(data[6])
            return {'attempts': attempts}, 208
        except:
            return {'error': 'JSON error'}, 432
    pass


    
api.add_resource(CheckBalance, '/checkBalance') 
api.add_resource(Withdraw, '/withdraw')
api.add_resource(CheckIfRegistered, '/checkIfRegistered')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckAttempts, '/checkAttempts')
api.add_resource(GetEmail, '/getEmail')

if __name__ == '__main__':
    #app.run() 
    #app.run(host='145.24.222.206', threaded=True)
    app.run(host="0.0.0.0")
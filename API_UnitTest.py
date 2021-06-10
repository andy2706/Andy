import unittest
import requests

class TestCheckIfRegistered(unittest.TestCase):
    def test_checkIfRegistered(self):
        request = requests.post('http://145.24.222.206:5000/checkIfRegistered', data=[('IBAN', "NI69NIBA00000001")])
        result = str(request.status_code)
        self.assertEqual(result, "208")
    
    def test_not_registered_checkIfRegistered(self):
        request = requests.post('http://145.24.222.206:5000/checkIfRegistered', data=[('IBAN', "NI69NIBA69696969")])
        result = str(request.status_code)
        self.assertEqual(result, "433")


class TestLogin(unittest.TestCase):
    def test_login(self):
        request = requests.post('http://145.24.222.206:5000/login', data=[('IBAN', "NI69NIBA00000001"),('pincode', "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0")])
        result = str(request.status_code)
        self.assertEqual(result, "208")

    def test_login_wrong_pincode(self):
        request = requests.post('http://145.24.222.206:5000/login', data=[('IBAN', "NI69NIBA00000001"),('pincode', "1234")])
        result = str(request.status_code)
        self.assertEqual(result, "435")

class TestCheckBalance(unittest.TestCase):
    def test_checkbalance(self):
        request = requests.post('http://145.24.222.206:5000/checkBalance', data=[('IBAN', "NI69NIBA00000001")])
        result = request.text
        result = result[:-2]
        result = result[8:]
        result = float(result)
        self.assertGreater(result,0)

class TestAPIWithdraw(unittest.TestCase):
    def test_withdraw(self):
        request = requests.post('http://145.24.222.206:5000/login', data=[('IBAN', "NI69NIBA00000001"),('pincode', "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0")])
        request = requests.post('http://145.24.222.206:5000/withdraw', data=[('IBAN', "NI69NIBA00000001"), ('amount', "100")])
        result = str(request.status_code)
        self.assertEqual(result, "208")
    
    def test_withdraw_not_enough_money(self):
        request = requests.post('http://145.24.222.206:5000/withdraw', data=[('IBAN', "NI69NIBA00000001"), ('amount', "10000000")])
        result = str(request.status_code)
        self.assertEqual(result, "437")

class TestLogout(unittest.TestCase):
    def test_logout(self):
        request = requests.post('http://145.24.222.156:5001/logout', data=[('IBAN', "NI69NIBA00000001")])
        result = str(request.status_code)
        self.assertEqual(result, "208")

class TestWhileLoggedOut(unittest.TestCase):
    def test_withdraw_while_logged_out(self):
        request = requests.post('http://145.24.222.206:5000/withdraw', data=[('IBAN', "NI69NIBA00000001"), ('amount', "100")])
        result = str(request.status_code)
        self.assertEqual(result, "436")
    def test_check_balanced_while_logged_out(self):
        request = requests.post('http://145.24.222.206:5000/checkBalance', data=[('IBAN', "NI69NIBA00000001")])
        result = str(request.status_code)
        self.assertEqual(result, "436")

if __name__=='__main__':
    unittest.main()
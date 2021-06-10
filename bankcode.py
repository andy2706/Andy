import serial
import sys
import time
import datetime
import requests
from webbrowser import open_new_tab
import smtplib
from email.message import EmailMessage
import hashlib


inputArduino = serial.Serial('/dev/cu.usbmodem14101', 9600)   #verbindingen met arduino
outputArduino = serial.Serial('/dev/cu.usbmodem14201', 9600)
#outputArduino = serial.Serial('/dev/cu.usbserial-1420', 9600)
inputArduino.flushInput()
card = ""
code = ""
iban = ""
getPas = True
getPin = False
inMenu = False
email = ""

outputArduino.timeout = 1

#links naar GUI pagina's
index = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/index.html"
pincode = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode.html"
pincode_1_ingevuld = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode_1_ingevuld.html"
pincode_2_ingevuld = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode_2_ingevuld.html"
pincode_3_ingevuld = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode_3_ingevuld.html"
pincode_4_ingevuld = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode_4_ingevuld.html"
menu = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/menu.html"
pincode_onjuist_2pog = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode_onjuist_2pog.html"
pincode_onjuist_1pog = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/pincode_onjuist_1pog.html"
saldobekijken = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/saldo.html"
opnemen = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/opnemen.html"
wilt_u_bon = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/wilt_u_bon.html"
wilt_u_digitale_bon = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/wilt_u_digitale_bon.html"
wachtscherm = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/wachtscherm.html"
snel_70_pinnen = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/70euro_pinnen.html"
geblokeerd = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/geblokeerd.html"
onvoldoende_saldo = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/onvoldoende_saldo.html"
error = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/error.html"
onjuiste_input = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/onjuiste_input.html"
welkebriefjes = "file:///Users/casper/Documents/TI-Jaar1/Kwartaal_3/Project_3-4/python/GUI/briefkeuze.html"

def geenVoorkeur(pin):
  if pin < 20:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  if pin > 350:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  
  bedrag50 = pin % 50
  bedrag20 = bedrag50
  
  if bedrag20 < 20:
      twintig = 0
      
  if bedrag20 >= 20:
        bedrag20 = bedrag20 / 20
        bedrag20 = int(bedrag20)
        twintig = bedrag20
    
  bedrag50 = pin - bedrag50
  bedrag50 = bedrag50 / 50
  bedrag50 = int(bedrag50)
  vijftig = bedrag50

  if bedrag20 >=10 and bedrag20 <= 19:
      vijftig = vijftig - 1
      twintig = twintig + 3

  pin = 50 * vijftig + 20 * twintig 

  return vijftig , twintig, pin  

def prio50(pin):
  if pin < 20:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  if pin > 350:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  
  bedrag50 = pin % 50
  bedrag20 = bedrag50
  
  if bedrag20 < 20:
      twintig = 0
      
  if bedrag20 >= 20:
        bedrag20 = bedrag20 / 20
        bedrag20 = int(bedrag20)
        twintig = bedrag20
    
  bedrag50 = pin - bedrag50
  bedrag50 = bedrag50 / 50
  bedrag50 = int(bedrag50)
  vijftig = bedrag50

  pin = 50 * vijftig + 20 * twintig 

  return vijftig , twintig, pin  

def prio20(pin):
  if pin < 20:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  if pin > 350:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  
  bedrag50 = pin % 20

  twintig = int(pin/20)

  if int(pin/20) > 9:
      bedrag50 = pin - 180
      twintig = 9
    #   bedrag50 = pin

  if bedrag50 < 50:
      vijftig = 0
      
  if bedrag50 > 50:
    bedrag50 = pin - bedrag50
    bedrag50 = bedrag50 / 50
    bedrag50 = int(bedrag50)
    vijftig = bedrag50

  pin = 50 * vijftig + 20 * twintig 

  return vijftig , twintig, pin

def printBon(iban, bedrag):   #functie om bon te laten printen
    func = "2"
    stuf = str(func) + str(datetime.datetime.now())[:-7] + str(iban) + str(bedrag)+ str("\n")
    outputArduino.write(stuf.encode())
    time.sleep(2)


def printGeld(aantal1, aantal2):  #functie om geld te laten printen
    func = "1"
    stuf = str(func) + str(aantal1) + str(aantal2)+ str("\n")
    outputArduino.write(stuf.encode())
    time.sleep(1.5)


def digiprinten(subject, body, to):   #functie om digitale bon te versturen
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "cnerdishihi@gmail.com"
    password = "qtklcwnyzxnjihwx"

    msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def getEmail(iban):   #functie om email op te vragen
  request = requests.post('http://145.24.222.206:5000/getEmail', data=[('IBAN', f"{iban}")])
  email = str(request.text)
  email = email[:-3]
  email = email[10:]
  return email


def checkIfRegistered(card):    #functie om te kijken of gebruiker geregistreerd is
  bankcode = card[:-8]
  bankcode = bankcode[4:]
  if bankcode == "NIBA":
    request = requests.post('http://145.24.222.206:5000/checkIfRegistered', data=[('IBAN', f"{card}")])
  else:
    request = requests.post('http://145.24.222.156:5001/checkIfRegistered', data=[('IBAN', f"{card}")])
  result = str(request.status_code)
  return result

def login(iban, code):    #functie om gebruiker in te loggen
  bankcode = iban[:-8]
  bankcode = bankcode [4:]
  if bankcode == "NIBA":
    request = requests.post('http://145.24.222.206:5000/login', data=[('IBAN', f"{iban}"),('pincode', f"{code}")])
  else:
    request = requests.post('http://145.24.222.156:5001/login', data=[('IBAN', f"{iban}"),('pincode', f"{code}")])
  result = str(request.status_code)
  return result

def getBalance(iban):   #functie om saldo te bekijken
    bankcode = iban[:-8]
    bankcode = bankcode [4:]
    if bankcode == "NIBA":
      request = requests.post('http://145.24.222.206:5000/checkBalance', data=[('IBAN', f"{iban}")])
    else:
      request = requests.post('http://145.24.222.156:5001/checkBalance', data=[('IBAN', f"{iban}")])
    result = request.text
    #result = result[:-2]
    #result = result[8:]
    return result

def changeBalance(iban, amount):    #functie om geld af te schrijven
    bankcode = iban[:-8]
    bankcode = bankcode [4:]
    if bankcode == "NIBA":
      request = requests.post('http://145.24.222.206:5000/withdraw', data=[('IBAN', f"{iban}"), ('amount', f"{amount}")])
    else:
      request = requests.post('http://145.24.222.156:5001/withdraw', data=[('IBAN', f"{iban}"), ('amount', f"{amount}")])
    result = str(request.status_code)
    return result

def logout(iban):   #functie om uit te loggen
    bankcode = iban[:-8]
    bankcode = bankcode [4:]
    if bankcode == "NIBA":
      request = requests.post('http://145.24.222.206:5000/logout', data=[('IBAN', f"{iban}")])
    else:
      request = requests.post('http://145.24.222.156:5001/logout', data=[('IBAN', f"{iban}")])
    result = str(request.status_code)
    return result

def checkAttempts(iban):    #functie om pogingen te checken
    bankcode = iban[:-8]
    bankcode = bankcode [4:]
    if bankcode == "NIBA":
      request = requests.post('http://145.24.222.206:5000/checkAttempts', data=[('IBAN', f"{iban}")])
    else:
      request = requests.post('http://145.24.222.156:5001/checkAttempts', data=[('IBAN', f"{iban}")])
    request = request.text
    request = request[:-4]
    request = request[13:]
    request = int(request)
    return request

printBon("NI69NIBA0000TEST","0")    #een lege bon printen om printer goed in te stellen

try:    
  while True:   #programma blijft constant draaien
    open_new_tab(index)
    inputArduino.write(b'Y')
    inputArduino.flushInput()
    ser_bytes = inputArduino.readline()
    card = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))   #lees de kaart uit
    print(card)
    isRegistered = checkIfRegistered(card)
    if isRegistered ==  "208":    #als de kaart geregistreerd is ga door naar pincode
        print("bekende user")
        iban = card
        inputArduino.write(b'N')
        getPas = False
        getPin = True
        open_new_tab(pincode)
    if isRegistered == "434":     #als kaart geblokeerd is laat dit dan zien op het scherm
        open_new_tab(geblokeerd)
        time.sleep(3)
        open_new_tab(index)
    else:
        print("onbekende user")
    while getPin:
        inputArduino.flushInput()
        ser_bytes = inputArduino.readline()
        keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))  #krijg input van de keypad
        if keypadInput:
            if len(keypadInput) == 1 and len(code) < 4:   #per input een nieuw scherm 
                code += keypadInput
                if len(code) == 1:
                    open_new_tab(pincode_1_ingevuld)
                if len(code) == 2:
                    open_new_tab(pincode_2_ingevuld)
                if len(code) == 3:
                    open_new_tab(pincode_3_ingevuld)
                if len(code) == 4:
                    open_new_tab(pincode_4_ingevuld)
            if keypadInput == "#":    #als er een hekje ingetoets wordt gaat het programma verder
                hashed_pin = hashlib.sha256(code.encode('ascii')).hexdigest()   #hash de pincode
                print(hashed_pin)
                isCodeCorrect = login(iban, hashed_pin)
                if isCodeCorrect == "208":  #als alles goed is ga dan door naar het menu
                  open_new_tab(menu)
                  getPin = False
                  inMenu = True
                elif isCodeCorrect == "434":  #als kaart geblokeerd is laat dit dan zien op het scherm
                  open_new_tab(geblokeerd)
                  time.sleep(3)
                  code = ""
                  getPin = False
                  getPas = True
                else:     #als de pincode onjuist is ga dan naar het pincode onjuist scherm
                  attempts = checkAttempts(iban)
                  if attempts >= 2:
                    open_new_tab(pincode_onjuist_2pog)
                  else:
                    open_new_tab(pincode_onjuist_1pog)
                  code = ""
                  time.sleep(3)
                  open_new_tab(pincode)   
            print(code)

    while inMenu:   #blijf in het menu totdat er uitgelogd wordt
        inputArduino.flushInput()
        ser_bytes = inputArduino.readline()
        keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))  #krijg input van de keypad
        if keypadInput == "D":    #als er een d wordt ingetoets worden alle variabelen gereset en de gebruiker uitgelogd
                logout(iban)
                code = ""
                card = ""
                iban = ""
                email = ""
                inMenu = False
                open_new_tab(index)
                time.sleep(4)
                getPas = True
        if keypadInput == "C":    #als er een c wordt ingetoets wordt het saldo weergegeven
                saldo = getBalance(iban)    #haal het huidige saldo op
                f = open('GUI/saldo.html','w')  #open het html bestand en verander het saldo
#region saldopage
                saldopagebegin = """
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                @import url(https://fonts.googleapis.com/css?family=Lato:100,300,400,700,900); 
                body {
                  background-color: #141414;
                  background-image:url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEyMCc+Cgk8ZGVmcz4KCQk8cGF0dGVybiBwYXR0ZXJuVW5pdHM9J3VzZXJTcGFjZU9uVXNlJyBpZD0nYycgd2lkdGg9JzYwJyBoZWlnaHQ9JzEyMCcgeD0nMCcgeT0nMCcgdmlld0JveD0nMCAwIDUgMTAnPgoJCQk8cGF0aCBmaWxsLW9wYWNpdHk9JzAnIHN0cm9rZT0nIzI5MjkyOScgc3Ryb2tlLXdpZHRoPScwLjA5JyBkPSdNLTIsMUw3LDEwTS0yLDZMNywxNU0tMiwtNEw3LDUnLz4KCQk8L3BhdHRlcm4+CgkJPHBhdHRlcm4gcGF0dGVyblVuaXRzPSd1c2VyU3BhY2VPblVzZScgaWQ9J2MyJyB3aWR0aD0nNjAnIGhlaWdodD0nMTIwJyB4PScxMDAlJyB5PScwJyB2aWV3Qm94PScwIDAgNSAxMCc+CgkJCTxwYXRoIGZpbGwtb3BhY2l0eT0nMCcgc3Ryb2tlPScjMjkyOTI5JyBzdHJva2Utd2lkdGg9JzAuMDknIGQ9J003LDFMLTIsMTBNNyw2TC0yLDE1TTcsLTRMLTIsNScvPgoJCTwvcGF0dGVybj4KCTwvZGVmcz4KCTxyZWN0IHdpZHRoPSc1MCUnIGhlaWdodD0nMTAwJScgZmlsbD0ndXJsKCNjKScvPgoJPHJlY3QgeD0nNTAlJyB3aWR0aD0nNTAlJyBoZWlnaHQ9JzEwMCUnIGZpbGw9J3VybCgjYzIpJy8+Cjwvc3ZnPg==');

                    margin:0; padding:0;
                    overflow-x:hidden;
                    height:100%;
                    font-family: 'Lato', Helvetica, arial, sans-serif;
                    font-weight: 300;
                    font-size: 20px;
                    line-height: 1.45;
                    color: #eee;
                    color: rgba(255,255,255,.85);
                }
                #container { 
                    padding-top: 50px;
                }
                #content {
                    max-width: 43em;
                    padding:10px;
                    margin: 0 auto;
                }
                h1 {
                    font-size: 4.8em;
                    font-weight: 100;
                    text-transform: uppercase;
                    margin: 0;
                }
                h3 {
                    font-size: 2.4em;
                    font-weight: 300;
                    line-height: 1.5;
                }
                p, li {
                    font-size: 1.7em;
                }
                a {
                    font-weight: 700;
                    text-decoration: none;
                    color: #fff;
                }
                a:hover {
                    text-decoration: underline;
                }
                p#pleft {
                    max-width:20em;
                    float:left;
                }
                p#pright {
                    max-width:20em;
                    float:left;
                }
                ul {
                    clear:both;
                }


                html { font-size: 62.5%; }
                body { font-size: 1em;}

                /* PYRAMID CODE */
                .stage {
                  -webkit-transform:scale(1.85);
                  transform:scale(0.85);
                  float:right;
                  margin-right:180px;
                  margin-top:60px;
                  width:0px; height:0px;

                  position:relative;  
                  -webkit-perspective:1200px;
                  -webkit-perspective-origin:50% 50%;
                  perspective:1200px;
                  perspective-origin:50% 50%;
                }
                .pyramid3d {
                  position:relative;
                  width:150px;
                  height:150px;

                  -webkit-transform-style: preserve-3d;
                  transform-style: preserve-3d;
                  -webkit-transform: rotateX(75deg) rotate(65deg);
                  transform: rotateX(75deg) rotate(65deg);
                  -webkit-animation: turnPyramid 10s linear infinite;
                  animation: turnPyramid 10s linear infinite;
                }
                .triangle {
                  -webkit-transform-style:preserve-3d;
                  transform-style:preserve-3d;
                  width:0; height:0;
                  background:none;
                }
                .triangle:before{
                  content:"";
                  position: absolute;
                  height: 0; width: 0;
                  border-style: solid;
                  border-width: 176px 75px 0 75px;
                }
                .side1 { -webkit-transform: translatex(0) rotatey(115.2deg) rotatez(90deg); transform: translatex(0) rotatey(115.2deg) rotatez(90deg); }
                .side2 { -webkit-transform: translatex(150px) rotatez(90deg) rotatex(64.8deg); transform: translatex(150px) rotatez(90deg) rotatex(64.8deg); }
                .side3 {  -webkit-transform: translatez(0) rotatex(64.8deg); transform: translatez(0) rotatex(64.8deg); }
                .side4 { -webkit-transform: translatey(150px) rotatex(115.2deg); transform: translatey(150px) rotatex(115.2deg); }
                .side1:before{ border-color: rgba(115, 115, 0, 0.3) transparent transparent transparent; }
                .side2:before{ border-color: rgba(20, 90, 225, 0.3) transparent transparent transparent; }
                .side3:before{ border-color: rgba(255,   0, 0, 0.3) transparent transparent transparent; } 
                .side4:before{ border-color: rgba(0, 255, 255, 0.3) transparent transparent transparent; }


                @-webkit-keyframes turnPyramid { 100% { -webkit-transform: rotateX(75deg) rotate(425deg); } }
                @keyframes turnPyramid { 100% { transform: rotateX(75deg) rotate(425deg); } }

                @media (max-width: 300px) {
                    html { font-size: 70%; }
                    .stage { -webkit-transform:scale(0.05); transform:scale(0.05); }
                }
                @media (max-width: 440px) {
                    h1 { line-height:55px; }    
                }
                @media (max-width: 460px) { 
                  .stage { position:absolute; top:25px; left:50%; margin-left:-45px; } 
                  h1 { margin-top:50px; text-align:center; }
                }
                @media (max-width:600px) { .stage { -webkit-transform:scale(0.55); transform:scale(0.55); margin-right:60px; } }
                @media (min-width: 600px) {
                    html { font-size: 80%; }
                    .stage { -webkit-transform:scale(0.68); transform:scale(0.68); margin-right:80px; }
                }
                @media (min-width: 880px) {
                    html { font-size: 120%; }
                    p, li { font-size: 1em; }
                    p#pright { margin-left:3em; }
                    .stage { -webkit-transform:scale(0.85); transform:scale(0.85); margin-right:120px; }
                </style>
                </head>

                <body>
                <div id="container">
                    <div id="content">
                      <div id="about">
                      <br> <br>
                        <h1>
                          <div style='float:left; margin-bottom:20px;'>
                            <b>Saldo</b>
                          </div>
                          <div class="stage">
                            <div class="pyramid3d">
                              <div class="triangle side1"></div>
                              <div class="triangle side2"></div>
                              <div class="triangle side3"></div>
                              <div class="triangle side4"></div>
                            </div>
                          </div> 
                        </h1>
                        <h3 style='clear:both' class="subhead">
                        <br>
                          <b>Betaalrekening</b>
                          </h3>
                          <h3 id="h3" style='clear:both' class="subhead">$
                          """

                saldopageeinde = """          
                        </h3>
                          <br>
                          <br>
                          <br>
                          <h4 style='clear:both' class="subhead">
                          <i>Druk op D om terug te gaan</i>
                          </h4>
                        </h3>
                            <script src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.js'></script>
                          <script>

                          var socket = io();

                          socket.on('data', function(data) {
                          console.log(data);
                          if (data == "!menu") {
                            window.location.replace("menu.html");
                          } 
                          document.getElementById("h3").innerHTML = '$ ' + data;

                          });

                        </script>
                      </div>
                    </div>
                  </div>
                  </body>
                  </html>
                  """
#endregion
                f.write(saldopagebegin + saldo + saldopageeinde)
                f.close()
                open_new_tab(saldobekijken)
                wachten = True
                while wachten:    #wacht tot de gebruiker klaar is met kijken
                  inputArduino.flushInput()
                  ser_bytes = inputArduino.readline()
                  keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                  if keypadInput == "D":
                    wachten = False
                    open_new_tab(menu)
        if keypadInput == "B":    #als er b wordt ingetoets wilt de gebruiker geld opnemen
              bedrag = "$ "
              f = open('GUI/opnemen.html','w')
#region opnemenpage
              opnemenBegin = """
              <!DOCTYPE html>
              <html>
              <head>
              <style>
              @import url(https://fonts.googleapis.com/css?family=Lato:100,300,400,700,900); 
              body {
                background-color: #141414;
                background-image:url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEyMCc+Cgk8ZGVmcz4KCQk8cGF0dGVybiBwYXR0ZXJuVW5pdHM9J3VzZXJTcGFjZU9uVXNlJyBpZD0nYycgd2lkdGg9JzYwJyBoZWlnaHQ9JzEyMCcgeD0nMCcgeT0nMCcgdmlld0JveD0nMCAwIDUgMTAnPgoJCQk8cGF0aCBmaWxsLW9wYWNpdHk9JzAnIHN0cm9rZT0nIzI5MjkyOScgc3Ryb2tlLXdpZHRoPScwLjA5JyBkPSdNLTIsMUw3LDEwTS0yLDZMNywxNU0tMiwtNEw3LDUnLz4KCQk8L3BhdHRlcm4+CgkJPHBhdHRlcm4gcGF0dGVyblVuaXRzPSd1c2VyU3BhY2VPblVzZScgaWQ9J2MyJyB3aWR0aD0nNjAnIGhlaWdodD0nMTIwJyB4PScxMDAlJyB5PScwJyB2aWV3Qm94PScwIDAgNSAxMCc+CgkJCTxwYXRoIGZpbGwtb3BhY2l0eT0nMCcgc3Ryb2tlPScjMjkyOTI5JyBzdHJva2Utd2lkdGg9JzAuMDknIGQ9J003LDFMLTIsMTBNNyw2TC0yLDE1TTcsLTRMLTIsNScvPgoJCTwvcGF0dGVybj4KCTwvZGVmcz4KCTxyZWN0IHdpZHRoPSc1MCUnIGhlaWdodD0nMTAwJScgZmlsbD0ndXJsKCNjKScvPgoJPHJlY3QgeD0nNTAlJyB3aWR0aD0nNTAlJyBoZWlnaHQ9JzEwMCUnIGZpbGw9J3VybCgjYzIpJy8+Cjwvc3ZnPg==');
                
                  margin:0; padding:0;
                  overflow-x:hidden;
                  height:100%;
                  font-family: 'Lato', Helvetica, arial, sans-serif;
                  font-weight: 300;
                  font-size: 20px;
                  line-height: 1.45;
                  color: #eee;
                  color: rgba(255,255,255,.85);
              }
              #container { 
                  padding-top: 50px;
              }
              #content {
                  max-width: 43em;
                  padding:10px;
                  margin: 0 auto;
              }
              h1 {
                  font-size: 4.8em;
                  font-weight: 100;
                  text-transform: uppercase;
                  margin: 0;
              }
              h3 {
                  font-size: 2.4em;
                  font-weight: 300;
                  line-height: 1.5;
              }
              p, li {
                  font-size: 1.7em;
              }
              a {
                  font-weight: 700;
                  text-decoration: none;
                  color: #fff;
              }
              a:hover {
                  text-decoration: underline;
              }
              p#pleft {
                  max-width:20em;
                  float:left;
              }
              p#pright {
                  max-width:20em;
                  float:left;
              }
              ul {
                  clear:both;
              }
              
              
              html { font-size: 62.5%; }
              body { font-size: 1em;}
              
              /* PYRAMID CODE */
              .stage {
                -webkit-transform:scale(1.85);
                transform:scale(0.85);
                float:right;
                margin-right:180px;
                margin-top:60px;
                width:0px; height:0px;
                
                position:relative;  
                -webkit-perspective:1200px;
                -webkit-perspective-origin:50% 50%;
                perspective:1200px;
                perspective-origin:50% 50%;
              }
              .pyramid3d {
                position:relative;
                width:150px;
                height:150px;
                
                -webkit-transform-style: preserve-3d;
                transform-style: preserve-3d;
                -webkit-transform: rotateX(75deg) rotate(65deg);
                transform: rotateX(75deg) rotate(65deg);
                -webkit-animation: turnPyramid 10s linear infinite;
                animation: turnPyramid 10s linear infinite;
              }
              .triangle {
                -webkit-transform-style:preserve-3d;
                transform-style:preserve-3d;
                width:0; height:0;
                background:none;
              }
              .triangle:before{
                content:"";
                position: absolute;
                height: 0; width: 0;
                border-style: solid;
                border-width: 176px 75px 0 75px;
              }
              .side1 { -webkit-transform: translatex(0) rotatey(115.2deg) rotatez(90deg); transform: translatex(0) rotatey(115.2deg) rotatez(90deg); }
              .side2 { -webkit-transform: translatex(150px) rotatez(90deg) rotatex(64.8deg); transform: translatex(150px) rotatez(90deg) rotatex(64.8deg); }
              .side3 {  -webkit-transform: translatez(0) rotatex(64.8deg); transform: translatez(0) rotatex(64.8deg); }
              .side4 { -webkit-transform: translatey(150px) rotatex(115.2deg); transform: translatey(150px) rotatex(115.2deg); }
              .side1:before{ border-color: rgba(115, 115, 0, 0.3) transparent transparent transparent; }
              .side2:before{ border-color: rgba(20, 90, 225, 0.3) transparent transparent transparent; }
              .side3:before{ border-color: rgba(255,   0, 0, 0.3) transparent transparent transparent; } 
              .side4:before{ border-color: rgba(0, 255, 255, 0.3) transparent transparent transparent; }
              
              
              @-webkit-keyframes turnPyramid { 100% { -webkit-transform: rotateX(75deg) rotate(425deg); } }
              @keyframes turnPyramid { 100% { transform: rotateX(75deg) rotate(425deg); } }
              
              @media (max-width: 300px) {
                  html { font-size: 70%; }
                  .stage { -webkit-transform:scale(0.05); transform:scale(0.05); }
              }
              @media (max-width: 440px) {
                  h1 { line-height:55px; }    
              }
              @media (max-width: 460px) { 
                .stage { position:absolute; top:25px; left:50%; margin-left:-45px; } 
                h1 { margin-top:50px; text-align:center; }
              }
              @media (max-width:600px) { .stage { -webkit-transform:scale(0.55); transform:scale(0.55); margin-right:60px; } }
              @media (min-width: 600px) {
                  html { font-size: 80%; }
                  .stage { -webkit-transform:scale(0.68); transform:scale(0.68); margin-right:80px; }
              }
              @media (min-width: 880px) {
                  html { font-size: 120%; }
                  p, li { font-size: 1em; }
                  p#pright { margin-left:3em; }
                  .stage { -webkit-transform:scale(0.85); transform:scale(0.85); margin-right:120px; }
              </style>
              </head>
              
              <body>
              <div id="container">
                  <div id="content">
                    <div id="about">
                    <br> <br>
                      <h1>
                        <div style='float:left; margin-bottom:20px;'>
                          <b>Opnemen</b>
                        </div>
                        <div class="stage">
                          <div class="pyramid3d">
                            <div class="triangle side1"></div>
                            <div class="triangle side2"></div>
                            <div class="triangle side3"></div>
                            <div class="triangle side4"></div>
                          </div>
                        </div> 
                      </h1>
                      <h3 style='clear:both' class="subhead">
                      <br>
                        <b>Voer het bedrag in dat u wilt opnemen</b>
                        </h3>
                        <h3 id="h3" style='clear:both' class="subhead">
                """
              opnemenEinde = """
                        </h3>
                        <br>
                        <br>
                        <br>
                        <h4 style='clear:both' class="subhead">
                        <i>Sluit af met een hekje(#) en druk op D om te annuleren</i>
                        </h4>
                      </h3>
                          <script src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.js'></script>
                        <script
                        var socket = io()
                        socket.on('data', function(data) {
                        console.log(data);
                        if (data == "!menu") {
                          window.location.replace("menu.html");
                        } 
                        document.getElementById("h3").innerHTML = '$ ' + data
                        })
                      </script>
                    </div>
                  </div>
                </div>
                </body>
                </html>
              """
#endregion
              f.write(opnemenBegin + bedrag + opnemenEinde) #maak het bestand leeg
              f.close()
              open_new_tab(opnemen)
              loop = True
              while loop:   #blijf om input vragen totdat de gebruiker cancelt of door gaat
                inputArduino.flushInput()
                ser_bytes = inputArduino.readline()
                bedragInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                if bedragInput == "D":    #cancel het opnemen
                    loop = False
                    open_new_tab(menu)
                elif bedragInput == "#":    #als er een hekje is ingetoets wilt de gebruiker het ingevoerde bedrag pinnen
                    loop = False
                    amount = bedrag[2:]
                    wachtOpKeuze = True
                    open_new_tab(welkebriefjes)
                    while wachtOpKeuze:
                      keuze = ""
                      inputArduino.flushInput()
                      ser_bytes = inputArduino.readline()
                      keuze = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                      if keuze == "A":
                        briefjes = prio50(int(amount))
                        wachtOpKeuze = False
                      elif keuze == "B":
                        briefjes = prio20(int(amount))
                        wachtOpKeuze = False
                      elif keuze == "C":
                        briefjes = geenVoorkeur(int(amount))
                        wachtOpKeuze = False
                    if briefjes[0] == 0 and briefjes[1] == 0 or briefjes[2] != int(amount):   #check of dit bedrag mogelijk is
                        open_new_tab(onjuiste_input)
                        time.sleep(4)
                        open_new_tab(menu)
                        keypadInput = ""
                        inWachtscherm = False
                    else:
                      result = changeBalance(iban, amount)  #stuur naar de API het bedrag en de iban
                      if result == "208":
                          open_new_tab(wilt_u_bon)
                          wachtOpAntwoord = True
                          while wachtOpAntwoord:    #vraag of de gebruiker een bon wilt
                            inputArduino.flushInput()
                            ser_bytes = inputArduino.readline()
                            keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                            if keypadInput == "A":
                              print("jabon")
                              wiltBon = True
                              wachtOpAntwoord = False
                            elif keypadInput == "B":
                              wiltBon = False
                              wachtOpAntwoord = False
                          open_new_tab(wilt_u_digitale_bon)
                          wachtOpAntwoord2 = True
                          while wachtOpAntwoord2:   #vraag of de gebruiker een digitale bon wilt
                            inputArduino.flushInput()
                            ser_bytes = inputArduino.readline()
                            keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                            if keypadInput == "A":
                              print("jabon")
                              try:
                                email = getEmail(iban)
                                print(email)
                                digiprinten("Pinbon", "Op datum: " + str(datetime.datetime.now())[:-7] + " heeft u dit gepind: " + amount, email)
                              except:
                                print("emailError")
                              wachtOpAntwoord2 = False
                            elif keypadInput == "B":
                              wachtOpAntwoord2 = False
                            inWachtscherm = True
                          while inWachtscherm:    #laat een wachtscherm zien terwijl de gebruiker op zijn geld/bon wacht
                            open_new_tab(wachtscherm)
                            printGeld(briefjes[0],briefjes[1])
                            if wiltBon == True:
                              printBon(iban,amount)
                            print(briefjes[0])
                            print(briefjes[1])
                            time.sleep((briefjes[0]+briefjes[1])*4)
                            keypadInput = ""
                            inWachtscherm = False
                            open_new_tab(menu)
                      elif result == "437":   #als de gebruiker onvoldoende saldo heeft wordt dit weergegeven
                        open_new_tab(onvoldoende_saldo)
                        time.sleep(3)
                        open_new_tab(menu)
                        keypadInput = ""
                else:
                    if bedragInput == "C" or bedragInput == "A" or bedragInput == "*" or bedragInput == "B":
                      print("*")
                    elif len(bedragInput) == 1:     #zorg ervoor dat er alleen getallen ingevoerd kunnen worden
                      bedrag += bedragInput
                      print(bedrag)
                      f = open('GUI/opnemen.html','w')
                      f.write(opnemenBegin + bedrag + opnemenEinde)   #verander de "opnemen" pagina met het ingevoerde bedrag
                      f.close()
                      open_new_tab(opnemen)
        if keypadInput == "A":    #hetzelfde als bij normaal opnemen maar dan automatisch $70
                wachtenOpAntwoord3 = True
                while wachtenOpAntwoord3:
                  open_new_tab(snel_70_pinnen)
                  inputArduino.flushInput()
                  ser_bytes = inputArduino.readline()
                  keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                  if keypadInput == "A":
                    result = changeBalance(iban, 70)
                    if result == "208":
                      open_new_tab(wilt_u_bon)
                      wachtOpAntwoord = True
                      wiltBon = False
                      while wachtOpAntwoord:
                        inputArduino.flushInput()
                        ser_bytes = inputArduino.readline()
                        keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                        if keypadInput == "A":
                          print("jabon")
                          wiltBon = True
                          wachtOpAntwoord = False
                        elif keypadInput == "B":
                          wachtOpAntwoord = False
                      open_new_tab(wilt_u_digitale_bon)
                      wachtOpAntwoord2 = True
                      while wachtOpAntwoord2:
                        inputArduino.flushInput()
                        ser_bytes = inputArduino.readline()
                        keypadInput = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                        if keypadInput == "A":
                          print("jabon")
                          try:
                              email = getEmail(iban)
                              print(email)
                              digiprinten("Pinbon", "Op datum: " + str(datetime.datetime.now())[:-7] + " heeft u dit gepind: " + "70", email)
                          except:
                              print("emailError")
                          wachtOpAntwoord2 = False
                        elif keypadInput == "B":
                          wachtOpAntwoord2 = False
                        open_new_tab(wachtscherm)
                        inWachtscherm = True
                      while inWachtscherm:
                          open_new_tab(wachtscherm)
                          printGeld(1,1)
                          if wiltBon == True:
                            printBon(iban,70)
                          time.sleep(8)
                          keypadInput = ""
                          inWachtscherm = False
                          wachtenOpAntwoord3 = False
                          open_new_tab(menu)
                    elif result == "437":
                      open_new_tab(onvoldoende_saldo)
                      time.sleep(3)
                      keypadInput = ""
                      wachtenOpAntwoord3 = False
                      open_new_tab(menu)
                  elif keypadInput == "B":
                    wachtenOpAntwoord3 = False
                    open_new_tab(menu)
                
except:   #indien er iets mis gaat komt er een error scherm
  open_new_tab(error)
  sys.exit("Error")

from flask import Flask
from flask import request
import serial
import smtplib, ssl

app= Flask(__name__)
ser= serial.Serial('COM3')
print(ser.name)

#inundatie---------------------------------------------------
def send_leak_mail():
        message = """S-a detectat o inundatie!"""
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context)
                server.login("dstudiostudio@gmail.com", 'dstudiostudio120') # Enable IMAP in contul google, iar apoi Enable less secure apps la https://myaccount.google.com/lesssecureapps
                server.sendmail('dstudiostudio@gmail.com', 'damaris.stanc@gmail.com', message)
#-----------------------------------------------------------


@app.route('/')
def hello_world():

        text = '<p style="font-size:30px;text-align:center;color:00cc00"><b> Proiect Sincretic 2021- sem 2</b></p>'
        text2 = '<p style="font-size:20px;text-align:center;color:#009933"><b> Stanc Damaris</b></p>'

        pr1 = '<p style="text-align:center; background:#99ff99; font-size:20px"><b>Vezi temperatura</b></p>'
        temp = 'Temperatura este: '
        temp_serial = ser.readline()
        temp_serial=temp_serial.decode()

        if temp_serial.find("ATENTIE!INUNDATIE!") == 0:
                send_leak_mail()

        pr2 = '<p style="text-align:center; background:#99ff99; font-size:20px"><b>Schimba lumina</b></p>'
        string_butoane = '<p><button onclick="document.location=\'led_on\'">LED ON</button>   <button onclick="document.location=\'led_off\'">LED OFF</button></p>'
        color_picker = '<p>LED RGB Selector: <p style="text-align:center"><form method=\"get\" action=\"color\"><input name=\"colpicker\" type=\"color\"/> <input type=\"submit\" value=\"send\"></form></p>>

        pr3 = '<p style="text-align:center; background:#99ff99; font-size:20px"><b>Trimite un mesaj</b></p>'
        text_form = '<p>Introduceti textul dorit: <form method=\"get\" action=\"mesaj\"><input name=\"msg\" type=\"text\"/> <input type=\"submit\" value=\"send\"></form></p>'

        return text+ text2+ pr1 + temp + temp_serial + pr2 + string_butoane + color_picker+ pr3+ text_form

@app.route('/led_on')
def led_oon():
        ser.write("A".encode())
        return "Am aprins ledul"

@app.route('/led_off')
def led_off():
        ser.write("S".encode())
        return "Am stins ledul"

@app.route('/color')
def color_picker():
    color=str(request.args['colpicker'])
    red = int("0x" + color[1:3], 16) * 99/255.0
    green = int("0x" + color[3:5], 16) * 99/255.0
    blue = int("0x" + color[5:7], 16) * 99/255.0

    color="P" + str(int(red)).zfill(2) + str(int(green)).zfill(2) + str(int(blue)).zfill(2) + "W"
    print(color)
    ser.write(color.encode())
    return "Am modificat culoarea RGB!"

@app.route('/mesaj')
def message_parser():
    mesaj = str(request.args['msg'])
    mesaj_serial = "#" + mesaj + "^"
    ser.write(mesaj_serial.encode())
    return "Am transmis pe display mesajul:  " + mesaj

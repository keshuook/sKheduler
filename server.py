from http.server import BaseHTTPRequestHandler
from cgi import FieldStorage
import json
from os import remove
from ctypes import windll
from threading import Thread

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        if self.path == "/favicon.ico":
            self.send_header("Content-Type", "image/x-icon")
            self.end_headers()
            f = open("public/favicon.ico", "rb")
            self.wfile.write(f.read())
            return
        elif self.path == "/":
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open("public/home.html", "r")
        elif self.path == "/dashboard":
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open("public/dash.html", "r")
        elif self.path == "/create":
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open("public/ui-create.html", "r")
        elif self.path == "/edit":
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open("public/ui-edit.html", "r")
        elif self.path == "/add_alarm_error":
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open("public/post.html", "r")
        elif self.path == "/css":
            self.send_header("Content-Type", "text/css")
            self.end_headers()
            f = open("public/style.css", "r")
        elif self.path == "/nojavascripterror":
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open("public/no-script.html", "r")
        elif self.path == "/$alarm":
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            f = open("data/alarms.json", "r")
        else:
            self.send_error(404, "PAGE NOT FOUND")
            return
        for l in f:
            self.wfile.write(bytes(l, "utf-8"))
        f.close()
        return
    def do_POST(self):
        self.send_response(301)

        form_data = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'}
        )
        if form_data.getvalue("reason") == None or form_data.getvalue("dotw") == None or form_data.getvalue("time") == None:
            self.send_header('Location','/add_alarm_error')
        elif self.path == "/add_alarm":
            data = None
            with open("data/alarms.json") as file:
                data = json.load(file)
                data['items'].append({"reason":form_data.getvalue("reason"),"day":form_data.getvalue("dotw").split(","),"time":form_data.getvalue("time"),"description":form_data.getvalue("description")})
                file.close()
                remove("data/alarms.json")
            with open("data/alarms.json", "w") as file:
                json.dump(data, file, indent=4)
                file.close()
            
            message_process = Thread(target=windll.user32.MessageBoxW,args=(0, "The alarm has been created.", "Alarm", 0))
            message_process.setName("Message Process")
            message_process.start()

            self.send_header('Location','/dashboard')
        elif self.path == "/edit_alarm":
            data = None
            with open("data/alarms.json") as file:
                data = json.load(file)
                data['items'][int(form_data.getvalue("element-number"))] = {
                    "reason": form_data.getvalue("reason"),
                    "day": form_data.getvalue("dotw").split(","),
                    "time": form_data.getvalue("time"),
                    "description": form_data.getvalue("description")
                }
                file.close()
                remove("data/alarms.json")
            with open("data/alarms.json", "w") as file:
                json.dump(data, file, indent=4)
                file.close()

            self.send_header('Content-Type','text/html')
        self.end_headers()
        self.wfile.write(bytes("<script>window.close();</script>", "utf-8"))
        return
    def do_DELETE(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        id = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))['id']

        data = None
        with open("data/alarms.json") as file:
            data = json.load(file)
            del data['items'][id]
            file.close()
            remove("data/alarms.json")
        with open("data/alarms.json", "w") as file:
            json.dump(data, file, indent=4)
            file.close()

def setup():
    data = json.loads("{\"items\":[]}")
    with open("data/alarms.json", "w") as file:
        json.dump(data, file, indent=4)
        file.close()
from http.server import HTTPServer
from threading import Thread
from sys import argv
from server import Server, setup
from alarm import alarm

if("-setup" in argv):
    setup()
    print("[info] Setup Complete.")
    raise SystemExit()
else:
    port = 9000
    if("-port" in argv):
        for index, item in enumerate(argv):
            if(item == "-port"):
                port = int(argv[index+1])


server = HTTPServer(("localhost", port), Server)

alarm_process = Thread(target=alarm, args=())
alarm_process.setName("Alarm Process")
alarm_process.setDaemon(True)
alarm_process.start()

server_process = Thread(target=server.serve_forever, args=())
server_process.setName("Python Server")
server_process.start()
import asyncio
import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from multiprocessing import Process
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from datetime import datetime
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Завантаження змінних із .env файлу
load_dotenv()
logging.basicConfig(level=logging.INFO)

MONGO_URI = os.getenv("MONGO_URI")


# Клас для HTTP-сервера
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/":
            self.send_html_file("web_application/index.html")
        elif parsed_url.path == "/message.html":
            self.send_html_file("web_application/message.html")
        elif parsed_url.path.startswith("/static/"):
            self.send_static_file(parsed_url.path[1:])
        else:
            self.send_html_file("web_application/error.html", 404)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        parsed_data = parse_qs(post_data.decode("utf-8"))
        username = parsed_data.get("username")[0]
        message = parsed_data.get("message")[0]

        # Формування JSON
        message_data = json.dumps({"username": username, "message": message})

        async def send_message():
            uri = "ws://localhost:5000"
            async with websockets.connect(uri) as websocket:
                await websocket.send(message_data)

        # Відправлення повідомлення WebSocket-серверу
        asyncio.run(send_message())

        # Відповідь клієнту
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Message sent!")

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())

    def send_static_file(self, filename, status=200):
        try:
            with open(filename, "rb") as file:
                self.send_response(status)
                if filename.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                elif filename.endswith(".png"):
                    self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_html_file("web_application/error.html", 404)


# WebSocket-сервер
class WebSocketServer:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.message_db
        self.collection = self.db.messages

    async def ws_handler(self, websocket: WebSocketServerProtocol):
        async for message in websocket:
            data = json.loads(message)
            data["date"] = datetime.now().isoformat()
            self.collection.insert_one(data)
            logging.info(f"Saved message: {data}")


async def run_websocket_server():
    server = WebSocketServer()
    async with websockets.serve(server.ws_handler, "0.0.0.0", 5000):
        logging.info("WebSocket server started on port 5000")
        await asyncio.Future()  # Запуск назавжди


def start_websocket_server():
    asyncio.run(run_websocket_server())


def run_http_server():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, HttpHandler)
    logging.info("HTTP server started on port 3000")
    httpd.serve_forever()


if __name__ == "__main__":
    http_process = Process(target=run_http_server)
    ws_process = Process(target=start_websocket_server)

    http_process.start()
    ws_process.start()

    http_process.join()
    ws_process.join()
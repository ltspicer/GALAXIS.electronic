# AsyncioNet/Connection.py
import asyncio
import threading
from .Channel import Channel

connection = None

# --------------------------
# AsyncioConnection
# --------------------------

class AsyncioConnection:
    def __init__(self):
        self.reader = None
        self.writer = None
        self.channel = None
        self.connected = False
        self.loop = None
        self.loop_thread = None

    def Connect(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            host, port = args[0]
        elif len(args) == 2:
            host, port = args
        else:
            host, port = "localhost", 10000

        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._connect_async(host, port))
            self.loop.run_forever()

        self.loop_thread = threading.Thread(target=run_loop, daemon=True)
        self.loop_thread.start()

        # Warten bis TCP steht
        import time
        timeout = 5.0
        start = time.time()
        while not self.connected and (time.time() - start) < timeout:
            time.sleep(0.01)

        if not self.connected:
            raise ConnectionError("AsyncioNet: Verbindung fehlgeschlagen!")

    async def _connect_async(self, host, port):
        try:
            self.reader, self.writer = await asyncio.open_connection(host, port)
            self.connected = True
            self.channel = Channel(self.reader, self.writer, server=self)
            asyncio.create_task(self.channel.listen_loop())
        except Exception as e:
            print("[ERROR] Verbindung fehlgeschlagen in _connect_async():", e)

    def Pump(self):
        pass

    def Close(self):
        try:
            if self.writer:
                self.writer.close()
            self.connected = False
            if self.channel:
                self.channel.queue.append({"action": "disconnected"})
        except Exception as e:
            print("[ERROR] Close():", e)

# --------------------------
# Globale Hilfsfunktionen
# --------------------------

def Connect(*args):
    global connection
    connection = AsyncioConnection()
    connection.Connect(*args)
    return connection

def Pump():
    global connection
    if connection is None:
        return
    connection.Pump()

def Send(data):
    global connection
    if connection is None or connection.channel is None:
        print("[AsyncioNet] Warnung: Verbindung noch nicht aufgebaut, Send ignored")
        return
    connection.channel.Send(data)

# --------------------------
# ConnectionListener
# --------------------------

class ConnectionListener:
    def Connect(self, *args, **kwargs):
        Connect(*args, **kwargs)
        self.Pump()

    def Pump(self):
        global connection
        if connection and connection.channel:
            for data in connection.channel.get_queue():
                for n in ("Network_" + data.get("action", ""), "Network"):
                    if hasattr(self, n):
                        getattr(self, n)(data)

    def Send(self, data):
        global connection
        if connection and connection.channel:
            connection.channel.Send(data)


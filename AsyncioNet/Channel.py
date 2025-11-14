# AsyncioNet/Channel.py
import asyncio
from .rencode import loads, dumps

class Channel:
    endchars = '\0---\0'

    def __init__(self, reader, writer, server=None):
        self.reader = reader
        self.writer = writer
        self.server = server
        self.addr = writer.get_extra_info("peername")
        self._buffer = b""
        self.sendqueue = []
        self.queue = []

    async def listen_loop(self):
        try:
            while True:
                try:
                    # 600 Sekunden Timeout beim Lesen
                    data = await asyncio.wait_for(self.reader.readuntil(self.endchars.encode()), timeout=600.0)
                except asyncio.TimeoutError:
                    # Server offline
                    self._trigger_disconnected()
                    break

                if not data:
                    self._trigger_disconnected()
                    break

                msg = data[:-len(self.endchars)]
                try:
                    obj = loads(msg)
                    self.queue.append(obj)
                    if isinstance(obj, dict) and "action" in obj:
                        for n in ("Network_" + obj["action"], "Network"):
                            if hasattr(self, n):
                                getattr(self, n)(obj)
                except Exception as e:
                    print("[WARN] Ungültige Nachricht empfangen:", msg, e)

        except asyncio.IncompleteReadError:
            self._trigger_disconnected()
        except Exception as e:
            print("[ERROR] Listen-Loop:", e)
            self._trigger_disconnected()


    def _trigger_disconnected(self):
        self.queue.append({"action": "disconnected"})
        if hasattr(self, "Network_disconnected"):
            try:
                self.Network_disconnected()
            except Exception as e:
                print("[ERROR] Network_disconnected:", e)

    def get_queue(self):
        q = self.queue[:]
        self.queue = []
        return q

    def Send(self, data):
        try:
            outgoing = dumps(data) + self.endchars.encode()
            self.writer.write(outgoing)
            return len(outgoing)
        except Exception as e:
            print("[ERROR] Channel.Send():", e)
            return 0


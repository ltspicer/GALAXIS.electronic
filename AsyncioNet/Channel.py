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
                data = await self.reader.readuntil(self.endchars.encode())
                if not data:
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
            pass
        except Exception as e:
            print("[ERROR] Listen-Loop:", e)

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


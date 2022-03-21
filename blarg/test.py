import asyncio
import websockets
from collections import deque
import json
async def read020C():
    url = "ws://107.155.81.113:8765"
    avoid = ['0209',  '0003', '0207']
    skips = [18, 19, 12, 16, 38, 39, 40]
    bTypes = []
    async with websockets.connect(url) as websocket:
        while True:
            packet = await websocket.recv()
            packet = json.loads(packet)
            data = deque([packet['data'][i:i+2] for i in range(0,len(packet['data']),2)])

            packet_id = data.popleft() + data.popleft()
            if packet_id in avoid: continue
            # print(packet['data'])
            if packet_id == '020C':
                print("020C" + "".join(list(data)))

            elif packet_id == '020A':
                continue
                print("020A" + "".join(list(data)))
            else:
                # print(packet_id)
                pass

            # print("Getting new packet")
            # packet = await websocket.recv()
            # packet = json.loads(packet)
            # data = deque([packet['data'][i:i+2] for i in range(0,len(packet['data']),2)])
            # packet_id = data.popleft() + data.popleft()
            # print(packet_id)
            await asyncio.sleep(0)
def process020C(data):
    data = deque(data[i:i+2] for i in range(0,len(data),2))



def run():
    asyncio.get_event_loop().run_until_complete(read020C())

if __name__ == "__main__":
    run()



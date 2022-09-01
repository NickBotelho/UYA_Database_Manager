import asyncio
import websockets
import json
import requests
import logging
import traceback
from collections import deque
from blarg.packets.tcp_map import tcp_map
from blarg.packets.udp_map import udp_map

from blarg.LiveGame import LiveGame
import datetime
GAMES = 'http://107.155.81.113:8281/robo/games'

class Blarg:
    def __init__(self, config: dict):
        self._config = config

        self._logger = logging.getLogger('blarg')
        self._logger.setLevel(logging.getLevelName(config['logger']))
        formatter = logging.Formatter('%(name)s | %(levelname)s | %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.getLevelName(config['logger']))
        self._logger.addHandler(sh)
        self.delay = True if config['delay'] == "True" else False
        self.delayTime = int(config['delayTime'])
        # self.live = LiveGame(dme_id=115)
        self.games = {}
        self.live = None
 
    def run(self, loop):
        asyncio.get_event_loop().run_until_complete(self.read_websocket())

    def process(self, packet: dict):
        # if packet['dme_world_id'] != 130:return 
        '''
        Process json from Robo's websocket.
        Structure:
        {
            "type": udp/tcp
            "dme_world_id": int
            "src": the source player dme id
            "dst": the destination player dme id, -1 for sending to all
            "data": a hex string of the raw data
        }
        '''

        # Convert to list. E.g. '000102030405' -> ['00', '01', '02', '03', '04', '05']
        data = deque([packet['data'][i:i+2] for i in range(0,len(packet['data']),2)])

        '''
        There may be multiple messages in each message.
        So we have to read the current message, and see if there's any leftover
        data which would be another message
        '''
        avoid = ['0018', '0009']
        # Keep reading until data is empty
        while len(data) != 0:
            if len(data) < 2: break
            packet_id = data.popleft() + data.popleft() # E.g. '0201'
            if packet_id in avoid: break
            if self._config['filter'] == packet_id:
                self._logger.info(f"{packet['type']} | {packet_id + ''.join(list(data))}") 

            # Check if the packet_id exists. If it does, serialize it
            try:
                if packet['type'] == 'tcp':
                    if packet_id not in tcp_map.keys():
                        break
                    else:
                        serialized = tcp_map[packet_id].serialize(data)

                elif packet['type'] == 'udp':
                    if packet_id not in udp_map.keys():
                        break
                    else:
                        serialized = udp_map[packet_id].serialize(data)
            except Exception as e:
                self._logger.info('problem serializing dme')
                self._logger.info(packet['dme_world_id'])
                self._logger.info(traceback.format_exc())
                data = []
                packet_id = '-1' if packet_id != '0004' else packet_id
                serialized = {}

            # Don't print correctly serialized unless it matches filter or the filter is empty.
            try:
                if packet_id == '0004' and packet['dme_world_id'] not in self.games:
                    self._logger.warning(f"Creating Live Game for DME ID = {packet['dme_world_id']}")
                    self.games[packet['dme_world_id']] = LiveGame(dme_id=packet['dme_world_id'], delay=self.delay, delayTime=self.delayTime)
                if self._config['filter'] == packet_id or self._config['filter'] == '' :
                    if packet['dme_world_id'] in self.games and len(serialized) > 0:
                        running = self.games[packet['dme_world_id']].load(packet_id, serialized, packet)
                        if not running:
                            del self.games[packet['dme_world_id']]
            except Exception as e:
                self._logger.info(f"{packet['dme_world_id']}: Problem with live game")
                self._logger.info(traceback.format_exc())


                # if packet_id not in avoid:
                #     if packet_id == '020C' and len(serialized) > 1:
                #         # if serialized['subtype'] == '21000000':
                #             self._logger.info(f"S | {packet_id} | {serialized}") 
            # self._logger.info(f"S | {packet_id} | {serialized}") 
                


    async def read_websocket(self):
        uri = f"ws://{self._config['robo_ip']}:8765"
        connected = True
        while True:
            self._logger.error("SOCKET STARTING")
            connected = True
            async with websockets.connect(uri) as websocket:
                while connected:
                    try:
                        data = await websocket.recv()
                        data = json.loads(data)
                        self._logger.debug(f"{data}")
                        self.process(data)
                    except Exception as e:
                        self._logger.critical("Problem with socket")
                        self._logger.critical(e)
                        self._logger.warning("Restarting socket in 60 seconds")
                        connected = False
                        await asyncio.sleep(60)

    async def garbageCollect(self):
        minutes = 10
        self._logger.error("INITIALIZING GARBAGE COLLECTOR")

        while True:
            self._logger.info("RUNNING GARBAGE COLLECTOR")
            self._logger.info("Calling server games api")
            res = requests.get(GAMES).json()
            activeGames = {game['dme_world_id'] for game in res}
           
            try:
                before = len(self.games)
                self._logger.info(f"before cleanup {before}")
                currentTime = datetime.datetime.now()
                stale = []
                for dme_id in self.games:                        
                    game = self.games[dme_id]
                    totalTime = currentTime - game.createTime
                    if dme_id not in activeGames:
                        game.endGame()
                        stale.append(dme_id)
                    elif game.state != 0: 
                        timeUp = currentTime - game.startTime
                        if (timeUp.total_seconds()//60) > 120:
                            game.endGame()
                            stale.append(dme_id)
                    elif (totalTime.total_seconds()//60) > 120:
                        game.endGame()
                        stale.append(dme_id)
                for dme_id in stale:
                    del self.games[dme_id]
                after = len(self.games)
                self._logger.info(f"after cleanup {after}")
                self._logger.error(f"GARBAGE COLLECTOR REMOVED {before -after} GAMES")
                await asyncio.sleep(60*minutes)
            except Exception as e:
                self._logger.critical("Problem collection garbage")
                self._logger.critical(e)
            

            




def read_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.loads(f.read())

# if __name__ == '__main__':
#     config = read_config()

#     blarg = Blarg(config)
#     blarg.run()

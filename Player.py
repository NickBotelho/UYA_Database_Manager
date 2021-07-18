# class Player():
#     def __init__(self, id, username,status,ladderstatswide) -> None:
#         self.id = id
#         self.username = username
#         self.status = status
#         self.ladderstatswide = ladderstatswide



class Player():
    def __init__(self, packet) -> None:
        self.packet = packet
        self.parse()
    def parse(self):
        self.id = self.packet['account_id']
        self.username = self.packet['username']
        self.status = self.packet['status']
        self.ladderstatswide = self.packet['ladderstatswide']

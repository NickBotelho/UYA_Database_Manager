import requests
import json
def read_config(config_file='Webhooks/subscribers.json'):
    with open(config_file, 'r') as f:
        return json.loads(f.read())


COLOR = 11043122
SUBSCRIBERS = read_config()

class Field():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def formatContent(self):
        body = {
            "name":self.name,
            "value":self.value
        }
        return body

class BaseWebook():
    def __init__(self, title, description, fields, color = None):
        self.title = title
        self.description = description
        self.fields = fields
        self.color = COLOR if color == None else color
    def formatContent(self):
        body = {
            "embeds":[{
                
                "title": self.title,
                "descrption": self.description,
                "color": self.color,
                "fields": [f.formatContent() for f in self.fields]
            
            }]
        }
        return json.dumps(body)
    def broadcast(self):
        body = self.formatContent()
        for url in SUBSCRIBERS:
            res = requests.post(url, body , headers={"Content-Type":"application/json"})



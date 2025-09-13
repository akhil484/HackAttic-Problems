# https://hackattic.com/challenges/websocket_chit_chat

import json
import requests
import asyncio
import websockets
import time



async def hello(token):
    uri = "wss://hackattic.com/_/ws/%s"%(token)
    print(uri)
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                start = time.time()
                print('starting connection')

                async for message in websocket:
                    print(message)
                    interval = int((time.time() - start) * 1000)
                    
                    if message == 'ping!':
                        start = time.time()
                        if interval <= 800:
                            await websocket.send("700")
                        elif interval <= 1600:
                            await websocket.send("1500")
                        elif interval <= 2100:
                            await websocket.send("2000")
                        elif interval <= 2600:
                            await websocket.send("2500")
                        else:
                            await websocket.send("3000")
                # print(message)
        
        except:
            print("Reconnecting in 3s...")
            await asyncio.sleep(3) 

if __name__ == '__main__':
    #Get the data from URL
    response = requests.get('https://hackattic.com/challenges/websocket_chit_chat/problem?access_token={access_token}')
    data = json.loads(response.text)
    print(data['token'])
    asyncio.run(hello(data['token']))
    
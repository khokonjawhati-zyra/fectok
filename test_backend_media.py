import asyncio
import websockets
import json

async def test_media():
    uri = "ws://fectok.com/ws/user"
    async with websockets.connect(uri) as websocket:
        # Claim session
        await websocket.send(json.dumps({
            "action": "CLAIM_SESSION",
            "mesh_id": "TEST_NODE"
        }))
        resp = await websocket.recv()
        print("Connected:", resp)
        
        # Fetch media
        await websocket.send(json.dumps({
            "action": "GET_LATEST_MEDIA"
        }))
        resp = await websocket.recv()
        data = json.loads(resp)
        print("Media Count:", len(data.get("media", [])))
        for i, m in enumerate(data.get("media", [])[:5]):
            print(f"Item {i}: URL={m.get('url')} FILE={m.get('file')}")

asyncio.run(test_media())

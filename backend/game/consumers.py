import simplejson as json
import redis
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from entity_lookup import entity_table

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                            port=int(os.getenv('REDIS_PORT')),
                            connection_class=redis.SSLConnection,
                            password=os.getenv('REDIS_PASSWORD'),
                            username=os.getenv('REDIS_USER'))


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["match_id"]

        # Join room group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        redis_client = redis.Redis(connection_pool=pool)
        lobby_state = json.load(redis_client.get(self.room_name))

        if (lobby_state != None):
            lobby_state.update({"players": lobby_state.players.append(self.channel_name)})
            redis_client.set(self.room_name, lobby_state)
            await self.accept()
        else:
            self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        payload = json.loads(text_data)
        eventType = payload.eventType

        # Send message to room group
        match eventType:
            case "start_game":
                redis_client = redis.Redis(connection_pool=pool)
                lobby_state = redis_client.get(self.room_name)
                # initialize game state at payload.key

                # -> initialize board
                board = [[None] * 10 for _ in range(10)]
                for i in range(10):
                    for j in range(10):
                        board[i][j] = {
                            "tile_id": "grass",
                            "passable": True
                        }

                # -> intialize units
                units = [[None] * 8]
                for i in range(4):
                    units[i] = {
                        "unit_id": "duelist",
                        "player_id": lobby_state.players[0],
                        "hp": 4
                    }
                for i in range(4,8):
                    units[i] = {
                        "unit_id": "duelist",
                        "player_id": lobby_state.players[1],
                        "hp": 4
                    }
                lobby_state.update({"board": board, "units": units})
                redis_client.set(self.room_name, json.dumps(lobby_state))

            case "move":
                try:
                    entity_table[payload.unit_type].move(payload)
                    await self.channel_layer.group_send(
                        self.room_name, {"type": "move", "message": "Unit moved on board"}
                    )
                except:
                    await self.channel_layer.group_send(
                        self.room_name, {
                            "type": "action_failed", "message": "Action was invalid, states may not be synced"}
                    )

    # Receive message from room group
    async def move(self, event):
        message = event.message

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

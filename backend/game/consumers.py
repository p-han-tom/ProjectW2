import simplejson as json
import redis
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from .entity_lookup import entity_table

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                            port=int(os.getenv('REDIS_PORT')),
                            connection_class=redis.SSLConnection,
                            password=os.getenv('REDIS_PASSWORD'),
                            username=os.getenv('REDIS_USER'))


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # TODO: Check self.scope for the user id (would have to set socket header in frontend)
        # TODO: Once there are two PlayerConsumer instances, we redirect all other connections to SpectatorConsumers

        # Try to join room group
        redis_client = redis.Redis(connection_pool=pool)
        lobby_text_data = redis_client.get(self.room_name)

        if (lobby_text_data != None):
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            lobby_state = json.loads(lobby_text_data)

            # TODO: Currently, we are only adding channel_name
            # We should be adding a persistent player ID to the lobby_state
            # Whenever a player connects, we should look for the player ID in players first
            # If it exists, we update the reconnected player's socket
            # i.e., lobby_state.players is an array of player data objects
            # A player data object might look like: { player_id: <some_id>, channel_name: self.channel_name }
            lobby_state.get("players").append(self.channel_name)
            redis_client.set(self.room_name, json.dumps(lobby_state))
            await self.accept()
        else:
            print("Error: Lobby %s does not exist" % self.room_name)
            self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

        # Delete from redis
        # TODO: We shouldn't actually delete the player from the redis instance
        # We need to set a timer - if the disconnected player doesn't come back in x seconds,
        # then we actually delete the player
        # ChatGPT this idk how to do this
        redis_client = redis.Redis(connection_pool=pool)
        lobby_state = json.loads(redis_client.get(self.room_name))
        lobby_state.get("players").remove(self.channel_name)
        redis_client.set(self.room_name, json.dumps(lobby_state))

    # Receive message from WebSocket
    async def receive(self, text_data):
        payload = json.loads(text_data)
        eventType = payload.get("eventType")

        # Send message to room group
        match eventType:
            case "start_game":
                redis_client = redis.Redis(connection_pool=pool)
                lobby_state = json.loads(redis_client.get(self.room_name))
                # initialize game state at payload.key

                # TODO: This is definitely not complete but works for now (see print on line 99)
                # We should probably put this in another method as well

                # -> initialize board
                board = [[None] * 10 for _ in range(10)]
                for i in range(10):
                    for j in range(10):
                        board[i][j] = {
                            "tile_id": "grass",
                            "passable": True
                        }

                # -> intialize units
                units = [None] * 8
                for i in range(4):
                    units[i] = {
                        "unit_id": "duelist",
                        "player_id": lobby_state["players"][0],
                        "hp": 4
                    }
                for i in range(4, 8):
                    units[i] = {
                        "unit_id": "duelist",
                        "player_id": lobby_state["players"][1],
                        "hp": 4
                    }

                # upsert to lobby_state
                lobby_state.update({"board": board, "units": units})
                redis_client.set(self.room_name, json.dumps(lobby_state))
                print(json.loads(redis_client.get(self.room_name)))

            case "move":
                # TODO: Implement move logic first
                try:
                    entity_table[payload.unit_type].move(payload)
                    await self.channel_layer.group_send(
                        self.room_name, {"type": "move",
                                         "message": "Unit moved on board"}
                    )
                except:
                    await self.channel_layer.group_send(
                        self.room_name, {
                            "type": "action_failed", "message": "Action was invalid, states may not be synced"
                        }
                    )

    # Receive message from room group
    async def move(self, event):
        # TODO: Think of event system to communicate changes to frontend
        message = event.message

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

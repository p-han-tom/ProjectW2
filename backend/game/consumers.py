import simplejson as json
import time
import threading
import redis
import os
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from .entity_lookup import entity_table

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                            port=int(os.getenv('REDIS_PORT')),
                            connection_class=redis.SSLConnection,
                            password=os.getenv('REDIS_PASSWORD'),
                            username=os.getenv('REDIS_USER'))

# TODO: Implement SpectatorConsumer (Low prio)
# class SpectatorConsumer(AsyncWebsocketConsumer):


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        query_params = parse_qs(self.scope['query_string'].decode())
        self.player_id = query_params['player_id']
        # TODO: Once there are two PlayerConsumer instances, we redirect all other connections to SpectatorConsumers

        # Try to join room group
        redis_client = redis.Redis(connection_pool=pool)
        lobby_text_data = redis_client.get(self.room_name)

        if (lobby_text_data != None):
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            lobby_state = json.loads(lobby_text_data)

            # Try to get player and update their current info
            players = lobby_state.get("players")
            curr_player = next((i for i, item in enumerate(players) if item['player_id'] == self.player_id), None)

            if (curr_player != None):
                players[curr_player]["last_connected"] = time.time()
            else:
                # Otherwise, this is a new player and we add their info to the lobby
                players.append(
                    {
                        "player_id": self.player_id,
                        "last_connected": time.time()
                    }
                )
            redis_client.set(self.room_name, json.dumps(lobby_state))
            await self.accept()
        else:
            print("Error: Lobby %s does not exist" % self.room_name)
            self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

        # Remove the player after <disconnect_limit> seconds of being disconnected
        #   unless they reconnect
        disconnect_time = time.time()
        disconnect_limit = 5
        await asyncio.sleep(disconnect_limit)

        redis_client = redis.Redis(connection_pool=pool)
        lobby_state = json.loads(redis_client.get(self.room_name))
        players = lobby_state.get("players")
        index = next(i for i, item in enumerate(players) if item['player_id'] == self.player_id)
        last_connected = players[index]["last_connected"]

        if (disconnect_time > last_connected or last_connected - disconnect_time > disconnect_limit * 1000):
            # remove the player
            del players[index]
            lobby_state.update({"players": players})
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

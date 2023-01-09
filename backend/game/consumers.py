import simplejson as json
import time
import random
import redis
import os
import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from .entity_lookup import entity_table

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                            port=int(os.getenv('REDIS_PORT')),
                            connection_class=redis.SSLConnection,
                            password=os.getenv('REDIS_PASSWORD'),
                            username=os.getenv('REDIS_USER'))

# TODO: Implement SpectatorConsumer (Low prio)
# class SpectatorConsumer(AsyncWebsocketConsumer):


class PlayerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"]
        query_params = parse_qs(self.scope['query_string'].decode())
        self.player_id = query_params['player_id'][0]
        # TODO: Once there are two PlayerConsumer instances, we redirect all other connections to SpectatorConsumers

        redis_client = redis.Redis(connection_pool=pool)
        lobby_text_data = redis_client.get(self.room_id)

        # Try to join lobby by id
        if (lobby_text_data == None):
            print("Error: Lobby %s does not exist" % self.room_id)
            await self.close()

        await self.channel_layer.group_add(self.room_id, self.channel_name)
        lobby_state = json.loads(lobby_text_data)

        # Try to get player and update their current info
        players = lobby_state.get("players")

        if (self.player_id in players):
            players[self.player_id]["last_connected"] = time.time()

            if (players[self.player_id]["ref_count"] == 0):
                # No player was connected, subtract from disconnect_limit
                players[self.player_id]["disconnect_limit"] -= (time.time() - players[self.player_id]["last_disconnected"])
                if (players[self.player_id]["disconnect_limit"] <= 0):
                    print("Player %s is out of time to reconnect" %
                          self.player_id)
                    # Player has been disconnected for too long, end the game
                    # End game logic here
                    pass
                print("New disconnect limit for player " + str(self.player_id) + ": " + str(players[self.player_id]["disconnect_limit"]))
            self.disconnect_limit = players[self.player_id]["disconnect_limit"]
            players[self.player_id]["ref_count"] += 1

        else:
            # Otherwise, this is a new player and we add their info to the lobby
            players[self.player_id] = {
                "player_id": self.player_id,
                "last_connected": time.time(),
                "disconnect_limit": 10,
                "ref_count": 1,
                "last_disconnected": None
            }
            self.disconnect_limit = 10
        redis_client.set(self.room_id, json.dumps(lobby_state))
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_id, self.channel_name)

        redis_client = redis.Redis(connection_pool=pool)
        lobby_state = json.loads(redis_client.get(self.room_id))
        players = lobby_state.get("players")

        # If a player has no more connections, then they are actually dc'd
        players[self.player_id]["ref_count"] -= 1
        disconnect_time = time.time()
        if (players[self.player_id]["ref_count"] == 0):
            # Update last disconnected time
            players[self.player_id]["last_disconnected"] = disconnect_time
        
            lobby_state.update({"players": players})
            redis_client.set(self.room_id, json.dumps(lobby_state))
            await asyncio.sleep(self.disconnect_limit)

            # After waiting, check if the player reconnected
            lobby_state = json.loads(redis_client.get(self.room_id))
            players = lobby_state.get("players")

            # If the player never reconnected
            if (disconnect_time > players[self.player_id]["last_connected"]):
                print("Player %s never reconnected" % self.player_id)
                # Then perform end of game logic
                pass
        else:
            lobby_state.update({"players": players})
            redis_client.set(self.room_id, json.dumps(lobby_state))
            return
        

    async def receive_json(self, content):
        eventType = content.get("eventType")

        # Send message to room group
        match eventType:
            case "start_game":
                redis_client = redis.Redis(connection_pool=pool)
                lobby_state = json.loads(redis_client.get(self.room_id))

                # Determine turn order
                turn_order = list(lobby_state["players"].keys())
                random.shuffle(turn_order)
                lobby_state["turn_order"] = turn_order

                # Initialize turn fields
                lobby_state["turns"] = 0
                lobby_state["curr_turn"] = 0 # index of turn_order

                # upsert to lobby_state
                redis_client.set(self.room_id, json.dumps(lobby_state))
            case "place_unit":
                unit_id = content.get("payload")["unit_type"]


                pass
            case "remove_unit":
                unit_id = content.get("payload")["unit_id"]
            case "move":
                # TODO: Implement move logic 
                try:
                    entity_table[content.get("event_type")].move(content)
                    await self.channel_layer.group_send(
                        self.room_id, {"type": "move",
                                         "message": "Unit moved on board"}
                    )
                except:
                    await self.channel_layer.group_send(
                        self.room_id, {
                            "type": "action_failed", "message": "Action was invalid, states may not be synced"
                        }
                    )
            # purely for testing
            case "reset":
                redis_client = redis.Redis(connection_pool=pool)
                redis_client.set(self.room_id, json.dumps({"players": {}}))

    # Receive message from room group
    async def move(self, event):
        # TODO: Think of event system to communicate changes to frontend
        message = event.get("message")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

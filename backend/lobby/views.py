from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import redis
import uuid
import json
import os

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                            port=int(os.getenv('REDIS_PORT')),
                            connection_class=redis.SSLConnection,
                            password=os.getenv('REDIS_PASSWORD'),
                            username=os.getenv('REDIS_USER'))


# for testing, create a lobby that others can join
# eventually, we want to make a matchmaking endpoint
@api_view(['GET'])
def create_lobby(request):
    # create new lobby key
    new_key = str(uuid.uuid4())

    # initialize game state in redis
    with redis.Redis(connection_pool=pool) as redis_client:
        new_game_state = {
            "players": {},
            "board": [
                [{
                    "tile_id": "grass",
                    "occupant_id": None,
                    "passable": True
                }] * 8 for _ in range(8)
            ],
            "active": False
            # add other states
        }
        redis_client.set(new_key, json.dumps(new_game_state))
    return Response({'lobby_code': new_key})

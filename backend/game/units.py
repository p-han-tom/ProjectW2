from abc import ABC, abstractmethod
import os
import redis
import simplejson as json

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                            port=int(os.getenv('REDIS_PORT')),
                            connection_class=redis.SSLConnection,
                            password=os.getenv('REDIS_PASSWORD'),
                            username=os.getenv('REDIS_USER'))


class Unit(ABC):
    @staticmethod
    @abstractmethod
    def move(payload): pass

    @staticmethod
    @abstractmethod
    def ability1(payload): pass


class Duelist(Unit):
    @staticmethod
    def move(payload):

        redis_client = redis.Redis(connection_pool=pool)
        game_state = json.loads(redis_client.get(payload.key))

        # validate the movement
        curr_pos = game_state.get("units")[payload.unit_id].get("position")
        new_pos = payload.get("target_cells")[0]

        if (
            (new_pos.get("row") >= game_state.board.length and new_pos.row < 0) or
            (new_pos.col >= game_state.board[0].length and new_pos.col < 0) or
            (not game_state.board[new_pos.row][new_pos.col].passable) or
            (abs(new_pos.row - curr_pos.row) +
             abs(new_pos.col - curr_pos.col) > 2)
        ):
            # send back some response explaining that the action failed, let player choose another action
            return

        # update tile pointers to units and unit position
        game_state.board[curr_pos.row][curr_pos.col].occupant_id = None
        game_state.board[new_pos.row][new_pos.col].occupantId = payload.unit_id
        game_state.units[payload.unit_id].position = new_pos

        # rewrite json to redis
        redis_client.set(payload.key, json.dumps(game_state))

    @staticmethod
    def ability1(payload):
        # sweeping edge attack, hits targets to the left and right of center unit

        redis_client = redis.Redis(connection_pool=pool)
        game_state = json.load(redis_client.get(payload.key))

        target_cell = payload.target_cells[0]
        curr_pos = game_state.units[payload.unit_id].position

        # validate that target cell is valid (distance from cell should be 1)
        if (
            (target_cell.row >= game_state.board.length and target_cell.row < 0) or
            (target_cell.col >= game_state.board[0].length and target_cell.col < 0) or
            (abs(target_cell.row - curr_pos.row) +
             abs(target_cell.col - curr_pos.col) != 1)
        ):
            return

        # loop through target cells
        if target_cell.row == curr_pos.row:
            # strike is left or right of unit
            for row in range(max(0, target_cell.row - 1), min(game_state.board.length, target_cell.row + 1)):
                occupant_id = game_state.board[row][target_cell.col].occupant_id
                if occupant_id != None:
                    game_state.units[occupant_id].hp -= 2
        else:
            # strike is up or down of unit
            for col in range(max(0, target_cell.col - 1), min(game_state.board[0].length, target_cell.col + 1)):
                occupant_id = game_state.board[target_cell.row][col].occupant_id
                if occupant_id != None:
                    game_state.units[occupant_id].hp -= 2

        redis_client.set(payload.key, json.dumps(game_state))

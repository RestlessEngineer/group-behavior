from Robot import *
from RobotFileld import *

class Simulation:

    _filed: RobotField = None
    _robots: list[Robot] = []


    def __init__(self, field: RobotField, robots: list[Robot]):
        self._field = field
        self._robots = robots


    def do_step(self):
        robots = self._robots.copy()
        
        adjacencyList = self._make_adjastment()
        strategies = setting_active(adjacencyList, self._robots)
        for (robot, strategy) in strategies.items():
            if strategy == 1:
                robot.move_strategy = MoveStrategy.ACTIVE

        for robot in self._robots:
            except_one = list(filter(lambda x: x != robot, robots))
            robot.do_next_step(except_one)
        
        for robot in self._robots:
            robot.move_strategy == MoveStrategy.PASSIVE


    def get_robots(self):
        return self._robots


    def is_all_robots_on_goals(self):
        for robot in self._robots:
            if robot.location != robot.goal:
                return False
        return True


    def _make_adjastment(self):
        adjacencyList = {}
        for vertex in self._robots:
            adjacencyList[vertex] = []
        
        robots = self._robots.copy()
        for robot in self._robots:
            except_one = list(filter(lambda x: x != robot, robots))
            for other_robot in except_one:
                if robot.distance(other_robot) < 2:
                    adjacencyList[robot].append(other_robot)
        return adjacencyList


def setting_active(adjacency: dict[int, list[int]], vertices: set[int]):
    queue = []
    states = {}
    for val in vertices:
        states[val] = -1

    #every isolate nodes is passive
    for (key, adj) in adjacency.items():
        if len(adj) == 0:
            states[key] = 0   

    min = 10000
    for (key, adj) in adjacency.items():
        if len(adj) < min and len(adj) > 0:
            min = len(adj)
    
    for (key, adj) in adjacency.items():
        if min == len(adj):
            queue.append(key)
    
    while len(queue) > 0:
        node = queue.pop(0)
        if states[node] == -1:
            states[node] = 1
            for adj in adjacency[node]:
                states[adj] = 0
                queue.append(adj)
        elif states[node] == 0:
            for adj in adjacency[node]:
                if states[adj] == -1:
                    queue.append(adj)

    return states


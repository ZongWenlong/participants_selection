# coding: utf-8


class TrajectoryRoadTriple:
    """轨迹匹配结果中，轨迹点对应的匹配路段
        [road_id, start_time, end_time]
    """
    def __init__(self, road_id="", start_time="", end_time=""):
        self.road_id = road_id
        self.start_time = start_time
        self.end_time = end_time


class Trajectory:
    """轨迹匹配结果
        id, [[road_id, start_time, end_time], [road_id, start_time, end_time], ...]
    """
    def __init__(self, vehicle_id="", roads=None):
        self.vehicle_id = vehicle_id
        if roads is None:
            self.roads = []
        else:
            self.roads = roads


class Road:
    """ 道路
        id, length, oneway
            oneway 1 - 单向
                   0 - 双向
    """
    def __init__(self, road_id="", length=0, oneway=1):
        self.road_id = road_id
        self.length = length
        self.oneway = oneway

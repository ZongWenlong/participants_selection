# coding: utf-8
import os


class TrajectoryRoadTriple:
    """轨迹匹配结果中，轨迹点对应的匹配路段
        [road_id, start_time, end_time]
    """
    def __init__(self, road_id, start_time, end_time):
        self.road_id = road_id
        self.start_time = start_time
        self.end_time = end_time


class Trajectory:
    """轨迹匹配结果
        id, [[road_id, start_time, end_time], [road_id, start_time, end_time], ...]
    """
    def __init__(self, vehicle_id = "", roads = None):
        self.vehicle_id = vehicle_id
        if roads is None:
            self.roads = []
        else:
            self.roads = roads


"""
 输入文件格式
     093452,20121108001613,116.30156,39.962814,47,59567212407
     车辆编号，时间戳，经度，纬度，速度，道路编号
 输出格式
    [vehicle_id,  [[road_id, start_time, end_time], [road_id, start_time, end_time], ...]]
"""


in_path = "E:\\workspaces\\MDT\\test\\3-match"
files = os.listdir(in_path)
ID_INDEX = 0
TIME_INDEX = 1
ROAD_ID_INDEX = 5

vehicles = []
for f in files:
    if not os.path.isdir(f):
        reader = open(in_path + '/' + f)
        pre_road_id = 0
        first = True
        for line in reader:
            record = line.split(',')
            print type(record[ID_INDEX])

        reader.close()

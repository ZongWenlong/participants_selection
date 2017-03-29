# coding: utf-8

import os
import pickle
from storage.model import *


def dump_trajectory(in_path, out_path):
    """
     输入文件格式
         093452,20121108001613,116.30156,39.962814,47,59567212407
         车辆编号，时间戳，经度，纬度，速度，道路编号
     输出格式:
        Trajectory 数组
        [vehicle_id,  [[road_id, start_time, end_time], [road_id, start_time, end_time], ...]]
     :param in_path: 输入文件夹路径，即需要载入in_path文件夹下所有文件
     :param out_path: 输出文件路径
    """
    files = os.listdir(in_path)
    id_index = 0
    time_index = 1
    road_id_index = 5

    match_result = []
    for f in files:
        if not os.path.isdir(f):
            reader = open(in_path + '/' + f)
            pre_road_id = 0
            first = True
            trajectory = Trajectory()
            road_triple = TrajectoryRoadTriple()
            for line in reader:
                line = line.strip('\n')
                record = line.split(',')
                cur_road_id = record[road_id_index]

                # 新的道路编号记录
                if pre_road_id != cur_road_id:
                    if not first:
                        road_triple = TrajectoryRoadTriple(cur_road_id, record[time_index], record[time_index])
                    else:
                        trajectory.vehicle_id = record[id_index]
                        road_triple.road_id = cur_road_id
                        road_triple.start_time = record[time_index]
                        road_triple.end_time = record[time_index]
                        first = False
                    pre_road_id = cur_road_id
                    trajectory.roads.append(road_triple)
                else:
                    if cmp(road_triple.start_time, record[time_index]) == 1:
                        road_triple.start_time = record[time_index]

                    if cmp(road_triple.end_time, record[time_index]) == -1:
                        road_triple.end_time = record[time_index]

            reader.close()
            match_result.append(trajectory)

    # output data to file
    serialize(out_path, match_result)


def dump_road(in_path, out_path):
    """
        载入道路数据, 文件内数据格式为:
            [59567200001,1100,1097,0.07,116.348854,39.939396,116.348114,39.939137,20.0,1]
            [道路id, 起点id, 终点id, 长度，起点坐标，终点坐标，平均速度，单双向]
    :param in_path: 道路数据输入路径
    :param out_path: 序列化数据输出文件路径
    """
    reader = open(in_path)
    id_index = 0
    len_index = 3
    oneway_index = 9

    road_array = []
    for line in reader:
        line = line.strip('\n')
        record = line.split(',')
        road = Road(record[id_index], float(record[len_index]), int(record[oneway_index]))
        road_array.append(road)

    # output data to file
    serialize(out_path, road_array)


def serialize(path, data):
    """
        序列化数据导出到指定文件
    :param path: 文件路径
    :param data: 数据
    """
    f = open(path, 'wb')
    pickle.dump(data, f)
    f.close()

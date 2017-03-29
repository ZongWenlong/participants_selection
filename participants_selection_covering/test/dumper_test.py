# coding: utf-8

from storage.dumper import *


def dump_test():
    dump_traj_test()
    dump_road_test()


def dump_traj_test():
    in_path_traj = "E:\\workspaces\\MDT\\test\\3-match"
    out_path_traj = "E:\\workspaces\\MDT\\test\\5-serialize\\trajectory"
    dump_trajectory(in_path_traj, out_path_traj)
    f = open(out_path_traj, 'rb')
    match_result = pickle.load(f)
    f.close()
    for m in match_result:
        print m.vehicle_id
        for r in m.roads:
            print r.road_id, r.start_time, r.end_time


def dump_road_test():
    in_path_road = "E:\\workspaces\\MDT\\test\\1-road\\grid\\road.txt"
    out_path_road = "E:\\workspaces\\MDT\\test\\5-serialize\\road"
    dump_road(in_path_road, out_path_road)

    f = open(out_path_road, 'rb')
    roads = pickle.load(f)
    f.close()
    for r in roads:
        print r.road_id, r.length, r.oneway

dump_test()


# coding: utf-8
from util.map_util import *

polygonCount = int(input())
polygon = []
for i in range(0, polygonCount):
    pointStr = input().split()
    point = Point(pointStr[0], pointStr[1])
    polygon.append(point)

testPointCount = int(input())
points = []
for i in range(0, testPointCount):
    pointStr = input().split()
    point = Point(pointStr[0], pointStr[1])
    points.append(point)

for p in points:
    print(in_convex_polygon(polygon, p))



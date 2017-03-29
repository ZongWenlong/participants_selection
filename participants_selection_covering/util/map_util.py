# coding: utf-8
""" 判断点是否在多边形内
    Reference: http://www.cnblogs.com/yym2013/p/3673616.html
"""


class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


# 求p1p0和p2p0的叉积,如果大于0,则p1在p2的顺时针方向
def multiply(p1, p2, p0):
    return (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)


def in_convex_polygon(polygon, target):
    """
    :type polygon: list[Point]
    :type target: Point
    :rtype: bool

    判断点target 是否在 凸多边形polygon内部
    :param polygon:Point数组，代表凸多边形的顶点，顺时针给出
    :param target:  Point对象，代表待查询的顶点
    :return: ture - target在凸多边形内

    """
    eps = 1e-10
    n = len(polygon) - 1
    #  在第一个点为起点的扇形之外或在边上
    if multiply(target, polygon[1], polygon[0]) <= eps or multiply(target, polygon[n], polygon[0]) >= -eps:
        return False
    left = 2
    right = n

    while right - left != 1:
        mid = (left+right) / 2
        if multiply(target, polygon[mid], polygon[0]) > eps:
            left = mid
        else:
            right = mid
    # 在边之外或在边上
    if multiply(target, polygon[right], polygon[left]) <= eps:
        return False
    return True



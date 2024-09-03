########################################################
# some function which are used without a special class #
########################################################

from math import sqrt

from .global_variables import startPoints, wireList

def distance_to_line_segment(line, point):
    """
    Calculate the shortest distance from a point to a line segment.

    :param line: QLineF object representing the line segment.
    :param point: QPointF object representing the point.
    :return: The shortest distance from the point to the line segment.
    """
    x1, y1 = line.p1().x(), line.p1().y()
    x2, y2 = line.p2().x(), line.p2().y()
    px, py = point.x(), point.y()

    # Calculate the line segment vector
    line_vec_x = x2 - x1
    line_vec_y = y2 - y1

    # Calculate the vector from the point to the line's start point
    point_vec_x = px - x1
    point_vec_y = py - y1

    # Calculate the projection of the point vector onto the line vector
    line_len_sq = line_vec_x ** 2 + line_vec_y ** 2
    if line_len_sq == 0:
        return sqrt(point_vec_x ** 2 + point_vec_y ** 2)  # Start and end points are the same

    t = (point_vec_x * line_vec_x + point_vec_y * line_vec_y) / line_len_sq

    # Clamp the projection to the segment
    t = max(0, min(1, t))

    # Find the closest point on the line segment
    closest_x = x1 + t * line_vec_x
    closest_y = y1 + t * line_vec_y

    # Calculate the distance from the point to the closest point on the line segment
    dist_x = px - closest_x
    dist_y = py - closest_y

    return sqrt(dist_x ** 2 + dist_y ** 2)

def is_point_on_line(line, point, tolerance=10.0):
    """
    Check if a point is close enough to a line to be considered as 'clicked' on it.

    :param line: QLineF object representing the line.
    :param point: QPointF object representing the point (click position).
    :param tolerance: Distance tolerance to determine if the point is on the line.
    :return: True if point is within tolerance distance from the line, otherwise False.
    """
    distance = distance_to_line_segment(line, point)
    return distance <= tolerance

def globalSimulationRun():
    print('start to run simulation')
    print()
    for id, startPoint in startPoints.items():
        for wireId in startPoint.outWire:
            wireList[wireId].setState(id)
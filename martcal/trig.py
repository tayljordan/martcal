import trianglesolver as triangle

def angular_distance(angle1: float, angle2: float):
    if angle2 < 180:
        angle2 = angle2 + 360 - 180
    else:
        angle2 = angle2 - 180

    c_max = max([angle1, angle2])
    c_min = min([angle1, angle2])

    angle = c_max - c_min

    if angle > 180:
        angle -= 180

    return angle

def distance(a: float, b: float, gamma: float):
    C = gamma * triangle.degree
    result = triangle.solve(b=b, a=a, C=C)
    return result[2]

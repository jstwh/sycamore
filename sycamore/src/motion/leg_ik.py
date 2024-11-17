import math
import numpy as np

def ja_from_xy(x: float, y: float, l1: float, l2: float) -> tuple[int, int]:
    """
    L1, L2 lengths of the arms in mm
    x, y coordinates where the arm should go
    """
    upper = x**2 + y**2 - l1**2 - l2**2
    lower = 2 * l1 * l2

    try:
        temp = math.acos(upper/lower)
    except:
        print("Out of bounds")
        return None
    
    if x == 0:
        x += 0.001
    
    q2 = math.degrees(temp)
    
    # q1 angle
    a = math.atan(y/x)
    
    a1 = (l2 * math.sin(math.radians(q2)))
    b1 = l1 + (l2 * math.cos(math.radians(q2)))
    c = math.radians(a1)/math.radians(b1)

    b= math.atan(c)
    q1 = math.degrees(a-b)
    
    return (int(q1), int(q2))

def xy_from_ja(theta_1: float, theta_2: float, L1: float, L2: float) -> tuple[float, float]:
    """
    L1, L2 lengths of the arms in mm
    theta_1, theta_2 joint angles in degrees
    """
    x = L1 * math.cos(np.radians(theta_1)) + L2 * math.cos(np.radians(theta_1) + np.radians(theta_2))
    y = L1 * math.sin(np.radians(theta_1)) + L2 * math.sin(np.radians(theta_1) + np.radians(theta_2))
    return (int(x), int(y))

if __name__ == "__main__":
    target_x = 40
    target_y = 60
    l1 = 100
    l2 = 100
    t_1, t_2 = ja_from_xy(0, -150, 100, 100)
    print(t_1, t_2)
    calculated_x, calculated_y = xy_from_ja(t_1, t_2, 100, 100)
    print(calculated_x, calculated_y)

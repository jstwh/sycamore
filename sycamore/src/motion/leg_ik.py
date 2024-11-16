import math

def ja_from_xy(x: float, y: float, L1: float, L2: float) -> tuple[int, int]:
    """
    L1, L2 lengths of the arms in cm
    x, y coordinates where the arm should go
    """
    r = math.sqrt(x**2 + y**2)

    if L1 + L2 < r:
        raise ValueError("Out of bounds")
    
    theta_2 = math.acos((L1**2+L2**2-r**2)/(2*L1*L2))
    phi = math.atan2(y, x)
    beta = math.atan2(L2*math.sin(theta_2), L1+L2*math.cos(theta_2))
    theta_1 = phi - beta

    return (math.degrees(theta_1), math.degrees(theta_2))

if __name__ == "__main__":
    # all in mm
    target_x = 40
    target_y = 60
    L1 = 100
    L2 = 100
    print(ja_from_xy(target_x, target_y, L1, L2))

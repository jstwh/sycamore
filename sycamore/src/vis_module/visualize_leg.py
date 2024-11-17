import numpy as np
import matplotlib.pyplot as plt
import math

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

    # Bruh
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
    
    return (int(normalize_angle(q1)), int(normalize_angle(q2)))

def normalize_angle(angle):
    """
    Useful for servo ranges
    """
    angle = (angle + 180) % 360 - 180
    return angle

def draw_leg(x, y, L1, L2):
    theta1, theta2 = ja_from_xy(x, y, L1, L2)
    
    print(f"Calculated Angles: Theta1: {theta1}°, Theta2: {theta2}°")

    theta1 = np.radians(theta1)
    theta2 = np.radians(theta2)

    x0, y0 = 0, 0
    
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)

    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    print(f"Joint 1 (x1, y1): ({x1}, {y1})")
    print(f"Joint 2 (x2, y2): ({x2}, {y2})")
    
    plt.figure()
    plt.plot([x0, x1], [y0, y1])
    plt.plot([x1, x2], [y1, y2])

    plt.xlim(-L1-L2, L1+L2)
    plt.ylim(-L1-L2, L1+L2)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    plt.gca().set_aspect('equal')

    plt.show()

if __name__ == "__main__":
    L1 = 100
    L2 = 100
    x = 0
    y = -150
    draw_leg(x, y, L1, L2)
import math

def inverse_kinematics_dh(x, y, z, L1, L2):
    """Calculate joint angles for a 3-DoF robot leg using DH parameters."""
    try:
        # Hip joint angle (θ₁)
        theta_hip = math.atan2(y, x)

        # Denavit-Hartenberg
        r = math.sqrt(x**2 + y**2)
        d = math.sqrt(r**2 + z**2) 

        # Check if the point is within reach
        if d > (L1 + L2):
            raise ValueError("Target point is out of reach")

        # Shoulder joint angle (θ₂)
        alpha = math.atan2(z, r)
        beta = math.acos((L1**2 + d**2 - L2**2) / (2 * L1 * d))
        theta_shoulder = alpha + beta

        # Knee joint angle (θ₃)
        theta_knee = math.acos((L1**2 + L2**2 - d**2) / (2 * L1 * L2))
        
        return theta_hip, theta_shoulder, theta_knee

    except ValueError as e:
        print(f"Error in IK calculation: {e}")
        return None

L1 = 10.0
L2 = 10.0

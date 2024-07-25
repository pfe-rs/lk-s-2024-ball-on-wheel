

def Geterror(setpoint,speednow):
    #racunanje errora
    error=setpoint-speednow
    return error


def pid(error,kp,ki,kd,dt):
    proportional = error
    integral += error * dt
    derivative = (error - previous) / dt
    previous = error
    output = ((kp * proportional)+1)+ (integral*ki)+(derivative*kd)
    return output












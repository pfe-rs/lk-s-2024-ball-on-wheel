

def Geterror(setpoint,speednow):
    #racunanje errora
    error=setpoint-speednow
    return error


def pid(error,dt):
    kp=0.8
    proportional = error
    #integral += error * dt
    #derivative = (error - previous) / dt
    #previous = error
    output = (kp * proportional)+1
    return output












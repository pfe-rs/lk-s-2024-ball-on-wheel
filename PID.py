
def Encoder():
    #brzina iz arduina
    return
    


def Time():
    #vreme iz arduina
    return

def Geterror(setpoint=500,speednow=Encoder()):
    #racunanje errora
    error=setpoint-speednow
    return error


def pid(error=Geterror(),dt=Time()):
    kp=0.8
    proportional = error
    #integral += error * dt
    #derivative = (error - previous) / dt
    #previous = error
    output = (kp * proportional)
    return output


def OutPut(speed=pid()):
    #salje speed na motor
    return



OutPut()






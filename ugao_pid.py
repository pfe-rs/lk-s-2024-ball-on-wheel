def Geterror(angle,angle_ref):
    error = angle_ref-angle
    return error


def pid(error, dt):
    Kp=0.8
    Ki = 0
    Kd = 0
    integral += error * dt
    derivative = (error - previous) / dt
    previous = error
    P = Kp*error
    I = integral*Ki
    D = Kd * derivative
    potrebna_ugaona_brzina_tocka = P + I + D
    return potrebna_ugaona_brzina_tocka

#angle getujes iz detekcije
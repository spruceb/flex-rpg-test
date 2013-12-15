import math

def normalize(vector):
    magnatude = math.sqrt(vector[0]**2 + vector[1]**2)
    return vector[0]/magnatude, vector[1]/magnatude


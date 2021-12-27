def reward(speedX, angle, trackPos):
	
    if trackPos > 1 or trackPos < -1:
        return -200
    else:
        return speedX*cos(angle) - speedX*abs(sin(angle)) - speedX*abs(trackPos)
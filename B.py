coord = [51,8,255,14,11,31,255,46,68,3,255,44,14,75,255,36,35,5,255,43,16,34,255,16,13,47,255,32,0,0,0]
result = []
while coord[-1] == 0:
    coord.pop(-1)
i = 0
tempy = ''
while i < len(coord)-1:
    if coord[i] != 255:
        tempy += str(coord[i])
    else:
        i += 1
        result.append((int(tempy), coord[i]))
        tempy = ''
    i += 1
print(result)


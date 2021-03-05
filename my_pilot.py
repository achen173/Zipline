import sys
import struct
import csv
result = []

MAX_X = 2000    # 0 - 2000
MAX_Y = 50      # -25 - 25

def get_direction(data):
    lidar_samples = data['sample']
    group = 5
    lidar_samples = [sum(lidar_samples[x-group:x])/group for x in range(group, len(lidar_samples))]
    right, left = False, False
    sample_len = len(lidar_samples)
    median_index = sample_len // 2
    median_nbr = lidar_samples[median_index]
    if median_nbr == 0:
        return (right, left)
    else:
        x = 1
        mini = median_nbr
        while median_index-x >= 0 and median_index+x < sample_len:
            data_left, data_right = lidar_samples[median_index-x], lidar_samples[median_index+x]
            if data_left == 0:
                return (True, False)
            elif data_right == 0:
                return (False, True)
            if data_left < mini:
                right, left = False, True
                mini = data_left
            if data_right < mini:
                right, left = True, False
                mini = data_right
            x += 1
        return right, left
    
def get_struct(windY, right, left):
    if right:
        ideal = -10
        if windY > 0:
            speed = ideal - windY
        else:
            speed = ideal + abs(windY)
        ans = struct.pack(">fBBBB", speed, 0, 0, 0, 0)
    elif left:
        ideal = 10
        if windY > 0:
            speed = ideal - windY
        else:
            speed = ideal + abs(windY)
        ans = struct.pack(">fBBBB", speed, 0, 0, 0, 0)
    else:
        ans = struct.pack(">fBBBB", -1*windY, 0, 0, 0, 0)
    return ans

def add_coord(coord):
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

with open('test.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    landing_X = []
    landing_coord = {}  # X:Y
    while True:
        x = sys.stdin.buffer.read(struct.calcsize(">Hhffb31B"))
        sim_input = list(struct.unpack(">Hhffb31B", x))
        data = {'time': sim_input[0], 'recX': sim_input[1], 'windX': sim_input[2], 'windY': sim_input[3], 'recY': sim_input[4],'sample': sim_input[-31:]}
        if data['time'] == 65535:   # this is for getting the landing coord
            add_coord(data['sample'])
            ans = struct.pack(">fBBBB", 0, 0, 0, 0, 0)
            spamwriter.writerow(sim_input)
            sys.stdout.buffer.write(ans)
            sys.stdout.buffer.flush()
        else:
            if data['recX'] <= 35:  # landing
                # derive lateral airspeed based on windX and recY
                if data['recY'] == 0:   # maintain course
                    ans = struct.pack(">fBBBB", -1*data['windY'], 0, 0, 0, 0)
                    spamwriter.writerow(sim_input)
                    sys.stdout.buffer.write(ans)
                    sys.stdout.buffer.flush()
                else:
                    if abs(data['recY']) >= 22:
                        ans = struct.pack(">fBBBB", (abs(data['recY'])/data['recY'])*30, 0, 0, 0, 0)
                        spamwriter.writerow(sim_input)
                        sys.stdout.buffer.write(ans)
                        sys.stdout.buffer.flush()
                    else:
                        ans = struct.pack(">fBBBB", (abs(data['recY'])/data['recY'])*30, 0, 0, 0, 0)
                        spamwriter.writerow(sim_input)
                        sys.stdout.buffer.write(ans)
                        sys.stdout.buffer.flush()
            else:
                right, left = get_direction(data)
                ans = get_struct(data['windY'], right, left)
                spamwriter.writerow(sim_input)
                sys.stdout.buffer.write(ans)
                sys.stdout.buffer.flush()

import sys
import struct
import csv
result = []
data = {}
MAX_X = 2000    # 0 - 2000
MAX_Y = 50      # -25 - 25

def struct_format(speed, drop):
    # speed = -/+30m/s
    # drop = 1/0
    return struct.pack(">fBBBB", speed, drop, 0, 0, 0)

def get_direction(data):
    lidar_samples = data['sample']
    group = 3
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
    
def get_struct(windY, right, left, drop):
    if right:
        ideal = -60
        if windY > 0:
            speed = ideal - windY
        else:
            speed = ideal + abs(windY)
        ans = struct_format(speed, drop)
    elif left:
        ideal = 60
        if windY > 0:
            speed = ideal - windY
        else:
            speed = ideal + abs(windY)
        ans = struct_format(speed, drop)
    else:
        ans = struct_format(-1*windY, drop)
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

def writeback(ans):
    sys.stdout.buffer.write(ans)
    sys.stdout.buffer.flush()

def avoid_sidelines(recY):
    ans = struct_format((abs(recY)/recY)*30, 0)
    writeback(ans)

def read_buffer():
    try:
        x = sys.stdin.buffer.read(struct.calcsize(">Hhffb31B"))
        sim_input = list(struct.unpack(">Hhffb31B", x))
        global data
        data = {'time': sim_input[0], 'recX': sim_input[1], 'windX': sim_input[2], 'windY': sim_input[3], 'recY': sim_input[4],'sample': sim_input[-31:]}
        return False
    except:
        exit()
        return True


while True:
    error = read_buffer()
    if error:
        break
    if data['time'] == 65535:   # this is for getting the landing coord
        add_coord(data['sample'])
        ans = struct_format(0, 0)
        writeback(ans)
    else:
        landing = False
        if len(result) > 0:
            temp_max = MAX_X - result[0][0] + 39
            temp_min = MAX_X - result[0][0] - 3
            landing = True

        if abs(data['recY']) >= 22: # remove getting stuck on the side
            avoid_sidelines(data['recY'])

        elif landing and data['recX'] < temp_max and data['recX'] > temp_min: #1927 # for package landing
            wantY = result[0][1]
            if wantY > 25:
                wantY = -51 + wantY

            while data['recX'] < temp_max and data['recX'] > temp_min:
                data['recY'] = data['recY'] * -1
                if data['recX'] == 2000 - result[0][0] + 9: # wwithin range of dropping package
                    ans = get_struct(data['windY'], False, False, 1)
                    writeback(ans)
                    error = read_buffer()
                    if error:
                        break
                    break
                if abs(data['recY']) >= 23:
                    ans = struct_format((abs(data['recY'])/data['recY'])*45, 0)
                    writeback(ans)
                    error = read_buffer()
                    if error:
                        break
                else:
                    if wantY > data['recY']:
                        ans = get_struct(data['windY'], False, True, 0)
                    elif wantY < data['recY']:
                        ans = get_struct(data['windY'], True, False, 0)
                    else:
                        ans = get_struct(data['windY'], False, False, 0)
                    writeback(ans)
                    error = read_buffer()
                    if error:
                        break
            result.pop(0)
            ans = get_struct(data['windY'], False, False, 0)
            writeback(ans)

        elif data['recX'] <= 35:  # landing
            # derive lateral airspeed based on windX and recY
            if data['recY'] == 0:   # maintain course
                ans = struct_format(-1*data['windY'], 0)
                writeback(ans)
            else:
                if abs(data['recY']) >= 22:
                    avoid_sidelines(data['recY'])
                else:
                    ans = struct_format((abs(data['recY'])/data['recY'])*30, 0)
                    writeback(ans)
        else:   # dodge trees
            right, left = get_direction(data)
            ans = get_struct(data['windY'], right, left, 0)
            writeback(ans)

import sys
import struct
import errno
import csv

def get_direction(lidar_samples):
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
        return (right, left)


with open('test.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    while True:
        x = sys.stdin.buffer.read(struct.calcsize(">Hhffb31B"))
        sim_input = list(struct.unpack(">Hhffb31B", x))
        data = {'time': sim_input[0], 'recX': sim_input[1], 'windX': sim_input[2], 'windY': sim_input[3], 'recY': sim_input[4],'sample': sim_input[-31:]}
        right, left = get_direction(data['sample'])
        if right:
            ideal = -20
            if data['windY'] > 0:
                speed = ideal - data['windY']
            else:
                speed = ideal + abs(data['windY'])
            ans = struct.pack(">fBBBB", speed, 0, 0, 0, 0)
        elif left:
            ideal = 20
            if data['windY'] > 0:
                speed = ideal - data['windY']
            else:
                speed = ideal + abs(data['windY'])
            ans = struct.pack(">fBBBB", speed, 0, 0, 0, 0)
        else:
            ans = struct.pack(">fBBBB", -1*data['windY'], 0, 0, 0, 0)
        # spamwriter.writerow(list(struct.unpack(">Hhffb31B", x)))
        # ans = struct.pack(">fBBBB", 0, 0, 0, 0, 0)
        sys.stdout.buffer.write(ans)
        sys.stdout.buffer.flush()







# import sys
# import struct
# import csv
# import subprocess
#
# with open('test.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     x = sys.stdin.buffer.read(struct.calcsize(">Hhffb31B"))
#     spamwriter.writerow([x, len(x)])
#     spamwriter.writerow(list(struct.unpack(">Hhffb31B", x)))
#     # spamwriter.writerow([len(bytes(line, 'utf-8'))])
#     ans = struct.pack(">fBBBB", 0, 0, 0, 0, 0)
#     spamwriter.writerow([ans, len(ans)])
#     sys.stdout.buffer.write(ans)
#     sys.stdout.buffer.flush()
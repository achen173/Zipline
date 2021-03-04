myin = [16,1994,1.2732183933258057,17.770814895629883,0,0,0,0,119,119,0,0,0,0,0,0,0,0,0,198,0,0,206,0,0,0,0,0,0,0,0,120,119,120,0,214]
print(len(myin))
data = {'time':myin[0], 'recX':myin[1], 'windX':myin[2], 'windY':myin[3],'recY':myin[4], 'sample': myin[-31:]}
print(data)
mysample = data['sample']
# middle = mysample[len(mysample)//2]
def get_direction(lidar_samples):
    print(len(lidar_samples))
    group = 5
    lidar_samples = [sum(lidar_samples[x-group:x])/group for x in range(group, len(lidar_samples)+1)]
    print(lidar_samples)
    right, left = False, False
    sample_len = len(lidar_samples)
    median_index = sample_len // 2
    median_nbr = lidar_samples[median_index]
    print(median_nbr)
    if median_nbr == 0:
        return (right, left, 0)
    else:
        x = 1
        mini = median_nbr
        resultant = 0
        while median_index-x >= 0 and median_index+x < sample_len:
            data_left, data_right = lidar_samples[median_index-x], lidar_samples[median_index+x]
            if data_left == 0:
                return (True, False, -1*x)
            elif data_right == 0:
                return (False, True, x)
            if data_left < mini:
                right, left = False, True
                mini = data_left
                resultant = -1*x
            if data_right < mini:
                right, left = True, False
                mini = data_right
                resultant = 1 * x
            x += 1
        return (right, left, resultant)

right, left, index = get_direction(mysample)
print(right, left, index)

# print(middle)
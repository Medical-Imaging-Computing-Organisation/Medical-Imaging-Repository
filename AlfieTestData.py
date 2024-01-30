# Generating test data for Alfie
# Format [[detector index, energy, time, delta E, delta t], ...] for each detector

# Detector 1 
detector1_fake_arr = np.ndarray((4000000,5), dtype=np.float32)
detector1_fake_arr[:,0] = 0
detector1_fake_arr[:,1] = 662
detector1_fake_arr[:,2] = np.arange(1414, 4001414, 1)
detector1_fake_arr[:,3] = np.random.rand(4000000)
detector1_fake_arr[:,4] = np.random.rand(4000000)

detector2_fake_arr = np.ndarray((4000000,5), dtype=np.float32)
detector2_fake_arr[:,0] = 1
detector2_fake_arr[:,1] = 662
detector2_fake_arr[:1000000,2] = np.arange(1414.2, 1001414.2, 1) # 0.2 time units apart for the first 1 million data points
detector2_fake_arr[1000000:2000000,2] = np.arange(2414, 1002414, 1) # 1000 time units apart for the second 1 million data points
detector2_fake_arr[2000000:3000000,2] = np.arange(2001414.3, 3001414.3, 1) # 0.3 time units apart for the third 1 million data points
detector2_fake_arr[3000000:4000000,2] = np.arange(8001414.3, 9001413.3, 1) # a lot of time units apart for the third 1 million data points
detector2_fake_arr[:,3] = np.random.rand(4000000)
detector2_fake_arr[:,4] = np.random.rand(4000000)
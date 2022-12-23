import numpy as np

class FileUtil:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.num_state = 0
        self.transition = 0
        self.R = None
        
    def parse_tra_file(self):
        contents = open(self.file_path, 'r')
        i = 0
        
        for line in contents.readlines():
            data = line.rstrip().split(' ')    
            if i == 0: # assume num state in first line
                self.num_state = int(data[1])
                self.R = np.zeros((self.num_state, self.num_state), dtype=np.int32)
            elif i == 1:  # assume num transition in second line
                self.transition = int(data[1])
            else:
                self.R[int(data[0]) - 1, int(data[1]) - 1] = int(data[2])
            i += 1
            
        return self.R
    
    def parse_reward_file(self, state):
        reward = np.zeros(state, dtype=np.int32)
        contents = open(self.file_path, 'r')
        
        for line in contents.readlines():
            data = line.rstrip().split(' ') 
            reward[int(data[0])-1] = int(data[1])
            
        return reward
    
    def parse_pi_file(self, state):
        pi_0 = np.zeros(state, dtype=np.float32)
        contents = open(self.file_path, 'r')
        
        for line in contents.readlines():
            data = line.rstrip().split(' ') 
            pi_0[int(data[0])-1] = float(data[1])
            
        return pi_0

    def save(self, content, path):
        np.savetxt(path, content, delimiter=',')
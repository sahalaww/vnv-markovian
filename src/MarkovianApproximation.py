import numpy as np
import scipy as scp
from scipy.sparse import csr_matrix
from scipy.stats import poisson

class MarkovianApproximation():
    
    def __init__(self, R, 
                 S, 
                 num_state, 
                 pi_0,
                 r, 
                 t_max, 
                 y_max, 
                 delta, 
                 epsilon=10e-4):
        
        self.R = R
        self.S = S
        self.num_state = num_state
        self.pi_0 = pi_0
        self.r = r
        self.t_max = t_max
        self.y_max = y_max
        self.delta = delta
        self.epsilon =  epsilon
        self.Q = self.generate_Q_matrix(R)
        self.D = self.generate_D_matrix(r)

    def generate_Q_matrix(self, R):
        """_Q matrix generator_

        Args:
            R : matrix or 2d array

        Returns:
            R : matrix or 2d array
        """
        length = len(R)
        
        for i in range(0, length):
            R[i][i] = -1 * np.sum(R[i][:])
        
        return R
    
    def generate_D_matrix(self, r):
        """_summary_

        Args:
            r (_type_): _description_

        Returns:
            _type_: _description_
        """
        return np.diag(r)
    
    
    def create_Qinf_transition_matrix(self, reward, dy, num_state, Q, D):
        """_summary_

        Args:
            reward (_type_): _description_
            dy (_type_): _description_
            num_state (_type_): _description_
            Q (_type_): _description_
            D (_type_): _description_

        Returns:
            _type_: _description_
        """
        new_transition = int(reward / dy)
        size_c = new_transition * num_state
        C = np.zeros((size_c, size_c))
        C = np.asmatrix(C)
        size_q = len(Q)
        size_d= len(D)
        
        for i in range(0, new_transition):
            idx = i * num_state
            if i == 0:
                C[idx:size_q, idx:size_q] = Q
                C[idx:size_q, idx + size_q:idx + size_d +size_d] = D/dy
            else:
                C[idx:size_q + idx, idx:size_q + idx] = Q
                if idx != (C.shape[0] - size_q):
                    C[idx:size_q + idx, idx + size_q:idx + size_q + size_q] = D/dy
                
        sum_C_diagonal = -C.sum(axis=1)
        main_diagonal_values = []
        tmp = 0
        
        for i in range(0, num_state):    
            if C[i,i] < 0:
                tmp =  sum_C_diagonal[i] + C[i,i]
            else:
                tmp = sum_C_diagonal[i] - C[i,i]
          
            C[i,i] = tmp
            main_diagonal_values.append(tmp)
        
        for i in range(num_state, size_c):
            C[i,i] = main_diagonal_values[i % num_state]
        
        return C
    
    def _sparse(self, M):
        
        return csr_matrix(M)

    def _poisson(self, lambd, t, n):
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html
        
        return poisson.pmf(k=n, mu=lambd*t)

    def _compute_joint_distribution(self):
        
        Cinf = self.create_Qinf_transition_matrix(reward=self.y_max, 
                                                  dy=self.delta,
                                                  num_state=self.num_state, 
                                                  Q=self.Q,
                                                  D=self.D)
        lambd = max(-1*np.diag(Cinf))
        size_c = Cinf.shape[0]
        U = np.eye(size_c)
        U = U + 1/lambd*Cinf
        U_sparse = self._sparse(U)
        n = 0
        t = self.t_max
        c_error = 1 - self._poisson(lambd, t, n)
        pi_0_new = np.zeros(Cinf.shape[0])
        pi_temp = pi_0_new
        # update initial prob new state
        for i in range(len(self.pi_0)):
            pi_0_new[i] = self.pi_0[i]
        
        while c_error >= self.epsilon:
            n += 1
            PP_n_t = self._poisson(lambd, t, n)
            c_error = c_error - PP_n_t
            pi_temp = pi_temp * U_sparse
            pi_0_new = pi_0_new + pi_temp*PP_n_t
        
        cdf = sum(pi_0_new)
        return cdf, pi_0_new
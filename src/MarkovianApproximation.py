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
        """Q matrix generator

        Args:
            R (matrix/2d array) : matrix or 2d array

        Returns:
            R (matrix/2d array) : R with transformed to Q matrix rules
        """
        length = len(R)
        
        for i in range(0, length):
            R[i][i] = -1 * np.sum(R[i][:])
        
        return R
    
    def generate_D_matrix(self, r):
        """D matrix generator from reward vector

        Args:
            r (vector/array): reward vector of each state

        Returns:
            r (matrix/2d array): diagonal matrix from reward vector
        """
        return np.diag(r)
    
    
    def generate_Qinf_transition_matrix(self, reward, dy, num_state, Q, D):
        """Qinf matrix generator

        Args:
            reward (float/int): y_max
            dy (float/int): delta/step
            num_state (float/int): number of state
            Q (matrix/2d array): Q matrix 
            D (matrix/2d array): D matrix 

        Returns:
            Qinf (matrix/2d array): Qinf matrix transition for markovian approximation
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
        """Convert matrix to sparse matrix (vector/array)

        Args:
            M (matrix/2d array): any matrix

        Returns:
            M (array): array
        """
        return csr_matrix(M)

    def _poisson(self, lambd, t, n):
        """ Compute poission distribution
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html

        Args:
            lambd (float/integer): lambda
            t (float/integer): t_max
            n (integer): n, counter

        Returns:
            p : poisson probability
        """
        
        return poisson.pmf(k=n, mu=lambd*t)

    def _compute_joint_distribution(self):
        """ Compute joint distribution with markovian approximation approach

        Returns:
            cdf, pdf : return two array cdf and pdf
        """
        
        Cinf = self.generate_Qinf_transition_matrix(reward=self.y_max, 
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
        PP_0 = self._poisson(lambd, t, n)
        c_error = 1 - PP_0
        pi_0_new = np.zeros(Cinf.shape[0])
        pi_U_t = 0

        # update initial prob new state
        for i in range(len(self.pi_0)):
            pi_0_new[i] = self.pi_0[i]
        pi_temp = pi_0_new
        
        while c_error >= self.epsilon:
            n += 1
            PP_n_t = self._poisson(lambd, t, n)
            c_error = c_error - PP_n_t
            pi_temp = pi_temp * U_sparse
            pi_U_t = pi_U_t + pi_temp*PP_n_t
        
        cdf = sum(pi_U_t)
        
        return cdf, pi_U_t
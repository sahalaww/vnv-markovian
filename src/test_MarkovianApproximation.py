from MarkovianApproximation import *
import numpy as np

ymax = 3.5
t = 0.5
delta = 0.5
num_state = 4
S = np.array([1, 2, 3, 4])
R = np.array([[0, 1, 0, 2],
            [1, 0, 4, 5],
            [1, 2, 0, 1],
            [9, 2, 3, 0]])
pi = np.array([0.5, 0,4, 0.1, 0])
r = np.array([2,2,4,5])
epsilon = 10e-4

markovian = MarkovianApproximation(R=R, 
                                S=S, 
                                num_state=num_state, 
                                pi_0=pi,
                                r=r, 
                                t_max=t, 
                                y_max=ymax, 
                                delta=delta, 
                                epsilon=10e-4)

def test_generate_Q():
    Q = markovian.Q
    expected_Q =  np.array([[-3, 1, 0, 2],
                        [1, -10, 4, 5],
                        [1, 2, -4, 1],
                        [9, 2, 3, -14]])

    np.testing.assert_array_equal(Q, expected_Q)
    
def test_generate_D():
    D = markovian.generate_D_matrix(markovian.r)
    excepted_D = np.diag(r)
    
    np.testing.assert_array_equal(D, excepted_D)

def test_create_Qinf_transition_matrix():
    D = markovian.generate_D_matrix(markovian.r)
    Qinf = markovian.create_Qinf_transition_matrix(reward=markovian.y_max, 
                                                  dy=markovian.delta,
                                                  num_state=markovian.num_state, 
                                                  Q=markovian.Q,
                                                  D=D)
    
    expected_Qinf = np.matrix([[ -7.,   1.,   0.,   2.,   4.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  1., -14.,   4.,   5.,   0.,   4.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  1.,   2., -12.,   1.,   0.,   0.,   8.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  9.,   2.,   3., -24.,   0.,   0.,   0.,  10.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,  -7.,   1.,   0.,   2.,   4.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   1., -14.,   4.,   5.,   0.,   4.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   1.,   2., -12.,   1.,   0.,   0.,
           8.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   9.,   2.,   3., -24.,   0.,   0.,
           0.,  10.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,  -7.,   1.,
           0.,   2.,   4.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1., -14.,
           4.,   5.,   0.,   4.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   2.,
         -12.,   1.,   0.,   0.,   8.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   9.,   2.,
           3., -24.,   0.,   0.,   0.,  10.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,  -7.,   1.,   0.,   2.,   4.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   1., -14.,   4.,   5.,   0.,   4.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   1.,   2., -12.,   1.,   0.,   0.,   8.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   9.,   2.,   3., -24.,   0.,   0.,   0.,  10.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,  -7.,   1.,   0.,   2.,
           4.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   1., -14.,   4.,   5.,
           0.,   4.,   0.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   1.,   2., -12.,   1.,
           0.,   0.,   8.,   0.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   9.,   2.,   3., -24.,
           0.,   0.,   0.,  10.,   0.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
          -7.,   1.,   0.,   2.,   4.,   0.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           1., -14.,   4.,   5.,   0.,   4.,   0.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           1.,   2., -12.,   1.,   0.,   0.,   8.,   0.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           9.,   2.,   3., -24.,   0.,   0.,   0.,  10.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,  -7.,   1.,   0.,   2.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   1., -14.,   4.,   5.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   1.,   2., -12.,   1.],
        [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   9.,   2.,   3., -24.]])
    
    np.testing.assert_array_equal(Qinf, expected_Qinf)

def test_compute_joint_distribution():
    
    cdf, pdf = markovian._compute_joint_distribution()
    new_transition = int(markovian.y_max / markovian.delta)

    size_c = new_transition * markovian.num_state
    
    assert cdf.size == 1
    assert pdf.shape[0] == 28
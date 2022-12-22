from src.MarkovianApproximation import *
import time

def main():
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
    t0 = time.time()
    markovian = MarkovianApproximation(R=R, 
                                    S=S, 
                                    num_state=num_state, 
                                    pi_0=pi,
                                    r=r, 
                                    t_max=t, 
                                    y_max=ymax, 
                                    delta=delta, 
                                    epsilon=epsilon)
    
    cdf, pdf = markovian._compute_joint_distribution()
    
    print("Joint distribution :", cdf)
    print("Probability each transition :", pdf)
    print("Time : ", time.time() - t0)
if __name__ == '__main__':
    main()
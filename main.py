from src.MarkovianApproximation import *
from src.FileUtil import *
import time
import argparse

def main():
    args_parser = argparse.ArgumentParser(
        prog = 'VNV Markovian Approximation',
        description= 'Compute joint distribution with markovian approximation method',
    )
    
    args_parser.add_argument('-t', '--tra-file', default='samples/game.tra', help='Transition file')
    args_parser.add_argument('-r', '--rew-file', default='samples/game.rew', help='Reward file')
    args_parser.add_argument('-p', '--pi-file', default='samples/game.pi', help='Initial distribution file')
    args_parser.add_argument('-d', '--delta', default=0.5, help='Delta value')
    args_parser.add_argument('-tm', '--t-max', default=0.5, help='T-max value')
    args_parser.add_argument('-ym', '--y-max', default=3.5, help='Y-max value')
    args_parser.add_argument('-e', '--epsilon', default=10e-3, help='Epsilon')
    
    args = args_parser.parse_args()

    R_trans = FileUtil(args.tra_file)
    R = R_trans.parse_tra_file()
    num_state = R_trans.num_state
    
    S = np.arange(1, num_state + 1)
    pi = FileUtil(args.pi_file).parse_pi_file(num_state)
    r = FileUtil(args.rew_file).parse_reward_file(num_state)
    
    epsilon = float(args.epsilon)
    t_max = float(args.t_max)
    y_max = float(args.y_max)
    delta = float(args.delta)
    
    t0 = time.time()
    
    markovian = MarkovianApproximation(R=R, 
                                    S=S, 
                                    num_state=num_state, 
                                    pi_0=pi,
                                    r=r, 
                                    t_max=t_max, 
                                    y_max=y_max, 
                                    delta=delta, 
                                    epsilon=epsilon)
    
    cdf, pdf = markovian.compute_joint_distribution()
    
    print("Joint distribution :", cdf)
    print("Probability each transition :", pdf)
    print("Time : ", time.time() - t0)

if __name__ == '__main__':
    main()
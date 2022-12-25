# Joint distribution with Markovian Approximation

## Requirement

- Python >=3.5
- pip
- scipy
- numpy


## Install Dependencies

```bash
git clone https://github.com/sahalaww/vnv-markovian.git
cd vnv-markovian/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run with sample data

```bash
./run.sh
```

## Help

```bash
python3 main.py --help
usage: VNV Markovian Approximation [-h] [-t TRA_FILE] [-r REW_FILE] [-p PI_FILE] [-d DELTA] [-tm T_MAX] [-ym Y_MAX]
                                   [-e EPSILON] [-o OUTPUT_FILE]

Compute joint distribution with markovian approximation method

optional arguments:
  -h, --help            show this help message and exit
  -t TRA_FILE, --tra-file TRA_FILE
                        Transition file
  -r REW_FILE, --rew-file REW_FILE
                        Reward file
  -p PI_FILE, --pi-file PI_FILE
                        Initial distribution file
  -d DELTA, --delta DELTA
                        Delta value
  -tm T_MAX, --t-max T_MAX
                        T-max value
  -ym Y_MAX, --y-max Y_MAX
                        Y-max value
  -e EPSILON, --epsilon EPSILON
                        Epsilon
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file


```

## References

[1] L. Cloth and B. R. Haverkort, “Five Performability Algorithms: A Comparison,” in MAM 2006: Markov Anniversary Meeting, Jun. 2006, pp. 39–54. Accessed: Sept. 10, 2022. [Online]. Available: https://research.utwente.nl/en/publications/five-performability-algorithms-a-comparison 

[2] L. Cloth, “Model Checking Algorithms for Markov Reward Models,” phdthesis, University of Twente, Netherlands, 2006.


# Transmitter Experiments
A guide on how to run experiments to assess wireless transmitter placement efficacy. Instructions are intended for UNIX systems.

There are two independent variables in this experiment: amount of traffic, and transmitter placement. In addition, the seed can be changed to allow for multiple trials.

Number of agents (`NA`): `10`, `100`, `300`

Number of transmitters (`NT`): `0`, `100`, `200`

Transmitter placement (`P`): random, popular

Seeds (`S`): `1`, `2`, `3`

File structure is as follows (replace `NA`, `NT`, `S` with numbers, `P` with "random" or "popular"):
- Agents: `input/transmitter_experiments/agents/NA/S.csv`
- Chargers: `input/transmitter_experiments/chargers/NT/P/S.csv`
- Results: `output/transmitter_experiments/NA/NT/P/S/`


## 1. Generate Agents
TODO!
Use `input/prepare_agents.py` to create these files. It may need altered to allow an ideal `lane_offset` distribution.
The following parameters should be randomized:
- `lane_offset`
- `init_soc`
- `hvac`


## 2. Generate Transmitters
### Open-Lane Transmitters (`open`)
```
python navigation/charger_options.py 2 1 -m Town06 --power 50_000 --efficiency 0.95 -n NT --seed S > input/transmitter_experiments/chargers/NT/random/S.csv
```

### Optimal Transmitters (`popular`)
To determine the best places for wireless transmitters, data is collected from 3 experiments. The seeds for these experiments, denoted `S^1`, `S^2`, and `S^3`, are 4-digit integers where the first digit is the experiment number (`1`, `2`, `3`) and the other digits are the seed `S` for the experiment, 0-padded left. For example, if `S = 42`, then `S^1 = 1042`, `S^2 = 2042`, and `S^3 = 3042`.

Note that placement is determined using moderate traffic (`NA = 100`). High-traffic or low-traffic experiments could result in different placement.
```
python multitracking.py input/transmitter_experiments/agents/100/S.csv input/transmitter_experiments/chargers/NT/P/S/S^1/ -m Town06 --seed S^1 -t 1500 -d 0.05 -r
python multitracking.py input/transmitter_experiments/agents/100/S.csv input/transmitter_experiments/chargers/NT/P/S/S^2/ -m Town06 --seed S^2 -t 1500 -d 0.05 -r
python multitracking.py input/transmitter_experiments/agents/100/S.csv input/transmitter_experiments/chargers/NT/P/S/S^3/ -m Town06 --seed S^3 -t 1500 -d 0.05 -r
python navigation/optimal_chargers.py -m Town06 2 1 NT input/transmitter_experiments/chargers/NT/P/S/S^1/ input/transmitter_experiments/chargers/NT/P/S/S^2/ input/transmitter_experiments/chargers/NT/P/S/S^3/ --power 50_000 --efficiency 0.95 > input/transmitter_experiments/chargers/NT/popular/S.csv
```
Cleanup (optional):
```
rm -r input/transmitter_experiments/chargers/NT/P/S/
```

## 3. Run Simulations
Toggle rendering off with the `-r` option. Although this shouldn't affect results, it should decrease computation time.

### Baseline Experiments
These experiments demonstrate normal electric vehicle power expenditure without wireless charging.

For each AGENTFILE:
```
python multitracking.py AGENTFILE OUTFOLDER -t 1500 -d 0.05 -m Town06 --seed 0 [-r]
```

### Transmitter Placement Experiments
For each CHARGEFILE:

For each AGENTFILE:
```
python multitracking.py AGENTFILE OUTFOLDER -t 1500 -d 0.05 -m Town06 -w CHARGEFILE --seed 0 [-r]
```

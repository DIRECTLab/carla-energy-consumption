# Transmitter Experiments
A guide on how to run experiments to assess wireless transmitter placement efficacy. Instructions are intended for UNIX systems.

There are two independent variables in this experiment: amount of traffic, and transmitter placement. In addition, the seed can be changed for multiple trials.

Number of agents (`NA`): `10`, `100`, `300`

Number of transmitters (`NT`): `0`, `100`, `200`

Transmitter placement (`P`): open lane, intersection

Seeds (`S`): `0`

File structure is as follows (replace `NA`, `NT`, `S` with numbers, `P` with "open" or "intersection"):
- Agents: `input/transmitter_experiments/agents/NA_S.csv`
- Chargers: `input/transmitter_experiments/chargers/NT_open_S.csv` or `input/transmitter_experiments/chargers/NT_intersection.csv`
- Results: `output/transmitter_experiments/NA/NT_P/S/`


## 1. Generate agents
TODO!


## 2. Generate transmitters
### Open-lane transmitters
```
python navigation/charger_options.py 2 1 -m Town06 -i 0.001 --power 50_000 --efficiency 0.95 -n NT --seed S > input/transmitter_experiments/chargers/NT_open_S.csv
```

### Transmitters at intersections, 1 row
Get chargers at junctions:
```
python navigation/junction_chargers.py 2 1 input/transmitter_experiments/chargers/stops/ -m Town06 -i 0.001 --power 50_000 --efficiency 0.95 
```
Remove junctions without stop lights:
```
for JUNCTION in 1034 396 1050 413 798 1187 1203 436 565 822 712 728 1128 747 1146
do
    rm input/transmitter_experiments/chargers/stops/junction$JUNCTION.csv
done
```
Remove chargers on lanes without stop lights:
```
sed -i '2,3d' input/transmitter_experiments/chargers/stops/junction1162.csv
sed -i '6,7d' input/transmitter_experiments/chargers/stops/junction763.csv
```
Combine files
```
FILES=(input/transmitter_experiments/chargers/stops/*)
cp "${FILES[0]}" input/transmitter_experiments/chargers/stops/combined.csv
for F in "${FILES[@]:1}"
do
    tail -n +2 $F >> input/transmitter_experiments/chargers/stops/combined.csv
done
```

### Transmitters at intersections, multiple rows


## 3. Run simulations
Toggle rendering off with the `-r` option. Although this shouldn't affect results, it should decrease computation time.

### Baseline experiments
These experiments demonstrate normal electric vehicle power expenditure without wireless charging.

For each AGENTFILE:
```
python multitracking.py AGENTFILE OUTFOLDER -t 1500 -d 0.05 -m Town06 --seed 0
```

### Transmitter placement experiments
For each CHARGEFILE:

For each AGENTFILE:
```
python multitracking.py AGENTFILE OUTFOLDER -t 1500 -d 0.05 -m Town06 -w CHARGEFILE --seed 0
```

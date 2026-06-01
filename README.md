# Hockey Analytics — Stanley Cup Final Scoring 2026

A small case study that simulates Stanley Cup Final games between two teams
(currently **Carolina (CAR)** vs **Vegas (VGK)**) and reports how often each side
wins. It uses each player's real per-game stats and resamples them with a simple
Monte-Carlo approach to produce a distribution of outcomes.

## How it works

For each simulated game, every skater contributes the stats from one of their
last 5 games chosen at random. The app produces two independent predictions:

- **Based on Player Performance** — sums each team's actual goals (`G`).
- **Based on Goalie SV%** — derives goals from shots on goal and the opposing
  goalie's save percentage: `goals ≈ SOG × (1 − opponent_SV%)`.

Each model simulates `count` games and prints the number of EAST wins, WEST
wins, and ties.

## Requirements

- Python 3.10+
- Dependencies pinned in [`requirements.txt`](requirements.txt) (pandas, numpy)

## Project layout

```
main.py                  # entry point + simulation logic
data/
  CAR/                   # one CSV per Carolina skater
  VGK/                   # one CSV per Vegas skater
  goalies/               # goalie CSVs (frederik_andersen.csv, carter_hart.csv)
```

Skater CSVs must contain the columns `G, A, SOG, TOI`; goalie CSVs must contain
`SV%` (stored as a fraction, e.g. `.915`). To change the matchup, edit the
team/goalie paths near the top of `main.py`.

## Getting started

### 1. Create and activate a virtual environment

```shell
# Windows (Git Bash)
python -m venv venv
source venv/Scripts/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```shell
pip install -r requirements.txt
```

### 3. Run the application

```shell
python main.py
```

Example output:

```
Based on Player Performance
WEST wins: 3
EAST wins: 3
Tie Games 4
-------------------------------------------------------
Based on Goalie SV%
WEST wins: 6
EAST wins: 3
Tie Games 1
```

> Results vary between runs because games are sampled randomly. To change the
> number of simulated games, adjust the `count` passed to `predictor(...)` and
> `predict_score_based_on_goalies(...)` in the `__main__` block.

## References

- All player data was collected from [Hockey Reference](https://www.hockey-reference.com/)
- Prediction model based on Rob Vollman's concepts in [Stat Shot](https://www.amazon.com/Hockey-Abstract-Presents-Stat-Shot/dp/177041309X/)

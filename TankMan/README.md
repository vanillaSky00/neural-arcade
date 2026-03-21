# TankMan 🪖

A team-based tank battle game where 2–6 players compete to eliminate the opposing team or outscore them before time runs out. Destroy walls, collect resources, and coordinate with teammates to dominate the battlefield.

<img src="https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/49dc8cb825ddd8dea61936fb6d339c846fe68d6c/asset/image/TankMan.svg" alt="logo" width="100"/>

[![TankMan](https://img.shields.io/github/v/tag/Jesse-Jumbo/TankMan)](https://github.com/Jesse-Jumbo/TankMan/tree/0.7.0)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame-10.2.5a0-<COLOR>.svg)](https://pypi.org/project/mlgame/10.2.5a0/)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)

![game.gif](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/game.gif)



## Overview

Two teams (Green vs. Blue) battle on a grid-based arena. Each player controls a tank that can move, turn, and fire bullets. The map contains destructible walls, fuel stations, and ammo stations — all of which are contested resources. Supplies respawn on a timer, so getting there first matters.

> **Note:** Since v0.6.0 the game supports 2–6 player team matches. Since v0.7.0 the tank body and turret can be rotated independently.



## Requirements

- Python 3.9
- mlgame 10.2.5a0
- pytmx 3.31


## Getting Started

The `.` in each command refers to the game project path. If no arguments are provided after `.`, the defaults from `game_config.json` are used.

```bash
# Manual play (2 players, keyboard controlled)
python -m mlgame -f 120 -i ml/ml_play_manual.py -i ml/ml_play_manual.py . \
  --green_team_num 1 --blue_team_num 1 --is_manual 1 --frame_limit 1000

# AI play (2 AI agents)
python -m mlgame -f 120 -i ml/ml_play.py -i ml/ml_play.py . \
  --green_team_num 1 --blue_team_num 1 --frame_limit 1000
```

### Launch Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| `green_team_num` | 1–3 | Number of players on the Green team |
| `blue_team_num` | 1–3 | Number of players on the Blue team |
| `is_manual` | 0 / 1 | Enable keyboard control mode |
| `frame_limit` | 30–3000 | Total game frames (duration) |
| `sound` | `on` / `off` | Toggle sound effects |

Add `-1` after `mlgame` to run a single game only.


## Controls

### Keyboard

| Action | 1P | 2P |
|--------|----|----|
| Move / Turn | Arrow keys | W / A / S / D |
| Shoot | M | F |

**Camera:** I / K / J / L to pan, O / U to zoom in/out. Press **H** to hide HUD overlay. Press **P** to pause (mlgame ≥ 10.2).

### AI Control

Write a Python script in the `ml/` directory. See `ml_play.py` (AI template) and `ml_play_manual.py` (manual template) for reference.


## Game Rules

### Win Conditions

The match ends when time expires or one team is eliminated. The winning team is determined by:

1. **Elimination** — Destroy all enemy tanks.
2. **Score** — If both teams survive, the higher-scoring team wins.

### Scoring

| Event | Points |
|-------|--------|
| Enemy life lost | +20 |
| Wall hit | +1 |
| Wall destroyed | +5 |

### Loss Conditions

A team loses if all its members reach zero lives, or if it has a lower score when time expires.


## Game Objects

### Tank

| Attribute | Value |
|-----------|-------|
| Move speed | 8 px/frame |
| Turn increment | 45° |
| Lives | 3 |
| Max fuel | 100 |
| Max ammo | 10 |

### Walls

Walls have **4 hit points** and become progressively transparent as they take damage.

### Supply Stations

| Station | Replenishes | Amount | Cap | On Contact |
|---------|-------------|--------|-----|------------|
| Fuel Station | Fuel | +30 | 100 | Relocates randomly |
| Ammo Station | Bullets | +5 | 10 | Relocates randomly |

Supplies respawn over time — first come, first served.


## Map

The arena is **1000 × 600 pixels**, divided into a grid of **50 × 50 px** cells. Each cell can hold one object. For custom map creation, see [Mapping.md](Mapping.md).

<img src="https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/view_ex.png" alt="Game view" width="800"/>


## Credits

**Art:** [Green/Blue Tank & Bullet](https://linevoom.line.me/user/_dV001P0rSN_bh8zGE0q4jmdr4Fn5d-j73cLrjTc), [Hourglass](https://opengameart.org/content/animated-hourglass), [Object Icons](https://opengameart.org/content/simple-shooter-icons)
**Audio:** [BGM](https://opengameart.org/content/commando-team-action-loop-cut), [SFX](https://opengameart.org/content/random-low-quality-sfx)
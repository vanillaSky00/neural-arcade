# Swimming Squid 🦑

A competitive 2-player arcade game where AI-controlled squids compete to eat food, avoid garbage, and outscore their opponent — built for reinforcement learning experimentation.

![swimming-squid](https://img.shields.io/github/v/tag/PAIA-Playful-AI-Arena/swimming-squid)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame->10.3.2-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)

![demo](https://github.com/PAIA-Playful-AI-Arena/swimming-squid-battle/blob/develop/asset/demo.gif?raw=true)

---

## Overview

Each player controls a squid navigating an ocean filled with floating food and garbage. Eat the right items to score points, grow in size and level, and reach the target score before time runs out. In 2-player mode, squids can collide — higher-level squids steal points from lower-level ones.

The game is designed as a testbed for training reinforcement learning agents through the [MLGame](https://github.com/PAIA-Playful-AI-Arena/MLGame) framework.

---

## Getting Started

### Quick Launch

```bash
python main.py
```

### Configuration

```python
# main.py
game = SwimmingSquid(
    level=1,            # Built-in level (default: 1)
    level_file=None,    # Path to custom level JSON (overrides `level`)
    game_times=1,       # Best-of-N series: 1, 3, or 5
    sound="off"         # Sound toggle: "on" / "off"
)
```

### Manual Controls

| Player | Up | Down | Left | Right |
|--------|----|------|------|-------|
| 1P     | ↑  | ↓    | ←    | →     |
| 2P     | W  | S    | A    | D     |

---

## Game Mechanics

### Leveling System

Squids start at Level 1 and level up or down based on their score. Higher levels increase the squid's size but reduce its speed:

| Level | Width (px) | Height (px) | Speed (px/frame) |
|-------|-----------|------------|-------------------|
| 1     | 30        | 45         | 25                |
| 2     | 36        | 54         | 21                |
| 3     | 42        | 63         | 18                |
| 4     | 48        | 72         | 16                |
| 5     | 54        | 81         | 12                |
| 6     | 60        | 90         | 9                 |

### Scoring

**Food & Garbage** — Items float across the ocean. Food grants points; garbage deducts them. The number of items increases over time.

| Item       | Size (px) | Score |
|------------|----------|-------|
| FOOD_1     | 30       | +1    |
| FOOD_2     | 40       | +2    |
| FOOD_3     | 50       | +4    |
| GARBAGE_1  | 30       | −1    |
| GARBAGE_2  | 40       | −4    |
| GARBAGE_3  | 50       | −10   |

**Collision** (enabled when map width and height both exceed 500 px):

- Higher-level squid: **+10 pts** / Lower-level squid: **−10 pts**
- Same level: both squids **−5 pts**

### Win & Loss Conditions

**Win:** Reach the target `score` before time expires. If both players pass, the higher score wins. Ties trigger overtime (+50 to target score, +600 frames), up to 3 extensions.

**Loss:** Fail to reach the target `score`. If neither player passes, the higher score wins. Ties trigger overtime (target unchanged, +300 frames), up to 3 extensions.

---

## AI Development

### Running an AI Agent

```bash
python -m mlgame -i ./ml/ml_play_template.py ./ --level 3
python -m mlgame -i ./ml/ml_play_template.py ./ --level_file /path/to/level.json
```

### Agent Template

```python
import random


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        print("Initial ml script")

    def update(self, scene_info: dict, *args, **kwargs):
        """Called every frame. Return an action string."""
        actions = ["UP", "DOWN", "LEFT", "RIGHT", "NONE"]
        return random.sample(actions, 1)

    def reset(self):
        """Called between rounds."""
        print("reset ml script")
```

### Available Actions

Return **one** of the following strings from `update()`:

| Action  | Effect          |
|---------|-----------------|
| `UP`    | Move up         |
| `DOWN`  | Move down       |
| `LEFT`  | Move left       |
| `RIGHT` | Move right      |
| `NONE`  | Stay in place   |

---

## Observation Space

The `scene_info` dictionary passed to `update()` contains the full game state:

```jsonc
{
  "frame": 15,                // Current frame number
  "collision_mode": "True",   // Whether collision is active
  "score": 8,                 // Current score
  "score_to_pass": 10,        // Target score to win

  // Self
  "self_x": 100,              // X position (center)
  "self_y": 300,              // Y position (center)
  "self_w": 30,               // Width in px
  "self_h": 45,               // Height in px
  "self_vel": 25,             // Speed (px/frame)
  "self_lv": 1,               // Level (1–6)

  // Opponent
  "opponent_x": 500,          // Opponent X (center)
  "opponent_y": 400,          // Opponent Y (center)
  "opponent_lv": 2,           // Opponent level (1–6)

  // Game status: "GAME_ALIVE" | "GAME_PASS" | "GAME_OVER"
  "status": "GAME_ALIVE",

  // Items on the field
  "foods": [
    { "x": 40, "y": 134, "w": 30, "h": 30, "type": "FOOD_1", "score": 1 },
    { "x": 422, "y": 192, "w": 40, "h": 40, "type": "FOOD_2", "score": 2 },
    { "x": 264, "y": 476, "w": 50, "h": 50, "type": "FOOD_3", "score": 4 },
    { "x": 100, "y": 496, "w": 30, "h": 30, "type": "GARBAGE_1", "score": -1 },
    { "x": 633, "y": 432, "w": 40, "h": 40, "type": "GARBAGE_2", "score": -4 },
    { "x": 54, "y": 194, "w": 50, "h": 50, "type": "GARBAGE_3", "score": -10 }
  ]
}
```

All coordinate values represent the **center point** of the object in pixels.

---

## Game Results

At the end of a match, results are output to the console (and returned to the PAIA platform if running on the server):

```json
{
  "frame_used": 100,
  "state": "FAIL",
  "attachment": [
    { "squid": "1P", "score": 0, "rank": 2, "wins": "1 / 3" },
    { "squid": "2P", "score": 10, "rank": 1, "wins": "2 / 3" }
  ]
}
```

| Field        | Description                             |
|--------------|-----------------------------------------|
| `frame_used` | Total frames elapsed                    |
| `state`      | `"FAIL"` or `"FINISH"`                 |
| `attachment`  | Per-player results (score, rank, wins) |

---

## Credits

**Sound Effects:** [soundeffect-lab.info](https://soundeffect-lab.info/sound/anime/)
**Background Music:** [MotionElements](https://www.motionelements.com/zh-hant/stock-music-28190007-bossa-nova-short-loop)
**Illustrations:** [illustcenter.com](https://illustcenter.com/) — squid, spoon, fries, can, fish, shrimp assets

---

## License

See [MLGame](https://github.com/PAIA-Playful-AI-Arena/MLGame) for framework licensing details.
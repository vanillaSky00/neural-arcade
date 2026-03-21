# Arkanoid 🧱

A classic brick breaker game — aim your serve, bounce the ball off your paddle, and destroy every brick on screen. Multiple difficulty levels and custom map support keep the challenge fresh.

<img src="https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/Paia-Desktop/master/media/arkanoid.svg" alt="logo" width="100"/>

![arkanoid](https://img.shields.io/github/v/tag/PAIA-Playful-AI-Arena/arkanoid)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame->9.5.3-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)

<img src="https://camo.githubusercontent.com/a2a0ed0f4e012779cdf3d7fdeda6371c1a4cb3483e91c56442db5d3b56440798/68747470733a2f2f692e696d6775722e636f6d2f627271615738352e676966" height="500"/>


## Getting Started

### Quick Launch

```bash
python main.py
```

### Configuration

```python
# main.py
game = Arkanoid(difficulty="EASY", level=3)
```

| Parameter | Options | Description |
|-----------|---------|-------------|
| `difficulty` | `EASY`, `NORMAL` | EASY = standard play; NORMAL = adds spin mechanic |
| `level` | integer | Level map to load (maps stored in `./asset/level_data/`) |

### Controls

| Action | Key |
|--------|-----|
| Move paddle left | ← |
| Move paddle right | → |
| Serve left | A |
| Serve right | D |


## Game Rules

### Objective

Destroy all bricks on the screen by bouncing the ball off your paddle.

**Win:** All bricks destroyed. **Loss:** Ball falls past the paddle.

### Game Objects

| Object | Size (W×H) | Speed (px/frame) | Details |
|--------|-----------|-------------------|---------|
| Paddle | 40 × 5 | ±5 horizontal | Starts at (75, 400) |
| Ball | 5 × 5 | ±7 in both axes | Launches from paddle position |
| Brick | 25 × 10 | — | Destroyed in 1 hit |
| Hard Brick | 25 × 10 | — | Requires 2 hits (becomes normal brick after 1st hit) |

The ball auto-serves in a random direction if not launched within 150 frames. All coordinates represent the **top-left corner** of each object. The screen size is **200 × 500 pixels**.

### Spin Mechanic (NORMAL difficulty)

The ball's horizontal speed changes based on paddle movement at the moment of contact:

| Paddle State | Result | Ball X Speed |
|-------------|--------|-------------|
| Moving same direction as ball | Speed boost (can 1-hit hard bricks) | ±10 |
| Stationary | Normal speed | ±7 |
| Moving opposite direction | Ball reverses X direction | ±7 |


## AI Development

### Running an AI Agent

```bash
python -m mlgame -i ./ml/ml_play_template.py . --difficulty NORMAL --level 5
```

### Agent Template

```python
class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        print(ai_name)

    def update(self, scene_info, *args, **kwargs):
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"
        if not scene_info["ball_served"]:
            return "SERVE_TO_LEFT"
        return "MOVE_LEFT"

    def reset(self):
        self.ball_served = False
```

### Available Actions

Return **one** of the following strings from `update()`:

| Action | Effect |
|--------|--------|
| `MOVE_LEFT` | Move paddle left |
| `MOVE_RIGHT` | Move paddle right |
| `SERVE_TO_LEFT` | Serve ball to the left |
| `SERVE_TO_RIGHT` | Serve ball to the right |
| `NONE` | No movement |


## Observation Space

The `scene_info` dictionary passed to `update()` each frame:

```jsonc
{
  "frame": 0,                    // Current frame number
  "status": "GAME_ALIVE",       // "GAME_ALIVE" | "GAME_PASS" | "GAME_OVER"
  "ball": [93, 395],            // Ball position (x, y)
  "ball_served": false,          // Whether the ball has been launched
  "platform": [75, 400],        // Paddle position (x, y)
  "bricks": [[50, 60], ...],    // Remaining normal bricks (includes damaged hard bricks)
  "hard_bricks": [[35, 50], ...]  // Remaining hard bricks (full health)
}
```


## Game Results

```json
{
  "frame_used": 5827,
  "state": "FINISH",
  "attachment": [
    {
      "player": "1P",
      "brick_remain": 2,
      "count_of_catching_ball": 51
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `frame_used` | Total frames elapsed |
| `state` | `"FINISH"` (all bricks cleared) or `"FAIL"` (ball dropped) |
| `brick_remain` | Normal bricks remaining + 2 × hard bricks remaining |
| `count_of_catching_ball` | Total successful catches |


## Custom Maps

Place custom level files in [`asset/level_data/`](asset/level_data/) with the naming format `<level_id>.dat`.

Each line contains three numbers: `x y type`. The first line defines a coordinate offset (type is always `-1`). Subsequent lines define bricks relative to that offset, where type `0` = normal brick and `1` = hard brick.

```
25 50 -1
10 0 0
35 10 0
60 20 1
```

This example creates three bricks: two normal and one hard, offset by (25, 50).

A visual [map editor](./asset/tool/arkanoid_map_editor.exe) is also available.


## Ball Physics

When the ball would clip through a surface on the next frame, it is moved to the exact intersection point of its trajectory and the collision surface before bouncing.

![Ball physics](./asset/github/打磚塊-球的物理.png)
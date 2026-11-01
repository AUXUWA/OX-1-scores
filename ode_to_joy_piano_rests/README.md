# ★ 休止步的写法：`step 0 1`

> 单轨曲谱（协议/示例） · `score.txt`（`step key [dur]`）+ `score.bin`（下发帧流）

## 说明

- 本曲是**单轨谱**（没有 4 轨 JSON）⇒ 不生成 `score.hex` / `preview.wav`；
  试听请直接下发 `score.bin`，或 `py tools/score_push.py --file scores/ode_to_joy_piano_rests/score.txt`
- 曲名与音色写在 `score.txt` 的**头注释**里（`tools/make_scores_index.py` 从这里派生 `scores/index.json`）

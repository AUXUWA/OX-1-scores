# C–Am–F–G 4 轨演示曲

> 4 轨 × 32 步 · `step_ms=120` · `loop=1` · 事件 32 条

## 文件

| 文件 | 用途 |
| :--- | :--- |
| `score.json` | 渲染器输入（4 轨完整信息）|
| `score.txt` | 下发用合并谱（`step key [dur]`，蓝牙/SerialTest/App）|
| `score.hex` | **可嵌入 FPGA**：32 行 × 4 字节，`{2'b0,on,pitch[4:0]}`（= SEQD 载荷同构；**和弦取最低音**）|
| `score.bin` | 下发帧流（HEAD+DATA，`tools/score_to_bin.py` 生成）|
| `preview.wav` | **与引擎一致**的离线渲染（`fm_engine_model` 逐比特 + `fx_model` 逐位 → 48 828 Hz/16 bit 立体声）|
| `meta.json` | 机器可读元数据 |

## 音色（板载 8 套，见 `mega60k/rtl/top/patch_bank.v`）

| 轨 | 角色 | patch | 音色 |
| :--: | :--- | :--: | :--- |
| 0 | 和弦伴奏（位图多键） | 1 | 电钢琴 |
| 1 | 根音铺底 | 6 | 弦乐群 |
| 2 | 低音 16 分律动 | 4 | 管风琴 |
| 3 | 主旋律 | 5 | Supersaw |

## 复现

```bash
py tools/render_multitrack.py scores/demo_camfg_4x32/score.json --out scores/demo_camfg_4x32/preview.wav
py tools/score_to_bin.py --file scores/demo_camfg_4x32/score.txt --out scores/demo_camfg_4x32/score.bin --loop 1
```

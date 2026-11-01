# 夜驰 Synthwave（电子 synthwave · 4 轨 × 32 步）

> 情绪：**夜路、霓虹、仪表盘** · 步长 **150 ms** · 循环 **loop=1** · 一轮 4.80 s（渲染含 2.00 s 尾巴）

## 音色表（板级 patch_bank.v 的 8 套之内）

| 轨 | 名字 | 音色 | patch | 声部/part | 为什么这么配 |
| :-: | :--- | :--- | :-: | :-: | :--- |
| 0 | Supersaw | Supersaw | 5 | 124/part0 | algo5 七振荡器 = synthwave 的门面 |
| 1 | 拨弦 | 拨弦 | 2 | 125/part1 | 拨弦短促 = synth bass pluck |
| 2 | 电钢琴 | 电钢琴 | 1 | 126/part2 | algo1 的亮色当 arp 上行 |
| 3 | 金属打击·树形 | 金属打击·树形 | 3 | 127/part3 | algo3 压 synthwave 的鼓点骨架 |

## 文件

| 文件 | 说明 |
| :--- | :--- |
| `score.json` | 渲染器输入（ox1-multitrack-score v1，4 轨 × 32 步）|
| `score.txt` | 下发用合并谱（`step key [dur]`，与所有 .txt 同语法）|
| `score.bin` | 下发帧流（`py tools/score_to_bin.py` 生成，HEAD+DATA+MODE+START，SEQ 递增）—— 给 SerialTest「发送文件」/ App 直接用 |
| `score.hex` | **可嵌入 FPGA 的 ROM 初值**（`$readmemh` 格式）：32 行 × 4 字节 = 4 轨，每字节 `{2'b0, on, pitch[4:0]}`，与 `docs/10-spec/SCORE_LINK_SPEC.md` §13.4 的 **SEQD 载荷字节完全同构**。下一轮可装成 32×32bit ROM（先例：`mega60k/rtl/io/video/sim/seq_tpl_rom.hex`）。**本轮不落 RTL**。 |
| `preview.wav` | 离线试听（48 828 Hz / 16 bit / 立体声）|
| `meta.json` | 机器可读指标 |

## 引擎一致性（这不是声明，是链路）

`preview.wav` 由 `py tools/render_multitrack.py` 生成：
曲谱 → 引擎寄存器写序列 → `fm_engine_model`（与 RTL **逐比特**对拍）→ `fx_model`（与 effects.v 逐位对拍）→ 48 828 Hz / 16 bit 立体声。
三个对拍门：`tools/cmp_fm_engine.py`（整机）、`tools/cmp_opl3.py`（算子，与 Nuked-OPL3 逐比特）、`tools/audit_presets.py`（音色参数与 patch_bank.v 逐比特）。

## 响度与时长（渲染器实测，未归一化）

| 项 | 值 |
| :--- | :--- |
| 时长（含尾巴） | 6.800 s |
| 峰值 | 7586.0（-12.71 dBFS）|
| RMS | -32.32 dBFS |
| 削波样本 | 0 |
| WAV | 1328140 B · md5 6be5271c33347d8dcee3f89f1e1a6659 |


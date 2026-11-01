# 多瑙河圆舞曲风（圆舞曲 · 4 轨 × 32 步）

> 情绪：**河畔、旋转、优雅** · 步长 **190 ms** · 循环 **loop=1** · 一轮 6.08 s（渲染含 2.00 s 尾巴）

## 音色表（板级 patch_bank.v 的 8 套之内）

| 轨 | 名字 | 音色 | patch | 声部/part | 为什么这么配 |
| :-: | :--- | :--- | :-: | :-: | :--- |
| 0 | 弦乐群 | 弦乐群 | 6 | 124/part0 | FB=3 的歌唱性适合圆舞曲连音 |
| 1 | 管风琴 | 管风琴 | 4 | 125/part1 | algo4 低音长门 + 和弦补位 |
| 2 | 拨弦 | 拨弦 | 2 | 126/part2 | 拨弦的短音在拍尾回声 |
| 3 | 钟 | 钟 | 7 | 127/part3 | 钟高音跟着旋转走 |

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
| 时长（含尾巴） | 8.080 s |
| 峰值 | 12287.0（-8.52 dBFS）|
| RMS | -23.26 dBFS |
| 削波样本 | 0 |
| WAV | 1578124 B · md5 18a95d5aa11adecc1f903d5578e30959 |


# 福音之光（福音 Soul · 4 轨 × 32 步）

> 情绪：**教堂、合唱、温暖** · 步长 **165 ms**（1 步 = 1 个十六分音符、16 步 = 1 小节 ⇒ BPM 90.9）
> · 循环 **loop=1** · 一轮 5.28 s（渲染含 2.00 s 尾巴）· 和声：C 大调（C–Am–F–G，每 8 步 = 半小节一换）

## 音色表（板级 patch_bank.v 的 8 套之内）

| 轨 | 名字 | 音色 | patch | 声部/part | 为什么这么配 |
| :-: | :--- | :--- | :-: | :--- | :--- |
| 0 | 管风琴 | 管风琴 | 4 | 124/part0 | Hammond 和弦（正拍 + 反拍加花） |
| 1 | 弦乐群 | 弦乐群 | 6 | 125/part1 | 合唱团（长音，只换不切） |
| 2 | 拨弦 | 拨弦 | 2 | 126/part2 | 行走低音（八分音符） |
| 3 | 金属打击 | 金属打击·树形 | 3 | 127/part3 | 手鼓 + 底鼓 |

## 文件

| 文件 | 说明 |
| :--- | :--- |
| `score.json` | 渲染器输入（ox1-multitrack-score v1，4 轨 × 32 步）|
| `score.txt` | 下发用合并谱（`step key [dur]`）—— 给 App / SerialTest / `score_push.py` |
| `score.bin` | 下发帧流（`py tools/score_to_bin.py` 生成，HEAD+DATA+MODE+START，SEQ 递增；HEAD 里带本曲的 step_ms）|
| `score.hex` | **可嵌入 FPGA 的 ROM 初值**（`$readmemh`）：32 行 × 4 字节 = 4 轨，每字节 `{2'b0, on, pitch[4:0]}` —— 与 `docs/10-spec/SCORE_LINK_SPEC.md` §13.4 的 SEQD 载荷字节同构 |
| `preview.wav` | 离线试听（48 828 Hz / 16 bit / 立体声）|
| `meta.json` | 机器可读指标 |

## 引擎一致性（这不是声明，是链路）

`preview.wav` 由 `py tools/render_multitrack.py` 生成：
曲谱 → 引擎寄存器写序列 → `fm_engine_model`（与 RTL **逐比特**对拍）→ `fx_model`（与 effects.v 逐位对拍）→ 48 828 Hz / 16 bit 立体声。
三个对拍门：`tools/cmp_fm_engine.py`（整机）、`tools/cmp_opl3.py`（算子）、`tools/audit_presets.py`（音色参数与 patch_bank.v 逐比特）。

## 响度与时长（渲染器实测，未归一化）

| 项 | 值 |
| :--- | :--- |
| 时长（含尾巴） | 7.28 s |
| 峰值 | 16635.5（-5.89 dBFS）|
| RMS | -21.44 dBFS |
| 削波样本 | 0 |
| WAV | 1421964 B · md5 f5a9460cad6988d54b27cbb87c6476d4 |

## 复现

```bash
py tools/make_new_songs.py --only gospel_soul_4x32      # 重新生成谱面与全部派生产物
py tools/check_score_files.py              # 曲谱硬约束
py scores/verify_score_hex.py              # hex ↔ bin ↔ json 三方同源
```

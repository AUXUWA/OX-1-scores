# 芯片街机（电子 8-bit · 4 轨 × 32 步）

> 情绪：**街机、怀旧、蹦跳** · 步长 **100 ms**（1 步 = 1 个十六分音符、16 步 = 1 小节 ⇒ BPM 150.0）
> · 循环 **loop=1** · 一轮 3.20 s（渲染含 2.00 s 尾巴）· 和声：A 小调（Am–F–C–G，每 8 步 = 半小节一换）

## 音色表（板级 patch_bank.v 的 8 套之内）

| 轨 | 名字 | 音色 | patch | 声部/part | 为什么这么配 |
| :-: | :--- | :--- | :-: | :--- | :--- |
| 0 | Supersaw | Supersaw | 5 | 124/part0 | 主奏（方波味钩子，八分音符） |
| 1 | 羽管键琴 | 羽管键琴 | 0 | 125/part1 | 琶音（十六分音符滚奏） |
| 2 | 拨弦 | 拨弦 | 2 | 126/part2 | 脉冲贝斯（根音-五音，八分音符） |
| 3 | 金属打击 | 金属打击·树形 | 3 | 127/part3 | 噪声鼓组（底鼓/军鼓/hi-hat） |

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
| 时长（含尾巴） | 5.20 s |
| 峰值 | 8884.5（-11.34 dBFS）|
| RMS | -28.86 dBFS |
| 削波样本 | 0 |
| WAV | 1015692 B · md5 172e8219a260f0e49ee798425b973f22 |

## 复现

```bash
py tools/make_new_songs.py --only chiptune_arcade_4x32      # 重新生成谱面与全部派生产物
py tools/check_score_files.py              # 曲谱硬约束
py scores/verify_score_hex.py              # hex ↔ bin ↔ json 三方同源
```

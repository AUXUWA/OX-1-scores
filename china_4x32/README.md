# 中国风 China（五声音阶，4 轨 × 32 步）

> 4 轨 × 32 步 · `step_ms=150` · `loop=1` · 事件 19 条

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
| 0 | 主旋律（五声，长音 + 装饰） | 0 | 羽管键琴 |
| 1 | 古筝式分解（宫-商-角-徵） | 6 | 弦乐群 |
| 2 | 低音（宫-徵-羽-商） | 4 | 管风琴 |
| 3 | 点缀（一记一记，不成拍） | 7 | 钟 |

## 复现

```bash
py tools/render_multitrack.py scores/china_4x32/score.json --out scores/china_4x32/preview.wav
py tools/score_to_bin.py --file scores/china_4x32/score.txt --out scores/china_4x32/score.bin --loop 1
```

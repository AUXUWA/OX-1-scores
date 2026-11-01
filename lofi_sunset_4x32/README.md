# 落日 Lo-fi（4 轨 × 32 步）

> 4 轨 × 32 步 · `step_ms=220` · `loop=1` · 事件 13 条

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
| 0 | 九和弦铺底（每 8 步一换） | 1 | 电钢琴 |
| 1 | 松散贝斯（半拍滞后） | 2 | 拨弦 |
| 2 | 长音垫（16 步全音符） | 6 | 弦乐群 |
| 3 | 风铃（偶发高音） | 7 | 钟 |

## 复现

```bash
py tools/render_multitrack.py scores/lofi_sunset_4x32/score.json --out scores/lofi_sunset_4x32/preview.wav
py tools/score_to_bin.py --file scores/lofi_sunset_4x32/score.txt --out scores/lofi_sunset_4x32/score.bin --loop 1
```

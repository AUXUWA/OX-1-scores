# patches/ —— 音色库（板级导出 + 本地新音色）

> **t43（2026-11-01）**：用户要求"更多的音色"。板载只有 8 套（`mega60k/rtl/top/patch_bank.v`，
> preset 选择 3 bit）⇒ 本目录分两层：
> **`board_*.json` = 板级 8 套的只读导出**（真源是 `tools/patch_designer/presets.json` 的
> board_id 0..7，**一个字节不许改**）；
> **`local_new/*.json` = 本地新音色**（16 套，**不带 board_id**），渲染器可离线试听，
> **上板需下一轮落 RTL**（见 `../patch_proposals.md` §四）。

## 一、板级导出（只读）

| 文件 | patch | 音色 | 算法 |
| :-- | :-: | :--- | :-: |
| `board_0.json` | 0 | 羽管键琴 | 0 |
| `board_1.json` | 1 | 电钢琴 | 1 |
| `board_2.json` | 2 | 拨弦 | 2 |
| `board_3.json` | 3 | 金属打击·树形 | 3 |
| `board_4.json` | 4 | 管风琴 | 4 |
| `board_5.json` | 5 | Supersaw | 5 |
| `board_6.json` | 6 | 弦乐群 | 6 |
| `board_7.json` | 7 | 钟 | 7 |

每个文件头写明：`"// 与 mega60k/rtl/top/patch_bank.v 逐比特一致，勿改"`。
守门：`py tools/audit_presets.py --check-bank`（本轮跑过 **PASS**，8 套逐条一致）。

## 二、本地新音色（16 套，`local_new/`）

| # | 名字 | 算法 | 听感 | 详见 |
| --: | :--- | :-: | :--- | :--- |
| 1 | 羽管键琴·暗拨 | 0 | 暗、干、拨弦感 | `../patch_proposals.md` §二.1 |
| 2 | 玻璃领奏 | 0 | 亮、玻璃感、带颤音 | §二.2 |
| 3 | 电钢·暖芯 | 1 | 暖、圆润、温和衰减 | §二.3 |
| 4 | Dinger 钟琴 | 1 | 脆、玻璃钟 | §二.4 |
| 5 | 指贝斯·圆 | 2 | 圆、低、指弹贝斯 | §二.5 |
| 6 | 马林巴 | 2 | 木质、清亮、打击 | §二.6 |
| 7 | 金属·雨滴 | 3 | 金属、细密 | §二.7 |
| 8 | 铜锣·闷 | 3 | 闷、低鸣、锣 | §二.8 |
| 9 | 管风琴·主音栓 | 4 | 明亮、齐奏感 | §二.9 |
| 10 | 和声人声 | 4 | 暖、人声感、合唱垫 | §二.10 |
| 11 | Night Pad 闷锯 | 5 | 闷、宽、磁带锯齿 | §二.11 |
| 12 | 先锋领奏·尖 | 5 | 尖、亮、穿透 | §二.12 |
| 13 | 弦乐·緊 | 6 | 紧、亮、快速弓弦 | §二.13 |
| 14 | 合唱人声·暗 | 6 | 暗、宽、人声合唱 | §二.14 |
| 15 | 风铃·散 | 7 | 散、金属、风铃 | §二.15 |
| 16 | 水下钟 | 7 | 闷、深、水下钟声 | §二.16 |

★ **命名纪律**：本地音色 JSON **禁止写 `board_id` 字段**（audit_presets.py 的 BANK CHECK
只认 board_id 0..7，多出来会 FAIL）⇒ 用 `local_name` / `local_id`。
★ **引用方式**：曲谱轨写 `"patch_local": "<local_name>"`（不带 .json 后缀）；
`tools/render_multitrack.py` 已支持（t43 起会先查 `patch_local` 再查 `patch` board_id）。
★ **上板代价**：见 `../patch_proposals.md` §四 —— preset 位宽 3→4 bit + patch_bank 加 8 套 +
  文档同步，本轮**不做**。

## 三、对照试听（同一段音乐 × 不同音色）

> 音乐 = `demo_camfg_4x32` 的 4 轨（**逐字节相同**，只换音色）—— 这是"差异全部来自音色"的证据。
> 三个 WAV 的 md5 互不相同：`a7d521af… / 1af4cf86… / 7afd659c…`。

| 文件 | 音色组合 | 听感（1 行，主观） | 指标 |
| :--- | :--- | :--- | :--- |
| `preview_bright.wav` | 玻璃领奏 / 弦乐·緊 / 马林巴 / 金属·雨滴 | 偏亮偏脆，高频颗粒强，打击位很跳 | peak −13.8 dBFS |
| `preview_mellow.wav` | 电钢·暖芯 / 和声人声 / 指贝斯·圆 / 铜锣·闷 | 闷一档，低频圆，人声垫"嗡"，最 lo-fi | peak −14.5 dBFS |
| `preview_metal.wav` | 先锋领奏·尖 / 合唱人声·暗 / 马林巴 / Dinger 钟琴 | 领奏尖利穿出，钟琴残响硬，最金属 | peak −10.4 dBFS |

（听感是 t43 作者的主观描述，未经他人复核；指标是渲染器实测。）

## 四、门禁（本轮真实输出）

```
py tools/audit_presets.py --check-bank   ⇒ *** BANK CHECK PASS ***（8 套逐条一致）
py tools/render_multitrack.py --selftest ⇒ *** SELFTEST PASS ***（S1..S6 全 OK）
py scores/verify_score_hex.py            ⇒ *** PASS ***（14/14 首 hex==json==bin）
```

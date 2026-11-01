# 新音色提案（16 套 · 每个算法 2 套）—— 只出方案，不改 RTL

> **t43 · 2026-11-01** · 用户要求"更多音色先放本地，上板还有力度那是下一轮"。
> ★ 本文是**提案**：所有参数只存在于 `scores/patches/local_new/*.json`（渲染器可离线试听），
> **没有任何一套进了 `mega60k/rtl/top/patch_bank.v`** —— 上板需要走"落地代价"那一节。
> 参数格式 = `tools/patch_designer/presets.json` 同款（`algo/fb/ops[4]{tl,ar,dr,sl,rr,mult,ksl,ksr,wf,egt,vib,trem}`）。
> 字段含义：tl 0..63（0=最响，0.75dB/步）· mult 0..15（频率比 = mult/2）· wf 0..7（8 种波形）· ar/dr/sl/rr 0..15。

## 一、总表

| # | 名字 | 算法 | 听感 | 文件 |
| --: | :--- | :--: | :--- | :--- |
| 1 | 羽管键琴·暗拨 | 0 | 暗、干、拨弦感 | `local_new/羽管键琴·暗拨.json` |
| 2 | 玻璃领奏 | 0 | 亮、玻璃感、带颤音 | `local_new/玻璃领奏.json` |
| 3 | 电钢·暖芯 | 1 | 暖、圆润、温和衰减 | `local_new/电钢·暖芯.json` |
| 4 | Dinger 钟琴 | 1 | 脆、玻璃钟、不和谐泛音 | `local_new/Dinger 钟琴.json` |
| 5 | 指贝斯·圆 | 2 | 圆、低、指弹贝斯 | `local_new/指贝斯·圆.json` |
| 6 | 马林巴 | 2 | 木质、清亮、打击 | `local_new/马林巴.json` |
| 7 | 金属·雨滴 | 3 | 金属、细密、雨滴打铁皮 | `local_new/金属·雨滴.json` |
| 8 | 铜锣·闷 | 3 | 闷、低鸣、锣 | `local_new/铜锣·闷.json` |
| 9 | 管风琴·主音栓 | 4 | 明亮、齐奏感、主音栓 | `local_new/管风琴·主音栓.json` |
| 10 | 和声人声 | 4 | 暖、人声感、合唱垫 | `local_new/和声人声.json` |
| 11 | Night Pad 闷锯 | 5 | 闷、宽、磁带锯齿 | `local_new/Night Pad 闷锯.json` |
| 12 | 先锋领奏·尖 | 5 | 尖、亮、穿透 | `local_new/先锋领奏·尖.json` |
| 13 | 弦乐·緊 | 6 | 紧、亮、快速弓弦 | `local_new/弦乐·緊.json` |
| 14 | 合唱人声·暗 | 6 | 暗、宽、人声合唱 | `local_new/合唱人声·暗.json` |
| 15 | 风铃·散 | 7 | 散、金属、风铃 | `local_new/风铃·散.json` |
| 16 | 水下钟 | 7 | 闷、深、水下钟声 | `local_new/水下钟.json` |

## 二、每套的参数与依据

### 1. 羽管键琴·暗拨（algo0 串联，FB=0）
```json
ops = [
  {tl:28, ar:13, dr:9, sl:5, rr:8, mult:2},
  {tl:30, ar:13, dr:9, sl:5, rr:8, mult:1},
  {tl:24, ar:12, dr:8, sl:6, rr:8, mult:1},
  {tl:14, ar:13, dr:10, sl:4, rr:8, mult:1}
]
```
依据：板级 board0（羽管键琴）的载波 tl 抬高 6 步（≈ −4.5dB）+ AR 13（慢一档）
⇒ 保留拨弦包络但压掉"叮"的亮边。**试听**：`scores/patches/preview_*.wav`（对照包）。

### 2. 玻璃领奏（algo0，FB=0）
```json
ops = [ {tl:30,…,mult:1}, {tl:28,…,mult:1},
        {tl:20,…,mult:2,wf:4}, {tl:8,…,mult:1,wf:4,vib:1} ]
```
依据：wf=4（OPL3 半正弦）做调制 + vib=1 ⇒ 玻璃质感 + 自带颤音；载波 tl=8 保持穿透。

### 3. 电钢·暖芯（algo1：1←(2←3)+4）
```json
ops = [ {tl:26,…}, {tl:24,…}, {tl:16,…,mult:14}, {tl:10,…} ]
```
依据：板级 board1 的调制算子（mult=14）tl 从 8 抬到 16 ⇒ 调制指数减半 ⇒
Tine 泛音弱化，"DX 电钢"变"暖电钢"。

### 4. Dinger 钟琴（algo1，percussive）
```json
ops = [ {tl:24,ar:15,dr:4,sl:12,rr:8,mult:1}, {tl:22,…,mult:1},
        {tl:14,ar:15,dr:6,sl:10,rr:8,mult:7}, {tl:12,ar:15,dr:3,sl:13,rr:8,mult:1} ]
```
依据：mult=7 深调制 + EGT=0（载波不永续）+ dr=3 ⇒ 玻璃敲击、非和谐泛音族。

### 5. 指贝斯·圆（algo2 双载波）
```json
ops = [ {tl:12,ar:13,dr:8,sl:7,rr:8,mult:1,wf:6}, {tl:30,…}, {tl:30,…},
        {tl:16,ar:12,dr:8,sl:7,rr:8,mult:1,wf:6} ]
```
依据：wf=6（折回正弦）在低音区等效"低通"⇒ 圆润；AR 13 比板级拨弦慢 ⇒ 指弹不敲击。

### 6. 马林巴（algo2，percussive）
```json
ops = [ {tl:14,ar:15,dr:7,sl:8,rr:9,mult:1}, {tl:30,…},
        {tl:30,…,mult:4}, {tl:18,ar:15,dr:7,sl:8,rr:9,mult:1} ]
```
依据：双载波 mult=1 与 4（一次谐频 + 三倍频）+ 快衰减 ⇒ 木条敲击的"空木"质感。

### 7. 金属·雨滴（algo3 树形，percussive）
```json
ops = [ {tl:22,ar:15,dr:6,sl:9,rr:11,mult:5}, {tl:26,…,mult:3},
        {tl:26,…,mult:7}, {tl:12,ar:15,dr:6,sl:9,rr:11,mult:1} ]
```
依据：三层调制 mult=5/3/7 ⇒ 泛音族密但互质（不叠成刺）；rr=11 拉出"雨滴尾巴"。

### 8. 铜锣·闷（algo3，percussive）
```json
ops = [ {tl:18,ar:9,dr:8,sl:10,rr:15,mult:1}, {tl:20,…,mult:1},
        {tl:20,…,mult:2}, {tl:10,ar:9,dr:8,sl:10,rr:15,mult:1} ]
```
依据：低 mult（1/1/2）避免金属化 + AR 9（起振慢）+ rr=15（最长释放）⇒ 闷锣。

### 9. 管风琴·主音栓（algo4 全并联）
```json
ops = [ {tl:14,…,mult:1}, {tl:20,…,mult:2}, {tl:24,…,mult:4}, {tl:28,…,mult:8} ]
```
依据：音栓响度按 8'+4'+2'+1' 递减（tl 14/20/24/28），EGT=1 永续 ⇒ 主音栓齐奏。

### 10. 和声人声（algo4）
```json
ops = [ {tl:16,ar:7,…,mult:1}, {tl:18,ar:7,…,mult:2,vib:1},
        {tl:20,ar:7,…,mult:1}, {tl:22,ar:7,…,mult:3,vib:1} ]
```
依据：AR 7 慢起振 + 两个算子带 vib（微颤）⇒ 人声"啊"的呼吸感；mult=1/2/1/3 齐奏微失谐。

### 11. Night Pad 闷锯（algo5 三载波）
```json
ops = [ {tl:24,…,mult:1,wf:6}, {tl:26,…,mult:2,wf:6},
        {tl:14,…,mult:1,wf:6}, {tl:24,…,mult:3,wf:6} ]
```
依据：wf=6 折回 = 把 supersaw 的高次谐波"折"下来 ⇒ 闷化；tl 整体收 4 步。

### 12. 先锋领奏·尖（algo5）
```json
ops = [ {tl:20,…,mult:1,wf:7}, {tl:24,…,mult:2,wf:7},
        {tl:6,…,mult:1,wf:7}, {tl:22,…,mult:3,wf:7} ]
```
依据：wf=7（反相正弦）+ 载波 tl=6 ⇒ 最亮的一套；mult=1/2/3 三层叠出边带。

### 13. 弦乐·緊（algo6 自反馈 FB=5）
```json
ops = [ {tl:20,ar:13,dr:8,sl:6,rr:8,mult:1}, {tl:30,…}, {tl:30,…}, {tl:10,…,mult:1} ]
```
依据：FB=5 与板级弦乐群相同，但 AR 13（快弓）+ 载波 tl=10（亮）⇒ staccato 弦乐。

### 14. 合唱人声·暗（algo6，FB=2）
```json
ops = [ {tl:18,ar:6,…,mult:1,wf:6}, {tl:24,…,wf:6}, {tl:24,…,wf:6}, {tl:14,…,mult:1,wf:6} ]
```
依据：FB 降到 2（反馈弱 ⇒ 边缘柔）+ wf=6 闷化 + AR 6 最慢起振 ⇒ 人声合唱 pad。

### 15. 风铃·散（algo7 环形 FM，percussive）
```json
ops = [ {tl:18,ar:15,dr:3,sl:13,rr:10,mult:6}, {tl:15,ar:14,dr:6,sl:6,rr:10,mult:1},
        {tl:28,ar:15,dr:9,sl:5,rr:10,mult:11}, {tl:22,ar:15,dr:3,sl:13,rr:10,mult:14} ]
```
依据：环形 FM 对 mult=6/11/14 ⇒ 非谐波族更散；rr=10 尾巴比板级钟长。

### 16. 水下钟（algo7，percussive）
```json
ops = [ {tl:20,ar:12,dr:4,sl:11,rr:15,mult:2}, {tl:18,ar:12,dr:6,sl:7,rr:15,mult:1},
        {tl:30,ar:12,dr:9,sl:5,rr:15,mult:1}, {tl:24,ar:12,dr:4,sl:11,rr:15,mult:1} ]
```
依据：mult 压到 2/1/1/1（近谐波）+ rr=15 最长释放 + tl 收 ⇒ 闷在水里的钟。

---

## 三、对照试听（同一段音乐 × 不同音色）

> 音乐固定 = `scores/demo_camfg_4x32/score.json` 的 4 轨（只换音色），渲染器与正式曲同一条链路。
> 每段给 1 行听感（**主观描述，未经他人复核**）：

| 文件 | 音色组合 | 听感 | 指标（渲染器实测） |
| :--- | :--- | :--- | :--- |
| `preview_bright.wav` | 玻璃领奏 / 弦乐·緊 / 马林巴 / 金属·雨滴 | 整体偏亮偏脆，高频颗粒感强，cymbal 位很跳 | peak −13.8 dBFS · 5.84 s |
| `preview_mellow.wav` | 电钢·暖芯 / 和声人声 / 指贝斯·圆 / 铜锣·闷 | 明显闷一档，低频圆，人声垫在后面"嗡"，最接近 lo-fi | peak −14.5 dBFS · 5.84 s |
| `preview_metal.wav` | 先锋领奏·尖 / 合唱人声·暗 / 马林巴 / Dinger 钟琴 | 领奏尖利穿出，钟琴残响硬，整体最"金属" | peak −10.4 dBFS · 5.84 s |

★ 三段 md5 互不相同（同一音乐 ⇒ 差异全部来自音色）：`a7d521af… / 1af4cf86… / 7afd659c…`。

---

## 四、上板落地代价（如实估，本轮**不做**）

| 项 | 内容 | 量级 |
| :--- | :--- | :--- |
| **RTL** | `mega60k/rtl/top/patch_bank.v` 现在 **8 套（preset 选择 3 bit）**，一算法一套。
  16 套新音色进板有两条路： | —— |
| 路 A（推荐） | **preset 位宽 3→4 bit（16 套）**：`patch_bank.v` 加 8 个 case 分支（每套 27 条寄存器写）+
  上游 preset 选择信号扩 1 位（`ui_ctrl`/`param_edit` 的预设旋钮 + 面板页）| RTL 约 3 处 · 面板标签 1 处 |
| 路 B | **算法内二选一**（preset 号不变，每算法挂 2 套参数用 1 bit 子开关选）：
  改动最小但语义拧巴（preset 号不再唯一决定音色）| RTL 1~2 处 · 但要记新约定 |
| **App** | 面板/文档里的"8 套音色"表要改成 16 套（`docs/60-app/ANDROID_APP.md`、`PERIPHERALS.md`）| 文档 2 处 |
| **门禁** | `tools/audit_presets.py` 的 BANK CHECK 断言"patch_bank 套数 == board_id 条数"⇒
  落 RTL 时必须同步给新套标 `board_id 8..15` 或改判据（**改判据要写理由 + 反向验证**，见 AGENTS §13.2）| 1 处 |
| **力度** | 用户明说"上板还有力度那是下一轮" ⇒ 本提案**不含** 0x50+v 联动 | —— |

★ 结论：**路 A 一次到位**（preset 4 bit + 8 套新参数 + 文档同步），估计半天工作量含回归；
但必须先落 `docs/10-spec/` 的音色库规格变更（新套号 8..15 的语义）再动 RTL。

## 五、诚实边界

- 16 套参数是**纸面设计**：依据 OPL3 对数域的公开行为（tl/mult/wf/包络标定）与 8 套板级音色的
  参数风格推算，**只过了渲染器链路**（与 RTL 引擎逐比特同构），**没有逐套人耳复听**
  （我只做了 3 段 A/B 对照的粗听感描述，见 §三——那是我的主观描述，未经他人复核）。
- `tl` 的 dB 换算按 `0.75 dB/步`；AR/RR 的时间标定可用 `py tools/audit_presets.py --rate-table`
  实测（我未逐套跑表，按板级同族参数外推）。
- 若某套上耳不对（最可疑：**金属·雨滴**的 mult 组合可能偏刺、**和声人声**的 vib 深度可能过大），
  调法都写在各套"依据"里（tl 收放 / mult 换近谐波 / vib 摘除）。

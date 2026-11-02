# scores/ —— 曲谱（根目录唯一曲谱目录）

> 这里是**曲谱的唯一真值位置**。文本曲谱给人看/编辑，`bin/` 里是同一首曲子的二进制帧流给 SerialTest 用。

## 一、文本格式（`.txt`）

```
# 一行一步；# 之后是注释；空行忽略
#   第 1 列 step ：步号（0 起，最大 255）
#   第 2 列 key  ：键号 = 半音偏移，0=C3, 1=C#3, …, 12=C4, …, 24=C5
#                 和弦用 + 连写，例如 8 0+7 2
#   第 3 列 dur  ：可选，持续几步（默认 1，1..64）
0 16 4
4 16 4
8 17 4
```

⚠ **键号只能 0..23**：线上 `DATA` 帧的 `bitmap` 只有 **24 bit**，`key=24`(C5) 发不出去
（`tools/score_push.py` 会报错，App 会标"⚠ 丢 N 个音"）。

## 二、文件清单

| 文件 | 大小 | 说明 |
| :--- | :--- | :--- |
| `ode_to_joy_piano.txt` | 3.9 KB | 《欢乐颂》单轨旋律，62 音 / 256 步 / 120 ms |
| `ode_to_joy_piano_rests.txt` | 3.9 KB | 同上，带休止符版本 |
| `demo_camfg_4x32.txt` | 7.3 KB | 4 轨 × 32 步演示曲 |
| `demo_camfg_4x32.json` | — | 同一首的结构化导出（音序器格式） |
| `bin/ode_to_joy_piano.bin` | 476 B | **19 帧**裸字节流（HEAD + 16×DATA + MODE + START，SEQ 0..18）|
| `bin/demo_twinkle.bin` | 82 B | 《小星星》5 帧，现场快演用 |

### 2.1 ★ 单轨「曲谱指引」曲包（8 首，2026-11-01）

> 用途：下发后 **25 颗 WS2812 出灯指引**，给演奏者跟弹 —— 每首都在头注释写明**建议 `step_ms`** 与
> **适配哪套板载音色**；逐首分析（音域集中度 / 节奏规整度 / 为什么适合跟弹）见
> [`docs/70-research/guide_scores.md`](../docs/70-research/guide_scores.md)。

| 曲名 | 文件 | 音符 | 谱长 | 建议 step_ms | 板载音色 |
| :--- | :--- | ---: | ---: | ---: | :--- |
| 两只老虎（零基础首选）| `guide_two_tigers.txt` | 28 | 128 | 150 | **4 管风琴**（只用 C D E F G 五个音）|
| Drunken Sailor（最易跟）| `guide_drunken_sailor.txt` | 24 | 136 | 150 | **2 拨弦**（8 键，四句同型）|
| 茉莉花（五声，音域最集中）| `guide_moli_hua.txt` | 67 | 152 | 160 | **6 弦乐群**（C3..C4 共 13 键）|
| 致爱丽丝（主题）| `guide_fur_elise.txt` | 26 | 128 | 150 | **1 电钢琴** |
| 卡农（主题）| `guide_canon.txt` | 40 | 160 | 160 | **0 羽管键琴**（全级进 ⇒ 灯相邻点亮）|
| 小步舞曲 BWV Anh.114 | `guide_minuet.txt` | 32 | 128 | 140 | **0 羽管键琴** |
| Greensleeves | `guide_greensleeves.txt` | 19 | 96 | 120 | **5 Supersaw**（全批最短 11.5 s）|
| 铃儿响叮当 | `guide_jingle_bells.txt` | 34 | 172 | 140 | **7 钟**（与音色天然匹配）|

- 二进制帧同名放 `bin/guide_*.bin`（`8 个`），SerialTest「发送文件」直接可用
- ★ **演示顺序建议**：两只老虎 → Drunken Sailor → 茉莉花（三种音色、音域逐步展开）
- 全部**公有领域**（巴赫/贝多芬/帕赫贝尔/英法传统歌谣/1867 Jingle Bells/江南民歌）
- 校验：`py tools/check_score_files.py` ⇒ **越界音 0**、`total_steps` 96~172 全 ≤256

### 2.2 ★ 4 轨 × 32 步多风格演示曲（5 首，2026-11-01）

> 用途：展示**合成器能力本身**（8 种 FM 拓扑 / 8 套板载音色 / 混响 / 复音）。
> 每首 `.json` 是 `ox1-multitrack-score` v1（4 轨 × 正好 32 步，每轨一个板级音色），
> 同名 `.txt` 是 4 轨合并谱（**App 曲库可直接读**）。
> 离线试听 WAV 由 `tools/render_multitrack.py` 渲染（**与板上同一条链路**：引擎模型 + FX 模型），
> 逐首配器分析与 WAV 清单见 [`docs/70-research/music_pack.md`](../docs/70-research/music_pack.md)。

| 曲名 | 风格 | 步长 | 4 轨音色 | 音符 | 同时发声 |
| :--- | :--- | ---: | :--- | ---: | ---: |
| `ambient_4x32` | **氛围** | 250 ms | 弦乐群·羽管键琴·管风琴·钟 | 12 | 4 |
| `orchestral_4x32` | **管弦** | 150 ms | 弦乐群·拨弦·管风琴·金属打击 | 36 | 4 |
| `pop_4x32` | **流行** | 120 ms | 电钢琴·管风琴·Supersaw·金属打击 | 78 | **7** |
| `experimental_4x32` | **实验** | 100 ms | 金属打击·钟·拨弦·电钢琴 | 42 | 5 |
| `china_4x32` | **中国风** | 150 ms | 羽管键琴·弦乐群·管风琴·钟 | 36 | 4 |

- ★ **8 套板载音色全部用上**（含 `preset 3 金属打击` —— 它在指引曲里用不了，这里用上了）
- 渲染：`py tools/render_multitrack.py --score scores/ambient_4x32/score.json --out work/wav/ambient_4x32.wav`
- 复现生成器：`tools/make_demo_songs.py`（曲谱是从这里生成的，改风格改它）
- WAV 规格：**48 828 Hz / 16 bit 立体声**（引擎原生率）· 峰值**未归一化**（就是板上的电平）
- ⚠ 多轨 JSON 比 v1 多一个顶层键 `"fx"`（总线混响参数）：`check_score_files.py` 忽略未知顶层键、
  App 不读多轨 JSON ⇒ **向后兼容**；渲染器若缺 `fx` 则用默认混响

> WAV 产物不入库（`work/` 被 ignore）；发布时挂在 GitHub Release 附件上。

## 三、三种用法

| 场景 | 怎么做 |
| :--- | :--- |
| **PC 直接下发**（TTL/USB 串口）| `py tools/score_push.py --file scores/ode_to_joy_piano/score.txt --port COM9` |
| **手机 + JDY-31**（推荐现场）| SerialTest 连 JDY-31（**115200**）→「**发送文件**」→ 选 `bin/ode_to_joy_piano.bin` → 发送 |
| **安卓 App**（在线曲库）| 曲库页填曲谱 URL（把 `.txt` 传到自己的服务器即可）或选本地文件 |

## 四、新增/修改曲谱后要做的两件事

```bash
# ① 语法 + 越界自检（键号 >23、步号 >255、dur 越界都会报）
py tools/check_score_files.py

# ② 重新生成 .bin（手机 SerialTest 用）
py tools/score_to_bin.py --file scores/你的曲子.txt --out scores/bin/你的曲子.bin
```

> 帧协议见 `docs/10-spec/SCORE_LINK_SPEC.md`；
> `total_steps` 的口径是 **`max(step+dur)`**（谱长），**不是事件个数**。

## 五、`index.json` 与「在线曲谱仓」（App 从这里拉）

`scores/index.json` 是**派生文件**：由各 `.txt` 的**头注释**（曲名 / 板载音色号）生成，
**不要手改**。改了曲谱就重跑生成器：

```bash
py tools/make_scores_index.py          # 重写 scores/index.json
py tools/make_scores_index.py --check  # 只比对（给门禁用；不一致 exit 1）
```

**在线曲谱仓**（公开，只放曲谱，不含源码）：<https://github.com/AUXUWA/OX-1-scores>

App 拉取时按这个顺序试（2026-11-01 本机实测；`raw.githubusercontent.com` 在国内**必败**：

| 顺序 | 地址 | 实测 |
| :--- | :--- | :--- |
| 1（首选）| `https://fastly.jsdelivr.net/gh/AUXUWA/OX-1-scores/index.json` | **HTTP 200 / 0.7 s** |
| 2 | `https://gcore.jsdelivr.net/gh/AUXUWA/OX-1-scores/index.json` | **HTTP 200 / 1.1 s** |
| 3 | `https://testingcf.jsdelivr.net/gh/AUXUWA/OX-1-scores/index.json` | **HTTP 200 / 2.0 s** |
| 4 | `https://cdn.jsdelivr.net/gh/AUXUWA/OX-1-scores/index.json` | HTTP 000（本机不通）|
| 5（兜底）| `https://raw.githubusercontent.com/AUXUWA/OX-1-scores/main/index.json` | **HTTP 000（被 reset）** |

单首曲谱 = `base + file`，例如
`https://fastly.jsdelivr.net/gh/AUXUWA/OX-1-scores/guide_two_tigers.txt`。

> ★★ **不要用 `@main`**（2026-11-01 实测教训，代价是一次 App 全挂）：
> jsDelivr 的 `@main` **不是「当前 main」** —— 它把「分支 → commit」的解析结果缓存最长 **12 小时**。
> `purge.jsdelivr.net` 清文件路径（`.../@main/index.json`）与分支级（`.../@main`）**都清不掉它**：
> 两者都返回 `status: finished`，内容仍然是旧的。
>
> 同一次推送后的实测对照（同一时刻、同一台机器）：
>
> | URL 形态 | `index.json` 实际内容 |
> | :--- | :--- |
> | `.../OX-1-scores@main/index.json` | **v1 / 13 首（旧）** ← 陷阱 |
> | `.../OX-1-scores/index.json`（无版本号）| **v2 / 26 首（新）** ← 正确 |
> | `.../OX-1-scores@<commit>/index.json` | v2 / 26 首（新，但每次发布都得改 URL）|
> | `.../OX-1-scores@v2/...`（非 semver tag）| 主文件 200，**子路径 404** ⇒ 不可用 |
>
> ⇒ 规则：**App 与两个生成器（`make_scores_index.py` / `make_patches_index.py`）一律用「无版本号」URL**；
> 单曲/音色文件走 `base + file`，base 同样无版本号。
>
> ★ **更正（同日复测，别信我上一版的话）**：`?cb=<时间戳>` 这类缓存破坏参数**对 jsDelivr 无效** ——
> 同一 URL 加随机 cb 仍然返回旧内容（我第一次判断"能拿到新内容"是单点观测，复测即被推翻）。
> ⇒ 若要求「推送后**立刻**可读」，只有两条路：
> ① `@<commit>` 形态（不可变引用，必然是新内容，但每次发布都要改 URL）；
> ② **GitHub Pages**：`https://auxuwa.github.io/OX-1-scores/`（直接从仓里按字节服务，不经 jsDelivr 缓存）。
> jsDelivr 的「无版本号」URL 只是**比 `@main` 新鲜**，仍可能有分钟级到小时级延迟 —— 不要把它当"实时"。
>
> ★★ **GitHub Pages 已启用并实测可用（2026-11-01）**：`https://auxuwa.github.io/OX-1-scores/`
> —— 直读仓库、**不经 jsDelivr 缓存**，所以"刚推的立刻能拿到"只有这条路靠得住。
> 实测：`index.json` 200（v2/26）· `patches/index.json` 200 · `patches/local_new/Dinger%20钟琴.json` 200
> （**须 URL 编码**）· `guide_canon/score.txt` 200（子目录形式）；
> 速度与 jsDelivr 同量级（`index.json` 各 3 次：Pages 0.71/0.76/1.43 s vs jsDelivr 0.76/1.05/1.75 s）。
> ★ 例外：`preview.wav` 单首约 1.3 MB，Pages 实测 **25 s** ⇒ App 试听必须懒加载，不要默认下载。
>
> ⇒ App 的 index 拉取顺序应为：**Pages 首选** → fastly → gcore → testingcf → raw（兜底）；
> 曲谱/音色**内容文件仍走 `base`（jsDelivr）**，因为它路径新、不受分支缓存影响。
> ⚠ Pages 首次构建踩过：`pages/builds/latest` 报 `status=building` 且 `duration=0` 卡了 25 分钟，
> `POST /repos/{owner}/{repo}/pages/builds` 重新触发后 21.9 s 完成 ⇒ 卡住就重触发，别干等。
> 更阴的一点：`@main` 下被**删除**的旧文件会立刻 404，而没变的文件仍是旧内容 —— 新旧混合最难查，
> 这正是必须避开 `@main` 的原因。

> ★ 为什么单独建一个**公开**仓：主仓是**私有**的，jsDelivr / Pages 都不服务私有仓
> （实测：私有仓的 CDN 请求一律 301 跳去 `raw.githubusercontent.com`，然后被 reset）。
> 曲谱都是 PD 曲目 + 我们自己的文本编码，公开没有泄密问题；源码仍留在私有主仓。

## 六、★ 两种布局并存（t43 起，2026-11-01）

| 布局 | 形态 | dir 字段 | 状态 |
| :--- | :--- | :--- | :--- |
| **旧扁平** | `scores/<name>.txt`（+ 同名 .json） | `""` | 兼容保留：**很多脚本/文档在引用**（`score_push.py`、`check_score_files.py`、`bin/*.bin`、App 文档），**不搬不改** |
| **新文件夹** | `scores/<slug>/`（一曲一文件夹） | `"<slug>/"` | **新曲一律走这里**（t43 起 10 首 + t44 起 6 首 = 16 首） |

> ⚠ 2026-11-01 工作区记录：并行批次曾把旧 5 首 .txt/.json **git mv 进同名文件夹**
> （`ambient_4x32/score.json` 等）—— 现在磁盘上旧扁平与文件夹**并存**（同内容双份）。
> `make_scores_index.py` v2 同时扫两种形态且去重靠文件路径 ⇒ index.json 里它们是**两条**
> （一条 dir=""、一条 dir="<slug>/"），App 侧拉取按 `dir + file` 拼 URL，两者都合法。
> 是否把旧扁平真正删除，等 Lead 决定（牵动面：score_push 文档、App 文档、外部引用）。

### 6.1 新文件夹规范（t43 定）

```
scores/<slug>/
├── score.json     渲染器输入（ox1-multitrack-score v1，4 轨 × 32 步）
├── score.txt      下发用合并谱（`step key [dur]`；头注释规范与所有 .txt 一致）
├── score.bin      下发帧流（`py tools/score_to_bin.py` 生成：HEAD+DATA+MODE+START，SEQ 递增）
├── score.hex      ★ 可嵌入 FPGA 的 ROM 初值（$readmemh）：32 行 × 4 字节 = 4 轨，
│                    每字节 {2'b0, on, pitch[4:0]} —— 与 SCORE_LINK_SPEC §13.4 的
│                    SEQD 载荷字节**同构**。本轮不落 RTL（下一轮可装 32×32bit ROM）。
├── preview.wav    离线试听（48 828 Hz / 16 bit / 立体声，render_multitrack 渲染）
├── meta.json      机器可读（slug/name/style/step_ms/loop/tracks/duration/peak_dbfs/
│                    renderer/rate/bits/channels/patch_bank_ref）
└── README.md      人读（风格/情绪/音色表/建议参数/响度）
```

一致性自证（hex ↔ bin ↔ json 三方同源，**从文件反解**，不是重新生成）：

```bash
py scores/verify_score_hex.py   # ⇒ *** PASS ***（14/14 首；逐帧 CRC + HEAD.total_steps + 事件⊆网格）
```

### 6.2 t43 新增 10 首（一文件夹一曲，8 套板载音色全覆盖）

| 曲名 | 风格 | step_ms | 4 轨音色（patch） | 时长（渲染实测） | 峰值 |
| :--- | :--- | ---: | :--- | ---: | ---: |
| 深空 Ambient | 氛围 | 260 | 弦乐群6 · 管风琴4 · 钟7 · 电钢琴1 | 10.32 s | −9.5 dBFS |
| 进行曲 March | 管弦/进行曲 | 140 | 弦乐群6 · 管风琴4 · 拨弦2 · 金属打击3 | 6.48 s | −9.7 dBFS |
| 放克 Funk | 流行 | 130 | 拨弦2 · Supersaw5 · 电钢琴1 · 金属打击3 | 6.16 s | −13.2 dBFS |
| 实验音块 Block | 实验 | 170 | 管风琴4 · 弦乐群6 · 羽管键琴0 · 金属打击3 | 7.44 s | −6.8 dBFS |
| 茉莉变奏 | 中国风 | 180 | 管风琴4 · 弦乐群6 · 拨弦2 · 钟7 | 7.76 s | −7.8 dBFS |
| 爵士漫步 Lounge | 爵士 | 160 | 管风琴4 · 电钢琴1 · 拨弦2 · 钟7 | 7.12 s | −10.0 dBFS |
| 落日 Lo-fi | 电子 lo-fi | 220 | 电钢琴1 · 拨弦2 · 弦乐群6 · 钟7 | 9.04 s | −10.7 dBFS |
| 追猎 Chase | 电影感 | 125 | 金属打击3 · 弦乐群6 · 管风琴4 · 钟7 | 6.00 s | −9.6 dBFS |
| 多瑙河圆舞曲风 | 圆舞曲 | 190 | 弦乐群6 · 管风琴4 · 拨弦2 · 钟7 | 8.08 s | −8.5 dBFS |
| 夜驰 Synthwave | 电子 synthwave | 150 | Supersaw5 · 拨弦2 · 电钢琴1 · 金属打击3 | 6.80 s | −12.7 dBFS |

### 6.3 ★ 音色使用矩阵（8 套板载音色全覆盖）

> 列 = `patch_bank.v` 的 8 套（preset 0..7）；✅ = 该曲有轨用这套；— = 未用。
> **8 列全部有 ✅**（列统计在最下行）；**组合去重后 12 种**（16 首里；进行曲/追猎 同用 {2,3,4,6} 与 {3,4,6,7}、爵士/圆舞曲 同用 {1,2,4,7} 的兄弟组）—— 已如实统计。
> ★ **列统计由 `score.json` 的 `patch` 字段实测得出**（改曲后请重算，别手改）。

| 曲名 | 0 羽管键琴 | 1 电钢琴 | 2 拨弦 | 3 金属打击 | 4 管风琴 | 5 Supersaw | 6 弦乐群 | 7 钟 |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 深空 Ambient | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| 进行曲 March | — | — | ✅ | ✅ | ✅ | — | ✅ | — |
| 放克 Funk | — | ✅ | ✅ | ✅ | — | ✅ | — | — |
| 实验音块 Block | ✅ | — | — | ✅ | ✅ | — | ✅ | — |
| 茉莉变奏 | — | — | ✅ | — | ✅ | — | ✅ | ✅ |
| 爵士漫步 Lounge | — | ✅ | ✅ | — | ✅ | — | — | ✅ |
| 落日 Lo-fi | — | ✅ | ✅ | — | — | — | ✅ | ✅ |
| 追猎 Chase | — | — | — | ✅ | ✅ | — | ✅ | ✅ |
| 多瑙河圆舞曲风 | — | — | ✅ | — | ✅ | — | ✅ | ✅ |
| 夜驰 Synthwave | — | ✅ | ✅ | ✅ | — | ✅ | — | — |
| 芯片街机（t44） | ✅ | — | ✅ | ✅ | — | ✅ | — | — |
| 探戈 · 烈焰（t44） | — | — | ✅ | ✅ | ✅ | — | ✅ | — |
| 午后波萨（t44） | — | ✅ | — | ✅ | ✅ | — | ✅ | — |
| 凯尔特海港（t44） | ✅ | — | — | — | ✅ | — | ✅ | ✅ |
| 福音之光（t44） | — | — | ✅ | ✅ | ✅ | — | ✅ | — |
| 午夜蓝调（t44） | — | ✅ | ✅ | ✅ | ✅ | — | — | — |
| **列统计（16 首里被用次数）** | **3** | **7** | **11** | **10** | **12** | **3** | **11** | **7** |

> ★ 0 羽管键琴在 t43 批只被"实验音块"用了 1 次（它的定位是"点状明亮拨弦"，多数曲目被更贴的
> 拨弦/电钢琴顶掉）—— **如实记录**；t44 批已按此建议**优先给 algo0**（芯片街机 / 凯尔特海港各 1 首）
> ⇒ 该列由 1 次增至 3 次。
> （旧 5 首 `ambient_4x32` 等也覆盖 0/1/3/4/5/6 —— 与本矩阵的"全覆盖"结论互证。）

### 6.4 ★ t44 新增 6 首：多风格曲包（2026-11-02）

> 生成器：`tools/make_new_songs.py`（**唯一真值源** —— `score.json` / `score.txt` / `score.hex` /
> `meta.json` / `README.md` 全部由它从同一份音符数据派生；`score.bin` 由 `tools/score_to_bin.py`、
> `preview.wav` 由 `tools/render_multitrack.py` 生成）。
>
> ```bash
> py tools/make_new_songs.py               # 全部生成 + 渲染（每首约 1 min）
> py tools/make_new_songs.py --only blues_shuffle_4x32   # 只重做一首
> py tools/make_new_songs.py --no-render   # 只出谱面/元数据，不渲染
> ```
>
> ★ **与 t43 批的三点差别**（这批是按"更好听"重新设计的，不是照抄）：
> 1. **每轨单声部**：同一轨内音符在时间上不重叠 —— 板上 PAGE-2 音序器
>    （`seq_page`/`seq_play4`）**每格只存一个音高**，4 轨 = 4 条单声部线；
>    本批的 `score.json` 与板端口径一致，可直接照搬进 ROM。
> 2. **音区分工**：低音区 0..11 · 和声区 9..19 · 主奏区 14..23 · 打击乐另占
>    10/11/20/22 —— **主奏与低音不共音高**（既有曲包有 `pop_4x32` 这类 15 步同音高叠加）。
> 3. **`.bin` 带本曲自己的 `step_ms`**：既有 16 首的 `.bin` 全部是 CLI 默认 120 ms
>    （与各自 `score.json` 的 `step_ms` 不符），本批由生成器显式传 `--step-ms`，
>    推送速度与曲谱一致。

| 曲名 | 风格 | step_ms | 4 轨音色（patch） | 时长（渲染实测） | 峰值 | RMS |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: |
| 芯片街机 | 电子 8-bit | 100 | Supersaw5 · 羽管键琴0 · 拨弦2 · 金属打击3 | 5.20 s | −11.3 dBFS | −28.9 dBFS |
| 探戈 · 烈焰 | 探戈 | 150 | 弦乐群6 · 拨弦2 · 管风琴4 · 金属打击3 | 6.80 s | −9.2 dBFS | −23.5 dBFS |
| 午后波萨 | 拉丁 Bossa | 130 | 弦乐群6 · 电钢琴1 · 管风琴4 · 金属打击3 | 6.16 s | −9.0 dBFS | −23.2 dBFS |
| 凯尔特海港 | 凯尔特 | 125 | 羽管键琴0 · 弦乐群6 · 管风琴4 · 钟7 | 6.00 s | −9.5 dBFS | −23.9 dBFS |
| 福音之光 | 福音 Soul | 165 | 管风琴4 · 弦乐群6 · 拨弦2 · 金属打击3 | 7.28 s | −5.9 dBFS | −21.4 dBFS |
| 午夜蓝调 | 布鲁斯 Shuffle | 150 | 拨弦2 · 电钢琴1 · 管风琴4 · 金属打击3 | 6.80 s | −9.9 dBFS | −28.4 dBFS |

> 全部 **削波样本 = 0**（渲染器实测，`meta.json` 有记录）。
> 栅格：**1 步 = 1 个十六分音符**（4 步 = 1 拍、16 步 = 1 小节、32 步 = 2 小节），
> 与渲染器打印的 `BPM = 60000 / (4 × 步长)` 同口径。

### 6.5 更多音色（16 套新提案，**只放本地**）

- `patches/board_0..7.json`：板级 8 套的**只读导出**（真源 presets.json board_id，勿改）。
- `patches/local_new/*.json`：**16 套新音色**（每算法 2 套，**无 board_id**），
  渲染器已支持 `"patch_local": "<名>"` 引用（t43 起已支持；board 0..7 参数一字未动）。
- `patches/preview_*.wav`：**3 段对照试听**（同一段音乐 × 不同音色，md5 各异）。
- 详见 [`patches/README.md`](patches/README.md) 与 [`patch_proposals.md`](patch_proposals.md)
  （含每套的参数依据 + **上板落地代价**：preset 位宽 3→4 bit，本轮不做）。

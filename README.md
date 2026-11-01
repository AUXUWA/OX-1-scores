# OX-1 曲谱仓（在线曲谱源）

**这是什么**：FPGA 实时 FM 合成器 **OX-1** 的安卓上位机 App 从这里**在线拉取曲谱**。
一共 13 首，全部可以离线内置在 App 里，本仓是「联网更新 / 换曲」的那条路。

## 怎么拉（App 里用这条）

| 方式 | URL | 说明 |
| :--- | :--- | :--- |
| **索引（首选）** | `https://fastly.jsdelivr.net/gh/AUXUWA/OX-1-scores@main/index.json` | jsDelivr CDN，国内实测可用 |
| 备用 CDN | `https://cdn.jsdelivr.net/gh/AUXUWA/OX-1-scores@main/index.json` | 同服务，另一入口 |
| 直连（**可能被 reset**） | `https://raw.githubusercontent.com/AUXUWA/OX-1-scores/main/index.json` | 国内常失败，仅作兜底 |

> ★ 为什么用 jsDelivr：`raw.githubusercontent.com` 在本机实测 **HTTP 000（连接被重置）**，
> 而 jsDelivr 实测 **HTTP 200**。App 端按「fastly → cdn → raw」顺序重试。

拿到 `index.json` 后，把 `base + file` 拼起来就是单首曲谱：
```
https://fastly.jsdelivr.net/gh/AUXUWA/OX-1-scores@main/guide_two_tigers.txt
```

## `index.json` 结构（v1）

```json
{
  "v": 1,
  "generated": "2026-11-01T10:52:00+08:00",
  "base": "https://fastly.jsdelivr.net/gh/AUXUWA/OX-1-scores@main/",
  "songs": [
    { "file": "guide_two_tigers.txt", "name": "两只老虎（Frère Jacques）",
      "group": "单轨指引", "preset": 4, "note": "preset 4 管风琴 · 128 步",
      "total_steps": 128, "events": 28, "notes": 28 }
  ]
}
```

- `group`：`单轨指引`（8 首，练琴用）或 `四轨合奏`（5 首，4 轨 × 32 步合并谱）
- `preset`：板载 8 套音色号（0~7）；四轨合奏为 `null`（各轨音色写在曲谱头注释里）
- `total_steps` = `max(step + dur)`（**不是**事件个数）
- 本文件由主仓 `tools/make_scores_index.py` 从各 `.txt` 的**头注释**派生 ⇒ 不要手改

## 曲谱文件格式（纯文本，`#` 开头是注释）

```
# 注释行：曲名 / 来源 / 调性 / 板载音色
step key[+key...] [dur]
```
- `step`：步号（十进制，从 0 起）
- `key`：键号 **0~24**（C3~C5 全半音）· 支持和弦 `0+12` · `-` 表示休止
- `dur`：持续步数，省略 = 1

例：
```
0 12 4
4 14 4
8 16 4
```

## 许可

曲目本身均为 **公有领域（PD）** 或传统民谣/儿歌（两只老虎、茉莉花、绿袖子、卡农、
小步舞曲 BWV Anh.114、致爱丽丝、铃儿响叮当、Drunken Sailor）。
本仓的**文本谱面**（step/key/dur 编码）为 OX-1 工程自行制作，可自由取用。

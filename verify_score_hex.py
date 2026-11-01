#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_score_hex.py —— 一致性自证：score.hex 与 score.bin / score.json / score.txt 同源。

用法：
    py scores/verify_score_hex.py                 # 扫 scores/*_4x32/（含 score.hex 的）
    py scores/verify_score_hex.py <slug> ...      # 只查指定曲

核对三件事（**全部从文件反解**，不重新生成）：
  H1  score.hex  32 行 × 4 字节，字节 ∈ {0x00} ∪ {0x20..0x37}（= {2'b0,on,pitch[4:0]} 值域）
  H2  hex 反解出的 (on,pitch) 网格 == score.json 的 steps（每步每轨：bitmap≠0 ⇒ on=1、pitch=最低位键号）
  H3  score.bin 反解回事件（SOA/CMD/LEN/CRC 走一遍）⇒ total_steps 与 HEAD 载荷一致 = 32，
      事件集合 ⊆ hex 网格（.bin 是合并谱，hex 是 4 轨视图）
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def crc8(data):
    c = 0
    for b in data:
        c ^= b
        for _ in range(8):
            c = ((c << 1) ^ 0x07) & 0xFF if (c & 0x80) else (c << 1) & 0xFF
    return c


def parse_bin(blob):
    """裸帧流 → [(cmd, payload, seq)]；校验每帧 CRC。"""
    frames = []
    off = 0
    while off < len(blob):
        if blob[off] != 0xA5:
            raise ValueError("offset %d: SOF != A5" % off)
        cmd = blob[off + 1]
        ln = blob[off + 2]
        flen = 5 + ln
        f = blob[off:off + flen]
        if len(f) < flen:
            raise ValueError("offset %d: 截断帧" % off)
        if crc8(blob[off + 1:off + flen - 1]) != blob[off + flen - 1]:
            raise ValueError("offset %d: CRC 错" % off)
        seq = f[3 + ln]
        frames.append((cmd, f[3:3 + ln], seq))
        off += flen
    return frames


def check(slug):
    d = os.path.join(ROOT, slug)
    errs = []
    # ---- H1: hex 形状 ----
    raw = open(os.path.join(d, "score.hex"), "rb").read().decode("utf-8")
    rows = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if len(rows) != 32:
        errs.append("hex 行数 %d != 32" % len(rows))
    grid = [[0, 0, 0, 0] for _ in range(32)]
    for i, ln in enumerate(rows):
        bs = [int(x, 16) for x in ln.split()]
        if len(bs) != 4:
            errs.append("hex 行 %d: %d 字节 != 4" % (i, len(bs)))
            continue
        for t, b in enumerate(bs):
            if b != 0x00 and not (0x20 <= b <= 0x37):
                errs.append("hex 行 %d 轨 %d: 0x%02x 不在 {00,20..37}" % (i, t, b))
            grid[i][t] = b
    # ---- H2: hex 反解 == score.json steps ----
    doc = json.load(open(os.path.join(d, "score.json"), encoding="utf-8"))
    for t, tr in enumerate(doc["tracks"]):
        for si, st in enumerate(tr["steps"]):
            bm = int(st.get("bitmap", 0))
            want = 0x00 if bm == 0 else (1 << 5) | ((bm & -bm).bit_length() - 1)
            if grid[si][t] != want:
                errs.append("hex(%d,%d)=%02x != json 期望 %02x" % (si, t, grid[si][t], want))
    # ---- H3: bin 的 HEAD 与事件落在网格里 ----
    blob = open(os.path.join(d, "score.bin"), "rb").read()
    frames = parse_bin(blob)
    head = [pl for (c, pl, _sq) in frames if c == 0x01]
    if len(head) != 1:
        errs.append("bin 里 HEAD 帧 %d 个（应 1）" % len(head))
    else:
        total = head[0][0] | (head[0][1] << 8)
        if total != doc["total_steps"]:
            errs.append("bin HEAD.total_steps=%d != json total_steps=%d" %
                        (total, doc["total_steps"]))
    events = set()
    for (c, p, s) in frames:
        if c != 0x02:
            continue
        for i in range(0, len(p), 6):
            step = p[i] | (p[i + 1] << 8)
            flag = p[i + 2]
            bm = p[i + 3] | (p[i + 4] << 8) | (p[i + 5] << 16)
            if flag & 0x80:
                k = (bm & -bm).bit_length() - 1 if bm else -1
                if k >= 0:
                    events.add((step, k))
    merged = set()
    for si in range(32):
        for t in range(4):
            b = grid[si][t]
            if b:
                merged.add((si, b & 0x1F))
    missing = events - merged
    if missing:
        errs.append("bin 事件 %d 个不在 hex 网格里：%s" % (len(missing), sorted(missing)[:5]))
    return errs, len(frames), len(events)


def main():
    args = sys.argv[1:]
    slugs = args or sorted(
        s for s in os.listdir(ROOT)
        if os.path.isfile(os.path.join(ROOT, s, "score.hex")))
    fails = 0
    for slug in slugs:
        try:
            errs, nfr, nev = check(slug)
        except Exception as e:
            errs = [str(e)]
            nfr = nev = -1
        if errs:
            fails += 1
            print("  [FAIL] %-32s %s" % (slug, "; ".join(errs)))
        else:
            print("  [ OK ] %-32s bin %d 帧 / %d 事件 == hex 网格（4×32）" % (slug, nfr, nev))
    print("*** %s *** verify_score_hex：%d/%d 首" %
          ("FAIL" if fails else "PASS", len(slugs) - fails, len(slugs)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

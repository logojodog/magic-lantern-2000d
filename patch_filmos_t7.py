#!/usr/bin/env python3
"""T7/2000D film OS performance patches applied after cloning upstream M-Film."""
from pathlib import Path
import sys

def patch_shelf(path: Path) -> None:
    text = path.read_text()
    old = """    for (int i = 0; i < nlist && n < 8; i++)
    {
        float d = i - pos.x;
        if (absf(d) > 2.7f) continue;
        order[n].i = i; order[n].d = d; n++;
    }
    /* far ones first */
    for (int a = 0; a < n; a++)
        for (int b = a + 1; b < n; b++)
            if (absf(order[b].d) > absf(order[a].d))
            {
                int ti = order[a].i; float td = order[a].d;
                order[a] = order[b];
                order[b].i = ti; order[b].d = td;
            }

    for (int k = 0; k < n; k++)
    {
        int i = list[order[k].i];
        float d = order[k].d;
        struct fos_can_pose p;
        int mid = absf(d) < 0.5f;
        pose_of(d, &p, mid ? lift_mid : 0, spread);
        if (!mid) p.light = (int) (p.light * (1 - fade_sides));
        if (drop.x > 0.002f)
        {
            /* a new shelf: its canisters drop in from above (or rise from below), the far ones a little later */
            float t = clampf(drop.x * (1 + absf(d) * 0.25f), 0, 1);
            p.floor_y -= (int) (t * 90 * drop_dir);
            p.light = (int) (p.light * (1 - t));
            p.reflect = (int) (p.reflect * (1 - t));
        }
        if (mid && leader_mid) p.leader = leader_mid;
        if (p.light <= 4) continue;
        struct fos_can *c = ui_can(i);
        int w = fos_can_width(p.scale);
        contact_shadow(p.cx8 >> 8, p.floor_y, w * 6 / 10, 7 * p.scale / 256 + 2, 150 * p.light / 256);
        fos_can_draw(cv, c, &p);"""

    new = """    /* T7: fewer cans + tighter range when moving or quality low */
    float max_d = (fos_can_quality <= 0 || absf(pos.v) > 0.9f) ? 1.6f : 2.7f;
    int max_n   = (fos_can_quality <= 0 || absf(pos.v) > 1.2f) ? 5 : 8;
    for (int i = 0; i < nlist && n < max_n; i++)
    {
        float d = i - pos.x;
        if (absf(d) > max_d) continue;
        order[n].i = i; order[n].d = d; n++;
    }
    /* far ones first */
    for (int a = 0; a < n; a++)
        for (int b = a + 1; b < n; b++)
            if (absf(order[b].d) > absf(order[a].d))
            {
                int ti = order[a].i; float td = order[a].d;
                order[a] = order[b];
                order[b].i = ti; order[b].d = td;
            }

    int skip_shadow = (fos_can_quality <= 0) || (absf(pos.v) > 0.7f);

    for (int k = 0; k < n; k++)
    {
        int i = list[order[k].i];
        float d = order[k].d;
        struct fos_can_pose p;
        int mid = absf(d) < 0.5f;
        pose_of(d, &p, mid ? lift_mid : 0, spread);
        if (!mid) p.light = (int) (p.light * (1 - fade_sides));
        if (drop.x > 0.002f)
        {
            /* a new shelf: its canisters drop in from above (or rise from below), the far ones a little later */
            float t = clampf(drop.x * (1 + absf(d) * 0.25f), 0, 1);
            p.floor_y -= (int) (t * 90 * drop_dir);
            p.light = (int) (p.light * (1 - t));
            p.reflect = (int) (p.reflect * (1 - t));
        }
        if (mid && leader_mid) p.leader = leader_mid;
        if (p.light <= 4) continue;
        if (!mid && (fos_can_quality <= 0 || absf(pos.v) > 0.8f))
            p.reflect = 0;
        struct fos_can *c = ui_can(i);
        int w = fos_can_width(p.scale);
        if (!skip_shadow)
            contact_shadow(p.cx8 >> 8, p.floor_y, w * 6 / 10, 7 * p.scale / 256 + 2, 150 * p.light / 256);
        fos_can_draw(cv, c, &p);"""

    if old not in text:
        raise SystemExit(f"fos_shelf draw_canisters body not found in {path}")
    path.write_text(text.replace(old, new))
    print(f"patched {path}")


def patch_ui(path: Path) -> None:
    text = path.read_text()
    old = """    int avg = (stat.draw_ms + stat.present_ms) / stat.frames;
    if (avg > 50) { slow++; quick = 0; }
    else if (avg < 26) { quick++; slow = 0; }
    else slow = quick = 0;
    if (slow >= 1 && fos_can_quality > 0) { fos_can_quality--; slow = 0; }
    if (quick >= 3 && fos_can_quality < 2) { fos_can_quality++; quick = 0; }"""
    new = """    int avg = (stat.draw_ms + stat.present_ms) / stat.frames;
    /* more aggressive on slow bodies (T7/2000D) */
    if (avg > 42) { slow++; quick = 0; }
    else if (avg < 22) { quick++; slow = 0; }
    else slow = quick = 0;
    if (slow >= 1 && fos_can_quality > 0) { fos_can_quality--; slow = 0; }
    if (quick >= 4 && fos_can_quality < 2) { fos_can_quality++; quick = 0; }"""
    if old not in text:
        raise SystemExit(f"fos_ui frame_stats thresholds not found in {path}")
    text = text.replace(old, new).replace("#define FRAME_PERIOD 28", "#define FRAME_PERIOD 32")
    path.write_text(text)
    print(f"patched {path}")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/M-Film")
    patch_shelf(root / "ml-dev/filmos/fos_shelf.c")
    patch_ui(root / "ml-dev/filmos/fos_ui.c")
    print("T7 optimizations applied")


if __name__ == "__main__":
    main()

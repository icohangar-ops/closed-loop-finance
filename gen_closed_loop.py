#!/usr/bin/env python3
"""Diagram 4: The Closed Loop — Cross-Period Learning Cycle."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch
import matplotlib.patheffects as pe

BG     = "#1a1a2e"
WHITE  = "#e0e0e0"
DIM    = "#8892a0"
CYAN   = "#00b4d8"
GREEN  = "#2ec4b6"
PURPLE = "#c77dff"
GOLD   = "#e2b714"
RED    = "#ff6b6b"

fig, ax = plt.subplots(figsize=(16, 12))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis("off")
ax.set_aspect("equal")

# ── Title ──
ax.text(8, 11.5, "The Closed Loop — Cross-Period Learning",
        fontsize=22, fontweight="bold", color=WHITE, ha="center", fontfamily="DejaVu Sans")
ax.text(8, 11.0, "Each month-end close improves the next through persistent memory",
        fontsize=12, color=DIM, ha="center", fontfamily="DejaVu Sans")

# ── Center hub ──
cx, cy = 8, 6.0
hub_r = 1.8
circle_bg = plt.Circle((cx, cy), hub_r, color="#0a0f1e", zorder=2)
circle_edge = plt.Circle((cx, cy), hub_r, fill=False, edgecolor=PURPLE, linewidth=2.5, zorder=3)
ax.add_patch(circle_bg)
ax.add_patch(circle_edge)

ax.text(cx, cy + 0.55, "Memory Agent", fontsize=13, fontweight="bold",
        color=PURPLE, ha="center", va="center", fontfamily="DejaVu Sans", zorder=4)
ax.text(cx, cy + 0.1, "+", fontsize=11, color=DIM, ha="center", va="center", zorder=4)
ax.text(cx, cy - 0.3, "Vector Search", fontsize=10, color="#c77dff",
        ha="center", va="center", fontfamily="DejaVu Sans", zorder=4)
ax.text(cx, cy - 0.65, "+ Notion Decision Log", fontsize=9, color=DIM,
        ha="center", va="center", fontfamily="DejaVu Sans", zorder=4)

# ── Month nodes around the circle ──
import math

months = [
    {
        "label": "Month 1\nMarch Close",
        "detail": "9 files parsed\n12 findings\n4 decisions approved",
        "color": GREEN, "bg": "#0d2f2f", "angle": 60,
    },
    {
        "label": "Month 2\nApril Close",
        "detail": "Prior context retrieved\n8 findings (3 recurring)\n3 new decisions",
        "color": CYAN, "bg": "#0a1f2e", "angle": 120,
    },
    {
        "label": "Month 3\nMay Close",
        "detail": "2 periods of history\nRecurring issues flagged early\n5 decisions approved",
        "color": GOLD, "bg": "#2e1f0a", "angle": 200,
    },
    {
        "label": "Month N\nFuture Close",
        "detail": "Full decision history\nAutomated pattern matching\nContinuous improvement",
        "color": PURPLE, "bg": "#1a0a2e", "angle": 320,
    },
]

orbit_r = 4.0
node_w, node_h = 3.2, 2.0

node_positions = []
for m in months:
    angle_rad = math.radians(m["angle"])
    nx = cx + orbit_r * math.cos(angle_rad) - node_w / 2
    ny = cy + orbit_r * math.sin(angle_rad) - node_h / 2
    node_positions.append((cx + orbit_r * math.cos(angle_rad),
                            cy + orbit_r * math.sin(angle_rad)))

    b = FancyBboxPatch((nx, ny), node_w, node_h, boxstyle="round,pad=0.25",
                        facecolor=m["bg"], edgecolor=m["color"],
                        linewidth=2, zorder=2)
    ax.add_patch(b)

    tcx = cx + orbit_r * math.cos(angle_rad)
    tcy = cy + orbit_r * math.sin(angle_rad)

    ax.text(tcx, tcy + 0.45, m["label"], fontsize=11, fontweight="bold",
            color=m["color"], ha="center", va="center", fontfamily="DejaVu Sans", zorder=3)

    # separator
    ax.plot([nx + 0.2, nx + node_w - 0.2],
            [tcy + 0.05, tcy + 0.05],
            color=m["color"], lw=0.7, alpha=0.4, zorder=3)

    for j, line in enumerate(m["detail"].split("\n")):
        ax.text(tcx, tcy - 0.2 - j * 0.3, line,
                fontsize=7.5, color=DIM, ha="center", va="center",
                fontfamily="DejaVu Sans", zorder=3)

# ── Curved arrows between month nodes (clockwise) ──
for i in range(len(months)):
    x1, y1 = node_positions[i]
    x2, y2 = node_positions[(i + 1) % len(months)]

    # Midpoint pushed outward
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # Push away from center
    dx = mx - cx
    dy = my - cy
    dist = math.sqrt(dx**2 + dy**2)
    push = 0.8
    mx += dx / dist * push
    my += dy / dist * push

    ax.annotate("",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="->,head_width=0.25,head_length=0.18",
                    color=months[(i + 1) % len(months)]["color"],
                    lw=2.2,
                    connectionstyle=f"arc3,rad=0.25",
                    zorder=4
                ))

# ── Arrows from month nodes to center hub ──
for i, (px, py) in enumerate(node_positions):
    # Direction toward center
    dx = cx - px
    dy = cy - py
    dist = math.sqrt(dx**2 + dy**2)
    # Start from edge of node toward hub
    sx = px + dx/dist * 1.6
    sy = py + dy/dist * 1.0
    ex = cx - dx/dist * hub_r
    ey = cy - dy/dist * hub_r

    # Write arrow (node -> hub)
    ax.annotate("",
                xy=(ex, ey), xytext=(sx, sy),
                arrowprops=dict(
                    arrowstyle="->,head_width=0.2,head_length=0.12",
                    color=PURPLE, lw=1.3, linestyle=":", alpha=0.7, zorder=4
                ))

    # Retrieve arrow (hub -> node)
    offset = 0.15
    sx2 = px + (dx/dist * 1.6) + offset * (dy/dist)
    sy2 = py + (dy/dist * 1.0) - offset * (dx/dist)
    ex2 = cx - (dx/dist * hub_r) + offset * (dy/dist)
    ey2 = cy - (dy/dist * hub_r) - offset * (dx/dist)

    ax.annotate("",
                xy=(sx2, sy2), xytext=(ex2, ey2),
                arrowprops=dict(
                    arrowstyle="->,head_width=0.2,head_length=0.12",
                    color=CYAN, lw=1.3, linestyle="--", alpha=0.7, zorder=4
                ))

# ── Labels on radial arrows ──
label_positions = [
    (cx + 2.8, cy + 2.4, "write\ndecisions", PURPLE),
    (cx - 2.8, cy + 2.4, "write\ndecisions", PURPLE),
    (cx - 3.2, cy - 1.5, "write\ndecisions", PURPLE),
    (cx + 3.2, cy - 1.5, "write\ndecisions", PURPLE),
]
for lx, ly, lt, lc in label_positions:
    ax.text(lx, ly, lt, fontsize=7, color=lc, ha="center", va="center",
            fontfamily="DejaVu Sans", alpha=0.8, zorder=5)

retrieve_positions = [
    (cx + 3.6, cy + 2.6, "retrieve\ncontext", CYAN),
    (cx - 3.6, cy + 2.6, "retrieve\ncontext", CYAN),
    (cx - 3.8, cy - 2.0, "retrieve\ncontext", CYAN),
    (cx + 3.8, cy - 2.0, "retrieve\ncontext", CYAN),
]
for lx, ly, lt, lc in retrieve_positions:
    ax.text(lx, ly, lt, fontsize=7, color=lc, ha="center", va="center",
            fontfamily="DejaVu Sans", alpha=0.8, zorder=5)

# ── Bottom annotation ──
ax.text(8, 0.8, "Each cycle enriches the Notion Decision Log → improving future analysis quality",
        fontsize=11, color=WHITE, ha="center", fontfamily="DejaVu Sans", style="italic")
ax.text(8, 0.35, "Dotted lines = write    Dashed lines = retrieve",
        fontsize=9, color=DIM, ha="center", fontfamily="DejaVu Sans")

# ── "Improves" label on clockwise arrows ──
improve_labels = [
    ((node_positions[0][0] + node_positions[1][0])/2 + 0.5,
     (node_positions[0][1] + node_positions[1][1])/2 + 1.0,
     "prior context\nretrieved →"),
    ((node_positions[1][0] + node_positions[2][0])/2 - 0.5,
     (node_positions[1][1] + node_positions[2][1])/2 - 0.5,
     "grounded\nfindings →"),
    ((node_positions[2][0] + node_positions[3][0])/2 - 1.5,
     (node_positions[2][1] + node_positions[3][1])/2 + 0.0,
     "richer history →"),
    ((node_positions[3][0] + node_positions[0][0])/2 + 1.0,
     (node_positions[3][1] + node_positions[0][1])/2 - 0.5,
     "better\ndecisions →"),
]
for lx, ly, lt in improve_labels:
    ax.text(lx, ly, lt, fontsize=8, color=GOLD, ha="center", va="center",
            fontfamily="DejaVu Sans", fontweight="bold", alpha=0.9, zorder=5,
            path_effects=[pe.withStroke(linewidth=2, foreground=BG)])

plt.tight_layout(pad=0.5)
out = "/home/z/my-project/closed-loop-finance/assets/closed-loop-cycle.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"✅ Saved {out}")

#!/usr/bin/env python3
"""Diagram 2: Agent Pipeline — Single Close Run."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

BG       = "#1a1a2e"
WHITE    = "#e0e0e0"
DIM      = "#8892a0"

fig, ax = plt.subplots(figsize=(20, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)
ax.axis("off")

# ── Title ──
ax.text(10, 9.5, "Agent Pipeline — Single Close Run",
        fontsize=22, fontweight="bold", color=WHITE, ha="center", fontfamily="DejaVu Sans")
ax.text(10, 9.05, "Sequential execution through the LangGraph StateGraph",
        fontsize=12, color=DIM, ha="center", fontfamily="DejaVu Sans")

# ── Step definitions ──
steps = [
    {
        "num": "1", "agent": "Evidence Agent",
        "desc": "Load & parse 9 files",
        "detail": "SHA-256 hash integrity\nPath, kind, rows, bytes\nFileEvidence[] populated",
        "color": "#2ec4b6", "bg": "#0d2f2f",
    },
    {
        "num": "2", "agent": "Analyst Agent",
        "desc": "Pandas + Gemini reasoning",
        "detail": "Summarize each table\nIdentify anomalies\nfacts[], likely_causes[]",
        "color": "#00b4d8", "bg": "#0a1f2e",
    },
    {
        "num": "3", "agent": "Memory Agent (R)",
        "desc": "Retrieve prior context",
        "detail": "Notion API query\nVector similarity search\nPriorDecision[] merged",
        "color": "#c77dff", "bg": "#1a0a2e",
    },
    {
        "num": "4", "agent": "CFO Brief Agent",
        "desc": "Synthesize memo + messages",
        "detail": "Executive memo (.md)\n3 board messages\nproposed_decisions[]",
        "color": "#e2b714", "bg": "#2e1f0a",
    },
    {
        "num": "5", "agent": "Human Gate",
        "desc": "Approve / Reject / Modify",
        "detail": "human_approved: bool\napprover: str\nOptional feedback edits",
        "color": "#ff6b6b", "bg": "#2e0a0a",
    },
    {
        "num": "6", "agent": "Memory Agent (W)",
        "desc": "Persist decisions",
        "detail": "Write to Notion DB\nEmbed & index\nClose the loop ✓",
        "color": "#c77dff", "bg": "#1a0a2e",
    },
]

x_start = 1.0
y_center = 5.0
box_w = 2.5
box_h = 3.2
gap = 0.35

def draw_step(i, step):
    x = x_start + i * (box_w + gap)
    y = y_center - box_h / 2

    # Main box
    b = FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0.25",
                        facecolor=step["bg"], edgecolor=step["color"],
                        linewidth=2, zorder=2)
    ax.add_patch(b)

    # Number circle
    circle = plt.Circle((x + box_w/2, y + box_h - 0.1), 0.3,
                         color=step["color"], zorder=3)
    ax.add_patch(circle)
    ax.text(x + box_w/2, y + box_h - 0.1, step["num"],
            fontsize=14, fontweight="bold", color=BG, ha="center", va="center",
            zorder=4, fontfamily="DejaVu Sans")

    # Agent name
    ax.text(x + box_w/2, y + box_h - 0.65, step["agent"],
            fontsize=11, fontweight="bold", color=step["color"],
            ha="center", va="center", zorder=3, fontfamily="DejaVu Sans")

    # Separator line
    ax.plot([x + 0.2, x + box_w - 0.2], [y + box_h - 0.9, y + box_h - 0.9],
            color=step["color"], lw=0.8, alpha=0.4, zorder=3)

    # Description
    ax.text(x + box_w/2, y + box_h - 1.15, step["desc"],
            fontsize=10, color=WHITE, ha="center", va="center",
            zorder=3, fontfamily="DejaVu Sans", style="italic")

    # Detail lines
    for j, line in enumerate(step["detail"].split("\n")):
        ax.text(x + box_w/2, y + box_h - 1.6 - j * 0.4, line,
                fontsize=8, color=DIM, ha="center", va="center",
                zorder=3, fontfamily="DejaVu Sans")

    # Arrow to next
    if i < len(steps) - 1:
        ax_start = x + box_w
        ax_end = x + box_w + gap
        mid_y = y_center + 0.3
        ax.annotate("", xy=(ax_end, mid_y), xytext=(ax_start, mid_y),
                    arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.15",
                                    color=step["color"], lw=2.0, zorder=4))

# Draw all steps
for i, s in enumerate(steps):
    draw_step(i, s)

# ── Bottom timeline bar ──
bar_y = 1.2
ax.plot([x_start, x_start + 5 * (box_w + gap) + box_w], [bar_y, bar_y],
        color=DIM, lw=1.5, alpha=0.5, zorder=1)
for i in range(len(steps)):
    cx = x_start + i * (box_w + gap) + box_w / 2
    ax.plot(cx, bar_y, "o", color=steps[i]["color"], markersize=8, zorder=3)
    ax.text(cx, bar_y - 0.35, f"Step {i+1}", fontsize=8, color=DIM,
            ha="center", fontfamily="DejaVu Sans")

ax.text(10, 0.4, "Each step reads from and writes to the shared GraphState — passed via LangGraph channels",
        fontsize=10, color=DIM, ha="center", fontfamily="DejaVu Sans", style="italic")

plt.tight_layout(pad=0.5)
out = "/home/z/my-project/closed-loop-finance/assets/agent-flow.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"✅ Saved {out}")

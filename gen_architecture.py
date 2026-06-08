#!/usr/bin/env python3
"""Diagram 1: System Architecture Overview for Closed Loop Finance."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BG       = "#1a1a2e"
BOX      = "#16213e"
BOX_EDGE = "#0f3460"
ACCENT   = "#00b4d8"
WHITE    = "#e0e0e0"
DIM      = "#8892a0"
CYAN     = "#00d4ff"
GOLD     = "#e2b714"
GREEN    = "#2ec4b6"

fig, ax = plt.subplots(figsize=(18, 11))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis("off")

# ── Title ──
ax.text(9, 10.5, "System Architecture", fontsize=22, fontweight="bold",
        color=WHITE, ha="center", va="center", fontfamily="DejaVu Sans")
ax.text(9, 10.1, "Closed Loop Finance — LangGraph Orchestration",
        fontsize=12, color=DIM, ha="center", va="center", fontfamily="DejaVu Sans")

# ── Helper: draw rounded box ──
def box(x, y, w, h, label, sublabel=None, fc=BOX, ec=ACCENT, lw=1.5, fontsize=12, label_color=WHITE, radius=0.3):
    b = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}",
                        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2)
    ax.add_patch(b)
    ty = y + h/2 + (0.18 if sublabel else 0)
    ax.text(x + w/2, ty, label, fontsize=fontsize, fontweight="bold",
            color=label_color, ha="center", va="center", zorder=3, fontfamily="DejaVu Sans")
    if sublabel:
        ax.text(x + w/2, ty - 0.38, sublabel, fontsize=9, color=DIM,
                ha="center", va="center", zorder=3, fontfamily="DejaVu Sans")

# ── Vertex AI (top) ──
box(5.5, 8.6, 7, 1.1, "[CLOUD] Vertex AI", sublabel="Google Cloud AI Platform", fc="#0d1b2a", ec=CYAN, fontsize=14)
# Models inside Vertex
models = [("Gemini 2.5 Pro", ACCENT), ("Gemini 2.5 Flash", GREEN), ("text-embedding-005", GOLD), ("Vector Search", "#ff6b6b")]
for i, (m, c) in enumerate(models):
    mx = 6.2 + i * 1.6
    box(mx, 8.7, 1.4, 0.45, m, fc=BOX, ec=c, lw=1, fontsize=7.5, label_color=c, radius=0.15)

# ── LangGraph StateGraph (center) ──
sg_x, sg_y, sg_w, sg_h = 3.5, 3.5, 11, 4.5
sg = FancyBboxPatch((sg_x, sg_y), sg_w, sg_h,
                     boxstyle="round,pad=0.4", facecolor="#0a0f1e",
                     edgecolor=CYAN, linewidth=2.5, zorder=1)
ax.add_patch(sg)
ax.text(sg_x + sg_w/2, sg_y + sg_h - 0.35, "LangGraph  StateGraph",
        fontsize=15, fontweight="bold", color=CYAN, ha="center", va="center",
        zorder=3, fontfamily="DejaVu Sans")

# ── Nodes inside StateGraph ──
node_w, node_h = 2.0, 0.7
nodes = [
    (4.0, 6.6, "Evidence\nAgent", "#1b4332", GREEN),
    (7.2, 6.6, "Analyst\nAgent", "#1b263b", ACCENT),
    (10.4, 6.6, "Memory\nAgent (R)", "#3c096c", "#c77dff"),
    (4.0, 4.7, "CFO Brief\nAgent", "#7f4f24", GOLD),
    (7.2, 4.7, "Human\nGate", "#3d0000", "#ff6b6b"),
    (10.4, 4.7, "Memory\nAgent (W)", "#3c096c", "#c77dff"),
]
for (nx, ny, nl, nfc, nec) in nodes:
    box(nx, ny, node_w, node_h, nl, fc=nfc, ec=nec, lw=1.5, fontsize=10, label_color=nec)

# Arrows between nodes (inside graph)
arrow_kw = dict(arrowstyle="->,head_width=0.3,head_length=0.2", color=CYAN, lw=1.8, zorder=4)
# Evidence -> Analyst
ax.annotate("", xy=(7.2, 7.0), xytext=(6.0, 7.0), arrowprops=arrow_kw)
# Analyst -> Memory(R)
ax.annotate("", xy=(10.4, 7.0), xytext=(9.2, 7.0), arrowprops=arrow_kw)
# Memory(R) -> CFO Brief  (down and left)
ax.annotate("", xy=(5.0, 5.4), xytext=(11.4, 6.6),
            arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.2", color=CYAN, lw=1.4,
                            connectionstyle="arc3,rad=0.35", zorder=4))
# CFO Brief -> Human Gate
ax.annotate("", xy=(7.2, 5.05), xytext=(6.0, 5.05), arrowprops=arrow_kw)
# Human Gate -> Memory(W)
ax.annotate("", xy=(10.4, 5.05), xytext=(9.2, 5.05), arrowprops=arrow_kw)

# ── Vertex AI arrows to nodes ──
for target_x, target_y in [(8.2, 7.35), (11.4, 7.35)]:
    ax.annotate("", xy=(target_x, target_y), xytext=(target_x, 8.6),
                arrowprops=dict(arrowstyle="->,head_width=0.3", color="#00b4d8", lw=1.5,
                                linestyle="--", zorder=4))

# ── SQLite Checkpointer (bottom of graph) ──
box(5.5, 3.65, 7, 0.6, "[DB] SQLite Checkpointer -- persistent state across runs",
    fc="#1a1a2e", ec=DIM, fontsize=10, label_color=DIM, radius=0.2)
# dashed lines from graph bottom
ax.plot([9, 9], [3.5, 3.5], color=DIM, lw=1, ls="--", zorder=1)

# ── Google Drive (left) ──
box(0.3, 6.2, 2.8, 1.6, "Google Drive",
    sublabel="9 financial spreadsheets\n+ GL / BS / P&L / Cash Flow",
    fc="#0d1b2a", ec=GREEN, fontsize=12, label_color=GREEN)
ax.annotate("", xy=(3.5, 7.0), xytext=(3.1, 7.0),
            arrowprops=dict(arrowstyle="->,head_width=0.35", color=GREEN, lw=2, zorder=4))
ax.text(3.3, 7.3, "load", fontsize=8, color=GREEN, ha="center", zorder=4)

# ── Notion Decision Log (right) ──
box(15.0, 5.2, 2.7, 2.2, "Notion\nDecision Log",
    sublabel="Approved decisions\nPrior context\nEmbeddings index",
    fc="#0d1b2a", ec="#c77dff", fontsize=12, label_color="#c77dff")

# Bidirectional arrows: Memory <-> Notion
ax.annotate("", xy=(12.4, 6.6), xytext=(15.0, 6.2),
            arrowprops=dict(arrowstyle="->,head_width=0.3", color="#c77dff", lw=1.8, zorder=4))
ax.annotate("", xy=(15.0, 6.2), xytext=(12.4, 6.6),
            arrowprops=dict(arrowstyle="->,head_width=0.3", color="#c77dff", lw=1.8,
                            connectionstyle="arc3,rad=0.3", zorder=4))
ax.text(13.7, 6.7, "retrieve", fontsize=8, color="#c77dff", ha="center", zorder=4)
ax.text(13.7, 5.8, "write", fontsize=8, color="#c77dff", ha="center", zorder=4)

# ── Legend ──
legend_items = [
    (GREEN, "Evidence I/O"),
    (ACCENT, "LLM Reasoning"),
    ("#c77dff", "Memory / Notion"),
    (GOLD, "CFO Synthesis"),
    ("#ff6b6b", "Human Gate"),
]
for i, (c, lbl) in enumerate(legend_items):
    lx = 1.0 + i * 3.2
    ly = 0.6
    ax.plot(lx, ly, "s", color=c, markersize=10, zorder=5)
    ax.text(lx + 0.2, ly, lbl, fontsize=9, color=WHITE, va="center", fontfamily="DejaVu Sans")

plt.tight_layout(pad=0.5)
out = "/home/z/my-project/closed-loop-finance/assets/architecture-overview.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"[OK] Saved {out}")

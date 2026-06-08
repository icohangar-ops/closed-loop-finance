#!/usr/bin/env python3
"""Diagram 3: GraphState Schema — TypedDict state flowing between nodes."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG     = "#1a1a2e"
WHITE  = "#e0e0e0"
DIM    = "#8892a0"
CYAN   = "#00b4d8"
GREEN  = "#2ec4b6"
PURPLE = "#c77dff"
GOLD   = "#e2b714"
RED    = "#ff6b6b"

fig, ax = plt.subplots(figsize=(18, 12))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis("off")

# ── Title ──
ax.text(9, 11.5, "GraphState Schema",
        fontsize=22, fontweight="bold", color=WHITE, ha="center", fontfamily="DejaVu Sans")
ax.text(9, 11.05, "TypedDict state passed through every LangGraph node",
        fontsize=12, color=DIM, ha="center", fontfamily="DejaVu Sans")

def field_block(x, y, w, h, title, fields, fc, ec, title_color):
    """Draw a titled box with field list."""
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                        facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=2)
    ax.add_patch(b)
    ax.text(x + 0.2, y + h - 0.25, title, fontsize=12, fontweight="bold",
            color=title_color, va="top", fontfamily="DejaVu Sans", zorder=3)
    # separator
    ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.55, y + h - 0.55],
            color=ec, lw=0.8, alpha=0.4, zorder=3)
    for j, f in enumerate(fields):
        ax.text(x + 0.3, y + h - 0.8 - j * 0.35, f,
                fontsize=8.5, color=WHITE, va="top", fontfamily="DejaVu Sans", zorder=3)

# ── Root: GraphState ──
root_x, root_y, root_w, root_h = 5.5, 9.3, 7, 0.8
b = FancyBboxPatch((root_x, root_y), root_w, root_h, boxstyle="round,pad=0.2",
                    facecolor="#0a1628", edgecolor=CYAN, linewidth=2.5, zorder=2)
ax.add_patch(b)
ax.text(root_x + root_w/2, root_y + root_h/2, "class GraphState(TypedDict)",
        fontsize=14, fontweight="bold", color=CYAN, ha="center", va="center",
        fontfamily="DejaVu Sans", zorder=3)

# ── Layer 1: Input fields (top center) ──
field_block(6.5, 7.8, 5, 1.2, "Input Fields", [
    "period: str          # e.g. '2025-03'",
    "repo_root: str       # project root path",
], "#0d1f2e", CYAN, CYAN)

# Arrow root -> Input
ax.annotate("", xy=(9, 9.3), xytext=(9, 9.0),
            arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.5, zorder=4))

# ── Layer 2: Three output blocks side by side ──

# Evidence
field_block(0.5, 5.2, 4.8, 2.2, "📁 FileEvidence[]", [
    "path: str",
    "sha256: str           # integrity hash",
    "kind: str             # gl|bs|pl|cf|...",
    "rows: int",
    "bytes: int",
], "#0d2f2f", GREEN, GREEN)

# Findings
field_block(6.0, 5.2, 5.5, 2.2, "🔍 Analyst Findings", [
    "facts: list[str]",
    "likely_causes: list[str]",
    "open_questions: list[str]",
    "follow_ups: list[str]",
], "#0a1f2e", CYAN, CYAN)

# Prior Decisions
field_block(12.3, 5.2, 5.2, 2.2, "🧠 PriorDecision[]", [
    "decision_id: str      # Notion page ID",
    "period: str",
    "summary: str",
    "embedding: list[float]",
], "#1a0a2e", PURPLE, PURPLE)

# Arrows from Input down to each
ax.annotate("", xy=(2.9, 7.4), xytext=(7.5, 7.8),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.3, zorder=4))
ax.annotate("", xy=(8.75, 7.4), xytext=(9, 7.8),
            arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.3, zorder=4))
ax.annotate("", xy=(14.9, 7.4), xytext=(10.5, 7.8),
            arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.3, zorder=4))

# ── Layer 3: CFO Brief (center bottom) ──
field_block(3.5, 2.2, 5.5, 2.5, "📄 CFO Brief Output", [
    "memo_path: str              # executive memo .md",
    "audit_note_path: str        # detailed notes",
    "three_messages: list[str]   # board comms",
    "proposed_decisions: list[str]",
    "summary: str",
], "#2e1f0a", GOLD, GOLD)

# Human Gate (right of CFO)
field_block(10.0, 2.2, 4.0, 2.5, "🚦 Human Gate", [
    "human_approved: bool",
    "approver: str",
    "feedback: str | None",
], "#2e0a0a", RED, RED)

# Messages (far right)
field_block(14.8, 2.5, 2.8, 2.0, "💬 Messages", [
    "Annotated[list,\n  add_messages]",
    "# Conversation trace",
], "#0d1f2e", DIM, WHITE)

# Arrows from findings/prior -> CFO
ax.annotate("", xy=(6.25, 4.7), xytext=(6.0, 5.2),
            arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.3, zorder=4))
ax.annotate("", xy=(7.5, 4.7), xytext=(12.3, 5.2),
            arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.3, zorder=4))

# Arrow CFO -> Human Gate
ax.annotate("", xy=(10.0, 3.45), xytext=(9.0, 3.45),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.5, zorder=4))

# Arrow Human Gate -> Messages
ax.annotate("", xy=(14.8, 3.45), xytext=(14.0, 3.45),
            arrowprops=dict(arrowstyle="->", color=DIM, lw=1.0, zorder=4))

# ── Labels on arrows ──
ax.text(1.5, 8.8, "Evidence\nAgent", fontsize=8, color=GREEN, ha="center", fontfamily="DejaVu Sans")
ax.text(9, 8.6, "Analyst\nAgent", fontsize=8, color=CYAN, ha="center", fontfamily="DejaVu Sans")
ax.text(16, 8.8, "Memory\nAgent (R)", fontsize=8, color=PURPLE, ha="center", fontfamily="DejaVu Sans")
ax.text(7.0, 4.9, "CFO Brief\nAgent", fontsize=8, color=GOLD, ha="center", fontfamily="DejaVu Sans")
ax.text(10.0, 4.9, "Human\nGate", fontsize=8, color=RED, ha="center", fontfamily="DejaVu Sans")

plt.tight_layout(pad=0.5)
out = "/home/z/my-project/closed-loop-finance/assets/state-schema.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"✅ Saved {out}")

#!/usr/bin/env python3
"""Generate the animated profile-README header SVG in light and dark variants."""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent / "assets"

W, H = 880, 190

THEMES = {
    "light": dict(name="#0f172a", sub="#475569", muted="#94a3b8",
                  accent="#2563eb", accent2="#0ea5e9", wave="#2563eb",
                  node="#2563eb", edge="#cbd5e1", rule="#e2e8f0"),
    "dark": dict(name="#e6edf3", sub="#9198a1", muted="#6e7681",
                 accent="#58a6ff", accent2="#39d0d8", wave="#58a6ff",
                 node="#58a6ff", edge="#30363d", rule="#21262d"),
}

# Waveform bars — speech/prosody motif, matches the speechgauge work.
BAR_N, BAR_W, BAR_GAP = 26, 5, 6
BAR_X0 = W - 40 - (BAR_N * BAR_W + (BAR_N - 1) * BAR_GAP)
BAR_CY = 96

# Deterministic pseudo-random heights so the shape is stable across regens.
def bar_height(i):
    v = abs(math.sin(i * 1.9) * 0.6 + math.sin(i * 0.7) * 0.4)
    return 10 + v * 52


# Small graph motif behind the text — the graph-RAG nod.
NODES = [(56, 158), (104, 172), (150, 152), (196, 168), (240, 156)]
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 2)]


def build(theme_name):
    c = THEMES[theme_name]
    p = []
    a = p.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" role="img" aria-label="Batın Örene — PhD researcher in AI">')

    a('<defs>')
    a(f'<linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0%" stop-color="{c["accent"]}"/>'
      f'<stop offset="100%" stop-color="{c["accent2"]}"/></linearGradient>')
    a('</defs>')

    a('<style>')
    a('  .f { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", '
      'Helvetica, Arial, sans-serif; }')
    # Slow, low-amplitude motion. Nothing blinks.
    a('  .bar { transform-box: fill-box; transform-origin: center; '
      'animation: pulse 2.8s ease-in-out infinite; }')
    a('  @keyframes pulse { 0%,100% { transform: scaleY(0.45); } '
      '50% { transform: scaleY(1); } }')
    a('  .node { animation: glow 4s ease-in-out infinite; }')
    a('  @keyframes glow { 0%,100% { opacity: 0.35; r: 3; } '
      '50% { opacity: 1; r: 4.2; } }')
    a('  .rule { animation: sweep 6s ease-in-out infinite; }')
    a('  @keyframes sweep { 0% { width: 0; opacity: 0; } '
      '18% { opacity: 1; } 70% { width: 176px; opacity: 1; } '
      '100% { width: 176px; opacity: 0.55; } }')
    a('  @media (prefers-reduced-motion: reduce) { '
      '.bar, .node, .rule { animation: none; } .rule { width: 176px; } }')
    a('</style>')

    # Left accent spine.
    a(f'<rect x="0" y="28" width="4" height="{H-56}" rx="2" fill="url(#accentGrad)"/>')

    # Graph motif (behind/below the text block).
    for i, j in EDGES:
        x1, y1 = NODES[i]
        x2, y2 = NODES[j]
        a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
          f'stroke="{c["edge"]}" stroke-width="1.25"/>')
    for k, (x, y) in enumerate(NODES):
        a(f'<circle class="node" cx="{x}" cy="{y}" r="3.4" fill="{c["node"]}" '
          f'style="animation-delay:{k * 0.5:.1f}s"/>')

    # Text block.
    a(f'<text class="f" x="34" y="74" font-size="42" font-weight="700" '
      f'fill="{c["name"]}" letter-spacing="-0.8">Batın Örene</text>')
    # width attribute is the resting state, so a static render still shows it.
    a(f'<rect class="rule" x="36" y="88" width="176" height="2.5" rx="1.25" '
      f'fill="url(#accentGrad)"/>')
    a(f'<text class="f" x="35" y="115" font-size="16.5" font-weight="500" '
      f'fill="{c["sub"]}">PhD researcher in AI · applied LLM, RAG and speech systems</text>')
    a(f'<text class="f" x="35" y="136" font-size="13" '
      f'fill="{c["muted"]}">agentic RAG · LLM evaluation · hallucination detection · '
      f'responsible AI</text>')

    # Waveform.
    for i in range(BAR_N):
        h = bar_height(i)
        x = BAR_X0 + i * (BAR_W + BAR_GAP)
        y = BAR_CY - h / 2
        op = 0.30 + 0.55 * (i / (BAR_N - 1))
        a(f'<rect class="bar" x="{x:.1f}" y="{y:.1f}" width="{BAR_W}" '
          f'height="{h:.1f}" rx="{BAR_W/2:.1f}" fill="{c["wave"]}" '
          f'opacity="{op:.2f}" style="animation-delay:{i * 0.09:.2f}s"/>')

    a('</svg>')
    return "\n".join(p) + "\n"


OUT.mkdir(parents=True, exist_ok=True)
for name in THEMES:
    path = OUT / f"header-{name}.svg"
    path.write_text(build(name), encoding="utf-8")
    print(f"wrote {path} ({path.stat().st_size} bytes)")

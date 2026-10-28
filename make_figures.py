"""Figures for 'Designing Population Health Studies' (POPH 001).
One visual language across all schematics; print-safe (labels carry meaning, not colour).
Column figures are ~620 units wide so text stays legible at half-slide width.
Writes imgs/src/*.svg and imgs/*.png (2x)."""
import os
import random
import cairosvg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgs")
SRC = os.path.join(OUT, "src")
os.makedirs(SRC, exist_ok=True)

FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
INK = "#1F2937"
GREY = "#6B7280"
TEAL = "#008080"
TEAL_BG = "#E6F2F2"
EXP_LINE, EXP_FILL = "#7F1D1D", "#F6E7E7"      # exposed
UNX_LINE, UNX_FILL = "#1F6F8B", "#E3EFF4"      # unexposed
DIS = "#374151"                                 # disease (dark) vs no disease (white)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=16, weight=400, fill=INK, anchor="middle", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def box(x, y, w, h, lines, fill="#FFFFFF", stroke=INK, sw=2, color=INK, rx=10):
    """lines: list of (string, size, weight[, style]), centred vertically"""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
           f'stroke="{stroke}" stroke-width="{sw}"/>']
    gap = 6
    total = sum(l[1] for l in lines) + gap * (len(lines) - 1)
    cy = y + (h - total) / 2
    for l in lines:
        s, size, weight = l[0], l[1], l[2]
        style = l[3] if len(l) > 3 else "normal"
        cy += size
        out.append(text(x + w / 2, cy - size * 0.18, s, size, weight, color, "middle", style))
        cy += gap
    return "\n".join(out)


def line(x1, y1, x2, y2, color=INK, sw=2, head=None, dash=None):
    m = f' marker-end="url(#ah-{head})"' if head else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}"{m}{d}/>')


def path(d, color=INK, sw=2, head=None):
    m = f' marker-end="url(#ah-{head})"' if head else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{m}/>'


def markers():
    out = ["<defs>"]
    for name, col in [("teal", TEAL), ("ink", INK), ("grey", GREY)]:
        out.append(f'<marker id="ah-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                   f'markerWidth="6" markerHeight="6" orient="auto">'
                   f'<path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    out.append("</defs>")
    return "\n".join(out)


def time_axis(y, x1=10, x2=610):
    return line(x1, y, x2, y, GREY, 2, "grey") + "\n" + text(x2, y - 10, "Time", 15, 600, GREY, "end")


def start_marker(x, y, lines):
    """teal triangle under the axis: where the investigator starts"""
    out = [f'<path d="M{x},{y + 4} l-8,14 h16 z" fill="{TEAL}"/>']
    for i, s in enumerate(lines):
        out.append(text(x, y + 38 + i * 19, s, 15, 600 if i == 0 else 400,
                        TEAL if i == 0 else GREY))
    return "\n".join(out)


def save(name, w, h, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" font-family="{FONT}">\n'
           f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>\n{markers()}\n{body}\n</svg>\n')
    with open(os.path.join(SRC, name + ".svg"), "w") as f:
        f.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, name + ".png"),
                     output_width=w * 2, output_height=h * 2)


def exposed(x, y, w, h, sub=None, size=17, title="Exposed (E₁)"):
    l = [(title, size, 700)] + ([(sub, 14, 400, "italic")] if sub else [])
    return box(x, y, w, h, l, EXP_FILL, EXP_LINE)


def unexposed(x, y, w, h, sub=None, size=17, title="Unexposed (E₀)"):
    l = [(title, size, 700)] + ([(sub, 14, 400, "italic")] if sub else [])
    return box(x, y, w, h, l, UNX_FILL, UNX_LINE)


def disease(x, y, w, h, s, size=15):
    return box(x, y, w, h, [(s, size, 700)], DIS, DIS, color="#FFFFFF")


def no_disease(x, y, w, h, s, size=15):
    return box(x, y, w, h, [(s, size, 600)], "#FFFFFF", DIS)


# 1. decision tree (full slide width) -------------------------------------------
def fig_tree():
    q = dict(fill="#FFFFFF", stroke=TEAL, sw=2)
    cat = dict(fill=TEAL, stroke=TEAL, color="#FFFFFF")
    leaf = dict(fill="#FFFFFF", stroke=INK, sw=2.5)
    other = dict(fill="#F3F4F6", stroke="#9CA3AF", sw=1.5, color=GREY)
    b = []
    b.append(box(20, 215, 215, 90, [("Did the investigator", 16, 600),
                                    ("assign the exposure?", 16, 600)], **q))
    b.append(box(300, 95, 180, 50, [("Experimental", 18, 700)], **cat))
    b.append(box(300, 375, 180, 50, [("Observational", 18, 700)], **cat))
    b.append(path("M235,260 H265 V120 H298", TEAL, 2, "teal"))
    b.append(path("M265,260 V400 H298", TEAL, 2, "teal"))
    b.append(text(272, 185, "Yes", 15, 700, TEAL, "start"))
    b.append(text(272, 345, "No", 15, 700, TEAL, "start"))
    b.append(box(525, 95, 165, 50, [("Random allocation?", 15, 600)], **q))
    b.append(line(480, 120, 523, 120, TEAL, 2, "teal"))
    b.append(box(740, 40, 200, 58, [("Randomized controlled", 15, 700),
                                    ("trial (RCT)", 15, 700)], **leaf))
    b.append(box(740, 145, 200, 50, [("Non-randomized trial", 15, 500)], **other))
    b.append(path("M690,120 H715 V69 H738", TEAL, 2, "teal"))
    b.append(path("M715,120 V170 H738", TEAL, 2, "teal"))
    b.append(text(709, 92, "Yes", 13, 700, TEAL, "end"))
    b.append(text(709, 155, "No", 13, 700, TEAL, "end"))
    b.append(box(525, 375, 165, 50, [("Comparison group?", 15, 600)], **q))
    b.append(line(480, 400, 523, 400, TEAL, 2, "teal"))
    b.append(box(740, 248, 200, 50, [("Descriptive study", 15, 600),
                                     ("e.g., case series", 13, 400, "italic")], **other))
    b.append(path("M607,375 V273 H738", TEAL, 2, "teal"))
    b.append(text(615, 330, "No", 13, 700, TEAL, "start"))
    for y, t, s in [(312, "Cohort", "exposure → outcome"),
                    (374, "Case-control", "outcome → exposure"),
                    (436, "Cross-sectional", "both at the same time")]:
        b.append(box(740, y, 200, 50, [(t, 16, 700), (s, 13, 400, "italic")], **leaf))
    b.append(path("M690,400 H715 V337 H738", TEAL, 2, "teal"))
    b.append(path("M715,400 H738", TEAL, 2, "teal"))
    b.append(path("M715,400 V461 H738", TEAL, 2, "teal"))
    b.append(text(700, 448, "Yes", 13, 700, TEAL, "end"))
    b.append(text(700, 466, "(analytical)", 11, 400, TEAL, "end"))
    save("design-tree", 960, 500, "\n".join(b))


# 2. cross-sectional ------------------------------------------------------------
def fig_cross_sectional():
    b = []
    b.append(box(190, 8, 240, 50, [("Population", 18, 700)], "#F3F4F6", "#9CA3AF", sw=1.5))
    b.append(line(310, 58, 310, 98, INK, 2, "ink"))
    b.append(text(322, 84, "representative sample", 15, 400, GREY, "start", "italic"))
    b.append(f'<rect x="10" y="104" width="600" height="300" rx="14" fill="{TEAL_BG}"/>')
    b.append(text(30, 134, "One point in time: a snapshot", 17, 700, TEAL, "start"))
    cx, cy = [225, 400], [190, 285]
    b.append(text(305, 178, "Disease (D₁)", 16, 700))
    b.append(text(480, 178, "No disease (D₀)", 16, 700))
    b.append(text(213, 237, "Exposed (E₁)", 16, 700, EXP_LINE, "end"))
    b.append(text(213, 332, "Unexposed (E₀)", 16, 700, UNX_LINE, "end"))
    for r, (fill, st) in enumerate([(EXP_FILL, EXP_LINE), (UNX_FILL, UNX_LINE)]):
        for c in range(2):
            b.append(box(cx[c], cy[r], 160, 80, [("abcd"[r * 2 + c], 28, 600, "italic")], fill, st))
    b.append(text(310, 392, "E and D are measured at the same time", 15, 400, GREY, "middle", "italic"))
    b.append(time_axis(440))
    b.append(start_marker(312, 440, ["Study takes place"]))
    save("design-cross-sectional", 620, 495, "\n".join(b))


# 3. case-control ---------------------------------------------------------------
def fig_case_control():
    b = []
    b.append(text(110, 28, "Past exposure", 16, 700, GREY))
    b.append(text(510, 28, "Chosen now, by disease", 16, 700, GREY))
    b.append(box(410, 45, 200, 118, [("Cases", 22, 700), ("have the disease (D₁)", 14, 400, "italic")],
                 DIS, DIS, color="#FFFFFF"))
    b.append(box(410, 225, 200, 118, [("Controls", 22, 700), ("do not (D₀)", 14, 400, "italic")],
                 "#FFFFFF", DIS))
    for top in (45, 225):
        b.append(exposed(10, top, 200, 50, size=16))
        b.append(unexposed(10, top + 68, 200, 50, size=16))
    for y0, ys in [(104, (70, 138)), (284, (250, 318))]:
        for y in ys:
            b.append(line(408, y0, 213, y, TEAL, 2.5, "teal"))
    b.append(text(310, 188, "Look back: were", 15, 700, TEAL, "middle", "italic"))
    b.append(text(310, 207, "they exposed?", 15, 700, TEAL, "middle", "italic"))
    b.append(time_axis(390))
    b.append(start_marker(510, 390, ["Study starts here", "with cases and controls"]))
    save("design-case-control", 620, 460, "\n".join(b))


# 4. cohort ---------------------------------------------------------------------
def fig_cohort():
    b = []
    b.append(text(120, 28, "At baseline", 16, 700, GREY))
    b.append(text(500, 28, "Follow-up", 16, 700, GREY))
    b.append(exposed(10, 60, 220, 90, "free of disease at start"))
    b.append(unexposed(10, 230, 220, 90, "free of disease at start"))
    for top, src_y in [(45, 105), (215, 275)]:
        b.append(disease(390, top, 220, 46, "Develop disease (D₁)"))
        b.append(no_disease(390, top + 58, 220, 46, "Remain free (D₀)"))
        for y in (top + 23, top + 81):
            b.append(line(232, src_y, 387, y, TEAL, 2.5, "teal"))
    b.append(text(310, 196, "Follow both groups forward", 15, 700, TEAL, "middle", "italic"))
    b.append(time_axis(375))
    b.append(line(120, 367, 120, 383, GREY, 2))
    b.append(line(500, 367, 500, 383, GREY, 2))
    b.append(start_marker(120, 375, ["Prospective cohort", "starts here, follows forward"]))
    b.append(start_marker(500, 375, ["Retrospective cohort", "starts here, uses records"]))
    save("design-cohort", 620, 450, "\n".join(b))


# 5. RCT ------------------------------------------------------------------------
def fig_rct():
    b = []
    b.append(box(10, 165, 120, 80, [("Eligible", 16, 700), ("participants", 16, 700)],
                 "#F3F4F6", "#9CA3AF", sw=1.5))
    b.append(line(130, 205, 147, 205, INK, 2, "ink"))
    b.append(f'<circle cx="180" cy="205" r="30" fill="{TEAL}"/>')
    b.append(text(180, 215, "R", 28, 700, "#FFFFFF"))
    b.append(text(180, 258, "Random", 14, 700, TEAL))
    b.append(text(180, 276, "allocation", 14, 700, TEAL))
    b.append(exposed(245, 60, 185, 90, "e.g., a new program", title="Intervention (E₁)"))
    b.append(unexposed(245, 260, 185, 90, "placebo or usual care", title="Control (E₀)"))
    b.append(line(203, 185, 243, 117, TEAL, 2.5, "teal"))
    b.append(line(203, 225, 243, 293, TEAL, 2.5, "teal"))
    for top, src_y in [(55, 105), (255, 305)]:
        b.append(disease(470, top, 140, 42, "Outcome (D₁)", 14))
        b.append(no_disease(470, top + 53, 140, 42, "No outcome (D₀)", 14))
        for y in (top + 21, top + 74):
            b.append(line(432, src_y, 467, y, TEAL, 2.5, "teal"))
    b.append(time_axis(400))
    b.append(start_marker(180, 400, ["Study starts here", "investigator assigns exposure"]))
    save("design-rct", 620, 470, "\n".join(b))


# 6. reliability vs validity ----------------------------------------------------
def fig_targets():
    rnd = random.Random(7)
    panels = [
        (140, 100, (32, -28), 22, "Low reliability, low validity", "scattered and off-center"),
        (420, 100, (0, 0), 25, "Low reliability", "centered on average, but scattered"),
        (140, 360, (34, -28), 6, "High reliability, low validity", "consistently off target: bias"),
        (420, 360, (0, 0), 6, "High reliability, high validity", "consistent and on target"),
    ]
    b = []
    for cx, cy, (mx, my), sd, t1, t2 in panels:
        for i, r in enumerate([85, 68, 51, 34]):
            fill = "#F3F4F6" if i % 2 == 0 else "#FFFFFF"
            b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="#9CA3AF" stroke-width="1.5"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="{TEAL}"/>')
        for _ in range(14):
            x, y = cx + mx + rnd.gauss(0, sd), cy + my + rnd.gauss(0, sd)
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{INK}" stroke="#FFFFFF" stroke-width="1"/>')
        b.append(text(cx, cy + 112, t1, 17, 700))
        b.append(text(cx, cy + 133, t2, 14, 400, GREY, "middle", "italic"))
    save("reliability-validity", 560, 505, "\n".join(b))


# 7. confounding ----------------------------------------------------------------
def fig_confounding():
    b = []
    b.append(box(205, 10, 210, 70, [("Smoking", 19, 700), ("confounder", 14, 400, "italic")],
                 TEAL_BG, TEAL))
    b.append(box(10, 210, 200, 70, [("Coffee drinking", 18, 700), ("exposure", 14, 400, "italic")],
                 EXP_FILL, EXP_LINE))
    b.append(box(410, 210, 200, 70, [("Lung cancer", 18, 700), ("outcome", 14, 400, "italic")],
                 "#FFFFFF", DIS))
    b.append(line(260, 82, 130, 206, INK, 2.5, "ink"))
    b.append(line(360, 82, 490, 206, INK, 2.5, "ink"))
    b.append(line(212, 245, 406, 245, GREY, 2.5, "grey", "8 6"))
    b.append(text(309, 233, "apparent association", 14, 400, GREY, "middle", "italic"))
    b.append(text(150, 130, "smokers drink", 14, 400, GREY, "end", "italic"))
    b.append(text(150, 148, "more coffee", 14, 400, GREY, "end", "italic"))
    b.append(text(470, 130, "smoking causes", 14, 400, GREY, "start", "italic"))
    b.append(text(470, 148, "lung cancer", 14, 400, GREY, "start", "italic"))
    save("confounding", 620, 290, "\n".join(b))


if __name__ == "__main__":
    for f in (fig_tree, fig_cross_sectional, fig_case_control, fig_cohort,
              fig_rct, fig_targets, fig_confounding):
        f()
    print("done:", sorted(os.listdir(OUT)))

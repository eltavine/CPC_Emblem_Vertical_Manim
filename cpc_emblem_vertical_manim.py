from manim import *
import numpy as np
from math import sqrt, atan2, pi

# ============================================================
# 9:16 vertical output
# ============================================================
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = WHITE

# Official standard colors:
# yellow RGB (253, 207, 48), red RGB (237, 44, 37)
OFFICIAL_YELLOW = ManimColor("#FDCF30")
OFFICIAL_RED = ManimColor("#ED2C25")

GRID_COLOR = ManimColor("#D7DCE2")
GUIDE_COLOR = ManimColor("#5B84B1")
EDGE_COLOR = ManimColor("#2F4858")
POINT_COLOR = ManimColor("#D1495B")
ACCENT = ManimColor("#E07A22")
TEXT_COLOR = ManimColor("#17212B")
SUBTEXT_COLOR = ManimColor("#5E6872")

# macOS normally provides this font.
# If unavailable, replace with another Chinese font.
CJK_FONT = "PingFang SC"

GRID_SIDE = 7.20
SCALE = GRID_SIDE / 32.0
DRAW_CENTER_Y = 2.45

SQ177 = sqrt(177)
SQ623 = sqrt(623)
SQ1105 = sqrt(1105)
SQ2129 = sqrt(2129)

# ============================================================
# Official 1..33 construction-grid coordinates
# x increases rightward, y increases downward.
# ============================================================
PTS = {
    "A": (1.0, 1.0),
    "B": (1.0, 33.0),
    "C": (33.0, 33.0),
    "D": (33.0, 1.0),

    "E": (29.0, 33.0),
    "F": (33.0, 29.0),

    "G": (8.5, 18.5),
    "H": (19.5, 7.5),
    "I": (4.0, 14.0),
    "J": (17.0, 5.0),
    "K": (13.5, 1.0),
    "L": ((61.0 - SQ177) / 4.0, (11.0 + SQ177) / 4.0),

    "M": (17.0, 17.0),
    "N": (17.0, 1.0),
    "O": (17.0, 33.0),

    "P": (17.0, 15.0),
    "Q": ((29.0 - SQ623) / 2.0, (25.0 + SQ623) / 2.0),

    "R": (11.0, 16.5),
    "S": (11.0 + SQ1105 / 2.0, 16.5),

    "T": (16.5, 16.5),
    "U": (16.5, 11.0 + SQ1105 / 2.0),

    "V": (16.5, 11.0),
    "W": (4.5, 22.5),

    "X": (3.5, 30.5),
    "Y": (6.0, 30.0),
    "Z": (4.0, 28.0),
}

# Hammer-handle intersections with GH.
HA = (11.5, 15.5)
HB = (15.5, 11.5)

# Sickle-handle bridge:
# upper side x+y=32, lower side x+y=36.
HANDLE_A = (1.0 + sqrt(8.75), 31.0 - sqrt(8.75))
HANDLE_B = ((75.0 - SQ2129) / 4.0, 32.0 - (75.0 - SQ2129) / 4.0)
HANDLE_C = (19.0 - sqrt(158.0), 17.0 + sqrt(158.0))
HANDLE_D = (4.5 + sqrt(2.125), 31.5 - sqrt(2.125))


def sp(xy):
    """Official grid coordinate -> Manim scene coordinate."""
    x, y = xy
    return np.array([
        (x - 17.0) * SCALE,
        DRAW_CENTER_Y + (17.0 - y) * SCALE,
        0.0,
    ])


def distance(a, b):
    ax, ay = a
    bx, by = b
    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def angle_screen(center, point):
    """Angle measured in the official y-down coordinate system."""
    cx, cy = center
    px, py = point
    return atan2(py - cy, px - cx)


def arc_points(center, start, end, increasing=True, samples=96):
    """
    Sample one official circular arc.

    `increasing` refers to angle in the original y-down construction grid.
    The y-axis is flipped only when mapped to the Manim scene.
    """
    radius = distance(center, start)
    a0 = angle_screen(center, start)
    a1 = angle_screen(center, end)

    if increasing:
        while a1 <= a0:
            a1 += 2 * pi
    else:
        while a1 >= a0:
            a1 -= 2 * pi

    ts = np.linspace(a0, a1, samples)
    cx, cy = center
    return [
        sp((cx + radius * np.cos(t), cy + radius * np.sin(t)))
        for t in ts
    ]


def sampled_arc(center, start, end, increasing=True, color=ACCENT, width=5):
    """Visible construction arc."""
    vm = VMobject()
    vm.set_points_as_corners(
        arc_points(center, start, end, increasing=increasing, samples=120)
    )
    vm.set_stroke(color=color, width=width)
    vm.set_fill(opacity=0)
    return vm


def filled_polygon(points, color=OFFICIAL_YELLOW):
    return Polygon(
        *points,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1.0,
    )


def guide_circle(center_name, through_name, opacity=0.44):
    center = PTS[center_name]
    radius = distance(center, PTS[through_name]) * SCALE
    return Circle(
        radius=radius,
        color=GUIDE_COLOR,
        stroke_width=2.0,
        stroke_opacity=opacity,
    ).move_to(sp(center))


def point_mark(name, direction=UP):
    dot = Dot(sp(PTS[name]), radius=0.045, color=POINT_COLOR)
    label = Text(
        name,
        font=CJK_FONT,
        font_size=20,
        color=TEXT_COLOR,
    ).next_to(dot, direction, buff=0.055)
    return VGroup(dot, label)


# ============================================================
# Final filled emblem
# ============================================================
def make_hammer(color=OFFICIAL_YELLOW):
    # Hammer head: I-G-H-J + circular arc J-L + L-I.
    head_pts = [
        sp(PTS["I"]),
        sp(PTS["G"]),
        sp(PTS["H"]),
        sp(PTS["J"]),
    ]
    head_pts += arc_points(
        PTS["K"], PTS["J"], PTS["L"],
        increasing=True, samples=110
    )[1:]
    head_pts.append(sp(PTS["I"]))

    head = filled_polygon(head_pts, color)

    # Hammer handle: two AC-parallel side lines.
    handle = filled_polygon(
        [sp(HA), sp(HB), sp(PTS["F"]), sp(PTS["E"])],
        color,
    )

    return VGroup(handle, head)


def make_sickle_blade(color=OFFICIAL_YELLOW):
    """
    Closed sickle-blade boundary:
    N -> O -> Q -> W -> U -> S -> N
    using five official circular arcs plus QW.
    """
    pts = []

    # N -> O, center M
    pts += arc_points(
        PTS["M"], PTS["N"], PTS["O"],
        increasing=True, samples=180
    )

    # O -> Q, center P
    pts += arc_points(
        PTS["P"], PTS["O"], PTS["Q"],
        increasing=True, samples=100
    )[1:]

    # Q -> W
    pts.append(sp(PTS["W"]))

    # W -> U, center V
    pts += arc_points(
        PTS["V"], PTS["W"], PTS["U"],
        increasing=False, samples=90
    )[1:]

    # U -> S, center T
    pts += arc_points(
        PTS["T"], PTS["U"], PTS["S"],
        increasing=False, samples=90
    )[1:]

    # S -> N, center R
    pts += arc_points(
        PTS["R"], PTS["S"], PTS["N"],
        increasing=False, samples=100
    )[1:]

    return filled_polygon(pts, color)


def make_sickle_handle(color=OFFICIAL_YELLOW):
    # Circle X, tangent to AB and BC: radius = 2.5 grid units.
    knob = Circle(
        radius=2.5 * SCALE,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1.0,
    ).move_to(sp(PTS["X"]))

    # Bridge between the X-circle and the sickle body.
    bridge = filled_polygon(
        [
            sp(HANDLE_A),
            sp(HANDLE_B),
            sp(HANDLE_C),
            sp(HANDLE_D),
        ],
        color,
    )

    return VGroup(bridge, knob)


def make_emblem(color=OFFICIAL_YELLOW):
    # Same fill + no strokes make overlaps visually merge.
    return VGroup(
        make_hammer(color),
        make_sickle_blade(color),
        make_sickle_handle(color),
    )


# ============================================================
# Bottom caption: every string is asserted <= 40 characters.
# ============================================================
CAPTION_FONT_SIZE = 44
CAPTION_MAX_WIDTH = 8.7
# The area below the construction runs from roughly y=-1.15 to the
# bottom edge of the 9:16 frame (y=-8).  Keep captions centered in that
# full lower area instead of placing them inside a separate panel.
CAPTION_CENTER = np.array([0.0, -4.58, 0.0])


class CaptionController:
    def __init__(self, scene):
        self.scene = scene
        self.current = None

    def show(self, text):
        assert len(text) <= 40, (
            f"Caption exceeds 40 chars: {len(text)} -> {text}"
        )

        target = Text(
            text,
            font=CJK_FONT,
            font_size=CAPTION_FONT_SIZE,
            color=TEXT_COLOR,
            weight="MEDIUM",
        )

        if target.width > CAPTION_MAX_WIDTH:
            target.scale_to_fit_width(CAPTION_MAX_WIDTH)

        target.move_to(CAPTION_CENTER)

        if self.current is None:
            self.scene.play(
                FadeIn(target, shift=UP * 0.10),
                run_time=0.35,
            )
            self.current = target
        else:
            self.scene.play(
                Transform(self.current, target),
                run_time=0.32,
            )


# ============================================================
# Main 9:16 construction animation
# ============================================================
class CPCEmblemConstruction(Scene):
    def construct(self):
        title = Text(
            "中国共产党党徽",
            font=CJK_FONT,
            font_size=42,
            color=TEXT_COLOR,
            weight="BOLD",
        ).move_to(UP * 7.32)

        source = Text(
            "依据《党徽党旗条例》附件1制法说明",
            font=CJK_FONT,
            font_size=24,
            color=SUBTEXT_COLOR,
        ).next_to(title, DOWN, buff=0.16)

        self.add(title, source)
        cc = CaptionController(self)

        # ----------------------------------------------------
        # Step 01: 32x32 grid and diagonals
        # ----------------------------------------------------
        cc.show("步骤01｜作32×32方格，并连AC、BD两条对角线。")

        grid_lines = []
        for i in range(33):
            x = 1 + i
            y = 1 + i
            grid_lines.append(
                Line(
                    sp((x, 1)), sp((x, 33)),
                    color=GRID_COLOR, stroke_width=1
                )
            )
            grid_lines.append(
                Line(
                    sp((1, y)), sp((33, y)),
                    color=GRID_COLOR, stroke_width=1
                )
            )

        border = Square(
            side_length=GRID_SIDE,
            color=EDGE_COLOR,
            stroke_width=2.4,
        ).move_to(np.array([0, DRAW_CENTER_Y, 0]))

        diag_ac = Line(
            sp(PTS["A"]), sp(PTS["C"]),
            color=GUIDE_COLOR, stroke_width=2.2
        )
        diag_bd = Line(
            sp(PTS["B"]), sp(PTS["D"]),
            color=GUIDE_COLOR, stroke_width=2.2
        )

        ticks = VGroup()
        for value in [1, 9, 17, 25, 33]:
            tx = Text(
                str(value),
                font=CJK_FONT,
                font_size=18,
                color=SUBTEXT_COLOR,
            ).next_to(sp((value, 1)), UP, buff=0.04)
            ticks.add(tx)

            ty = Text(
                str(value),
                font=CJK_FONT,
                font_size=18,
                color=SUBTEXT_COLOR,
            ).next_to(sp((1, value)), LEFT, buff=0.04)
            ticks.add(ty)

        self.play(
            LaggedStart(
                *[Create(line) for line in grid_lines],
                lag_ratio=0.006,
            ),
            Create(border),
            run_time=2.2,
        )
        self.play(
            Create(diag_ac),
            Create(diag_bd),
            FadeIn(ticks),
            run_time=0.8,
        )

        # ----------------------------------------------------
        # Step 02: hammer handle
        # ----------------------------------------------------
        cc.show("步骤02｜取E、F，过两点作AC平行线形成锤把。")

        ef = Line(
            sp(PTS["E"]), sp(PTS["F"]),
            color=EDGE_COLOR, stroke_width=4
        )
        hline1 = Line(
            sp(HA), sp(PTS["E"]),
            color=ACCENT, stroke_width=4
        )
        hline2 = Line(
            sp(HB), sp(PTS["F"]),
            color=ACCENT, stroke_width=4
        )
        marks_ef = VGroup(
            point_mark("E", DOWN),
            point_mark("F", RIGHT),
        )

        self.play(
            FadeIn(marks_ef),
            Create(ef),
            Create(hline1),
            Create(hline2),
            run_time=1.4,
        )

        # ----------------------------------------------------
        # Step 03: hammer-head straight edges
        # ----------------------------------------------------
        cc.show("步骤03｜取G、H、I、J，按平行关系画出锤头直边。")

        gh = Line(
            sp(PTS["G"]), sp(PTS["H"]),
            color=EDGE_COLOR, stroke_width=4
        )
        ig = Line(
            sp(PTS["I"]), sp(PTS["G"]),
            color=ACCENT, stroke_width=4
        )
        hj = Line(
            sp(PTS["H"]), sp(PTS["J"]),
            color=ACCENT, stroke_width=4
        )

        # Through I, parallel to BD: x+y=18.
        i_guide = Line(
            sp((1, 17)),
            sp((17, 1)),
            color=GUIDE_COLOR,
            stroke_width=2.2,
        )

        marks_ghij = VGroup(
            point_mark("G", DOWN + LEFT),
            point_mark("H", UP + RIGHT),
            point_mark("I", LEFT),
            point_mark("J", UP),
        )

        self.play(
            FadeIn(marks_ghij),
            Create(gh),
            Create(ig),
            Create(hj),
            Create(i_guide),
            run_time=1.5,
        )

        # ----------------------------------------------------
        # Step 04: K circle and J-L arc
        # ----------------------------------------------------
        cc.show("步骤04｜以K为圆心、KJ为半径，作弧交I线于L。")

        k_circle = guide_circle("K", "J")
        jl_arc = sampled_arc(
            PTS["K"], PTS["J"], PTS["L"],
            increasing=True
        )
        marks_kl = VGroup(
            point_mark("K", UP),
            point_mark("L", LEFT),
        )

        self.play(
            FadeIn(marks_kl),
            Create(k_circle),
            run_time=0.8,
        )
        self.play(Create(jl_arc), run_time=1.0)

        # ----------------------------------------------------
        # Step 05: close and fill hammer
        # ----------------------------------------------------
        cc.show("步骤05｜连接L-I，锤头闭合；锤头与锤把合成。")

        li = Line(
            sp(PTS["L"]), sp(PTS["I"]),
            color=EDGE_COLOR, stroke_width=4
        )
        hammer_fill = make_hammer(
            OFFICIAL_YELLOW
        ).set_opacity(0.92)

        self.play(Create(li), run_time=0.45)
        self.play(FadeIn(hammer_fill), run_time=0.85)

        # ----------------------------------------------------
        # Step 06: sickle outer arc N-O
        # ----------------------------------------------------
        cc.show("步骤06｜以M为圆心、MN为半径，作外圆弧N-O。")

        m_circle = guide_circle("M", "N")
        no_arc = sampled_arc(
            PTS["M"], PTS["N"], PTS["O"],
            increasing=True
        )
        marks_mno = VGroup(
            point_mark("M", DOWN),
            point_mark("N", UP),
            point_mark("O", DOWN),
        )

        self.play(
            FadeIn(marks_mno),
            Create(m_circle),
            run_time=0.8,
        )
        self.play(Create(no_arc), run_time=1.25)

        # ----------------------------------------------------
        # Step 07: lower outer arc O-Q
        # ----------------------------------------------------
        cc.show("步骤07｜以P为圆心、PO为半径，作弧O-Q。")

        p_circle = guide_circle("P", "O")
        oq_arc = sampled_arc(
            PTS["P"], PTS["O"], PTS["Q"],
            increasing=True
        )
        marks_pq = VGroup(
            point_mark("P", LEFT),
            point_mark("Q", LEFT),
        )

        self.play(
            FadeIn(marks_pq),
            Create(p_circle),
            run_time=0.75,
        )
        self.play(Create(oq_arc), run_time=0.9)

        # ----------------------------------------------------
        # Step 08: inner arc N-S
        # ----------------------------------------------------
        cc.show("步骤08｜以R为圆心、RN为半径，作内弧N-S。")

        r_circle = guide_circle("R", "N")
        ns_arc = sampled_arc(
            PTS["R"], PTS["N"], PTS["S"],
            increasing=True
        )
        r_horizontal = Line(
            sp((1, PTS["R"][1])),
            sp((33, PTS["R"][1])),
            color=GUIDE_COLOR,
            stroke_width=1.8,
        )
        marks_rs = VGroup(
            point_mark("R", DOWN),
            point_mark("S", RIGHT),
        )

        self.play(
            FadeIn(marks_rs),
            Create(r_horizontal),
            Create(r_circle),
            run_time=0.9,
        )
        self.play(Create(ns_arc), run_time=0.85)

        # ----------------------------------------------------
        # Step 09: inner quarter arc S-U
        # ----------------------------------------------------
        cc.show("步骤09｜以T为圆心、TS为半径，作四分之一弧S-U。")

        t_circle = guide_circle("T", "S")
        su_arc = sampled_arc(
            PTS["T"], PTS["S"], PTS["U"],
            increasing=True
        )
        t_vertical = Line(
            sp((PTS["T"][0], 1)),
            sp((PTS["T"][0], 33)),
            color=GUIDE_COLOR,
            stroke_width=1.8,
        )
        marks_tu = VGroup(
            point_mark("T", DOWN + LEFT),
            point_mark("U", DOWN),
        )

        self.play(
            FadeIn(marks_tu),
            Create(t_vertical),
            Create(t_circle),
            run_time=0.85,
        )
        self.play(Create(su_arc), run_time=0.75)

        # ----------------------------------------------------
        # Step 10: inner arc U-W
        # ----------------------------------------------------
        cc.show("步骤10｜以V为圆心、VU为半径，作弧U-W。")

        v_circle = guide_circle("V", "U")
        uw_arc = sampled_arc(
            PTS["V"], PTS["U"], PTS["W"],
            increasing=True
        )
        marks_vw = VGroup(
            point_mark("V", LEFT),
            point_mark("W", LEFT),
        )

        self.play(
            FadeIn(marks_vw),
            Create(v_circle),
            run_time=0.8,
        )
        self.play(Create(uw_arc), run_time=0.85)

        # ----------------------------------------------------
        # Step 11: Q-W closes sickle blade
        # ----------------------------------------------------
        cc.show("步骤11｜连接Q-W，镰刀刀体的封闭轮廓完成。")

        qw = Line(
            sp(PTS["Q"]), sp(PTS["W"]),
            color=EDGE_COLOR,
            stroke_width=4,
        )
        sickle_blade_fill = make_sickle_blade(
            OFFICIAL_YELLOW
        ).set_opacity(0.92)

        self.play(Create(qw), run_time=0.45)
        self.play(
            FadeIn(sickle_blade_fill),
            run_time=0.8,
        )

        # ----------------------------------------------------
        # Step 12: sickle handle
        # ----------------------------------------------------
        cc.show("步骤12｜以X作切圆；过Y、Z作BD平行线成镰刀把。")

        x_circle_guide = Circle(
            radius=2.5 * SCALE,
            color=GUIDE_COLOR,
            stroke_width=2.2,
        ).move_to(sp(PTS["X"]))

        # x+y=32 and x+y=36
        yz_upper = Line(
            sp((1, 31)),
            sp((31, 1)),
            color=ACCENT,
            stroke_width=3.2,
        )
        yz_lower = Line(
            sp((3, 33)),
            sp((33, 3)),
            color=ACCENT,
            stroke_width=3.2,
        )

        marks_xyz = VGroup(
            point_mark("X", DOWN),
            point_mark("Y", RIGHT),
            point_mark("Z", LEFT),
        )

        sickle_handle_fill = make_sickle_handle(
            OFFICIAL_YELLOW
        ).set_opacity(0.92)

        self.play(
            FadeIn(marks_xyz),
            Create(x_circle_guide),
            Create(yz_upper),
            Create(yz_lower),
            run_time=1.1,
        )
        self.play(
            FadeIn(sickle_handle_fill),
            run_time=0.7,
        )

        # ----------------------------------------------------
        # Step 13: remove guides, reveal clean color emblem
        # ----------------------------------------------------
        cc.show("步骤13｜淡出辅助线，按标准黄色填充完整党徽。")

        final_emblem = make_emblem(OFFICIAL_YELLOW)

        construction = VGroup(
            *grid_lines,
            border,
            diag_ac,
            diag_bd,
            ticks,

            ef,
            hline1,
            hline2,
            gh,
            ig,
            hj,
            i_guide,
            k_circle,
            jl_arc,
            li,

            marks_ef,
            marks_ghij,
            marks_kl,

            m_circle,
            no_arc,
            marks_mno,

            p_circle,
            oq_arc,
            marks_pq,

            r_circle,
            r_horizontal,
            ns_arc,
            marks_rs,

            t_circle,
            t_vertical,
            su_arc,
            marks_tu,

            v_circle,
            uw_arc,
            marks_vw,

            qw,

            x_circle_guide,
            yz_upper,
            yz_lower,
            marks_xyz,

            hammer_fill,
            sickle_blade_fill,
            sickle_handle_fill,
        )

        self.play(
            FadeOut(construction),
            FadeIn(final_emblem),
            run_time=1.3,
        )

        final_label = Text(
            "标准黄色 RGB 253 · 207 · 48",
            font=CJK_FONT,
            font_size=25,
            color=SUBTEXT_COLOR,
        ).move_to(DOWN * 2.35)

        self.play(
            FadeIn(final_label, shift=UP * 0.10),
            run_time=0.4,
        )
        self.wait(2.5)


# ============================================================
# Clean final image scene
# Render it with `-s` to export a PNG.
# ============================================================
class CPCEmblemStill(Scene):
    def construct(self):
        emblem = make_emblem(OFFICIAL_YELLOW)
        emblem.scale(1.04)
        emblem.move_to(ORIGIN)
        self.add(emblem)

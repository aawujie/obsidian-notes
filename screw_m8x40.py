from build123d import *
from math import cos, radians, pi


def gen_step():
    """M8 x 40mm hex head screw with ISO metric coarse thread."""

    # --- M8 screw parameters ---
    major_d = 8.0
    pitch = 1.25
    shaft_len = 40.0

    # Thread geometry (ISO metric 60 deg)
    H = pitch * cos(radians(30))  # fundamental triangle height ~1.083
    groove_depth = 5 * H / 8       # working thread depth ~0.677
    groove_top_w = 7 * pitch / 8   # groove opening at crest ~1.094
    groove_bot_w = pitch / 4       # groove flat at root ~0.3125

    # Hex head (standard M8)
    waf = 13.0          # width across flats
    head_h = 5.3        # head height

    shaft_r = major_d / 2

    with BuildPart() as screw:
        # 1. Shaft blank at major diameter
        Cylinder(
            radius=shaft_r,
            height=shaft_len,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

        # 2. Hex head on top of shaft (do before thread to keep clean geometry)
        with BuildSketch(Plane.XY.offset(shaft_len)) as head_sk:
            hex_radius = waf / cos(radians(30))
            RegularPolygon(radius=hex_radius, side_count=6)
        extrude(amount=head_h)

        # 3. Chamfer top edge of hex head
        top_face = screw.faces().sort_by(Axis.Z)[-1]
        chamfer(top_face.edges(), length=0.6)

        # 4. Cut helical thread groove
        helix_h = shaft_len + pitch
        helix = Helix(
            pitch=pitch,
            height=helix_h,
            radius=shaft_r,
            center=(0, 0, -pitch / 2),
        )

        profile_plane = Plane(
            origin=(shaft_r, 0, -pitch / 2),
            x_dir=(1, 0, 0),
            z_dir=(0, 0, 1),
        )

        hw_top = groove_top_w / 2
        hw_bot = groove_bot_w / 2

        with BuildSketch(profile_plane) as groove_sk:
            with BuildLine() as outline:
                Polyline(
                    (-hw_top, 0),
                    (hw_top, 0),
                    (hw_bot, -groove_depth),
                    (-hw_bot, -groove_depth),
                    close=True,
                )
            make_face()

        sweep(path=helix, mode=Mode.SUBTRACT)

    screw.label = "screw_m8x40"
    return screw.part
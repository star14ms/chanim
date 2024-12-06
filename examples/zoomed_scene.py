# manim -p example/zoomed_scene.py AlkaneMeltingAndBoilingPointGraph
from manim import *
import math

from rich import print


# Source:
    # https://docs.manim.community/en/stable/examples.html#movingzoomedscenearound
    # https://docs.manim.community/en/stable/examples.html#heatdiagramplot
class AlkaneMeltingAndBoilingPointGraph(ZoomedScene):
    boiling_points = [
        -161.5, -88.6, -42.1, -0.5, 36.1, 68.7, 98.4, 125.6, 150.5, 174.1, 
        195.9, 216.3, 235.4, 253.6, 270.6, 286.9, 303, 316, 330, 344.1, 
        359, 369, 381, 391, 401.9, 415, 428.1, 432, 441, 451
    ]
    melting_points = [
        -182.6, -183, -187.6, -138.3, -129.7, -95.4, -90.5, -56.7, -53.5, -29.7, 
        -25.5, -9.6, -5.4, 5.9, 10.0, 18.2, 22.0, 28.2, 31.5, 36.5, 
        40.4, 43.8, 47.4, 50.3, 53.3, 56.1, 58.8, 61.3, 63.7, 65.9
    ]
    boiling_points = [int(x) for x in boiling_points]
    melting_points = [int(x) for x in melting_points]
    # flash_points = [
    #     -188, -135, -104, -60, -40, -22, -4, 13, 31, 46, 
    #     62, 83, 94, 100, '?', 135, 149, 166, 100, 113, 
    #     113, 113, 113, 113, 120, '?', '?', '?', '?', '?',
    # ]

    # Data Source:
    # Haynes, W.M. (ed.) CRC Handbook of Chemistry and Physics. 91st ed. Boca Raton, FL: CRC Press Inc., 2010-2011
    # Haynes, W.M. (ed.). CRC Handbook of Chemistry and Physics. 95th Edition. CRC Press LLC, Boca Raton: FL 2014-2015
    # Larranaga, M.D., Lewis, R.J. Sr., Lewis, R.A.; Hawley's Condensed Chemical Dictionary 16th Edition. John Wiley & Sons, Inc. Hoboken, NJ 2016., p. 704
    def __init__(self, max_n_carbons=30, axes_scale=0.33, zoomed_frame_pad=0.15, **kwargs):
        self.max_n_carbons = max_n_carbons
        self.axes_scale = axes_scale
        self.zoomed_frame_pad = zoomed_frame_pad
        self.dots = VGroup()
        ax = self.create_axes()

        ZoomedScene.__init__(
            self,
            zoom_factor=0.15,
            zoomed_display_height=ax.height * 3*self.axes_scale,
            zoomed_display_width=ax.width * 3*self.axes_scale,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        # ax, labels = self.create_and_draw_axes()
        ax, labels = self.create_axes_and_labels(corner=DL)
        self.play(LaggedStart(Write(ax),  Write(labels), run_time=3, lag_ratio=0.5))
        x0 = 1
        n_carbons = list(range(28, self.max_n_carbons+1))

        # graph_bp = ax.plot_line_graph(x_values=n_carbons, y_values=self.boiling_points, vertex_dot_radius=0.08*self.axes_scale, line_color=RED)
        # graph_mp = ax.plot_line_graph(x_values=n_carbons, y_values=self.melting_points, vertex_dot_radius=0.08*self.axes_scale, line_color=BLUE)
        # self.add(ax, labels, graph_bp, graph_mp)
        # return

        t, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next = self.add_dynamic_graph(self, ax, x0, n_carbons)
        frame, _, _ = self.highlight_graph(self, ax, n_carbons, label_bp_next, label_mp_next, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp)
        frame_offset = ax.get_corner(DL) - frame.get_corner(DL)

        for n_carbon in n_carbons[1:]:
            label_bp_prev = label_bp_next
            label_mp_prev = label_mp_next

            label_bp_next, label_mp_next, dot_bp, dot_mp, scale_factor, vector_to_shift = \
                self.build_next_graph_objects(ax, frame, n_carbon, frame_offset, h_line_bp, h_line_mp
            )
            animatons = self.build_animation_next_graph(
                t, frame, n_carbon, vector_to_shift, scale_factor, 
                label_bp_prev, label_bp_next, label_mp_prev, label_mp_next, dot_bp, dot_mp
            )
            self.play(*animatons[0], run_time=0.3)
            self.play(*animatons[1], run_time=0.3)
            self.play(*animatons[2], run_time=0.3)

    def create_axes(self):
        return Axes(
            x_range=[0, 30, 5],
            y_range=[-200, 500, 100],
            x_length=9,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 30, 5), "font_size": 64, 'label_direction': UP},
            # y_axis_config={"numbers_to_include": np.arange(-200, 500, 100)},
            tips=False,
        )

    def create_axes_and_labels(self, corner=ORIGIN, shift=0):
        ax = self.create_axes()
        ax.scale(self.axes_scale).to_corner(corner).shift(shift)
        labels = ax.get_axis_labels(
            x_label=Tex("N Carbon", font_size=max(32, 48*self.axes_scale)), y_label=Tex("Temperature ($^\circ C$)", font_size=max(32, 48*self.axes_scale))
        )
        return ax, labels

    def add_dynamic_graph(self, self_scene, ax: Axes, x0, n_carbons):
        t = ValueTracker(x0)

        graph_bp = always_redraw(lambda: ax.plot(
            lambda x: self.func_boiling_points(x-1e-4), x_range=[x0, t.get_value()], color=RED
        ))
        graph_mp = always_redraw(lambda: ax.plot(
            lambda x: self.func_melting_points(x-1e-4), x_range=[x0, t.get_value()], color=BLUE
        ))
        h_line_bp = always_redraw(lambda: get_horizontal_line_to_graph(
            axes=ax, function=graph_bp, x=t.get_value(), width=4, color=RED, dot_radius=0.08*self.axes_scale
        ))
        h_line_mp = always_redraw(lambda: get_horizontal_line_to_graph(
            axes=ax, function=graph_mp, x=t.get_value(), width=4, color=BLUE, dot_radius=0.08*self.axes_scale
        ))
        dot_bp_moving = Dot(point=ax.coords_to_point(n_carbons[0], self.boiling_points[0]), radius=0.08*self.axes_scale, color=RED)
        dot_bp_moving.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), self.func_boiling_points(t.get_value()-1e-4))))
        dot_mp_moving = Dot(point=ax.coords_to_point(n_carbons[0], self.melting_points[0]), radius=0.08*self.axes_scale, color=BLUE)
        dot_mp_moving.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), self.func_melting_points(t.get_value()-1e-4))))

        label_bp_next = Text(str(self.boiling_points[0]), font_size=48*self.axes_scale).next_to(h_line_bp, LEFT, buff=0.1).shift([0, 0.12, 0]) # Prevent Overlapping
        label_mp_next = Text(str(self.melting_points[0]), font_size=48*self.axes_scale).next_to(h_line_mp, LEFT, buff=0.1)

        self_scene.add(graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next)

        return t, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next

    def highlight_graph(self, self_scene, ax, n_carbons, label_bp_next, label_mp_next, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp):
        label_bp_temp = Text('Boiling Point', font_size=48*self.axes_scale, color=RED).next_to(h_line_bp, LEFT, buff=0.1).shift([0, 0.12, 0])
        label_mp_temp = Text('Melting Point', font_size=48*self.axes_scale, color=BLUE).next_to(h_line_mp, LEFT, buff=0.1)

        frame, zoomed_display_frame, zd_rect = self.use_zoomed_camera(self_scene, ax, label_bp_temp)

        self_scene.play(FadeTransform(label_bp_next, label_bp_temp))
        self_scene.play(Indicate(label_bp_temp), Flash(dot_bp_moving))
        self_scene.play(FadeTransform(label_mp_next, label_mp_temp))
        self_scene.play(Indicate(label_mp_temp), Flash(dot_mp_moving))
        self_scene.play(FadeTransform(label_mp_temp, label_mp_next), FadeTransform(label_bp_temp, label_bp_next))

        point_middle_of_dots = (dot_bp_moving.get_center() + dot_mp_moving.get_center()) / 2
        self_scene.play(frame.animate.scale(5/6*0.66).move_to(point_middle_of_dots + [-0.2, 0.1, 0])) 

        dot_bp = Dot(point=ax.coords_to_point(n_carbons[0], self.boiling_points[0]), radius=0.08*self.axes_scale)
        dot_mp = Dot(point=ax.coords_to_point(n_carbons[0], self.melting_points[0]), radius=0.08*self.axes_scale)
        self.dots.add(dot_bp, dot_mp)
        self_scene.play(FadeIn(dot_bp, dot_mp), zoomed_display_frame.animate.set_color(PURPLE), run_time=0.3)

        return frame, zoomed_display_frame, zd_rect
 
    def use_zoomed_camera(self, self_scene, ax: Axes, label_bp_temp):
        zoomed_camera = self_scene.zoomed_camera
        zoomed_display = self_scene.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.scale(6/5).move_to(label_bp_temp.get_center())
        zoomed_display.scale(0.3).move_to(ax)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self_scene.add_foreground_mobject(zd_rect)

        # unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        self_scene.play(Create(frame))
        self_scene.activate_zooming()
        self_scene.play(self_scene.get_zoomed_display_pop_out_animation(), frame.animate.set_opacity(0)) # , unfold_camera

        return frame, zoomed_display_frame, zd_rect

    def build_next_graph_objects(self, ax: Axes, frame, n_carbon, frame_offset, h_line_bp, h_line_mp): 
        point_next_bp = ax.c2p(n_carbon, self.boiling_points[n_carbon-1])
        point_next_mp = ax.c2p(n_carbon, self.melting_points[n_carbon-1])
        label_bp_next = Text(str(self.boiling_points[n_carbon-1]), font_size=48*self.axes_scale).next_to(h_line_bp, LEFT, buff=0.1).shift([0, point_next_bp[1]-h_line_bp.get_center()[1], 0])
        label_mp_next = Text(str(self.melting_points[n_carbon-1]), font_size=48*self.axes_scale).next_to(h_line_mp, LEFT, buff=0.1).shift([0, point_next_mp[1]-h_line_mp.get_center()[1], 0])

        dot_bp = Dot(point=ax.coords_to_point(n_carbon, self.boiling_points[n_carbon-1]), radius=0.08*self.axes_scale)
        dot_mp = Dot(point=ax.coords_to_point(n_carbon, self.melting_points[n_carbon-1]), radius=0.08*self.axes_scale)

        scale_factor = 1
        if frame.get_corner(UR)[1] - point_next_bp[1] < self.zoomed_frame_pad:
            scale_factor = (point_next_bp[1] - frame.get_bottom()[1] + self.zoomed_frame_pad) / (frame.get_top()[1] - frame.get_bottom()[1])
        if frame.get_corner(DR)[0] - point_next_bp[0] < self.zoomed_frame_pad:
            scale_factor = max(scale_factor, (point_next_bp[0] - frame.get_left()[0] + self.zoomed_frame_pad) / (frame.get_right()[0] - frame.get_left()[0]))
        print('scale_factor: %.2f' % scale_factor)
        frame.scale(scale_factor)
        vector_to_shift = ax.get_corner(DL) - frame.get_corner(DL) - frame_offset 
        frame.scale(1/scale_factor)

        return label_bp_next, label_mp_next, dot_bp, dot_mp, scale_factor, vector_to_shift

    def build_animation_next_graph(self, t, frame, n_carbon, vector_to_shift, scale_factor, label_bp_prev, label_bp_next, label_mp_prev, label_mp_next, dot_bp, dot_mp):
        bp_increased = float(label_bp_prev.original_text) < float(label_bp_next.original_text)
        mp_increased = float(label_mp_prev.original_text) < float(label_mp_next.original_text)
        label_bp_next.set_color(GREEN if bp_increased else RED)
        label_mp_next.set_color(GREEN if mp_increased else RED)

        return [
            [
                FadeToColor(label_bp_prev, GREEN if bp_increased else RED),
                FadeToColor(label_mp_prev, GREEN if mp_increased else RED),
            ],
            [
                t.animate.set_value(n_carbon), 
                frame.animate.shift(vector_to_shift).scale(scale_factor),
                FadeTransform(label_bp_prev, label_bp_next),
                FadeTransform(label_mp_prev, label_mp_next),
            ], 
            [
                FadeIn(dot_bp, dot_mp),
                FadeToColor(VGroup(label_bp_next, label_mp_next), WHITE),
            ],
        ]

    def func_boiling_points(self, x):
        x_prev = math.floor(x)
        y_prev = self.boiling_points[x_prev-1]
        y_next = self.boiling_points[x_prev]

        return calculate_y(x_prev, y_prev, x_prev+1, y_next, x)

    def func_melting_points(self, x):
        x_prev = math.floor(x)
        y_prev = self.melting_points[x_prev-1]
        y_next = self.melting_points[x_prev]

        return calculate_y(x_prev, y_prev, x_prev+1, y_next, x)


def calculate_y(x1, y1, x2, y2, x):
    if x1 == x2:
        raise ValueError("The two x-coordinates must be different to define a line.")
    
    # Calculate the slope (m)
    slope = (y2 - y1) / (x2 - x1)
    
    # Calculate the y-intercept (b)
    intercept = y1 - slope * x1
    
    # Calculate the y value for the given x
    y = slope * x + intercept
    return y


# Source: https://github.com/brianamedee/Manim-Tutorials-2021/blob/main/5Tutorial_Adv2D.py
def get_horizontal_line_to_graph(axes, function, x, width, color, dot_radius=DEFAULT_DOT_RADIUS):
    result = VGroup()
    line = DashedLine(
        start=axes.c2p(0, function.underlying_function(x)),
        end=axes.c2p(x, function.underlying_function(x)),
        stroke_width=width,
        stroke_color=color,
    )
    dot = Dot(radius=dot_radius).set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
    result.add(line, dot)
    return result


# Source: https://docs.manim.community/en/stable/examples.html#movingzoomedscenearound
class MovingZoomedSceneAround(ZoomedScene):
# contributed by TheoremofBeethoven, www.youtube.com/c/TheoremofBeethoven
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        dot = Dot().shift(UL * 2)
        image = ImageMobject(np.uint8([[0, 100, 30, 200],
                                       [255, 0, 5, 33]]))
        image.height = 7
        frame_text = Text("Frame", color=PURPLE, font_size=67)
        zoomed_camera_text = Text("Zoomed camera", color=RED, font_size=67)

        self.add(image, dot)
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        frame_text.next_to(frame, DOWN)

        self.play(Create(frame), FadeIn(frame_text, shift=UP))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        zoomed_camera_text.next_to(zoomed_display_frame, DOWN)
        self.play(FadeIn(zoomed_camera_text, shift=UP))
        # Scale in        x   y  z
        scale_factor = [0.5, 1.5, 0]
        self.play(
            frame.animate.scale(scale_factor),
            zoomed_display.animate.scale(scale_factor),
            FadeOut(zoomed_camera_text),
            FadeOut(frame_text)
        )
        self.wait()
        self.play(ScaleInPlace(zoomed_display, 2))
        self.wait()
        self.play(frame.animate.shift(2.5 * DOWN))
        self.wait()
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        self.wait()

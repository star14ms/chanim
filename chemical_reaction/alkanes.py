# Main Command: manim -p chemical_reaction/alkanes.py
import sys, os
sys.path.append(os.path.abspath('.'))

from rich import print
from time import perf_counter
from chanim_manim import *

from base import ReactionScene
from template import TransformMatchingLocation, TransformMatchingElementTex
from examples.zoomed_scene import AlkaneMeltingAndBoilingPointGraph


class PictureTransforms(Scene):
    images = [
        'C1_methane gas.png',
        'C1to4_plastic manufacturing.jpg',
        'C3_propane stove.jpg',
        'C1to4_cooking1.jpeg', # C4
        'C5_blowing agent.jpg',
        'C6_cooking oil making',
        'C5to8_petrol.jpeg',
        'C5to8_gasoline.webp', # C8
        'C9to12_jet fuel.jpeg',
        'C9to12_kerosene1.jpeg',
        'C9to12_kerosene2.jpeg',
        'C12_DALL·E 2024-11-22 20.40.23 - A whimsical illustration featuring a pair of cockroaches at the center, embracing or showing affection towards one another, surrounded by a pair of mo.webp', # C12
        'C13_Abelmoschus-esculentus.jpg',
        'C14_phase change material.jpg',
        'C13to16_diesel1.png',
        'C16_black walnuts.jpg', # C16
        'C17to20_bicycle chain oils.jpg',
        'C17to20_lubricating oils1.jpeg',
        'C17to20_lubricating oils2.jpeg',
        'C21to30_paraffin wax1.jpg', # C20
        'C21_pheromone.jpg',
        'C22,24_magnolia.jpg',
        'C23_biosensor.jpg',
        'C22,24_vanilla madagascariensis', # C24
        'C21to30_paraffin wax2.webp',
        'C26_DALL·E 2024-11-20 23.52.06 - A still life illustration featuring a peach (복숭아), a sunflower (해바라기), a parsnip (파스닙), a coconut (코코넛), and a papaya (파파야). The composition should sh.webp',
        'C27_Euphorbia piscatoria.jpeg',
        'C28_Andrachne rotundifolia.jpg', # C28
        'C29_ginkgo nuts.jpg',
        'C30_German-vs-Roman-Chamomile.jpg', # C30
        'C31to70_heavy fuel oil.jpeg', # C40
        'C31to70_shipping.jpg',
        'C31to70_factory.jpg',
        'C70+_bitumen.jpg', # C70
        'C70+_Asphalt vs. Bitumen vs. Tar.png',
        'C70+_road construction.jpg',
        'C70+_asphalts.jpg',
    ]
    dir_images = 'media/source/alkanes'
    image_max_width = 12/3
    image_max_height = 8/3
    
    def __init__(self, **kwargs):
        assert self.images != [], 'images should be set in subclass'
        super().__init__(**kwargs)

    def construct(self):
        image_next = self.build_next_image(self.images[0])
        self.play(FadeIn(image_next), run_time=1.0)

        for picture in self.images[1:]:
            image_prev = image_next
            image_next = self.build_next_image(picture)
            anim_transform_imgs = self.build_animation_next_image(image_prev, image_next)

            self.play(*anim_transform_imgs, run_time=1.0)
            self.wait(duration=1.0)
            
    def build_next_image(self, picture, edge=DOWN, shift=RIGHT * 4):
        image = ImageMobject(self.dir_images + '/' + picture)
        image.set(height=self.image_max_height).to_edge(edge).shift(shift)
        if image.get_width() > self.image_max_width:
            image.set(width=self.image_max_width)

        return image

    def build_animation_next_image(self, image_prev: ImageMobject, image_next: ImageMobject, image_path: str | None):
        if image_prev is None or (image_next is not None and image_prev.pixel_array.shape == image_next.pixel_array.shape and (image_prev.pixel_array == image_next.pixel_array).all()):
            return []
        elif image_path is None:
            return [FadeOut(image_prev)]
        else:
            return [FadeTransform(image_prev, image_next)]


class SequentialReactionScene(ReactionScene, AlkaneMeltingAndBoilingPointGraph, PictureTransforms):
    molecules = [] # should be set in subclass
    number_of_C_list = [] # should be set in subclass
    chemcode_initial = None # should be set in subclass
    substrings_to_isolate = []
    chemfig_params = {'angle increment': 15}
    key_map_for_line_diagram = {}
    key_maps = {}
    n_carbon_to_remove_zoom_camera = 21
    n_carbon_to_keep_graph_until = 30
    CONFIG = {
        'match_same_key': False,
        'draw_graph': False,
    }

    def __init__(self, **kwargs):
        assert self.molecules != [], 'molecules should be set in subclass'
        assert self.number_of_C_list != [], 'number_of_C_list should be set in subclass'
        assert self.chemcode_initial is not None, 'chemcode_initial should be set in subclass'
        
        if len(self.images) == 0:
            self.images = [None] * len(self.molecules)

        super().__init__(**kwargs)

    def construct(self, self_scene=None, title_next=None, chem_next=None, numbering_next=None, chemcode=None, image_next=None):
        if self_scene is None:
            self_scene = self

        chemcode, title_next, chem_next, numbering_next, image_next, ax, graph_components_main, frame_offset, graph_components, labels, image_path_prev = self.initiate_scene(self_scene, title_next, chem_next, numbering_next, chemcode, image_next)
        t, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next = graph_components
        frame, zoomed_display_frame, zd_rect = graph_components_main
        
        if chemcode == self.chemcode_initial:
            zipped_iterables = zip(self.molecules[1:], self.number_of_C_list[1:], self.images[1:])
        else:
            zipped_iterables = zip(self.molecules, self.number_of_C_list, self.images)

        for i, (molecule, n_carbon, image_path) in enumerate(zipped_iterables):
            title_prev = title_next
            chem_prev = chem_next
            numbering_prev = numbering_next
            title_next, chem_next, numbering_next, chemcode = self.build_next_objects(molecule, n_carbon, chemcode, i)
            print(n_carbon, chemcode)

            image_prev = image_next
            if image_path is None:
                image_next = None
            elif image_path != image_path_prev:
                image_next = self.build_next_image(image_path, shift=RIGHT * 4.8 if self.__class__.__name__ == 'CycloAlkanes' and n_carbon >= 6 else RIGHT * 4 if n_carbon <= self.n_carbon_to_keep_graph_until else 0)
                image_path_prev = image_path

            anims_transform_img = self.build_animation_next_image(image_prev, image_next, image_path)

            speed_factor = self.get_new_speed_factor(molecule, n_carbon)

            if self.CONFIG['draw_graph']:
                label_bp_prev = label_bp_next
                label_mp_prev = label_mp_next

                if n_carbon <= self.n_carbon_to_keep_graph_until:
                    label_bp_next, label_mp_next, dot_bp, dot_mp, scale_factor, vector_to_shift = \
                        self.build_next_graph_objects(ax, frame, n_carbon, frame_offset, h_line_bp, h_line_mp
                    )
                    graph_animations = self.build_animation_next_graph(
                        t, frame, n_carbon, vector_to_shift, scale_factor, 
                        label_bp_prev, label_bp_next, label_mp_prev, label_mp_next, dot_bp, dot_mp
                    )
                elif n_carbon == 40:
                    group_to_ignore = VGroup(ax, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next, labels, self.dots)
                    self_scene.play(group_to_ignore.animate.set_opacity(0), run_time=1.0 * speed_factor)
                    self_scene.remove(group_to_ignore)
                    graph_animations = [[], [], []]
                else:
                    graph_animations = [[], [], []]
            else:
                graph_animations = [[], [], []]

            self.apply_next_objects(self_scene, title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, graph_animations, n_carbon, frame, zoomed_display_frame, anims_transform_img, speed_factor=speed_factor)
            
            if self.CONFIG['draw_graph']:
                self.dots.add(dot_bp, dot_mp)
            
            if n_carbon == 10 and self.__class__.__name__ == 'Alkanes':
                group_to_ignore = VGroup(ax, h_line_bp, h_line_mp, label_bp_next, label_mp_next, labels, self.dots)
                chem_next, numbering_next, image_next = self.transform_to_line_diagram_and_back(self_scene, chem_next, numbering_next, group_to_ignore, zd_rect, zoomed_display_frame, image_next)

        return title_next, chem_next, numbering_next, chemcode, image_next

    def initiate_scene(self, self_scene, title_next=None, chem_next=None, numbering_next=None, chemcode=None, image_next=None):
        if title_next is None:
            chemcode = self.chemcode_initial
            print(f'number of C: {self.number_of_C_list[0]}')
            title_next = VMobject()
            for n, title_line in enumerate(self.molecules[0].split('\n')):
                title_next.add(ChemObject(title_line, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate))
            title_next.arrange(DOWN).to_edge(UP)
            title_next.name = self.molecules[0].split('\n')[0]
            chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
            numbering_next = self.carbon_numbering(chem_next)

            self_scene.play(Write(title_next), Create(chem_next), run_time=1.0)
            self_scene.play(Write(numbering_next), run_time=0.5)
            self_scene.play(FadeToColor(numbering_next, WHITE), run_time=0.5)
            self_scene.wait(duration=0.5)
            animations = [VGroup(chem_next, numbering_next).animate.shift(UP * 0.5)]
            
            if self.images[0] is None:
                image_next = None
            else:
                image_next = self.build_next_image(self.images[0])
                animations.append(FadeIn(image_next))
        else:
            animations = []

        if self.CONFIG['draw_graph']:
            ax, labels = self.create_axes_and_labels(corner=DL, shift=RIGHT * 0.5)
            animations.extend([Write(ax), Write(labels)])
        else:
            ax, labels = None, None

        if len(animations) > 0:
            self_scene.play(LaggedStart(*animations, run_time=3 if len(animations) > 1 else 1, lag_ratio=0.5))

        x0 = 1
        n_carbons = list(range(x0, self.max_n_carbons))
        
        if self.CONFIG['draw_graph']:
            graph_components = self.add_dynamic_graph(self_scene, ax, x0, n_carbons)
            t, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next = graph_components
            graph_components_main = self.highlight_graph(self_scene, ax, n_carbons, label_bp_next, label_mp_next, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp)
            frame, zoomed_display_frame, zd_rect = graph_components_main
            frame_offset = ax.get_corner(DL) - frame.get_corner(DL)
        else:
            graph_components = None, None, None, None, None, None, None, None, None
            graph_components_main = None, None, None
            frame_offset = None

        image_path_prev = None

        return chemcode, title_next, chem_next, numbering_next, image_next, ax, graph_components_main, frame_offset, graph_components, labels, image_path_prev

    def build_next_objects(self, molecule, n_carbon, chemcode, i):
        chemcode = self.build_next_chemcode(molecule, n_carbon, chemcode, i)
        title_next = VMobject()
        for n, title_line in enumerate(molecule.split('\n')):
            title_next.add(ChemObject(title_line, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate))
        title_next.arrange(DOWN).to_edge(UP)
        title_next.name = molecule.split('\n')[0]
        
        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
        if chem_next.height > 3.0:
            chem_next.next_to(title_next, DOWN)
        else:
            chem_next.shift(UP * 0.5)

        numbering_next = self.carbon_numbering(chem_next, n_prev_carbon=self.number_of_C_list[i])

        return title_next, chem_next, numbering_next, chemcode

    def apply_next_objects(self, self_scene, title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, graph_animations, n_carbon, frame, zoomed_display_frame, anims_transform_img, speed_factor=1.0):
        animations1 = []
        for n in range(max(len(title_prev), len(title_next))):
            title_prev_line = title_prev[n] if len(title_prev) > n else ChemObject(title_prev[n-1].tex_string, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
            title_next_line = title_next[n] if len(title_next) > n else ChemObject('', font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate)
            animations1.append(TransformMatchingElementTex(title_prev_line, title_next_line))
            
        numbering_prev_parts = numbering_prev.submobjects
        numbering_next_parts = numbering_next.submobjects
        # numbering_prev_parts = TransformMatchingShapes.get_mobject_parts(numbering_prev)
        # numbering_next_parts = TransformMatchingShapes.get_mobject_parts(numbering_next)
        
        # animations2 = []
        # for n in range(max(len(numbering_prev_parts), len(numbering_next_parts))):
        #     if len(numbering_prev_parts) < n and len(numbering_next_parts) < n:
        #         animations1.append(Transform(numbering_prev_parts[n], numbering_next_parts[n]))
        #     elif len(numbering_prev_parts) < n:
        #         numbering_prev_parts[n].set_color(RED)
        #         animations1.append(FadeOut(numbering_prev_parts[n]))
        #     elif len(numbering_next_parts) < n:
        #         animations2.append(Write(numbering_next_parts[n]))

        numbering_prev_to_remove = VGroup()
        for numbering_prev_item in numbering_prev_parts[len(numbering_next):]:
            numbering_prev_to_remove.add(numbering_prev_item)
        numbering_prev_to_remove.set_color(RED)
        animations1.append(FadeOut(numbering_prev_to_remove))

        animations1.extend([
            Transform(numbering_prev_part, numbering_next_part) for numbering_prev_part, numbering_next_part in zip(numbering_prev_parts, numbering_next_parts)
        ])
        animations2 = [Write(numbering_next_partial) for numbering_next_partial in numbering_next[len(numbering_prev):]]

        if n_carbon == self.n_carbon_to_remove_zoom_camera:
            self_scene.play(self_scene.get_zoomed_display_pop_out_animation(), rate_func=lambda t: smooth(1 - t), run_time=1.0 * speed_factor)
            self_scene.play(Uncreate(zoomed_display_frame), FadeOut(frame), run_time=1.0 * speed_factor)
        
        if (key_map := self.key_maps.get(title_prev.name, None)) is not None:
            key_map = key_map.get(title_next.name, None)

        self_scene.play([
            TransformMatchingLocation(chem_prev, chem_next, match_same_location=True, key_map=key_map, in_ratio_possible_match=0.01, match_same_key=self.CONFIG['match_same_key'], match_carbons=True if len(animations2) == 0 else False), 
            *animations1,
            *anims_transform_img,
        ], run_time=1.5 * speed_factor)
        if len(animations2) > 0:
            self_scene.play(*animations2, run_time=0.5 * speed_factor)
        if graph_animations[0] != []:
            self_scene.play(*graph_animations[0], run_time=0.5 * speed_factor)
            self_scene.play(*graph_animations[1], run_time=1.0 * speed_factor)
        self_scene.play([
            FadeToColor(VGroup(title_next, chem_next, numbering_next), WHITE),
            *graph_animations[2],
        ], run_time=0.5 * speed_factor)
        self_scene.remove(numbering_prev, *numbering_prev_parts)
        self_scene.remove(title_prev)
        self_scene.wait(duration=0.5 * speed_factor)

    def transform_to_line_diagram_and_back(self, self_scene, chem_next: Mobject, numbering_next, group_to_ignore, zd_rect, zoomed_display_frame, image_next):
        subtitle1 = Tex('Structural Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        numbering_next.set_color(RED)
        chem_next_original_point = chem_next.get_center()
        self_scene.play(
            Write(subtitle1), 
            FadeOut(numbering_next, image_next), 
            group_to_ignore.animate.set_opacity(0), 
            zd_rect.animate.set_opacity(1), 
            zoomed_display_frame.animate.set_color(BLACK), 
            chem_next.animate.move_to(ORIGIN)
        )
        self_scene.wait(duration=1)

        line_diagram_1 = ChemObject('-'.join(['C']*len(numbering_next)), auto_scale=False).scale(chem_next.initial_scale_factor)
        line_diagram_1.initial_scale_factor = chem_next.initial_scale_factor
        self_scene.play(TransformMatchingLocation(chem_next, line_diagram_1, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True), run_time=1)
        # self.add_numbering(line_diagram_1, file_name='line_diagram_1')

        chemcode = '-[2]' + ''.join('-[22]' if n % 2 == 0 else '-[2]' for n in range(len(numbering_next)-2))
        line_diagram2 = ChemObject(chemcode, chemfig_params=self.chemfig_params, auto_scale=False)
        line_diagram2.scale(line_diagram_1.width / line_diagram2.width)
        subtitle2 = Tex('Skeletal Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        self_scene.play(TransformMatchingLocation(line_diagram_1, line_diagram2, key_map=self.key_map_for_line_diagram), TransformMatchingTex(subtitle1, subtitle2), run_time=1.5)
        # self.add_numbering(line_diagram2, file_name='line_diagram')
        self_scene.wait(duration=1)

        self_scene.play(
            FadeOut(subtitle2), 
            TransformMatchingLocation(line_diagram2, line_diagram_1, color_fadeout='white', color_fadein='white'), 
        run_time=1.0)
        numbering_next.set_color(WHITE)
        self_scene.play(
            TransformMatchingLocation(
                line_diagram_1, chem_next, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True, 
                color_fadeout='white', color_fadein='white'), 
        run_time=1),
        self_scene.play(FadeIn(numbering_next, image_next), group_to_ignore.animate.set_opacity(1), zd_rect.animate.set_opacity(0), zoomed_display_frame.animate.set_color(PURPLE), chem_next.animate.move_to(chem_next_original_point), run_time=0.5)

        return chem_next, numbering_next, image_next

    def carbon_numbering(self, mobject, n_prev_carbon=0):
        numbering = VGroup()
        next_carbon_number = 1
        for mob in TransformMatchingShapes.get_mobject_parts(mobject):
            if len(mob.points) == 64:
                numbering.add(
                    MarkupText(str(next_carbon_number), weight=BOLD)
                    .scale(0.4 * mobject.initial_scale_factor)
                    .move_to(mob.get_center()).shift(UR * 0.25 * mobject.initial_scale_factor)
                    .set_color(GREEN if next_carbon_number > n_prev_carbon else WHITE)
                )
                next_carbon_number += 1

        return numbering

    def get_new_speed_factor(self, molecule, n_carbon):
        # can be implemented in subclass
        return 1.0

    def build_next_chemcode(self, molecule, n_carbon, chemcode, i):
        # to be implemented in subclass
        assert False, 'This method should be implemented in subclass'


class Alkanes(SequentialReactionScene):
    molecules = [
        'methane\nCH_{4}',
        'ethane\nC_{2}H_{6}',
        'propane\nC_{3}H_{8}',
        'butane\nC_{4}H_{10}',
        'pentane\nC_{5}H_{12}',
        'hexane\nC_{6}H_{14}',
        'heptane\nC_{7}H_{16}',
        'octane\nC_{8}H_{18}',
        'nonane\nC_{9}H_{20}',
        'decane\nC_{10}H_{22}',
        'undecane\nC_{11}H_{24}',
        'dodecane\nC_{12}H_{26}',
        'tridecane\nC_{13}H_{28}',
        'tetradecane\nC_{14}H_{30}',
        'pentadecane\nC_{15}H_{32}',
        'hexadecane\nC_{16}H_{34}',
        'heptadecane\nC_{17}H_{36}',
        'octadecane\nC_{18}H_{38}',
        'nonadecane\nC_{19}H_{40}',
        'icosane\nC_{20}H_{42}',
        'henicosane\nC_{21}H_{44}',
        'docosane\nC_{22}H_{46}',
        'tricosane\nC_{23}H_{48}',
        'tetracosane\nC_{24}H_{50}',
        'pentacosane\nC_{25}H_{52}',
        'hexacosane\nC_{26}H_{54}',
        'heptacosane\nC_{27}H_{56}',
        'octacosane\nC_{28}H_{58}',
        'nonacosane\nC_{29}H_{60}',
        'triacontane\nC_{30}H_{62}',

        'tetracontane\nC_{40}H_{82}',
        'pentacontane\nC_{50}H_{102}',
        'hexacontane\nC_{60}H_{122}',
        'heptacontane\nC_{70}H_{142}',
        'octacontane\nC_{80}H_{162}',
        'nonacontane\nC_{90}H_{182}',
        'hectane\nC_{100}H_{202}',

        # 'dictane\nC_{200}H_{402}',
        # 'trictane\nC_{300}H_{602}',
        # 'tetractane\nC_{400}H_{802}',
        # 'pentactane\nC_{500}H_{1002}',
        # 'kilactane\nC_{1000}H_{2002}',
    ]
    images = [
        'C1_methane gas.png',
        'C1to4_plastic manufacturing.jpg',
        'C3_propane stove.jpg',
        'C1to4_cooking1.jpeg', # C4
        'C5_blowing agent.jpg',
        'C6_cooking oil making',
        'C5to8_petrol.jpeg',
        'C5to8_gasoline.webp', # C8
        'C9to12_jet fuel.jpeg',
        'C9to12_kerosene1.jpeg',
        'C9to12_kerosene2.jpeg',
        'C12_DALL·E 2024-11-22 20.40.23 - A whimsical illustration featuring a pair of cockroaches at the center, embracing or showing affection towards one another, surrounded by a pair of mo.webp', # C12
        'C13_Abelmoschus-esculentus.jpg',
        'C14_phase change material.jpg',
        'C13to16_diesel1.png',
        'C16_black walnuts.jpg', # C16
        'C17to20_bicycle chain oils.jpg',
        'C17to20_lubricating oils1.jpeg',
        'C17to20_lubricating oils2.jpeg',
        'C21to30_paraffin wax1.jpg', # C20
        'C21_pheromone.jpg',
        'C22,24_magnolia.jpg',
        'C23_biosensor.jpg',
        'C22,24_vanilla madagascariensis', # C24
        'C21to30_paraffin wax2.webp',
        'C26_DALL·E 2024-11-20 23.52.06 - A still life illustration featuring a peach (복숭아), a sunflower (해바라기), a parsnip (파스닙), a coconut (코코넛), and a papaya (파파야). The composition should sh.webp',
        'C27_Euphorbia piscatoria.jpeg',
        'C28_Andrachne rotundifolia.jpg', # C28
        'C29_ginkgo nuts.jpg',
        'C30_German-vs-Roman-Chamomile.jpg', # C30
        'C31to70_heavy fuel oil.jpeg', # C40
        'C31to70_shipping.jpg',
        'C31to70_factory.jpg',
        'C70+_bitumen.jpg', # C70
        'C70+_Asphalt vs. Bitumen vs. Tar.png',
        'C70+_road construction.jpg',
        'C70+_asphalts.jpg',
    ]
    number_of_C_list = list(range(1, 30)) + list(range(30, 101, 10))
    chemcode_initial = 'C(-[0]H)(-[6]H)(-[12]H)(-[18]H)'
    chemcode_secondary = 'C(-[6]H)(-[12]H)(-[18]H)-C(-[0]H)(-[6]H)(-[18]H)'
    chemcode_to_add = '-C(-[6]H)(-[18]H)'
    len_chemcode_prefix = len('C(-[6]H)(-[12]H)(-[18]H)')
    substrings_to_isolate = ['ane', 'dec', 'cos', 'cont', '(', ')']
    key_map_for_line_diagram = {2 * i: i - 1 for i in range(1, number_of_C_list[-1])}
    CONFIG = {
        'match_same_key': False,
        'draw_graph': True,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_new_speed_factor(self, molecule, n_carbon):
        if n_carbon >= 31:
            return 0.50
        # elif n_carbon >= 25:
        #     return 0.24
        elif n_carbon >= 21:
            return 0.36
        elif n_carbon >= 13:
            return 0.42
        elif n_carbon >= 13:
            return 0.45
        elif n_carbon >= 10:
            return 0.8
        else:
            return 1.0

    def build_next_chemcode(self, molecule, n_carbon, chemcode, i):
        if n_carbon == 1:
            print(f'number of C: 1 (+1C)')
            chemcode = self.chemcode_initial
        elif n_carbon == 2:
            print(f'number of C: 2 (+1C)')
            chemcode = self.chemcode_secondary
        else:
            print(f'number of C: {n_carbon} (+{n_carbon - self.number_of_C_list[i]}C)')
            chemcode = \
                chemcode[:self.len_chemcode_prefix+(self.number_of_C_list[i]-2)*len(self.chemcode_to_add)] + \
                (n_carbon - self.number_of_C_list[i])*self.chemcode_to_add + \
                self.chemcode_secondary[self.len_chemcode_prefix:]
        
        return chemcode


class CycloAlkanes(SequentialReactionScene):
    molecules = [
        'propane\nC_{3}H_{8}',
        'cyclopropane\nC_{3}H_{6}',
        'cyclobutane\nC_{4}H_{8}',
        'cyclopentane\nC_{5}H_{10}',
        'cyclohexane\nC_{6}H_{12}',
        'cycloheptane\nC_{7}H_{14}',
        'cyclooctane\nC_{8}H_{16}',
        'cyclononane\nC_{9}H_{18}',
        'cyclodecane\nC_{10}H_{20}',
        'cycloicosane\nC_{20}H_{40}',
        'cyclotriacontane\nC_{30}H_{60}',
        'cyclotetracontane\nC_{40}H_{80}',
        'cyclopentacontane\nC_{50}H_{100}',
        'cyclohexacontane\nC_{60}H_{120}',
        'cycloheptacontane\nC_{70}H_{140}',
        'cyclooctacontane\nC_{80}H_{160}',
        'cyclononacontane\nC_{90}H_{180}',
        'cyclohectacontane\nC_{100}H_{200}',
    ]
    images = [
        'C1to4_cooking2.jpeg',
        'cyclo_C3_anesthetic.webp',
        'cyclo_C4_ladderane.png',
        'cyclo_C5_Polyurethane_Products.png',
        'cyclo_C6_nylon.jpg',
        'cyclo_C7_medication.jpg',
        'cyclo_C8_homogeneous catalysis.png',
        'cyclo_C9_1,4,7-triazacyclononane.png',
        'cyclo_C10_nylon12.jpeg',
        'cyclo_C20_bio-pesticides.jpeg',
        'cyclo_C30.png',
        'cyclo_C30.png',
        'cyclo_C50.webp',
        'cyclo_C50.webp',
        'cyclo_C70.jpeg',
        'cyclo_C70.jpeg',
        'cyclo_C90_The_Mad_Science.webp',
        'cyclo_C90_The_Mad_Science.webp',
    ]
    number_of_C_list = [3] + list(range(3, 10)) + list(range(10, 101, 10))
    chemcode_partial = '-C(-[6]H)(-[18]H)'
    chemcode_initial = f'C(-[6]H)(-[12]H)(-[18]H){chemcode_partial}-C(-[0]H)(-[6]H)(-[18]H)'
    substrings_to_isolate = ['ane', 'dec', 'cos', 'cont', '(', ')', 'cyclo', 'prop']
    chemfig_params = {'angle increment': 15}
    key_map_for_line_diagram = {2 * i: i - 1 for i in range(1, number_of_C_list[-1])}
    key_maps = {
        'propane': {
            'cyclopropane': {
                0: 0,
                1: 1,
                2: 2,
                5: 3,
                6: 9,
                7: 10,
                8: 11,
                9: 12,
                10: 13,
                11: 14,
                12: 20,
                13: 21,
                14: 22,
                17: 23,
                18: 24,
                19: 25,
                20: 31,
                16: 32,
            }
        }
    }
    CONFIG = {
        'match_same_key': True,
        'draw_graph': False,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_new_speed_factor(self, molecule, n_carbon):
        if n_carbon == 3:
            if molecule == 'propane\nC_{3}H_{8}':
                return 1.2
            return 1.0
        elif n_carbon < 12:
            return 0.40
        else:
            return 0.36

    def build_next_chemcode(self, molecule, n_carbon, chemcode, i):
        print(f'number of C: {n_carbon} (+{n_carbon - self.number_of_C_list[i]}C)')

        if molecule == 'propane\nC_{3}H_{8}':
            return self.chemcode_initial

        unit = round(360/n_carbon, 2)
        chemcode = ''.join([f'C(<[:{unit*(n+1)+(360-unit)/2-15}]H)(<:[:{unit*(n+1)+(360-unit)/2+15}]H)-[:{(n+1)*unit+270},{1 if n != n_carbon-1 else 0.70}]' for n in range(n_carbon)])

        return chemcode


class AlkanesAndCycloAlkanes(AlkaneMeltingAndBoilingPointGraph):
    def measure_running_time(func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            time_start = perf_counter()
            func(*args, **kwargs)
            time_end = perf_counter()
            total_time = time_end - time_start
            hours, remainder = divmod(total_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f'Total time: {int(hours)}h:{int(minutes)}m:{seconds:.2f}s')
        return wrapper

    @measure_running_time
    def construct(self):
        alkanes = Alkanes()
        cycloalkanes = CycloAlkanes()

        prev_objects = Alkanes.construct(alkanes, self)
        self.wait(duration=2.0)
        prev_objects = CycloAlkanes.construct(cycloalkanes, self, *prev_objects)

        alkanes.molecules = [
            'methane\nCH_{4}',
        ]
        alkanes.images = [None]
        alkanes.CONFIG = {
            'match_same_key': False,
            'draw_graph': False,
        }
        self.wait(duration=2.0)
        title_next, chem_next, numbering_next, chemcode, image_next = Alkanes.construct(alkanes, self, *prev_objects)
        self.play(VGroup(chem_next, numbering_next).animate.shift(DOWN * 0.5), run_time=1.0)
        self.wait(duration=3.0)


class Propane(ReactionScene):
    def construct(self):
        chem1 = ChemObject(CycloAlkanes.chemcode_initial, chemfig_params={'angle increment': 15})
        self.add(chem1)
        self.add_numbering(chem1, file_name='propane')

        unit = round(360/3, 2)
        chemcode = ''.join([f'C(<[:{unit*(n+1)+(360-unit)/2-15}]H)(<:[:{unit*(n+1)+(360-unit)/2+15}]H)-[:{(n+1)*unit+270},{1 if n != 3-1 else 0.70}]' for n in range(3)])
        self.remove(chem1)
 
        chem2 = ChemObject(chemcode, chemfig_params={'angle increment': 15})
        self.add(chem2)
        self.add_numbering(chem2, file_name='cyclopropane')
        
        # self.play(TransformMatchingLocation(chem1, chem2, match_same_location=True, key_map=CycloAlkanes.key_maps['propane']['cyclopropane'], in_ratio_possible_match=0.01))

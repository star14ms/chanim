# Main Command: manim -p chemical_reaction/alkanes.py
import sys, os
sys.path.append(os.path.abspath('.'))

from rich import print
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
        image.set_height(self.image_max_height).to_edge(edge).shift(shift)

        return image

    def build_animation_next_image(self, image_prev: ImageMobject, image_next: ImageMobject):
        if image_prev.pixel_array.shape != image_next.pixel_array.shape or not (image_prev.pixel_array == image_next.pixel_array).all():
            return [FadeTransform(image_prev, image_next)]
        else:
            return []


class Alkanes(ReactionScene, AlkaneMeltingAndBoilingPointGraph, PictureTransforms):
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
    number_of_C_list = list(range(1, 30)) + list(range(30, 101, 10))
    chemcode_primary = 'C(-[0]H)(-[6]H)(-[12]H)(-[18]H)'
    chemcode_secondary = 'C(-[6]H)(-[12]H)(-[18]H)-C(-[0]H)(-[6]H)(-[18]H)'
    chemcode_to_add = '-C(-[6]H)(-[18]H)'
    len_chemcode_prefix = len('C(-[6]H)(-[12]H)(-[18]H)')
    substrings_to_isolate = ['ane', 'dec', 'cos', 'cont', '(', ')']
    chemfig_params = {'angle increment': 15}
    key_map = {2 * i: i - 1 for i in range(1, number_of_C_list[-1])}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self):
        chemcode = self.chemcode_primary
        print(f'number of C: 1 (+1C)')
        title_next = VMobject()
        for n, title_line in enumerate(self.molecules[0].split('\n')):
            title_next.add(ChemObject(title_line, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate))
        title_next.arrange(DOWN).to_edge(UP)
        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
        numbering_next = self.carbon_numbering(chem_next)

        self.play(Write(title_next), Create(chem_next), run_time=1.0)
        self.play(Write(numbering_next), run_time=0.5)
        self.play(FadeToColor(numbering_next, WHITE), run_time=0.5)
        self.wait(duration=0.5)

        ax, labels = self.create_axes_and_labels(corner=DL, shift=RIGHT * 0.5)
        image_next = self.build_next_image(self.images[0])
        self.play(LaggedStart(VGroup(chem_next, numbering_next).animate.shift(UP * 0.5), FadeIn(image_next), Write(ax),  Write(labels), run_time=3, lag_ratio=0.5))

        x0 = 1
        n_carbons = list(range(x0, self.max_n_carbons))
        t, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next = self.add_dynamic_graph(ax, x0, n_carbons)
        frame, zoomed_display_frame, zd_rect = self.highlight_graph(ax, n_carbons, label_bp_next, label_mp_next, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp)
        frame_offset = ax.get_corner(DL) - frame.get_corner(DL)
        image_path_prev = None

        for i, (molecule, n_carbon, image_path) in enumerate(zip(self.molecules[1:], self.number_of_C_list[1:], self.images[1:])):
            title_prev = title_next
            chem_prev = chem_next
            numbering_prev = numbering_next
            title_next, chem_next, numbering_next, chemcode = self.build_next_objects(molecule, n_carbon, chemcode, i)

            image_prev = image_next
            if image_path != image_path_prev:
                print(image_path, image_path_prev)
                image_next = self.build_next_image(image_path, shift=RIGHT * 4 if n_carbon <= 30 else 0)
                image_path_prev = image_path
            anims_transform_img = self.build_animation_next_image(image_prev, image_next)

            label_bp_prev = label_bp_next
            label_mp_prev = label_mp_next
            speed_factor = self.get_new_speed_factor(n_carbon)

            if n_carbon <= 30:
                label_bp_next, label_mp_next, dot_bp, dot_mp, scale_factor, vector_to_shift = \
                    self.build_next_graph_objects(ax, frame, n_carbon, frame_offset, h_line_bp, h_line_mp
                )
                graph_animations = self.build_animation_next_graph(
                    t, frame, n_carbon, vector_to_shift, scale_factor, 
                    label_bp_prev, label_bp_next, label_mp_prev, label_mp_next, dot_bp, dot_mp
                )
            elif n_carbon == 40:
                group_to_ignore = VGroup(ax, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next, labels, self.dots)
                self.play(group_to_ignore.animate.set_opacity(0), run_time=1.0 * speed_factor)
                self.remove(group_to_ignore)
                graph_animations = [[], [], []]
            else:
                graph_animations = [[], [], []]

            self.apply_next_objects(title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, graph_animations, n_carbon, frame, zoomed_display_frame, anims_transform_img, speed_factor=speed_factor)
            self.dots.add(dot_bp, dot_mp)

            if n_carbon == 10:
                group_to_ignore = VGroup(ax, h_line_bp, h_line_mp, label_bp_next, label_mp_next, labels, self.dots)
                chem_next, numbering_next, image_next = self.transform_to_line_diagram_and_back(chem_next, numbering_next, group_to_ignore, zd_rect, zoomed_display_frame, image_next)

    def build_next_objects(self, molecule, n_carbon, chemcode, i):
        if i == 0:
            print(f'number of C: 2 (+1C)')
            chemcode = self.chemcode_secondary
        else:
            print(f'number of C: {n_carbon} (+{n_carbon - self.number_of_C_list[i]}C)')
            chemcode = \
                chemcode[:self.len_chemcode_prefix+(self.number_of_C_list[i]-2)*len(self.chemcode_to_add)] + \
                (n_carbon - self.number_of_C_list[i])*self.chemcode_to_add + \
                self.chemcode_secondary[self.len_chemcode_prefix:]
        
        title_next = VMobject()
        for n, title_line in enumerate(molecule.split('\n')):
            title_next.add(ChemObject(title_line, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate))
        title_next.arrange(DOWN).to_edge(UP)

        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params).shift(UP * 0.5)
        numbering_next = self.carbon_numbering(chem_next, n_prev_carbon=self.number_of_C_list[i])
        
        return title_next, chem_next, numbering_next, chemcode

    def apply_next_objects(self, title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, graph_animations, n_carbon, frame, zoomed_display_frame, anims_transform_img, speed_factor=1.0):
        animations1 = []
        for n in range(max(len(title_prev), len(title_next))):
            title_prev_line = title_prev[n] if len(title_prev) > n else ChemObject(title_prev[n-1].tex_string, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
            title_next_line = title_next[n] if len(title_next) > n else ChemObject('', font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate)
            animations1.append(TransformMatchingElementTex(title_prev_line, title_next_line))

        animations1.extend([
            Transform(numbering_prev_part, numbering_next_part) for numbering_prev_part, numbering_next_part in zip(
                TransformMatchingShapes.get_mobject_parts(numbering_prev), 
                TransformMatchingShapes.get_mobject_parts(numbering_next)
            )
        ])
        animations2 = [Write(numbering_next_partial) for numbering_next_partial in numbering_next[len(numbering_prev):]]

        if n_carbon == 21:
            self.play(self.get_zoomed_display_pop_out_animation(), rate_func=lambda t: smooth(1 - t), run_time=1.0 * speed_factor)
            self.play(Uncreate(zoomed_display_frame), FadeOut(frame), run_time=1.0 * speed_factor)

        self.play([
            TransformMatchingLocation(chem_prev, chem_next, match_same_location=True, min_ratio_possible_match=0.01), 
            *animations1,
            *anims_transform_img,
        ], run_time=1.5 * speed_factor)
        self.play(*animations2, run_time=0.5 * speed_factor)
        if graph_animations[0] != []:
            self.play(*graph_animations[0], run_time=0.5 * speed_factor)
            self.play(*graph_animations[1], run_time=1.0 * speed_factor)
        self.play([
            FadeToColor(VGroup(title_next, chem_next, numbering_next), WHITE),
            *graph_animations[2],
        ], run_time=0.5 * speed_factor)
        self.remove(numbering_prev)
        self.remove(title_prev)
        self.wait(duration=0.5 * speed_factor)

    def transform_to_line_diagram_and_back(self, chem_next: Mobject, numbering_next, group_to_ignore, zd_rect, zoomed_display_frame, image_next):
        subtitle1 = Tex('Structural Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        numbering_next.set_color(RED)
        chem_next_original_point = chem_next.get_center()
        self.play(
            Write(subtitle1), 
            FadeOut(numbering_next, image_next), 
            group_to_ignore.animate.set_opacity(0), 
            zd_rect.animate.set_opacity(1), 
            zoomed_display_frame.animate.set_color(BLACK), 
            chem_next.animate.move_to(ORIGIN)
        )
        self.wait(duration=1)

        line_diagram_1 = ChemObject('-'.join(['C']*len(numbering_next)), auto_scale=False).scale(chem_next.initial_scale_factor)
        line_diagram_1.initial_scale_factor = chem_next.initial_scale_factor
        self.play(TransformMatchingLocation(chem_next, line_diagram_1, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True), run_time=1)
        # self.add_numbering(line_diagram_1, file_name='line_diagram_1')

        chemcode = '-[2]' + ''.join('-[22]' if n % 2 == 0 else '-[2]' for n in range(len(numbering_next)-2))
        line_diagram2 = ChemObject(chemcode, chemfig_params=self.chemfig_params, auto_scale=False)
        line_diagram2.scale(line_diagram_1.width / line_diagram2.width)
        subtitle2 = Tex('Skeletal Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        self.play(TransformMatchingLocation(line_diagram_1, line_diagram2, key_map=self.key_map), TransformMatchingTex(subtitle1, subtitle2), run_time=1.5)
        # self.add_numbering(line_diagram2, file_name='line_diagram')
        self.wait(duration=1)

        self.play(
            FadeOut(subtitle2), 
            TransformMatchingLocation(line_diagram2, line_diagram_1, color_fadeout='white', color_fadein='white'), 
        run_time=1.0)
        numbering_next.set_color(WHITE)
        self.play(
            TransformMatchingLocation(
                line_diagram_1, chem_next, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True, 
                color_fadeout='white', color_fadein='white'), 
        run_time=1),
        self.play(FadeIn(numbering_next, image_next), group_to_ignore.animate.set_opacity(1), zd_rect.animate.set_opacity(0), zoomed_display_frame.animate.set_color(PURPLE), chem_next.animate.move_to(chem_next_original_point), run_time=0.5)

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

    def get_new_speed_factor(self, n_carbon):
        if n_carbon >= 31:
            return 0.56
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


class CycloAlkanes(ReactionScene, AlkaneMeltingAndBoilingPointGraph, PictureTransforms):
    molecules = [
        'cyclopropane\nC_{3}H_{6}',
        'cyclobutane\nC_{4}H_{8}',
        'cyclopentane\nC_{5}H_{10}',
        'cyclohexane\nC_{6}H_{12}',
        'cycloheptane\nC_{7}H_{14}',
        'cyclooctane\nC_{8}H_{16}',
        # 'cyclononane\nC_{9}H_{18}',
        # 'cyclodecane\nC_{10}H_{20}',
        # 'cycloundecane\nC_{11}H_{22}',
        # 'cyclododecane\nC_{12}H_{24}',
        # 'cyclotridecane\nC_{13}H_{26}',
        # 'cyclotetradecane\nC_{14}H_{28}',
        # 'cyclopentadecane\nC_{15}H_{30}',
        # 'cyclohexadecane\nC_{16}H_{32}',
        # 'cycloheptadecane\nC_{17}H_{34}',
        # 'cyclooctadecane\nC_{18}H_{36}',
        # 'cyclononadecane\nC_{19}H_{38}',
        # 'cycloicosane\nC_{20}H_{40}',
        # 'cyclohenicosane\nC_{21}H_{42}',
        # 'cyclodocosane\nC_{22}H_{44}',
        # 'cyclotricosane\nC_{23}H_{46}',
        # 'cyclotetracosane\nC_{24}H_{48}',
        # 'cyclopentacosane\nC_{25}H_{50}',
        # 'cyclohexacosane\nC_{26}H_{52}',
        # 'cycloheptacosane\nC_{27}H_{54}',
        # 'cyclooctacosane\nC_{28}H_{56}',
        # 'cyclononacosane\nC_{29}H_{58}',
        # 'cyclotriacontane\nC_{30}H_{60}',
        # 'cyclotetracontane\nC_{40}H_{62}',
        # 'cyclopentacontane\nC_{50}H_{82}',
        # 'cyclohexacontane\nC_{60}H_{102}',
        # 'cycloheptacontane\nC_{70}H_{122}',
        # 'cyclooctacontane\nC_{80}H_{142}',
        # 'cyclononacontane\nC_{90}H_{162}',
        # 'cyclohectane\nC_{100}H_{182}',
    ]
    number_of_C_list = list(range(3, 30)) + list(range(30, 101, 10))
    chemcode_initial = 'C*3(-C-C-)'
    substrings_to_isolate = ['ane', 'dec', 'cos', 'cont', '(', ')']
    chemfig_params = {'angle increment': 15}
    key_map = {2 * i: i - 1 for i in range(1, number_of_C_list[-1])}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self):
        chemcode = self.chemcode_initial
        print(f'number of C: 1 (+1C)')
        title_next = VMobject()
        for n, title_line in enumerate(self.molecules[0].split('\n')):
            title_next.add(ChemObject(title_line, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate))
        title_next.arrange(DOWN).to_edge(UP)
        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
        numbering_next = self.carbon_numbering(chem_next)

        self.play(Write(title_next), Create(chem_next), run_time=1.0)
        self.play(Write(numbering_next), run_time=0.5)
        self.play(FadeToColor(numbering_next, WHITE), run_time=0.5)
        self.wait(duration=0.5)

        ax, labels = self.create_axes_and_labels(corner=DL, shift=RIGHT * 0.5)
        image_next = self.build_next_image(self.images[0])
        self.play(LaggedStart(VGroup(chem_next, numbering_next).animate.shift(UP * 0.5), FadeIn(image_next), Write(ax),  Write(labels), run_time=3, lag_ratio=0.5))

        x0 = 1
        n_carbons = list(range(x0, self.max_n_carbons))
        t, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next = self.add_dynamic_graph(ax, x0, n_carbons)
        frame, zoomed_display_frame, zd_rect = self.highlight_graph(ax, n_carbons, label_bp_next, label_mp_next, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp)
        frame_offset = ax.get_corner(DL) - frame.get_corner(DL)
        image_path_prev = None

        for i, (molecule, n_carbon, image_path) in enumerate(zip(self.molecules[1:], self.number_of_C_list[1:], self.images[1:])):
            title_prev = title_next
            chem_prev = chem_next
            numbering_prev = numbering_next
            title_next, chem_next, numbering_next, chemcode = self.build_next_objects(molecule, n_carbon, chemcode, i)

            image_prev = image_next
            if image_path != image_path_prev:
                print(image_path, image_path_prev)
                image_next = self.build_next_image(image_path, shift=RIGHT * 4 if n_carbon <= 30 else 0)
                image_path_prev = image_path
            anims_transform_img = self.build_animation_next_image(image_prev, image_next)

            label_bp_prev = label_bp_next
            label_mp_prev = label_mp_next
            speed_factor = self.get_new_speed_factor(n_carbon)

            if n_carbon <= 30:
                label_bp_next, label_mp_next, dot_bp, dot_mp, scale_factor, vector_to_shift = \
                    self.build_next_graph_objects(ax, frame, n_carbon, frame_offset, h_line_bp, h_line_mp
                )
                graph_animations = self.build_animation_next_graph(
                    t, frame, n_carbon, vector_to_shift, scale_factor, 
                    label_bp_prev, label_bp_next, label_mp_prev, label_mp_next, dot_bp, dot_mp
                )
            elif n_carbon == 40:
                group_to_ignore = VGroup(ax, graph_bp, graph_mp, dot_bp_moving, dot_mp_moving, h_line_bp, h_line_mp, label_bp_next, label_mp_next, labels, self.dots)
                self.play(group_to_ignore.animate.set_opacity(0), run_time=1.0 * speed_factor)
                self.remove(group_to_ignore)
                graph_animations = [[], [], []]
            else:
                graph_animations = [[], [], []]

            self.apply_next_objects(title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, graph_animations, n_carbon, frame, zoomed_display_frame, anims_transform_img, speed_factor=speed_factor)
            self.dots.add(dot_bp, dot_mp)

            if n_carbon == 10:
                group_to_ignore = VGroup(ax, h_line_bp, h_line_mp, label_bp_next, label_mp_next, labels, self.dots)
                chem_next, numbering_next, image_next = self.transform_to_line_diagram_and_back(chem_next, numbering_next, group_to_ignore, zd_rect, zoomed_display_frame, image_next)

    def build_next_objects(self, molecule, n_carbon, chemcode, i):
        print(f'number of C: {n_carbon} (+{n_carbon - self.number_of_C_list[i]}C)')
        chemcode_partial = ('C-' * n_carbon)[1:]
        chemcode = f'C*{n_carbon}({chemcode_partial})'
        title_next = VMobject()
        for n, title_line in enumerate(molecule.split('\n')):
            title_next.add(ChemObject(title_line, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate))
        title_next.arrange(DOWN).to_edge(UP)

        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params).shift(UP * 0.5)
        numbering_next = self.carbon_numbering(chem_next, n_prev_carbon=self.number_of_C_list[i])

        return title_next, chem_next, numbering_next, chemcode

    def apply_next_objects(self, title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, graph_animations, n_carbon, frame, zoomed_display_frame, anims_transform_img, speed_factor=1.0):
        animations1 = []
        for n in range(max(len(title_prev), len(title_next))):
            title_prev_line = title_prev[n] if len(title_prev) > n else ChemObject(title_prev[n-1].tex_string, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
            title_next_line = title_next[n] if len(title_next) > n else ChemObject('', font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate)
            animations1.append(TransformMatchingElementTex(title_prev_line, title_next_line))

        animations1.extend([
            Transform(numbering_prev_part, numbering_next_part) for numbering_prev_part, numbering_next_part in zip(
                TransformMatchingShapes.get_mobject_parts(numbering_prev), 
                TransformMatchingShapes.get_mobject_parts(numbering_next)
            )
        ])
        animations2 = [Write(numbering_next_partial) for numbering_next_partial in numbering_next[len(numbering_prev):]]

        if n_carbon == 21:
            self.play(self.get_zoomed_display_pop_out_animation(), rate_func=lambda t: smooth(1 - t), run_time=1.0 * speed_factor)
            self.play(Uncreate(zoomed_display_frame), FadeOut(frame), run_time=1.0 * speed_factor)

        self.play([
            TransformMatchingLocation(chem_prev, chem_next, match_same_location=True, min_ratio_possible_match=0.01, match_same_key=True), 
            *animations1,
            *anims_transform_img,
        ], run_time=1.5 * speed_factor)
        self.play(*animations2, run_time=0.5 * speed_factor)
        if graph_animations[0] != []:
            self.play(*graph_animations[0], run_time=0.5 * speed_factor)
            self.play(*graph_animations[1], run_time=1.0 * speed_factor)
        self.play([
            FadeToColor(VGroup(title_next, chem_next, numbering_next), WHITE),
            *graph_animations[2],
        ], run_time=0.5 * speed_factor)
        self.remove(numbering_prev)
        self.remove(title_prev)
        self.wait(duration=0.5 * speed_factor)

    def transform_to_line_diagram_and_back(self, chem_next: Mobject, numbering_next, group_to_ignore, zd_rect, zoomed_display_frame, image_next):
        subtitle1 = Tex('Structural Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        numbering_next.set_color(RED)
        chem_next_original_point = chem_next.get_center()
        self.play(
            Write(subtitle1), 
            FadeOut(numbering_next, image_next), 
            group_to_ignore.animate.set_opacity(0), 
            zd_rect.animate.set_opacity(1), 
            zoomed_display_frame.animate.set_color(BLACK), 
            chem_next.animate.move_to(ORIGIN)
        )
        self.wait(duration=1)

        line_diagram_1 = ChemObject('-'.join(['C']*len(numbering_next)), auto_scale=False).scale(chem_next.initial_scale_factor)
        line_diagram_1.initial_scale_factor = chem_next.initial_scale_factor
        self.play(TransformMatchingLocation(chem_next, line_diagram_1, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True), run_time=1)
        # self.add_numbering(line_diagram_1, file_name='line_diagram_1')

        chemcode = '-[2]' + ''.join('-[22]' if n % 2 == 0 else '-[2]' for n in range(len(numbering_next)-2))
        line_diagram2 = ChemObject(chemcode, chemfig_params=self.chemfig_params, auto_scale=False)
        line_diagram2.scale(line_diagram_1.width / line_diagram2.width)
        subtitle2 = Tex('Skeletal Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        self.play(TransformMatchingLocation(line_diagram_1, line_diagram2, key_map=self.key_map), TransformMatchingTex(subtitle1, subtitle2), run_time=1.5)
        # self.add_numbering(line_diagram2, file_name='line_diagram')
        self.wait(duration=1)

        self.play(
            FadeOut(subtitle2), 
            TransformMatchingLocation(line_diagram2, line_diagram_1, color_fadeout='white', color_fadein='white'), 
        run_time=1.0)
        numbering_next.set_color(WHITE)
        self.play(
            TransformMatchingLocation(
                line_diagram_1, chem_next, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True, 
                color_fadeout='white', color_fadein='white'), 
        run_time=1),
        self.play(FadeIn(numbering_next, image_next), group_to_ignore.animate.set_opacity(1), zd_rect.animate.set_opacity(0), zoomed_display_frame.animate.set_color(PURPLE), chem_next.animate.move_to(chem_next_original_point), run_time=0.5)

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

    def get_new_speed_factor(self, n_carbon):
        if n_carbon >= 31:
            return 0.56
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

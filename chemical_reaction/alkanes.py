# Main Command: manim -p chemical_reaction/alkanes.py
import sys, os
sys.path.append(os.path.abspath('.'))

from rich import print
from chanim_manim import *

from base import ReactionScene
from template import TransformMatchingLocation, TransformMatchingElementTex


class Alkanes(ReactionScene):
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

    def construct(self):
        speed_factor = 1.0

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

        for i, (molecule, n_carbon) in enumerate(zip(self.molecules[1:], self.number_of_C_list[1:])):
            title_prev = title_next
            chem_prev = chem_next
            numbering_prev = numbering_next

            title_next, chem_next, numbering_next, chemcode = self.build_next_objects(molecule, n_carbon, chemcode, i)

            if n_carbon >= 13:
                speed_factor = 0.6
            elif n_carbon >= 8:
                speed_factor = 0.8

            self.apply_next_objects(title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, speed_factor=speed_factor)
 
            if n_carbon == 10:
                chem_next, numbering_next = self.transform_to_line_diagram_and_back(chem_next, numbering_next)

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

        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
        numbering_next = self.carbon_numbering(chem_next, n_prev_carbon=self.number_of_C_list[i])
        
        return title_next, chem_next, numbering_next, chemcode

    def apply_next_objects(self, title_prev, title_next, chem_prev, chem_next, numbering_prev, numbering_next, speed_factor=1.0):
        animations = []
        for n in range(max(len(title_prev), len(title_next))):
            title_prev_line = title_prev[n] if len(title_prev) > n else ChemObject(title_prev[n-1].tex_string, font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
            title_next_line = title_next[n] if len(title_next) > n else ChemObject('', font_size=64 if n == 0 else 48, substrings_to_isolate=self.substrings_to_isolate)
            animations.append(TransformMatchingElementTex(title_prev_line, title_next_line))

        animations.extend([
            Transform(numbering_prev_part, numbering_next_part) for numbering_prev_part, numbering_next_part in zip(
                TransformMatchingShapes.get_mobject_parts(numbering_prev), 
                TransformMatchingShapes.get_mobject_parts(numbering_next)
            )
        ])
        animations2 = [Write(numbering_next_partial) for numbering_next_partial in numbering_next[len(numbering_prev):]]

        self.play([
            TransformMatchingLocation(chem_prev, chem_next, match_same_location=True, min_ratio_possible_match=0.01), 
            *animations,
        ], run_time=1.0 * speed_factor)
        self.play(*animations2, run_time=0.5 * speed_factor)
        self.play([
            FadeToColor(title_next, WHITE),
            FadeToColor(chem_next, WHITE),
            FadeToColor(numbering_next, WHITE),
        ], run_time=0.5 * speed_factor)
        self.remove(numbering_prev)
        self.remove(title_prev)
        self.wait(duration=0.5 * speed_factor)

    def transform_to_line_diagram_and_back(self, chem_next, numbering_next):
        subtitle1 = Tex('Structural Formula', font_size=48, substrings_to_isolate=['Formula']).to_edge(DOWN)
        numbering_next.set_color(RED)
        self.play(Write(subtitle1), FadeOut(numbering_next))
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

        self.play(FadeOut(subtitle2), TransformMatchingLocation(line_diagram2, line_diagram_1, color_fadeout='white', color_fadein='white'), run_time=1.5)
        numbering_next.set_color(WHITE)
        self.play(TransformMatchingLocation(line_diagram_1, chem_next, min_ratio_possible_match=0.01, min_ratio_to_accept_match=0.3, match_same_location=True, color_fadeout='white', color_fadein='white'), FadeIn(numbering_next), run_time=1)

        return chem_next, numbering_next

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

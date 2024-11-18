# Main Command: manim -p chemical_reaction/alkanes.py
import sys, os
sys.path.append(os.path.abspath('.'))

from chanim_manim import *

from base import ReactionScene, TransformMatchingLocation, TransformMatchingTexColorHighlight


class Alkanes(ReactionScene):
    molecules = [
        'methane',
        'ethane',
        'propane',
        'butane',
        'pentane',
        'hexane',
        'heptane',
        'octane',
        'nonane',
        'decane',
        'undecane',
        'dodecane',
    ]
    chemcode_primary = 'C(-[0]H)(-[6]H)(-[12]H)(-[18]H)'
    chemcode_secondary = 'C(-[6]H)(-[12]H)(-[18]H)-C(-[0]H)(-[6]H)(-[18]H)'
    chemcode_to_add = '-C(-[6]H)(-[18]H)'
    len_chemcode_prefix = len('C(-[6]H)(-[12]H)(-[18]H)')
    substrings_to_isolate = ['ane']
    chemfig_params = {'angle increment': 15}
    key_map = {2 * i: i - 1 for i in range(1, len(molecules))}

    def construct(self):
        len_chemcode_to_add = len(self.chemcode_to_add)

        chemcode = self.chemcode_primary
        title_next = Tex(self.molecules[0], font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
        chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
        numbering_next = self.carbon_numbering(chem_next)

        self.play(Write(title_next), Create(chem_next))
        self.play(Write(numbering_next), run_time=0.5)
        self.play(FadeToColor(numbering_next, WHITE), run_time=0.5)
        self.wait(duration=1)

        for i, molecule in enumerate(self.molecules[1:]):
            title_prev = title_next
            chem_prev = chem_next
            numbering_prev = numbering_next

            if i == 0:
                chemcode = self.chemcode_secondary
            else:
                chemcode = chemcode[:self.len_chemcode_prefix+(i-1)*len_chemcode_to_add] + self.chemcode_to_add + chemcode[self.len_chemcode_prefix+(i-1)*len_chemcode_to_add:]

            title_next = Tex(molecule, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
            chem_next = ChemObject(chemcode, chemfig_params=self.chemfig_params)
            numbering_next = self.carbon_numbering(chem_next)

            animations = [
                Transform(numbering_prev_part, numbering_next_part) for numbering_prev_part, numbering_next_part in zip(
                    TransformMatchingShapes.get_mobject_parts(numbering_prev), 
                    TransformMatchingShapes.get_mobject_parts(numbering_next)
                )
            ]
            self.play([
                TransformMatchingTexColorHighlight(title_prev, title_next, target_position=ORIGIN),
                TransformMatchingLocation(chem_prev, chem_next, match_same_location=True), 
                *animations,
            ], run_time=1.5)
            self.play(Write(numbering_next[-1]))
            self.play([
                FadeToColor(title_next, WHITE),
                FadeToColor(chem_next, WHITE),
                FadeToColor(numbering_next, WHITE),
            ], run_time=0.5)
            self.remove(numbering_prev)
            self.wait(duration=0.5)

        self.transform_to_line_diagram(numbering_next, chem_next)

    def transform_to_line_diagram(self, numbering_next, chem_next):
        subtitle1 = Tex('Structural Formula', font_size=48).to_edge(DOWN)
        self.play(Write(subtitle1))
        self.wait(duration=1)

        line_diagram_1 = ChemObject('-'.join(['C']*(len(self.molecules))))
        numbering_next.set_color(RED)
        self.play([
            TransformMatchingLocation(chem_next, line_diagram_1, min_ratio_possible_match=0.1, match_same_location=True),
            FadeOut(numbering_next),
        ], run_time=1)
        # self.add_numbering(line_diagram_1, file_name='line_diagram_1')

        chemcode = '-[2]' + ''.join('-[22]' if n % 2 == 0 else '-[2]' for n in range(len(self.molecules)-2))
        line_diagram2 = ChemObject(chemcode, chemfig_params=self.chemfig_params)
        subtitle2 = Tex('Line Diagram', font_size=48).to_edge(DOWN)
        self.play(TransformMatchingLocation(line_diagram_1, line_diagram2, key_map=self.key_map), FadeTransform(subtitle1, subtitle2), run_time=1.5)
        # self.add_numbering(line_diagram2, file_name='line_diagram')
        self.wait(duration=2)

    def carbon_numbering(self, mobject):
        max_carbon_number = sum(1 for mob1 in TransformMatchingShapes.get_mobject_parts(mobject) if len(mob1.points) == 64)

        numbering = VGroup()
        next_carbon_number = 1
        for mob2 in TransformMatchingShapes.get_mobject_parts(mobject):
            if len(mob2.points) == 64:
                numbering.add(
                    MarkupText(str(next_carbon_number), weight=BOLD)
                    .scale(0.4)
                    .move_to(mob2.get_center()).shift(UR*0.25)
                    .set_color(GREEN if next_carbon_number == max_carbon_number else WHITE)
                )
                next_carbon_number += 1

        return numbering

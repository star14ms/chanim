import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chanim_manim import *

from base import SceneCairo
from template import TransformMatchingShapesSameLocation, TransformMatchingTexColorHighlight
from constant import N_POINTS_THRESHOLD_AS_BOND


substrings_to_isolate = ['eth', 'ne']

key_map = {
    0: 0,
    1: 5,
    2: 6,
    3: 1,
    4: 2,
    5: 7,
    6: 8,
    8: 9,
    9: 10,
    10: 13,
    11: 14,
    12: 3,
    13: 11,
}


class AdditionReaction(SceneCairo):
    def get_numbering(self, mobject):
        numbering = VGroup()
        id_shape_map = 0
        for mobject in TransformMatchingShapes.get_mobject_parts(mobject):
            numbering.add(
                MarkupText(str(id_shape_map))
                .scale(0.5)
                .move_to(mobject.get_center())
                .set_color(RED if len(mobject.points) > N_POINTS_THRESHOLD_AS_BOND else GREEN)
            )
            id_shape_map += 1
            
        return numbering
    
    def add_numbering(self, mobject):
        numbering = self.get_numbering(mobject)
        self.add(numbering)
        self.wait(duration=2)
        self.remove(numbering)

    def add_keys(self, mobject: VGroup):
        id_shape_map = 0
        for i in range(len(mobject.submobjects)):
            for n in range(len(mobject[i].submobjects[0].submobjects)):
                mobject[i].submobjects[0].submobjects[n].key = id_shape_map
                id_shape_map += 1

    def construct(self):
        reactant = ChemObject('C(-[:225]H)(-[:135]H)=C(-[:-45]H)(-[:45]H)')
        title_prev = Tex('ethene', font_size=64, substrings_to_isolate=substrings_to_isolate).to_edge(UP)
        byreactant = ChemObject('H-H').to_edge(LEFT, buff=0.75)

        self.play(Create(reactant), Write(title_prev), run_time=1.5)
        self.play(Create(byreactant), run_time=1.0)
        self.wait(duration=0.5)

        reactants = VGroup(reactant, byreactant)
        # self.add_numbering(reactants)
        self.add_keys(reactants)

        title_next = Tex('ethane', font_size=64, substrings_to_isolate=substrings_to_isolate).to_edge(UP)
        product = ChemObject('C(-[:90]H)(-[:180]H)(-[:270]H)-C(-[:-90]H)(-[:0]H)(-[:90]H)')

        animations = [
            TransformMatchingTexColorHighlight(title_prev, title_next, fade_transform_mismatches=True),
            TransformMatchingShapesSameLocation(reactants, product, key_map=key_map, min_ratio_possible_match=0.1, min_ratio_to_accept_match=0.1),
        ]
        self.wait(duration=1)
        self.play(*animations, run_time=1.5)
        # self.add_numbering(product)

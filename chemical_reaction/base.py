from chanim_manim import *

from template import (
    construct_chemobject, 
    construct_chemobject_animation, 
    TransformMatchingShapesSameLocation, 
    TransformMatchingTexColorHighlight,
)
from constant import N_POINTS_THRESHOLD_AS_BOND


class SceneCairo(Scene):
    # Two D Manim Chemistry objects require Cairo renderer
    config.renderer = "cairo"


def create_molecule_classes(molecule_and_chemcodes, module_name):
    """
    Create individual molecule classes dynamically and return a dictionary of class names to class objects.
    """
    classes = {}
    for i, chemcodes in enumerate(molecule_and_chemcodes):
        class_name = f"{i+1:02d}_" + ''.join(
            map(lambda x: x.capitalize().replace(',', '').replace(' ', ''), chemcodes[-1][0].split('-'))
        )
        created_class = type(class_name, (SceneCairo,), {'construct': construct_chemobject})
        created_class.chemcodes = chemcodes
        created_class.add_numbering = True
        created_class.animation = False
        created_class.__module__ = module_name
        classes[class_name] = created_class
    return classes


def create_chain_of_reactions_class(
    title, molecule_and_chemcodes, enzymes, by_reactants_products, 
    molecules_parts_to_separate, substrings_to_isolate, key_maps, module_name
):
    """
    Dynamically create the main class with the specified attributes and return it.
    """
    created_class = type(
        title, 
        (SceneCairo,), 
        {
            'construct': construct_chemobject_animation,
            'molecules': molecule_and_chemcodes,
            'enzymes': enzymes,
            'by_reactants_products': by_reactants_products,
            'molecules_parts_to_separate': molecules_parts_to_separate,
            'substrings_to_isolate': substrings_to_isolate,
            'key_maps': key_maps
        }
    )
    created_class.__module__ = module_name
    return created_class


def create_Scenes(title, molecules, chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate, key_maps, module_name):
    """
    Create individual molecule classes and the main class dynamically and return them.
    """
    molecule_and_chemcodes = []
    for molecule, chemcode in zip(molecules, chemcodes):
        molecule_and_chemcodes.append(list(zip(molecule, chemcode)))

    molecule_classes = create_molecule_classes(molecule_and_chemcodes, module_name)
    main_class = create_chain_of_reactions_class(
        title, molecule_and_chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate, key_maps, module_name
    )
    return molecule_classes, main_class


class ReactioinBase(SceneCairo):
    molecules = []
    chemcodes = []
    byreactants = []
    byproducts = []
    substrings_to_isolate = []
    key_map = {}
    numbering = False
    
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

    def add_keys(self, mobject: VMobject):
        id_shape_map = 0

        def _add_keys(mobject: VMobject):
            nonlocal id_shape_map

            if isinstance(mobject, VGroup):
                for mob in mobject:
                    _add_keys(mob)
            else:
                for submob in mobject.submobjects[0].submobjects:
                    submob.key = id_shape_map
                    id_shape_map += 1
                    
        _add_keys(mobject)

    def build_chem_group(self, mobjects: list[VMobject], arrange_direction=DOWN, arrange_buff=0.5, edge=LEFT, edge_buff=0.75):
        group = VGroup()
        for mobject in mobjects:
            group.add(ChemObject(mobject))
        group.arrange(arrange_direction, buff=arrange_buff).to_edge(edge, buff=edge_buff)
        
        return group

    def construct(self):
        title_reactant = Tex(self.molecules[0], font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
        reactant = ChemObject(self.chemcodes[0])
        byreactants_group = self.build_chem_group(self.byreactants, edge=LEFT, edge_buff=0.75)
        reactants = VGroup(reactant, byreactants_group)

        if self.numbering:
            self.add_numbering(reactants)
        self.add_keys(reactants)

        self.play(Create(reactant), Write(title_reactant), run_time=1.5)
        self.play(Create(byreactants_group), run_time=1.0)
        self.wait(duration=0.5)

        title_product = Tex(self.molecules[1], font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
        product = ChemObject(self.chemcodes[1])
        byproducts_group = self.build_chem_group(self.byproducts, edge=RIGHT, edge_buff=0.75)
        products = VGroup(product, byproducts_group)

        animations = [
            TransformMatchingTexColorHighlight(title_reactant, title_product, fade_transform_mismatches=True),
            TransformMatchingShapesSameLocation(reactants, products, key_map=self.key_map, min_ratio_possible_match=0.1, min_ratio_to_accept_match=0.1),
        ]
        self.wait(duration=1)
        self.play(*animations, run_time=1.5)

        if self.numbering:
            self.add_numbering(products)


def create_reaction_classes(reactions, module_name):
    """
    Create individual molecule classes dynamically and return a dictionary of class names to class objects.
    """
    classes = {}
    for i, reaction in enumerate(reactions):
        class_name = f"{i+1:02d}_" + reaction['title']
        created_class = type(class_name, (ReactioinBase,), {})
        created_class.molecules = reaction['molecules']
        created_class.chemcodes = reaction['chemcodes']
        created_class.byreactants = reaction['byreactants']
        created_class.byproducts = reaction['byproducts']
        created_class.substrings_to_isolate = reaction['substrings_to_isolate']
        created_class.key_map = reaction['key_map']

        created_class.__module__ = module_name
        classes[class_name] = created_class
    return classes

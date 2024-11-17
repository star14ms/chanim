from manim import Scene, config

from template import construct_chemobject, construct_chemobject_animation


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


def create_main_class(
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
    main_class = create_main_class(
        title, molecule_and_chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate, key_maps, module_name
    )
    return molecule_classes, main_class

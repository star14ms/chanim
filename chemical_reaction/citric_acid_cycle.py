# Main Command: manim chemical_reaction/citric_acid_cycle.py CitricAcidCycle
from pathlib import Path
from rich import print

from template import SceneCairo, construct_mmolecule, construct_mmolecule_animation


title = 'CitricAcidCycle'

script_path = Path(__file__).absolute().parent.parent
files_path = script_path / "data/citric_acid_cycle"
font = 'Comic Sans MS'

molecules = [
    ('oxaloacetate',),
    ('citrate',),
    ('isocitrate',),
    ('alpha-ketoglutarate',),
    ('succinyl-CoA',),
    ('succinate',),
    ('fumarate',),
    ('malate',),
    ('oxaloacetate',),
]

substrings_to_isolate = ['ate', 'citrate', 'succin']

enzymes = [
    'citrate synthase',
    'aconitase',
    'isocitrate dehydrogenase',
    'alpha-ketoglutarate dehydrogenase', # ɑ-ketoglutarate dehydrogenase
    'succinyl-CoA synthetase',
    'succinate dehydrogenase',
    'fumarase',
    'malate dehydrogenase',
]

by_reactants_products = [
    (('H2O',), ('',)),
    (),
    (('NAD+', 'CO2'), ('NADH', '')),
    (('NAD+', 'CO2', 'coenzyme A'), ('NADH', '', '')),
    (('GDP', 'Pi', ''), ('GTP', '', 'coenzyme A')), # Pᵢ
    (('FAD',), ('FADH2',)),
    (('H2O',), ('',)),
    (('NAD+', 'H2O'), ('NADH', '')),
]

molecules_parts_to_separate = {}


for i, molecule in enumerate(molecules):
    class_name = str(i+1) + '_' + ''.join(map(lambda x: x.capitalize().replace(',', '').replace(' ', ''), molecule[-1].split('-')))

    globals()[class_name] = type(class_name, (SceneCairo,), {'construct': construct_mmolecule})
    globals()[class_name].files_path = files_path
    globals()[class_name].molecule = molecule[-1]


def create_class(title, base_class, files_path, molecules, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate):

    # Create the class dynamically
    return type(title, (base_class,), {
        'construct': construct_mmolecule_animation, 
        'files_path': files_path, 
        'molecules': molecules, 
        'enzymes': enzymes, 
        'by_reactants_products': by_reactants_products, 
        'molecules_parts_to_separate': molecules_parts_to_separate, 
        'substrings_to_isolate': substrings_to_isolate
    })


# Create and assign the class to globals
globals()[title] = create_class(title, SceneCairo, files_path, molecules, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate)

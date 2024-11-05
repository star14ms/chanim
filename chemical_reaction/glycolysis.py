# Main Command: manim chemical_reaction/glycolysis.py Glycolysis
import sys, os
sys.path.append(os.path.abspath('.'))

from chanim_manim import ChemWithName

from pathlib import Path
from rich import print

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from template import SceneCairo, construct_chemobject, construct_chemobject_animation


title = 'Glycolysis'

script_path = Path(__file__).absolute().parent.parent
files_path = script_path / "data/glycolysis"
font = 'Comic Sans MS'

molecules = [
    ('glucose',),
    ('glucose-6-phosphate',),
    ('fructose-6-phosphate',),
    ('fructose-1,6-bisphosphate',),
    ('glyceraldehyde-3-phosphate', 'dihydroxyacetone phosphate'),
    ('glyceraldehyde-3-phosphate', 'glyceraldehyde-3-phosphate'),
    ('1,3-bisphosphoglycerate',),
    ('3-phosphoglycerate',),
    ('2-phosphoglycerate',),
    ('phosphoenolpyruvate',),
    ('pyruvate',),
]
mmolecules = [
    ChemWithName("*6((>HO)-(>:OH)-(>OH)-(>:OH)-(>C-[:150]HO)-O-)", "glucose", premables=['\hflipnext']),
    ChemWithName("*6((>HO)-(>:OH)-(>OH)-(>:OH)-(>C-[:150]O-P(-[:0]O)(=[:180]O)-O)-O-)", "glucose-6-phosphate", premables=['\hflipnext']),
]

substrings_to_isolate = ['glucose', 'fructose', 'phosphate', 'phospho', 'glycer', 'pyruvate']

enzymes = [
    'hexokinase',
    'phosphoglucose isomerase',
    'phosphofructokinase',
    'aldolase',
    'triose phosphate isomerase',
    'glyceraldehyde-3-phosphate dehydrogenase',
    'phosphoglycerate kinase',
    'phosphoglyceromutase',
    'enolase',
    'pyruvate kinase',
]

by_reactants_products = [
    (('ATP',), ('ADP',)),
    (),
    (('ATP',), ('ADP',)),
    (),
    (),
    (('NAD+','Pi'), ('NADH','')),
    (('ADP',), ('ATP',)),
    (),
    (),
    (('ADP',), ('ATP',)),
]

molecules_parts_to_separate = {
    'fructose-1,6-bisphosphate': [
        {'bonds': (0, 1, 2, 3, 8, 10, 11, 12, 13, 17), 'atoms': (1, 4, 5, 7, 9, 10, 11, 15, 16, 19)},
        {'bonds': (4, 5, 6, 7, 9, 14, 15, 16, 18, 19), 'atoms': (2, 3, 6, 8, 12, 13, 14, 17, 18, 20)},
    ]
}


for i, (molecule, mmolecule) in enumerate(zip(molecules, mmolecules)):
    class_name = str(i+1) + '_' + ''.join(map(lambda x: x.capitalize().replace(',', '').replace(' ', ''), molecule[-1].split('-')))

    globals()[class_name] = type(class_name, (SceneCairo,), {'construct': construct_chemobject})
    globals()[class_name].chem_object = mmolecule
    globals()[class_name].add_numbering = False
    globals()[class_name].animation = False

def create_class(title, base_class, files_path, molecules, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate):

    # Create the class dynamically
    return type(title, (base_class,), {
        'construct': construct_chemobject_animation, 
        'files_path': files_path, 
        'molecules': molecules, 
        'enzymes': enzymes, 
        'by_reactants_products': by_reactants_products, 
        'molecules_parts_to_separate': molecules_parts_to_separate, 
        'substrings_to_isolate': substrings_to_isolate
    })


# Create and assign the class to globals
globals()[title] = create_class(title, SceneCairo, files_path, mmolecules, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate)

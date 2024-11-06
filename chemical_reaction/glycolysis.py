# Main Command: manim -p chemical_reaction/glycolysis.py Glycolysis
import sys, os
sys.path.append(os.path.abspath('.'))

from template import SceneCairo, construct_chemobject, construct_chemobject_animation


title = 'Glycolysis'
font = 'Comic Sans MS'

molecules = [
    ['glucose'],
    ['glucose-6-phosphate'],
    ['fructose-6-phosphate'],
    ['fructose-1,6-bisphosphate'],
    ['glyceraldehyde-3-phosphate', 'dihydroxyacetone phosphate'],
    ['glyceraldehyde-3-phosphate', 'glyceraldehyde-3-phosphate'],
    ['1,3-bisphosphoglycerate'],
    ['3-phosphoglycerate'],
    ['2-phosphoglycerate'],
    ['phosphoenolpyruvate'],
    ['pyruvate'],
]
chemcodes = [
    ['*6((<HO)-(<:OH)-(<OH)-(<:OH)-(<-[:150]HO)-O-)'],
    ['*6((<HO)-(<:OH)-(<OH)-(<:OH)-(<-[:150]O-P(-[:0]O)(=[:180]O)-O)-O-)'],
    ['[:18]*5((<-[:198,,,,line width=7pt]HO)(<:HO)-(<OH)-(<:OH)-(<-[:150]O-P(-[:0]O)(=[:180]O)-O)-O-)'],
    ['[:18]*5((<-[:198,,,,line width=7pt]O-[:180]P(-[:90]O)(=[:-90]O)-[:180]O)(<:HO)-(<OH)-(<:OH)-(<-[:150]O-P(-[:0]O)(=[:180]O)-O)-O-)'],
    ['*6((=O)-(<OH)-(-O-[:30]P(=[:120]O)(-[:-60]O)-[:30]O))', '*6((-OH)-(=O)-(-O-[:30]P(=[:120]O)(-[:-60]O)-[:30]O))'],
    ['*6((=O)-(<OH)-(-O-[:30]P(=[:120]O)(-[:-60]O)-[:30]O))', '*6((=O)-(<OH)-(-O-[:30]P(=[:120]O)(-[:-60]O)-[:30]O))'],
    ['[:-30]*6(O(-[:180]P(-[:90]O)(=[:-90]O)-[:180]O)-(=O)-(-OH)-(-O-[:60]P(=[:150]O)(-[:-30]O)-[:60]O))'],
    ['[:-30]*6(HO-(=O)-(-OH)-(-O-[:60]P(=[:150]O)(-[:-30]O)-[:60]O))'],
    ['[:-30]*6(HO-(=O)-(-O-[:0]P(-[:-90]O)(=[:90]O)-[:0]O)-(-OH))'],
    ['[:-30]*6(HO-(=O)-(-O-[:0]P(-[:-90]O)(=[:90]O)-[:0]O)=)'],
    ['[:-30]*6(HO-(=O)-(-O)=)'],
]

substrings_to_isolate = ['glucose', 'fructose', 'phosph', 'glycer', 'pyruvate', 'A', 'T', 'P', 'D', '3-']

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
    (('',),('H2O',)),
    (('ADP',), ('ATP',)),
]

molecules_parts_to_separate = {
    'fructose-1,6-bisphosphate': [
        {'bonds': (27, 28, 29, 30, 31, 32, 33, 34, 36, 38, 40, 42, 43, 45, 47), 'atoms': (25, 26, 35, 37, 39, 41, 44, 46)},
        {'bonds': (0, 2, 4, 6, 8, 9, 11, 13, 14, 15, 16, 17, 18, 20, 23, 24, 48), 'atoms': (1, 3, 5, 7, 10, 12, 19, 21, 22)},
    ]
}

key_maps = {
    'fructose-1,6-bisphosphate': {
        'glyceraldehyde-3-phosphate': {
            0: 7,
            1: 8,
            2: 9,
            3: 10,
            4: 11,
            5: 15,
            6: 16,
            7: 12,
            8: 13,
            9: 14,
            10: 17,
            11: 18,
            12: 4,
            18: 6,
            19: 5,
            20: 3,
            21: 0,
            23: 2,
            23: 1,
        },
        'dihydroxyacetone phosphate': {
            25: 0,
            26: 2,
            32: 1,
            33: 3,
            34: 7,
            35: 8,
            36: 9,
            37: 10,
            38: 11,
            39: 15,
            40: 16,
            41: 12,
            42: 13,
            43: 14,
            44: 17,
            45: 18,
            46: 4,
            47: 5,
            # 47: 6,
        }
    },
    'glyceraldehyde-3-phosphate': {
        '1,3-bisphosphoglycerate': {
            0: 11,
            1: 12,
            2: 13,
            3: 14,
            4: 15,
            5: 16,
            6: 17,
            7: 18,
            8: 19,
            9: 20,
            10: 21,
            11: 22,
            12: 23,
            13: 24,
            14: 25,
            15: 26,
            16: 27,
            17: 28,
            18: 29,
        },
    },
}

molecule_and_chemcodes = []
for molecule, chemcode in zip(molecules, chemcodes):
    molecule_and_chemcodes.append(list(zip(molecule, chemcode)))


for i, chemcodes in enumerate(molecule_and_chemcodes):
    class_name = str(i+1) + '_' + ''.join(map(lambda x: x.capitalize().replace(',', '').replace(' ', ''), chemcodes[-1][0].split('-')))

    globals()[class_name] = type(class_name, (SceneCairo,), {'construct': construct_chemobject})
    globals()[class_name].chemcodes = chemcodes
    globals()[class_name].add_numbering = True
    globals()[class_name].animation = False

def create_class(title, base_class, molecule_and_chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate, key_maps):

    # Create the class dynamically
    return type(title, (base_class,), {
        'construct': construct_chemobject_animation, 
        'molecules': molecule_and_chemcodes, 
        'enzymes': enzymes, 
        'by_reactants_products': by_reactants_products, 
        'molecules_parts_to_separate': molecules_parts_to_separate, 
        'substrings_to_isolate': substrings_to_isolate,
        'key_maps': key_maps
    })


# Create and assign the class to globals
globals()[title] = create_class(title, SceneCairo, molecule_and_chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate, key_maps)

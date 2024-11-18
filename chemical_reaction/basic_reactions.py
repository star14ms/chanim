# Main Command: manim -p chemical_reaction/basic_reactions.py
import sys, os
sys.path.append(os.path.abspath('.'))

from base import create_reaction_classes

reactions = [
    {
        'title': 'Ethene2Ethane',
        'molecules': [
            'ethene',
            'ethane',
        ],
        'chemcodes': [
            'C(-[:225]H)(-[:135]H)=C(-[:-45]H)(-[:45]H)',
            'C(-[2]H)(-[4]H)(-[6]H)-C(-[6]H)(-[0]H)(-[2]H)',
        ],
        'byreactants': [
            'H-H',
        ],
        'byproducts': [
        ],
        'substrings_to_isolate': [
            'eth', 'ne'
        ],
        'key_map': {
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
        },
    },
    {
        'title': 'Benzene2Chlorobenzene',
        'molecules': [
            'benzene',
            'chlorobenzene',
        ],
        'chemcodes': [
            '**6(------)',
            '**6(----(-Cl)--)',
        ],
        'byreactants': [
            'Cl-Cl',
        ],
        'byproducts': [
            'HCl',
        ],
        'substrings_to_isolate': [
            'benzene'
        ],
        'key_map': {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 8,
            6: 9,
            7: 5,
            8: 6,
            9: 11,
            10: 12,
        },
    },
    {
        'title': 'PropeneToPropan2ol',
        'molecules': [
            'propene',
            'propan-2-ol',
        ],
        'chemcodes': [
            'C(-[4]H)(-[6]H)=C(-[6]H)-C(-H)(-[2]H)(-[6]H)',
            'C(-[2]H)(-[4]H)(-[6]H)-C(-[6]H)(-[2]OH)-C(-H)(-[2]H)(-[6]H)',
        ],
        'byreactants': [
            'HOH',
        ],
        'byproducts': [
        ],
        'substrings_to_isolate': [
            'prop', 'ene', 'ol', '-'
        ],
        'key_map': {
            0: 0,
            1: 3,
            2: 4,
            3: 5,
            4: 6,
            5: 7,
            6: 8,
            8: 9,
            9: 10,
            10: 14,
            11: 15,
            12: 16,
            13: 17,
            14: 18,
            15: 19,
            16: 20,
            17: 21,
            18: 1,
            19: 11,
            20: 12,
        },
    },
    {
        'title': 'Ether',
        'molecules': [
            'ethanol',
            'methoxyethane',
        ],
        'chemcodes': [
            'C(-[2]H)(-[4]HO)(-[6]H)-C(-[0]H)(-[2]H)(-[6]H)',
            'C(-[2]H)(-[4]H)(-[6]H)-O-C(-[2]H)(-[6]H)-C(-[0]H)(-[2]H)(-[6]H)',
        ],
        'byreactants': [
            'C(-[2]H)(-[4]H)(-[6]H)-OH'
        ],
        'byproducts': [
            'HOH'
        ],
        'substrings_to_isolate': [
            'eth', 'ol', 'meth', 'oxy', 'ane'
        ],
        'key_map': {
            0: 9,
            1: 11,
            2: 12,
            3: 7,
            4: 10,
            5: 25,
            6: 13,
            7: 14,
            8: 15,
            9: 16,
            10: 17,
            11: 18,
            12: 19,
            13: 20,
            14: 21,
            15: 22,
            16: 0,
            17: 1,
            18: 2,
            19: 3,
            20: 4,
            21: 5,
            22: 6,
            23: 24,
            24: 23,
        },
        'enzyme': 'H2SO4',
    }
]

molecule_classes = create_reaction_classes(reactions, __name__, numbering=False)
globals().update(molecule_classes)

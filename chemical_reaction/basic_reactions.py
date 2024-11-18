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
            'C(-[:90]H)(-[:180]H)(-[:270]H)-C(-[:-90]H)(-[:0]H)(-[:90]H)',
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
]

molecule_classes = create_reaction_classes(reactions, __name__)
globals().update(molecule_classes)

# Main Command: manim -p chemical_reaction/catecholamines.py Catecholamines_Synthesis
import sys, os
sys.path.append(os.path.abspath('.'))

from base import create_Scenes


title = 'Catecholamines_Synthesis'
font = 'Comic Sans MS'

molecules = [
    ['phenylalanine'],
    ['tyrosine'],
    ['dihydroxyphenylalanine'],
    ['dopamine'],
    ['norepinephrine\n(noradrenaline)'],
    ['epinephrine\n(adrenaline)'],
]
chemcodes = [
    ["[:180]*6((--[:-30](-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})-[:30](=[:90]O)-[:-30]\charge{45:1.5pt=$\scriptstyle-$}{O})=-=-=-)"],
    ["*6((-HO)-=-(--[:-30](-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})-[:30](=[:90]O)-[:-30]\charge{45:1.5pt=$\scriptstyle-$}{O})=-=)"],
    ["[:-60]*6((-HO)=(-HO)-=-(--[:-30](-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})-[:30](=[:90]O)-[:-30]\charge{45:1.5pt=$\scriptstyle-$}{O})=-)"],
    ["[:-60]*6((-HO)=(-HO)-=-(--[:-30]-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})=-)"],
    ["[:-60]*6((-HO)=(-HO)-=-(-(-[:90]OH)-[:-30]-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})=-)"],
    ["[:-60]*6((-HO)=(-HO)-=-(-(-[:90]OH)-[:-30]-[:30]\chemabove{N}{H}-[:-30]CH3)=-)"],
]

substrings_to_isolate = ['d', 'o', 'p', 'henyl', 'ine', 'hydr', 'tyros', 'nor', 'epinephr', 'hydro-', 'adrenal', '(', ')', 'ascorbate', 'adenosyl-', 'methion']

enzymes = [
    'phenylalanine hydroxylase',
    'tyrosine hydroxylase',
    'aromatic amino acid decarboxylase',
    'dopamine beta-monooxygenase',
    'phenylethanolamine N-methyltransferase',
]

by_reactants_products = [
    (('tetrahydro-', 'biopterin'), ('dihydro-', 'biopterin')),
    (('tetrahydro-', 'biopterin'), ('dihydro-', 'biopterin')),
    (('',), ('CO2',)),
    (('ascorbate', '(vitamin C)',), ('dehydroascorbate', '(vitamin C)')),
    (('S-adenosyl-', 'methionine'), ('S-adenosyl-', 'homocysteine')),
]

molecules_parts_to_separate = {}

key_maps = {}

molecule_classes, main_class = create_Scenes(title, molecules, chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate, key_maps, __name__)
globals().update(molecule_classes)

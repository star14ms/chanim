# Main Command: manim -p chemical_reaction/catecholamines.py Catecholamines_Synthesis
import sys, os
sys.path.append(os.path.abspath('.'))

from template import SceneCairo, construct_chemobject, construct_chemobject_animation


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

molecule_and_chemcodes = []
for molecule, chemcode in zip(molecules, chemcodes):
    molecule_and_chemcodes.append(list(zip(molecule, chemcode)))


for i, chemcodes in enumerate(molecule_and_chemcodes):
    class_name = str(i+1) + '_' + ''.join(map(lambda x: x.capitalize().replace(',', '').replace(' ', ''), chemcodes[-1][0].split('-')))

    globals()[class_name] = type(class_name, (SceneCairo,), {'construct': construct_chemobject})
    globals()[class_name].chemcodes = chemcodes
    globals()[class_name].add_numbering = True
    globals()[class_name].animation = False


def create_class(title, base_class, molecule_and_chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate):

    # Create the class dynamically
    return type(title, (base_class,), {
        'construct': construct_chemobject_animation, 
        'molecules': molecule_and_chemcodes, 
        'enzymes': enzymes, 
        'by_reactants_products': by_reactants_products, 
        'molecules_parts_to_separate': molecules_parts_to_separate, 
        'substrings_to_isolate': substrings_to_isolate
    })


# Create and assign the class to globals
globals()[title] = create_class(title, SceneCairo, molecule_and_chemcodes, enzymes, by_reactants_products, molecules_parts_to_separate, substrings_to_isolate)

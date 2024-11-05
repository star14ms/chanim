# Main Command: manim -p chemical_reaction/catecholamines.py Catecholamines_Synthesis
from chanim import ChemWithName

from pathlib import Path
from rich import print

from template import SceneCairo, construct_chemobject, construct_chemobject_animation


title = 'Catecholamines_Synthesis'

script_path = Path(__file__).absolute().parent.parent
files_path = script_path / "data/glycolysis"
font = 'Comic Sans MS'

molecules = [
    ('phenylalanine',),
    ('tyrosine',),
    ('dihydroxyphenylalanine',),
    ('dopamine',),
    ('norepinephrine,(noradrenaline)',),
    ('epinephrine,(adrenaline)',),
]
mmolecules = [
    ChemWithName("[:180]*6((--[:-30](-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})-[:30](=[:90]O)-[:-30]\charge{45:1.5pt=$\scriptstyle-$}{O})=-=-=-)", "phenylalanine"),
    ChemWithName("*6((-HO)-=-(--[:-30](-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})-[:30](=[:90]O)-[:-30]\charge{45:1.5pt=$\scriptstyle-$}{O})=-=)", "tyrosine"),
    ChemWithName("[:-60]*6((-HO)=(-HO)-=-(--[:-30](-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})-[:30](=[:90]O)-[:-30]\charge{45:1.5pt=$\scriptstyle-$}{O})=-)", "dihydroxyphenylalanine"),
    ChemWithName("[:-60]*6((-HO)=(-HO)-=-(--[:-30]-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})=-)", "dopamine"),
    ChemWithName("[:-60]*6((-HO)=(-HO)-=-(-(-[:90]OH)-[:-30]-[:-90]NH\charge{45:1.5pt=$\scriptstyle+$}{3})=-)", "norepinephrine,(noradrenaline)"),
    ChemWithName("[:-60]*6((-HO)=(-HO)-=-(-(-[:90]OH)-[:-30]-[:30]\chemabove{N}{H}-[:-30]CH3)=-)", "epinephrine,(adrenaline)"),
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


for i, (molecule, mmolecule) in enumerate(zip(molecules, mmolecules)):
    class_name = str(i+1) + '_' + ''.join(map(lambda x: x.capitalize().replace(',', '').replace(' ', ''), molecule[-1].split('-')))

    globals()[class_name] = type(class_name, (SceneCairo,), {'construct': construct_chemobject})
    globals()[class_name].chem_object = mmolecule
    globals()[class_name].add_numbering = True
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

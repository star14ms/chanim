# Main Command: manim chemical_reaction/glycolysis.py Glycolysis
from manim import Scene, config
from manim import *
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase
from chanim_manim import *

from collections import defaultdict, Counter
from svgelements.svgelements import Line
from copy import deepcopy
from rich import print
import numpy as np
import math


def match_atoms(atoms1, atoms2, atom1_idx, atom2_idx, atoms1_counters, atoms2_counters, depth=1):
    atom1_neighbors = atoms1_counters[atom1_idx]
    atom2_neighbors = atoms2_counters[atom2_idx]
    atom1 = atoms1[atom1_idx]
    atom2 = atoms2[atom2_idx]
    
    if atom1_neighbors.get('H'):
        del atom1_neighbors['H']
    if atom2_neighbors.get('H'):
        del atom2_neighbors['H']
    
    matching_map = np.zeros([len(atom1.bond_to), len(atom2.bond_to)])
    
    if depth == 1:
        return atom1.element == atom2.element and atom1_neighbors == atom2_neighbors
    
    for i, (atom1_neighbor_idx, element1) in enumerate(atom1.bond_to.items()):
        for j, (atom2_neighbor_idx, element2) in enumerate(atom2.bond_to.items()):
            if element1 == element2 and match_atoms(atoms1, atoms2, atom1_neighbor_idx, atom2_neighbor_idx, atoms1_counters, atoms2_counters, depth-1):
                    matching_map[i, j] = 1

    # TODO: Prevent the same atom to be matched with multiple atoms
    for i in range(len(atom1.bond_to)):
        if not np.any(matching_map[i]):
            return False
    for j in range(len(atom2.bond_to)):
        if not np.any(matching_map.T[j]):
            return False
        
    return True


def match_bonds(atoms1, atoms2, bonds1, bonds2, bond1_idx, bond2_idx, atoms1_counters, atoms2_counters, matching_level):
    bond1 = bonds1[bond1_idx]
    bond2 = bonds2[bond2_idx]

    bonds1_atom1 = bonds1[bond1_idx].from_atom
    bonds1_atom2 = bonds1[bond1_idx].to_atom
    bonds2_atom1 = bonds2[bond2_idx].from_atom
    bonds2_atom2 = bonds2[bond2_idx].to_atom
    
    bonds1_atom1_element = bonds1_atom1.element[0]
    bonds1_atom2_element = bonds1_atom2.element[0]
    bonds2_atom1_element = bonds2_atom1.element[0]
    bonds2_atom2_element = bonds2_atom2.element[0]

    if matching_level == 2 or matching_level >= 4:
        bonds1_atom1_neighbors = atoms1_counters[bond1.from_atom.index]
        bonds1_atom2_neighbors = atoms1_counters[bond1.to_atom.index]
        bonds2_atom1_neighbors = atoms2_counters[bond2.from_atom.index]
        bonds2_atom2_neighbors = atoms2_counters[bond2.to_atom.index]
        
        # for removed_atom in removed_atoms:
        #     if removed_atom in bonds1_atom1_neighbors:
        #         del bonds1_atom2_neighbors[removed_atom]
        #     if removed_atom in bonds1_atom2_neighbors:
        #         del bonds1_atom2_neighbors[removed_atom]
        
        if bonds1_atom1_neighbors.get('H'):
            del bonds1_atom1_neighbors['H']
        if bonds1_atom2_neighbors.get('H'):
            del bonds1_atom2_neighbors['H']
        if bonds2_atom1_neighbors.get('H'):
            del bonds2_atom1_neighbors['H']
        if bonds2_atom2_neighbors.get('H'):
            del bonds2_atom2_neighbors['H']
                
    def is_neighbor_matched(atom1, atom2, atoms1_counters, atoms2_counters, depth):
        matching_map = np.zeros((len(atom1.bond_to), len(atom2.bond_to)))
        for i, atom1_neighbor_idx in enumerate(atom1.bond_to.keys()):
            for j, atom2_neighbor_idx in enumerate(atom2.bond_to.keys()):
                if match_atoms(atoms1, atoms2, atom1_neighbor_idx, atom2_neighbor_idx, atoms1_counters, atoms2_counters, depth):
                    matching_map[i, j] = 1
        for i in range(len(atom1.bond_to)):
            if not np.any(matching_map[i]):
                return False
        for j in range(len(atom2.bond_to)):
            if not np.any(matching_map.T[j]):
                return False
        return True
    
    if matching_level == 1:
        if bonds1_atom1_element == bonds2_atom1_element or bonds1_atom1_element == bonds2_atom2_element:
            return True
        if bonds1_atom2_element == bonds2_atom1_element or bonds1_atom2_element == bonds2_atom2_element:
            return True
        return False
    elif matching_level == 2:
        if (bonds1_atom1_element == bonds2_atom1_element and bonds1_atom1_neighbors == bonds2_atom1_neighbors) or \
            (bonds1_atom1_element == bonds2_atom2_element and bonds1_atom1_neighbors == bonds2_atom2_neighbors):
            return True
        if (bonds1_atom2_element == bonds2_atom1_element and bonds1_atom2_neighbors == bonds2_atom1_neighbors) or \
            (bonds1_atom2_element == bonds2_atom2_element and bonds1_atom2_neighbors == bonds2_atom2_neighbors):
            return True
        return False
    elif matching_level == 3:
        if (
            (bonds1_atom1_element == bonds2_atom1_element and bonds1_atom2_element == bonds2_atom2_element) or \
            (bonds1_atom1_element == bonds2_atom2_element and bonds1_atom2_element == bonds2_atom1_element)
        ) and bond1.type == bond2.type:
            return True
        return False
    elif matching_level == 4:
        if bonds1_atom1_element == bonds2_atom1_element and bonds1_atom2_element == bonds2_atom2_element and bond1.type == bond2.type and \
            bonds1_atom1_neighbors == bonds2_atom1_neighbors and bonds1_atom2_neighbors == bonds2_atom2_neighbors:
            return True
        if bonds1_atom1_element == bonds2_atom2_element and bonds1_atom2_element == bonds2_atom1_element and bond1.type == bond2.type and \
            bonds1_atom1_neighbors == bonds2_atom2_neighbors and bonds1_atom2_neighbors == bonds2_atom1_neighbors:
            return True
        return False
    elif matching_level >= 5:
        if (bonds1_atom1_element == bonds2_atom1_element and bonds1_atom2_element == bonds2_atom2_element) and bond1.type == bond2.type and \
            (bonds1_atom1_neighbors == bonds2_atom1_neighbors and bonds1_atom2_neighbors == bonds2_atom2_neighbors) and \
            is_neighbor_matched(bonds1_atom1, bonds2_atom1, atoms1_counters, atoms2_counters, depth=matching_level-4) and \
            is_neighbor_matched(bonds1_atom2, bonds2_atom2, atoms1_counters, atoms2_counters, depth=matching_level-4):
                return True

        if (bonds1_atom1_element == bonds2_atom2_element and bonds1_atom2_element == bonds2_atom1_element) and bond1.type == bond2.type and \
            (bonds1_atom1_neighbors == bonds2_atom2_neighbors and bonds1_atom2_neighbors == bonds2_atom1_neighbors) and \
            is_neighbor_matched(bonds1_atom1, bonds2_atom2, atoms1_counters, atoms2_counters, depth=matching_level-4) and \
            is_neighbor_matched(bonds1_atom2, bonds2_atom1, atoms1_counters, atoms2_counters, depth=matching_level-4):
                return True
        return False


def match_molecules(molecule1, molecule2, limited_part=None, matching_level=10, verbose=False):
    '''
    # Guideline of the bond matching 
    ### 1: One atom forming a bond is same as an atom forming a bond in another molecule
    ### 2: 1 + Whose neibor atoms are also matched
    ### 3: Two atoms forming a bond is same as two atoms forming a bond in another molecule
    ### 4: 3 + Whose neibor atoms are also matched
    ### 5: 4 + Whose neibor's neibor atoms are also matched
    '''
    atoms1, _  = molecule1.get_atoms()
    bonds1 = molecule1.get_bonds()
    atoms2, _ = molecule2.get_atoms()
    bonds2 = molecule2.get_bonds()
    
    atoms1_dict = defaultdict(list)
    atoms1_counters = defaultdict(dict)
    atoms2_dict = defaultdict(list)
    atoms2_counters = defaultdict(dict)

    for i in range(len(atoms1)):
        if limited_part is not None and i+1 not in limited_part['atoms']:
            continue
        atoms1_dict[atoms1[i+1].element].append(i+1)
        atoms1_counters[i+1] = Counter(atoms1[i+1].bond_to.values())
    for j in range(len(atoms2)):
        atoms2_dict[atoms2[j+1].element].append(j+1)
        atoms2_counters[j+1] = Counter(atoms2[j+1].bond_to.values())

    # removed_atoms = set(atoms1_dict.keys()) ^ set(atoms2_dict.keys())
    atoms1_undefined_dict = deepcopy(atoms1_dict)
    atoms2_undefined_dict = deepcopy(atoms2_dict)
    # print(atoms1_undefined_dict)
    # print(atoms2_undefined_dict)

    bonds1_idxs = list(range(len(bonds1)) if limited_part is None else limited_part['bonds'])
    bonds2_idxs = list(range(len(bonds2)))
    matched_bonds = list()
    matched_atoms = list()

    while True:
        bonds1_idxs_temp = deepcopy(bonds1_idxs)
        bonds2_idxs_temp = deepcopy(bonds2_idxs)
        progress_flag = False
        
        for bond1_idx in bonds1_idxs_temp: # For each bond, find the corresponding bond of another molecule 
            bond1_atom1 = bonds1[bond1_idx].from_atom
            bond1_atom2 = bonds1[bond1_idx].to_atom
            
            bonds2_idxs_temp = deepcopy(bonds2_idxs)

            same_bonds_idxs = []
            for bond2_idx in bonds2_idxs_temp:
                is_matched = match_bonds(atoms1, atoms2, bonds1, bonds2, bond1_idx, bond2_idx, atoms1_counters, atoms2_counters, matching_level)

                if is_matched:
                    same_bonds_idxs.append(bond2_idx)

            if len(same_bonds_idxs) > 1:
                if len(matched_atoms) > 1:
                    # distances_from_matched_atom = [distance_nd(atoms1[matched_atoms[0][0]].coords, bonds1[bond1_idx].from_atom.coords) - distance_nd(atoms2[matched_atoms[0][1]].coords, bonds2[same_bonds_idx].from_atom.coords) for same_bonds_idx in same_bonds_idxs]
                    cos_similarities = [cos_similarity(np.array(atoms1[matched_atoms[0][0]].coords)-np.array(bonds1[bond1_idx].from_atom.coords), np.array(atoms2[matched_atoms[0][1]].coords)-np.array(bonds2[same_bonds_idx].from_atom.coords)) for same_bonds_idx in same_bonds_idxs]
                    # cos_similarities_passed = [1 for cos_similarity in cos_similarities if cos_similarity > 0.9999] # len(cos_similarities_passed) == 1
                    if max(cos_similarities) > 0.9999: # min(distances_from_matched_atom) < 0.0001 and cos_similarities_passed
                        idx_min_distance = np.argmax(cos_similarities)
                        same_bonds_idxs = [same_bonds_idxs[idx_min_distance]]

            if len(same_bonds_idxs) == 1:
                progress_flag = True

                bond2_idx = same_bonds_idxs[0]
                bond2_atom1 = bonds2[bond2_idx].from_atom
                bond2_atom2 = bonds2[bond2_idx].to_atom
                if (bond1_idx, bond2_idx) not in matched_bonds:
                    matched_bonds.append((bond1_idx, bond2_idx))

                if verbose:
                    bond1 = bond1_atom1.element + ('-' if bonds1[bond1_idx].type == 1 else '=') + bond1_atom2.element
                    bond2 = bond2_atom1.element + ('-' if bonds2[bond2_idx].type == 1 else '=') + bond2_atom2.element
                    if bond1 != bond2:
                        bond1 = bond1 + ' ' + bond2
                    print(f'{bond1} bonds matched | bond1: {bond1_idx}, bond2: {bond2_idx}, matching_distance:', max(matching_level-3, 0))

                molecule1_atom1_element_list = atoms1_undefined_dict[bond1_atom1.element]
                molecule1_atom2_element_list = atoms1_undefined_dict[bond1_atom2.element]
                molecule2_atom1_element_list = atoms2_undefined_dict[bond2_atom1.element]
                molecule2_atom2_element_list = atoms2_undefined_dict[bond2_atom2.element]
                
                bonds1_idxs.remove(bond1_idx)
                bonds2_idxs.remove(bond2_idx)

                if bond1_atom1.index in molecule1_atom1_element_list:
                    molecule1_atom1_element_list.remove(bond1_atom1.index)
                if bond1_atom2.index in molecule1_atom2_element_list:
                    molecule1_atom2_element_list.remove(bond1_atom2.index)
                if bond2_atom1.index in molecule2_atom1_element_list:
                    molecule2_atom1_element_list.remove(bond2_atom1.index)
                if bond2_atom2.index in molecule2_atom2_element_list:
                    molecule2_atom2_element_list.remove(bond2_atom2.index)

                if bond1_atom1.element == bond2_atom1.element:
                    if (bond1_atom1.index, bond2_atom1.index) not in matched_atoms:
                        matched_atoms.append((bond1_atom1.index, bond2_atom1.index))
                    if (bond1_atom2.index, bond2_atom2.index) not in matched_atoms:
                        matched_atoms.append((bond1_atom2.index, bond2_atom2.index))
                elif bond1_atom1.element == bond2_atom2.element:
                    if (bond1_atom1.index, bond2_atom2.index) not in matched_atoms:
                        matched_atoms.append((bond1_atom1.index, bond2_atom2.index))
                    if (bond1_atom2.index, bond2_atom1.index) not in matched_atoms:
                        matched_atoms.append((bond1_atom2.index, bond2_atom1.index))

        # print(matched_atoms)
        # print(matched_bonds)
        # print(atoms1_undefined_dict)
        # print(atoms2_undefined_dict)
        # print('matching_level:', matching_level)

        if progress_flag == False:
            if matching_level == 1:
                break
            matching_level -= 1
    
    # Match the undefined atoms (H atoms)
    if len(atoms1_undefined_dict['H']) != 0 and len(atoms2_undefined_dict['H']) != 0:
        for atom1_matched_idx, atom2_matched_idx in matched_atoms[:]:
            if not ('H' in set(atoms1[atom1_matched_idx].bond_to.values()) and 'H' in set(atoms2[atom2_matched_idx].bond_to.values())):
                continue

            distances_atoms1 = [distance_nd(atoms1[atom1_idx].coords, atoms1[atom1_matched_idx].coords) for atom1_idx in atoms1_undefined_dict['H']]
            distances_atoms2 = [distance_nd(atoms2[atom2_idx].coords, atoms2[atom2_matched_idx].coords) for atom2_idx in atoms2_undefined_dict['H']]

            min_disatance_atom1_idx = np.argmin(distances_atoms1)
            min_disatance_atom2_idx = np.argmin(distances_atoms2)
            
            atom1_matched_idx = atoms1_undefined_dict['H'][min_disatance_atom1_idx]
            atom2_matched_idx = atoms2_undefined_dict['H'][min_disatance_atom2_idx]
            atoms1_undefined_dict['H'].remove(atom1_matched_idx)
            atoms2_undefined_dict['H'].remove(atom2_matched_idx)
            matched_atoms.append((atom1_matched_idx, atom2_matched_idx))

            if verbose:
                print('H atoms matched | atom1: {}, atom2: {}'.format(atom1_matched_idx, atom2_matched_idx))
                
            if atoms1_undefined_dict['H'] == [] or atoms2_undefined_dict['H'] == []:
                break
                    
    # print(atoms1_undefined_dict)
    # print(atoms2_undefined_dict)
    # print(matched_atoms)
    # print(matched_bonds)
    # breakpoint()

    matched_bonds = {str(k): str(v) for k, v in matched_bonds}
    matched_atoms = {'atom_'+str(k): 'atom_'+str(v) for k, v in matched_atoms}
    return {**matched_atoms, **matched_bonds}


class TransformMatchingShapesMMoleculeObject(TransformMatchingShapes):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        transform_mismatches: bool = False,
        fade_transform_mismatches: bool = False,
        key_map: dict | None = None,
        **kwargs,
    ):
        if isinstance(mobject, VMobject):
            group_type = VGroup
        else:
            group_type = Group

        source_map = self.get_shape_map(mobject)
        target_map = self.get_shape_map(target_mobject)

        if key_map is None:
            key_map = {}

        # Create two mobjects whose submobjects all match each other
        # according to whatever keys are used for source_map and
        # target_map
        transform_source = group_type()
        transform_target = group_type()
        kwargs["final_alpha_value"] = 0
        for key in set(source_map).intersection(target_map):
            transform_source.add(source_map[key])
            transform_target.add(target_map[key])
        anims = [Transform(transform_source, transform_target, **kwargs)]
        # User can manually specify when one part should transform
        # into another despite not matching by using key_map
        key_mapped_source = group_type()
        key_mapped_target = group_type()
        for key1, key2 in key_map.items():
            if key1 in source_map and key2 in target_map:
                key_mapped_source.add(source_map[key1])
                key_mapped_target.add(target_map[key2])
                source_map.pop(key1, None)
                target_map.pop(key2, None)
                
                sub_idx = 1
                while key1 + '-' + str(sub_idx) in source_map and key2 + '-' + str(sub_idx) in target_map:
                    key_mapped_source.add(source_map[key1 + '-' + str(sub_idx)])
                    key_mapped_target.add(target_map[key2 + '-' + str(sub_idx)])
                    source_map.pop(key1 + '-' + str(sub_idx), None)
                    target_map.pop(key2 + '-' + str(sub_idx), None)
                    sub_idx += 1

        if len(key_mapped_source) > 0:
            anims.append(
                FadeTransformPieces(key_mapped_source, key_mapped_target, **kwargs),
            )
        fade_source = group_type()
        fade_target = group_type()
        for key in set(source_map).difference(target_map):
            fade_source.add(source_map[key])
        for key in set(target_map).difference(source_map):
            fade_target.add(target_map[key])
        fade_target_copy = fade_target.copy()

        if transform_mismatches:
            if "replace_mobject_with_target_in_scene" not in kwargs:
                kwargs["replace_mobject_with_target_in_scene"] = True
            anims.append(Transform(fade_source, fade_target, **kwargs))
        elif fade_transform_mismatches:
            anims.append(FadeTransformPieces(fade_source, fade_target, **kwargs))
        else:
            anims.append(FadeOut(fade_source, target_position=fade_target, **kwargs))
            anims.append(
                FadeIn(fade_target_copy, target_position=fade_target, **kwargs),
            )

        super(TransformMatchingAbstractBase, self).__init__(*anims)

        self.to_remove = [mobject, fade_target_copy]
        self.to_add = target_mobject

    def get_shape_map(self, mobject: Mobject) -> dict:
        shape_map = {}
        atoms, bonds = mobject

        for atom in atoms:
            key = 'atom_' + str(atom.index)
            sub_idx = 0
            for sm in self.get_mobject_parts(atom):
                suffix = '-' + str(sub_idx := sub_idx + 1) if key in shape_map else ''
                shape_map[key + suffix] = sm

        for bond in bonds:
            key = str(bond.index)
            sub_idx = 0
            for sm in self.get_mobject_parts(bond):
                suffix = '-' + str(sub_idx := sub_idx + 1) if key in shape_map else ''
                shape_map[key + suffix] = sm

        return shape_map


class TransformMatchingShapesSameLocation(TransformMatchingShapes):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        transform_mismatches: bool = False,
        fade_transform_mismatches: bool = False,
        key_map: dict | None = None,
        **kwargs,
    ):
        if isinstance(mobject, VMobject):
            group_type = VGroup
        else:
            group_type = Group

        source_map = self.get_shape_map(mobject)
        target_map = self.get_shape_map(target_mobject)
        key_map = self.get_key_map(source_map, target_map)

        if key_map is None:
            key_map = {}

        # Create two mobjects whose submobjects all match each other
        # according to whatever keys are used for source_map and
        # target_map
        transform_source = group_type()
        transform_target = group_type()
        kwargs["final_alpha_value"] = 0
        for key in set(source_map).intersection(target_map):
            transform_source.add(source_map[key])
            transform_target.add(target_map[key])
        anims = [Transform(transform_source, transform_target, **kwargs)]
        # User can manually specify when one part should transform
        # into another despite not matching by using key_map
        key_mapped_source = group_type()
        key_mapped_target = group_type()
        # print(source_map)
        # print(target_map)
        # print(key_map)
        for key1, key2 in key_map.items():
            # print(key1, key1 in source_map, key2, key2 in target_map)
            if key1 in source_map and key2 in target_map:
                key_mapped_source.add(source_map[key1])
                key_mapped_target.add(target_map[key2])
                source_map.pop(key1, None)
                target_map.pop(key2, None)
                
                sub_idx = 1
                while key1 + '-' + str(sub_idx) in source_map and key2 + '-' + str(sub_idx) in target_map:
                    key_mapped_source.add(source_map[key1 + '-' + str(sub_idx)])
                    key_mapped_target.add(target_map[key2 + '-' + str(sub_idx)])
                    source_map.pop(key1 + '-' + str(sub_idx), None)
                    target_map.pop(key2 + '-' + str(sub_idx), None)
                    sub_idx += 1

        if len(key_mapped_source) > 0:
            anims.append(
                FadeTransformPieces(key_mapped_source, key_mapped_target, **kwargs),
            )
        fade_source = group_type()
        fade_target = group_type()
        # print(source_map)
        # print(target_map)
        for key in source_map:
            source_map[key].set_color('red') # added
            fade_source.add(source_map[key])
        for key in target_map:
            target_map[key].set_color('green') # added
            fade_target.add(target_map[key])
        fade_target_copy = fade_target.copy()

        if transform_mismatches:
            if "replace_mobject_with_target_in_scene" not in kwargs:
                kwargs["replace_mobject_with_target_in_scene"] = True
            anims.append(Transform(fade_source, fade_target, **kwargs))
        elif fade_transform_mismatches:
            anims.append(FadeTransformPieces(fade_source, fade_target, **kwargs))
        else:
            anims.append(FadeOut(fade_source, **kwargs))
            anims.append(
                FadeIn(fade_target_copy, **kwargs),
            )

        super(TransformMatchingAbstractBase, self).__init__(*anims)

        self.to_remove = [mobject, fade_target_copy]
        self.to_add = target_mobject
        
    def get_shape_map(self, mobject: Mobject) -> dict:
        shape_map = {}

        id_shape_map = 0
        for mobject in self.get_mobject_parts(mobject):
            n_points = len(mobject.points)

            key = ('atom_' if n_points > 8 else '') + str(id_shape_map) # not isinstance(mobject.path_obj[1], Line)
            shape_map[key] = mobject
            id_shape_map += 1

        return shape_map

    def get_key_map(self, source_map: Mobject, target_map: Mobject, only_using_identical_distances=True) -> dict:
        
        # Get possible distances between two molecules
        mobject_counter = Counter([len(sm.points) for sm in source_map.values()])
        target_mobject_counter = Counter([len(sm.points) for sm in target_map.values()])
        
        identical_n_points = []
        for key, value in mobject_counter.items():
            if value == 1 and target_mobject_counter.get(key) == 1:
                identical_n_points.append(key)

        distances_between_identical_mobjects = []
        for mobject_source in source_map.values():
            n_points = len(mobject_source.points)
            
            if only_using_identical_distances and n_points not in identical_n_points:
                continue

            for mobject_target in target_map.values():
                if len(mobject_target.points) == n_points:
                    # print(' '.join(map(lambda x: '%.6f' % x, mobject_target.get_center() - mobject_source.get_center())))
                    distances_between_identical_mobjects.append(mobject_target.get_center() - mobject_source.get_center())

        # match mobjects based on possible distances
        key_maps = []

        print('n_possible_distances', len(distances_between_identical_mobjects))
        for distance_xyz_identical in distances_between_identical_mobjects:
            key_map = {}
        
            for key_source, mobject_source in source_map.items():
                n_points = len(mobject_source.points)

                if key_source in key_map:
                    continue

                for key_target, mobject_target in target_map.items():
                    if key_target in key_map.values():
                        continue

                    distance_xyz = mobject_target.get_center() - mobject_source.get_center()

                    # if key_source == 'atom_20' and key_target == 'atom_20':
                    #     print(' '.join(map(lambda x: '%.6f' % x, mobject_target.get_center() - mobject_source.get_center())))
                    #     breakpoint()

                    if len(mobject_target.points) == n_points and len(mobject_target.path_obj) == len(mobject_source.path_obj) and \
                        ((n_points in identical_n_points) or (abs(distance_xyz[0] - distance_xyz_identical[0]) <= 0.0001 and abs(distance_xyz[1] - distance_xyz_identical[1]) <= 0.0001 and abs(distance_xyz[2] - distance_xyz_identical[2]) <= 0.0001)): 
                        # print(len(mobject_target.points), not isinstance(mobject_source.path_obj[1], Line))
                        key_map[key_source] = key_target
                        break
                    
            key_map_max_matching = max(key_maps, key=len) if len(key_maps) != 0 else {}

            if len(key_map_max_matching) >= 0.7 * len(source_map) or not only_using_identical_distances:
                for key_source, mobject_source in source_map.items():
                    n_points = len(mobject_source.points)

                    if key_source in key_map:
                        continue

                    for key_target, mobject_target in target_map.items():
                        if key_target in key_map.values():
                            continue

                        if len(mobject_target.points) == n_points and len(mobject_target.path_obj) == len(mobject_source.path_obj):
                            key_map[key_source] = key_target
                            break
                        
            key_maps.append(key_map)

        if len(key_map_max_matching) >= 0.7 * len(source_map) or not only_using_identical_distances:
            return key_map_max_matching if len(key_map_max_matching) != 0 else None
        else:
            return self.get_key_map(source_map, target_map, only_using_identical_distances=False)


class TransformMatchingTexColorHighlight(TransformMatchingTex):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        transform_mismatches: bool = False,
        fade_transform_mismatches: bool = False,
        key_map: dict | None = None,
        color_fadeout: str = 'red',
        color_fadein: str = 'green',
        **kwargs,
    ):
        if isinstance(mobject, VMobject):
            group_type = VGroup
        else:
            group_type = Group

        source_map = self.get_shape_map(mobject)
        target_map = self.get_shape_map(target_mobject)

        if key_map is None:
            key_map = {}

        # Create two mobjects whose submobjects all match each other
        # according to whatever keys are used for source_map and
        # target_map
        transform_source = group_type()
        transform_target = group_type()
        kwargs["final_alpha_value"] = 0
        for key in set(source_map).intersection(target_map):
            transform_source.add(source_map[key])
            transform_target.add(target_map[key])
        anims = [Transform(transform_source, transform_target, **kwargs)]
        # User can manually specify when one part should transform
        # into another despite not matching by using key_map
        key_mapped_source = group_type()
        key_mapped_target = group_type()
        # print(source_map, target_map)
        for key1, key2 in key_map.items():
            if key1 in source_map and key2 in target_map:
                key_mapped_source.add(source_map[key1])
                key_mapped_target.add(target_map[key2])
                source_map.pop(key1, None)
                target_map.pop(key2, None)
        if len(key_mapped_source) > 0:
            anims.append(
                FadeTransformPieces(key_mapped_source, key_mapped_target, **kwargs),
            )

        fade_source = group_type()
        fade_target = group_type()
        for key in set(source_map).difference(target_map):
            source_map[key].set_color(color_fadeout) ### set color
            fade_source.add(source_map[key])
        for key in set(target_map).difference(source_map):
            target_map[key].set_color(color_fadein) ### set color
            fade_target.add(target_map[key])
        fade_target_copy = fade_target.copy()

        if transform_mismatches:
            if "replace_mobject_with_target_in_scene" not in kwargs:
                kwargs["replace_mobject_with_target_in_scene"] = True
            anims.append(Transform(fade_source, fade_target, **kwargs))
        elif fade_transform_mismatches:
            anims.append(FadeTransformPieces(fade_source, fade_target, **kwargs))
        else:
            anims.append(FadeOut(fade_source, target_position=fade_target, **kwargs))
            anims.append(
                FadeIn(fade_target_copy, target_position=fade_target, **kwargs),
            )

        super(TransformMatchingAbstractBase, self).__init__(*anims)

        self.to_remove = [mobject, fade_target_copy]
        self.to_add = target_mobject


def distance_nd(vector1, vector2):
    """
    Calculate the Euclidean distance between two N-dimensional vectors.

    Args:
    vector1 (tuple or list): An iterable of floats representing the first vector.
    vector2 (tuple or list): An iterable of floats representing the second vector.

    Returns:
    float: The Euclidean distance between vector1 and vector2.
    """
    if len(vector1) != len(vector2):
        raise ValueError("Both vectors must have the same number of dimensions.")
    
    return math.sqrt(sum((x2 - x1) ** 2 for x1, x2 in zip(vector1, vector2)))


def cos_similarity(vector1, vector2):
    """
    Calculate the cosine similarity between two N-dimensional vectors.

    Args:
    vector1 (tuple or list): An iterable of floats representing the first vector.
    vector2 (tuple or list): An iterable of floats representing the second vector.

    Returns:
    float: The cosine similarity between vector1 and vector2.
    """
    if len(vector1) != len(vector2):
        raise ValueError("Both vectors must have the same number of dimensions.")
    
    dot_product = sum(x1 * x2 for x1, x2 in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(x ** 2 for x in vector1))
    magnitude2 = math.sqrt(sum(x ** 2 for x in vector2))
    
    return dot_product / (magnitude1 * magnitude2)


class SceneCairo(Scene):
    # Two D Manim Chemistry objects require Cairo renderer
    config.renderer = "cairo"


def construct_chemobject(self):
    numbering = VGroup()

    id_shape_map = 0
    for mobject in TransformMatchingShapes.get_mobject_parts(self.chem_object.chem):
        if self.add_numbering:
            numbering.add(
                MarkupText(str(id_shape_map))
                .scale(0.5)
                .move_to(mobject.get_center())
                .set_color(RED if len(mobject.points) > 8 else GREEN)
            )
        
        id_shape_map += 1

    if self.animation:
        self.play(self.chem_object.creation_anim())
        self.wait()
    else:
        self.add(self.chem_object)
        self.add(numbering)


def construct_chemobject_animation(self, verbose=False):
    if not isinstance(self.molecules[0], list):
        position_title = [UP]
        position_molecule = [ORIGIN]
        font_size = 64
    elif len(self.molecules[0]) == 2:
        position_title = [UL, UR]
        position_molecule = [LEFT, RIGHT]
        font_size = 48
        
    n_molecules = 1
    animations = []
    next_titles = []
    next_molecules = []
    for i, molecule in enumerate([self.molecules[0]]):
        title = VMobject()
        for title_line in molecule.name.tex_string.split(','):
            title.add(Tex(title_line, font_size=font_size, substrings_to_isolate=self.substrings_to_isolate))
        title.arrange(DOWN).to_edge(position_title[i])
        next_purural_sign = Tex('x{}'.format(n_molecules) if n_molecules > 1 else '', font_size=48).next_to(title, RIGHT)
        molecule = ChemObject(molecule.chem.tex_string).scale(0.8).to_edge(position_molecule[i])
        next_titles.append(title)
        next_molecules.append(molecule)
        animations.extend([Write(title), Write(next_purural_sign), Create(molecule)])
        break

    self.play(*animations, run_time=1.5)
    self.wait(duration=0.5)

    for i, (molecule, enzyme, byreaction) in enumerate(zip(self.molecules[1:], self.enzymes, self.by_reactants_products)):
        next_enzyme = Tex(enzyme, font_size=48).to_edge(DOWN)

        animations = [Write(next_enzyme)]
        if len(byreaction) != 0:
            (byreactants, byproducts) = byreaction

            byreactants_group = VMobject()
            for byreactant in byreactants:
                byreactants_group.add(Tex(byreactant, font_size=48, substrings_to_isolate=self.substrings_to_isolate))
            byproducts_group = VMobject()
            for byproduct in byproducts:
                byproducts_group.add(Tex(byproduct, font_size=48, substrings_to_isolate=self.substrings_to_isolate))
            byreactants_group.arrange(DOWN).to_edge(LEFT, buff=0.75)
            byproducts_group.arrange(DOWN).to_edge(RIGHT, buff=0.75)
            animations.append(Write(byreactants_group))

        self.play(*animations, run_time=1.5)
        self.wait(duration=0.5)

        prev_enzyme = next_enzyme
        prev_titles = next_titles
        prev_purural_sign = next_purural_sign
        prev_molecules = next_molecules

        if not isinstance(molecule, list):
            title = VMobject()
            for title_line in molecule.name.tex_string.split(','):
                title.add(Tex(title_line, font_size=64, substrings_to_isolate=self.substrings_to_isolate))
            title.arrange(DOWN).to_edge(UP)
            next_titles = [title]
            next_purural_sign = Tex('x{}'.format(n_molecules) if n_molecules > 1 else '', font_size=48).next_to(next_titles[0], RIGHT)
            next_molecules = [ChemObject(molecule.chem.tex_string).scale(0.8)] # .scale(0.8 if title != 'succinyl-CoA' else 0.3)

            animations1 = []
            is_prev_enzyme_used = False
            for j, (prev_title, prev_molecule) in enumerate(zip(prev_titles, prev_molecules)):
                if len(prev_enzyme) == 1 and j != 0 and is_prev_enzyme_used:
                    prev_enzyme = Tex(prev_enzyme.tex_string, font_size=48).to_edge(DOWN)
                animations1.append(FadeOut(prev_enzyme, target_position=prev_molecules[0] if len(prev_titles) == 1 else prev_molecule, scale=0.5))
                is_prev_enzyme_used = True

            animations2 = []
            print('Matching molecules | Reactant: [yellow]{}[/yellow], Product: [yellow]{}[/yellow]'.format(prev_titles[0].submobjects[0].tex_string, next_titles[0].submobjects[0].tex_string))
            # key_map = match_molecules(prev_molecules[0], next_molecules[0], verbose=verbose)

            if n_molecules > 1:
                animations2.append(TransformMatchingTexColorHighlight(prev_purural_sign, next_purural_sign))

            # for prev_title, next_title in zip(prev_titles[0], next_titles[0]):
            #     print(prev_title, next_title)
            #     animations2.append(TransformMatchingTexColorHighlight(prev_title, next_title, fade_transform_mismatches=True))
                
            for i in range(max(len(prev_titles[0]), len(next_titles[0]))):
                prev_title = prev_titles[0][i] if len(prev_titles[0]) > i else Tex(prev_titles[0][i-1].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
                next_title = next_titles[0][i] if len(next_titles[0]) > i else Tex('', font_size=64, substrings_to_isolate=self.substrings_to_isolate)
                animations2.append(TransformMatchingTexColorHighlight(prev_title, next_title, fade_transform_mismatches=True))

            animations2.extend([
                TransformMatchingShapesSameLocation(prev_molecules[0], next_molecules[0]) # , key_map=key_map
            ])

        elif len(molecule) == 2:
            title1 = VMobject()
            for title_line in molecule[0].name.tex_string.split(','):
                title1.add(Tex(title_line, font_size=64, substrings_to_isolate=self.substrings_to_isolate))
            title1.arrange(DOWN).to_edge(UP)
            title2 = VMobject()
            for title_line in molecule[1].name.tex_string.split(','):
                title2.add(Tex(title_line, font_size=64, substrings_to_isolate=self.substrings_to_isolate))
            title2.arrange(DOWN).to_edge(UP)
            next_titles = [
                Tex(title1),
                Tex(title2),
            ]
            next_molecules = [
                ChemObject(molecule[0].chem.tex_string),
                ChemObject(molecule[1].chem.tex_string),
            ]

            animations1 = []
            is_prev_enzyme_used = False
            for j, (prev_title, next_title, prev_molecule) in enumerate(zip(prev_titles, next_titles, prev_molecules)):
                if prev_title.tex_string == next_title.tex_string:
                    continue
                if len(prev_enzyme) == 1 and j != 0 and is_prev_enzyme_used:
                    prev_enzyme = Tex(prev_enzyme, font_size=48).to_edge(DOWN)
                animations1.append(FadeOut(prev_enzyme, target_position=prev_molecules[0] if len(prev_titles) == 1 else prev_molecule, scale=0.5))
                is_prev_enzyme_used = True

            if len(prev_molecules) == 1 and (prev_molecule_parts_to_separate := self.molecules_parts_to_separate.get(prev_title.tex_string)):
                animations1.append(FadeOut(prev_molecule))

                prev_molecules_partial = []
                for _ in prev_molecule_parts_to_separate:
                    prev_molecule_partial = ChemObject(self.molecules[1:][i-1].chem.tex_string).scale(0.8).next_to(prev_molecule, ORIGIN)
                    prev_molecules_partial.append(prev_molecule_partial)
                    animations1.append(FadeIn(prev_molecule_partial))

            animations2 = []
            for j, (next_title, next_molecule) in enumerate(zip(next_titles, next_molecules)):
                if len(prev_titles) == 1 and j != 0:
                    prev_title = Tex(prev_titles[0].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).next_to(prev_titles[0], ORIGIN)
                    prev_molecule = ChemObject(self.molecules[1:][i-1].chem.tex_string).scale(0.8).next_to(prev_molecule, ORIGIN)
                else:
                    prev_title = prev_titles[0] if len(prev_titles) == 1 else prev_titles[j]
                    prev_molecule = prev_molecules[0] if len(prev_titles) == 1 else prev_molecules[j]

                animations2.append(TransformMatchingTexColorHighlight(prev_title, next_title))

                print('Matching molecules | Reactant: [yellow]{}[/yellow], Product: [yellow]{}[/yellow]'.format(prev_title.tex_string, next_title.tex_string))
                if len(prev_molecules) == 1:
                    # key_map = match_molecules(prev_molecules_partial[j], next_molecule, limited_part=prev_molecule_parts_to_separate[j], verbose=verbose)
                    animations2.append(TransformMatchingShapesSameLocation(prev_molecules_partial[j], next_molecule)) # , key_map=key_map
                else:
                    # key_map = match_molecules(prev_molecule, next_molecule, limited_part=None, verbose=verbose)
                    animations2.append(TransformMatchingShapesSameLocation(prev_molecule, next_molecule)) # , key_map=key_map

        if len(byreaction) > 0 and len(byreaction[0]) != 0:
            for byreactant, byproduct in zip(byreactants_group, byproducts_group):
                animations2.append(TransformMatchingTexColorHighlight(byreactant, byproduct, fade_transform_mismatches=True))

        self.play(*animations1, run_time=1)
        self.play(*animations2, run_time=1.5)
        
        animations3 = []
        for j, (next_title, next_molecule) in enumerate(zip(next_titles, next_molecules)):
            animations3.extend([
                FadeToColor(next_title, WHITE),
                FadeToColor(next_molecule, WHITE),
            ])
        
        if len(byreaction) == 2 and len(byreaction[1]) != 0:
            self.play([
                *animations3,
                FadeOut(byproducts_group),
            ], run_time=1)
        else:
            self.play(animations3, run_time=1)

        if isinstance(molecule, list) and len(molecule) > 1 and molecule[0].name.tex_string == molecule[1].name.tex_string:
            title = molecule[0].name.tex_string
            prev_titles = next_titles
            prev_molecules = next_molecules
            next_titles = [Tex(title, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)]
            next_molecules = [ChemObject(molecule[0].chem.tex_string).scale(0.8)]

            animations = []
            animations.append(TransformMatchingTexColorHighlight(prev_titles[0], next_titles[0]))
            animations.append(TransformMatchingShapesSameLocation(prev_molecules[0], next_molecules[0])) # , key_map=key_map

            n_molecules *= len(title)
            next_purural_sign = Tex('x{}'.format(n_molecules), font_size=48).next_to(next_titles[0], RIGHT)
            for prev_title, prev_molecule in zip(prev_titles[1:], prev_molecules[1:]):
                animations.append(FadeIn(next_purural_sign))
                animations.append(FadeOut(prev_title, target_position=next_purural_sign, scale=0.3))
                animations.append(FadeOut(prev_molecule, target_position=next_purural_sign, scale=0.3))

            self.play(*animations, run_time=1)

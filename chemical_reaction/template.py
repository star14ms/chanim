from chanim_manim import *
from manim.mobject.geometry.line import Line
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase

from collections import defaultdict, Counter
from rich import print
import numpy as np

from constant import N_POINTS_THRESHOLD_AS_BOND


class TransformMatchingLocation(TransformMatchingShapes):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        transform_mismatches: bool = False,
        fade_transform_mismatches: bool = False,
        match_same_location: bool = False,
        key_map: dict | None = None,
        target_position: str | None = None,
        color_fadeout: str = 'red',
        color_fadein: str = 'green',
        error_tolerance: float = 0.1,
        min_ratio_possible_match: float = 0.33,
        min_ratio_to_accept_match: float = 0.9,
        match_same_key = False,
        match_carbons = False,
        **kwargs,
    ):
        self.error_tolerance = error_tolerance
        self.min_ratio_possible_match = min_ratio_possible_match
        self.min_ratio_to_accept_match = min_ratio_to_accept_match
        self.match_same_location = match_same_location
        self.match_same_key = match_same_key
        self.match_carbons = match_carbons

        if isinstance(mobject, VMobject):
            group_type = VGroup
        else:
            group_type = Group

        source_map, target_map, key_map, all_keys_source, source_map_values = self.get_key_maps(key_map, mobject, target_mobject)

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
            key1, key2 = str(key1), str(key2)
            # print(key1, key1 in source_map, key2, key2 in target_map)
            if (key1 in source_map or 'atom_' + key1 in source_map or key1 in all_keys_source) and (key2 in target_map or 'atom_' + key2 in target_map):
                key2 = key2 if key2 in target_map else 'atom_' + key2
                target_mob = target_map[key2]
                key_mapped_target.add(target_mob)
                target_map.pop(key2, None)

                if all_keys_source == []:
                    key1 = key1 if key1 in source_map else 'atom_' + key1
                    source_mob = source_map[key1]
                else:
                    source_mob = filter(lambda x: str(x.key) == key1, source_map_values).__next__()
                    index = str(list(source_map_values).index(source_mob))
                    key1 = index if 'atom' not in key2 else 'atom_' + index

                key_mapped_source.add(source_mob)
                source_map.pop(key1, None)

                if (id_dashed_cram := target_mob.__dict__.get('id_dashed_cram', None)) is not None and not isinstance(source_mob, Line):
                    for key in target_map.copy():
                        if target_map[key].__dict__.get('id_dashed_cram', None) == id_dashed_cram:
                            anims.append(
                                FadeTransformPieces(source_mob, target_map.pop(key), **kwargs),
                            )

                if all_keys_source != []:
                    if (id_dashed_cram := source_mob.__dict__.get('id_dashed_cram', None)) is not None:
                        key1_list_to_pop = []

                        for key in source_map:
                            if source_map[key].__dict__.get('id_dashed_cram', None) == id_dashed_cram:
                                anims.append(FadeOut(source_map[key], target_position=target_mob))

                                index = str(list(source_map_values).index(source_map[key]))
                                key1_ = index if 'atom' not in key2 else 'atom_' + index
                                key1_list_to_pop.append(key1_)
                        
                        for key in key1_list_to_pop:  
                            source_map.pop(key, None)

                # sub_idx = 1
                # while key1 + '-' + str(sub_idx) in source_map and key2 + '-' + str(sub_idx) in target_map:
                #     key_mapped_source.add(source_map[key1 + '-' + str(sub_idx)])
                #     key_mapped_target.add(target_map[key2 + '-' + str(sub_idx)])
                #     source_map.pop(key1 + '-' + str(sub_idx), None)
                #     target_map.pop(key2 + '-' + str(sub_idx), None)
                #     sub_idx += 1

        # print(key_mapped_source.submobjects)
        # print(key_mapped_target.submobjects)
        
        if len(key_mapped_source) > 0:
            anims.append(
                FadeTransformPieces(key_mapped_source, key_mapped_target, **kwargs),
            )
        fade_source = group_type()
        fade_target = group_type()
        # print(source_map)
        # print(target_map)
        for key in source_map:
            source_map[key].set_color(color_fadeout) # added
            fade_source.add(source_map[key])
        for key in target_map:
            target_map[key].set_color(color_fadein) # added
            fade_target.add(target_map[key])
        fade_target_copy = fade_target.copy()

        if transform_mismatches:
            if "replace_mobject_with_target_in_scene" not in kwargs:
                kwargs["replace_mobject_with_target_in_scene"] = True
            anims.append(Transform(fade_source, fade_target, **kwargs))
        elif fade_transform_mismatches:
            anims.append(FadeTransformPieces(fade_source, fade_target, **kwargs))
        else:
            if target_position is not None:
                fadeout_list = [FadeOut(fade_source_mob, target_position=target_position if len(fade_source_mob.points) > N_POINTS_THRESHOLD_AS_BOND else None, **kwargs) for fade_source_mob in fade_source]
                anims.append(AnimationGroup(*fadeout_list))
                fadein_list = [FadeIn(fade_target_mob, target_position=target_position if len(fade_target_mob.points) > N_POINTS_THRESHOLD_AS_BOND else None, **kwargs) for fade_target_mob in fade_target_copy]
                anims.append(AnimationGroup(*fadein_list))
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

            key = ('atom_' if n_points > N_POINTS_THRESHOLD_AS_BOND else '') + str(id_shape_map)
            shape_map[key] = mobject
            id_shape_map += 1

        return shape_map

    def original_scale(func):
        def wrapper(*args, **kwargs):
            for arg in args[2:]: # Skip self
                arg.scale(1 / getattr(arg, 'initial_scale_factor', 1))
            result = func(*args, **kwargs)
            for arg in args[2:]:
                arg.scale(getattr(arg, 'initial_scale_factor', 1))
            return result
        return wrapper

    @original_scale
    def get_key_maps(self, key_map, mobject, target_mobject):
        source_map = self.get_shape_map(mobject)
        target_map = self.get_shape_map(target_mobject)
        
        if key_map is None or key_map == {}:
            if self.match_carbons:
                source_map_only_carbons = {key: value for key, value in source_map.items() if len(value.points) == 64}
                target_map_only_carbons = {key: value for key, value in target_map.items() if len(value.points) == 64}
                key_map = {key: value for key, value in zip(source_map_only_carbons.keys(), target_map_only_carbons.keys())}
                all_keys_source = []
                source_map_values = []
            elif self.match_same_key:
                key_map = {key: key for key in source_map.keys() & target_map.keys()}
                all_keys_source = []
                source_map_values = []
            else:
                key_map = self.get_key_map(source_map, target_map) or {}
                all_keys_source = []
                source_map_values = []
        else:
            def add_keys(mobject: VMobject):
                id_shape_map = 0

                def _add_keys(mobject: VMobject):
                    nonlocal id_shape_map

                    if isinstance(mobject, VGroup):
                        for mob in mobject:
                            _add_keys(mob)
                    else:
                        for submob in mobject.submobjects[0].submobjects:
                            submob.key = id_shape_map
                            id_shape_map += 1
                            
                _add_keys(mobject)

            def get_key_map_values(mobject):
                if isinstance(mobject, VGroup):
                    return [get_key_map_values(submob) for submob in mobject]
                else:
                    return [str(submob.key) for submob in mobject[0]]
                
            add_keys(mobject)
            key_map = key_map
            all_keys_source = get_key_map_values(mobject)
            source_map_values = list(source_map.values())
            
        return source_map, target_map, key_map, all_keys_source, source_map_values

    def get_key_map(self, source_map: Mobject, target_map: Mobject, matching_level=3) -> dict:
        if set(source_map.keys()) == set(target_map.keys()):
            return {key: key for key in source_map}
        
        distances_between_identical_mobjects, identical_n_points = self.get_possible_distances(source_map, target_map, matching_level=matching_level)

        key_maps = []
        for distance_identical in distances_between_identical_mobjects:
            key_map = self.match_translated_points(distance_identical, identical_n_points, source_map, target_map)
            matching_ratio = len(key_map) / len(source_map)

            if matching_ratio >= self.min_ratio_possible_match:
                key_map = self.match_dashed_crams(source_map, target_map, key_map)
                if not self.match_same_location:
                    key_map = self.match_closest_mobjects(source_map, target_map, key_map)
                key_maps.append(key_map)
                matching_ratio = len(key_map) / len(source_map)
                # print('matching_ratio', matching_ratio)
                if matching_ratio > self.min_ratio_to_accept_match:
                    break

        key_map = max(key_maps, key=len) if len(key_maps) != 0 else {}
        # print(len(key_map), len(source_map), len(target_map))

        if len(key_map) / len(source_map) >= self.min_ratio_possible_match or matching_level == 0:
            return key_map if len(key_map) != 0 else None
        else:
            return self.get_key_map(source_map, target_map, matching_level=matching_level-1)

    def get_possible_distances(self, source_map, target_map, matching_level=3):
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
            
            # 160 is the number of points of the Hydrogen molecule
            if (matching_level >= 3 and n_points not in identical_n_points) or \
                (matching_level >= 2 and n_points == 160) or \
                (matching_level >= 1 and n_points <= N_POINTS_THRESHOLD_AS_BOND):
                continue

            for mobject_target in target_map.values():
                if len(mobject_target.points) == n_points:
                    # print(' '.join(map(lambda x: '%.6f' % x, mobject_target.get_center() - mobject_source.get_center())))
                    distances_between_identical_mobjects.append(mobject_target.get_center() - mobject_source.get_center())

        print(('n identical mobjects' if matching_level == 3 else 'n similar mobjects'), len(distances_between_identical_mobjects))
        
        return distances_between_identical_mobjects, identical_n_points

    def match_translated_points(self, distance_identical, identical_n_points, source_map, target_map):
        key_map = {}

        for key_source, mobject_source in source_map.items():
            n_points = len(mobject_source.points)
            # print(key_source, n_points)

            if key_source in key_map:
                continue

            for key_target, mobject_target in target_map.items():
                if key_target in key_map.values() or type(mobject_target) != type(mobject_source):
                    continue

                distance_xyz = mobject_target.get_center() - mobject_source.get_center()

                # if key_source == '26' and key_target == '27':
                #     print(' '.join(map(lambda x: '%.6f' % x, mobject_target.get_center() - mobject_source.get_center())))

                if len(mobject_target.points) == n_points and (isinstance(mobject_target, Line) or (len(mobject_target.path_obj) == len(mobject_source.path_obj))) and \
                    ((n_points in identical_n_points) or (abs(distance_xyz[0] - distance_identical[0]) <= self.error_tolerance and abs(distance_xyz[1] - distance_identical[1]) <= self.error_tolerance and abs(distance_xyz[2] - distance_identical[2]) <= self.error_tolerance)): 
                    # print(len(mobject_target.points), not isinstance(mobject_source.path_obj[1], Line))
                    key_map[key_source] = key_target
                    break
                
        return key_map
   
    def match_dashed_crams(self, source_map, target_map, key_map):
        key_map_dashed_cram = defaultdict(dict)
        source_dashed_cram = defaultdict(list)
        target_dashed_cram = defaultdict(list)

        for key_source in source_map:
            if id_dashed_cram := source_map[key_source].__dict__.get('id_dashed_cram', None) is not None:
                source_dashed_cram[id_dashed_cram].append(key_source)
            
        for key_target in target_map:
            if id_dashed_cram := target_map[key_target].__dict__.get('id_dashed_cram', None) is not None:
                target_dashed_cram[id_dashed_cram].append(key_target)
        
        for source_id_dashe_cram, key_sources in source_dashed_cram.items():
            for target_id_dashe_cram, key_targets in target_dashed_cram.items():
                    distances = []
                    for points_source, points_target in zip(source_map[key_sources[0]].points, target_map[key_targets[0]].points):
                        distances.append(np.sqrt(sum((x ** 2 for x in points_source - points_target))))
                    distance_mean = np.mean(distances)
                    key_map_dashed_cram[source_id_dashe_cram][target_id_dashe_cram] = distance_mean
        
        while len(key_map_dashed_cram) != 0:
            source_key_min_distance = min(key_map_dashed_cram, key=lambda x: min(key_map_dashed_cram[x].values()))
            target_key_min_distance = min(key_map_dashed_cram[source_key_min_distance], key=key_map_dashed_cram[source_key_min_distance].get)
            
            for key_source, key_target in zip(source_dashed_cram[source_key_min_distance], target_dashed_cram[target_key_min_distance]):
                key_map[key_source] = key_target

            key_map_dashed_cram.pop(source_key_min_distance)
            for key in key_map_dashed_cram:
                key_map_dashed_cram[key].pop(target_key_min_distance, None)

        return key_map

    def match_closest_mobjects(self, source_map, target_map, key_map):
        key_map_extended = defaultdict(dict)

        for key_source, mobject_source in source_map.items():
            n_points = len(mobject_source.points)

            if key_source in key_map:
                continue

            for key_target, mobject_target in target_map.items():
                if key_target in key_map.values() or type(mobject_target) != type(mobject_source):
                    continue

                if len(mobject_target.points) == n_points and (
                    (isinstance(mobject_target, Line)) or len(mobject_target.path_obj) == len(mobject_source.path_obj)
                ):
                    distance_xyz = mobject_target.get_center() - mobject_source.get_center()
                    distance_xyz = np.sqrt(sum((x ** 2 for x in distance_xyz)))
                    key_map_extended[key_source][key_target] = distance_xyz
                    # if key_source == '19' and key_target == '20':
                    #     breakpoint()
                    
        # print(key_map_extended)
        
        while len(key_map_extended) != 0:
            source_key_min_distance = min(key_map_extended, key=lambda x: min(key_map_extended[x].values()))
            target_key_min_distance = min(key_map_extended[source_key_min_distance], key=key_map_extended[source_key_min_distance].get)
            key_map[source_key_min_distance] = target_key_min_distance
            key_map_extended.pop(source_key_min_distance)
            
            for key in key_map_extended.copy():
                key_map_extended[key].pop(target_key_min_distance, None)
                
                if len(key_map_extended[key]) == 0:
                    key_map_extended.pop(key)
                    
        return key_map


class TransformMatchingTexColorHighlight(TransformMatchingTex):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        transform_mismatches: bool = False,
        fade_transform_mismatches: bool = False,
        key_map: dict | None = None,
        target_position: str | None = None,
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
            source_map[key].set_color(color_fadeout)
            fade_source.add(source_map[key])
        for key in set(target_map).difference(source_map):
            target_map[key].set_color(color_fadein)
            fade_target.add(target_map[key])
        fade_target_copy = fade_target.copy()

        if transform_mismatches:
            if "replace_mobject_with_target_in_scene" not in kwargs:
                kwargs["replace_mobject_with_target_in_scene"] = True
            anims.append(Transform(fade_source, fade_target, **kwargs))
        elif fade_transform_mismatches:
            anims.append(FadeTransformPieces(fade_source, fade_target, **kwargs))
        else:
            anims.append(FadeOut(fade_source, target_position=target_position if target_position is not None else fade_target, **kwargs))
            anims.append(
                FadeIn(fade_target_copy, target_position=target_position if target_position is not None else fade_target, **kwargs),
            )

        super(TransformMatchingAbstractBase, self).__init__(*anims)

        self.to_remove = [mobject, fade_target_copy]
        self.to_add = target_mobject


class TransformMatchingElementTex(TransformMatchingTexColorHighlight):
    def get_shape_map(self, mobject: Mobject) -> dict:
        shape_map = super().get_shape_map(mobject)

        if len(shape_map) != 1:
            return shape_map

        key = list(shape_map.keys())[0]
        shape_map = {}
        rest_group = VGroup()

        for submob in mobject.submobjects[0].submobjects:
            n_points = len(submob.points)
            if 'C' in mobject.tex_string and n_points == 64:
                shape_map['C'] = submob
            elif 'H' in mobject.tex_string and n_points == 160:
                shape_map['H'] = submob
            else:
                rest_group.add(submob)

        shape_map[key] = rest_group

        return shape_map


def construct_chemobject(self):
    name, chemcode = self.chemcodes[-1]
    chem_object = ChemWithName(chemcode, name)

    numbering = VGroup()

    id_shape_map = 0
    for mobject in TransformMatchingShapes.get_mobject_parts(chem_object.chem):
        if self.add_numbering:
            numbering.add(
                MarkupText(str(id_shape_map))
                .scale(0.5)
                .move_to(mobject.get_center())
                .set_color(RED if len(mobject.points) > N_POINTS_THRESHOLD_AS_BOND else GREEN)
            )
        
        id_shape_map += 1

    if self.animation:
        self.play(self.chem_object.creation_anim())
        self.wait()
    else:
        self.add(chem_object)
        self.add(numbering)


def construct_chemobject_animation(self, verbose=False):
    if len(self.molecules[0]) == 1:
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
    for i, molecule in enumerate(self.molecules[0]):
        title = VMobject()
        for title_line in molecule[0].split('\n'):
            title.add(Tex(title_line, font_size=font_size, substrings_to_isolate=self.substrings_to_isolate))
        title.arrange(DOWN).to_edge(position_title[i])
        next_purural_sign = Tex('x{}'.format(n_molecules) if n_molecules > 1 else '', font_size=48).next_to(title, RIGHT)
        molecule = ChemObject(molecule[1]).to_edge(position_molecule[i], buff=0.5 if len(self.molecules[0]) == 1 else 0.75)
        next_titles.append(title)
        next_molecules.append(molecule)
        animations.extend([Write(title), Write(next_purural_sign), Create(molecule)])

    self.play(*animations, run_time=1.5)
    self.wait(duration=0.5)
    
    if len(self.molecules[0]) > 1 and self.molecules[0][0][0] == self.molecules[0][1][0]:
        title = self.molecules[0][0][0]
        prev_titles = next_titles
        prev_molecules = next_molecules
        titles = VMobject()
        titles.add(Tex(self.molecules[0][0][0], font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP))
        next_titles = [titles]
        next_molecules = [ChemObject(self.molecules[0][0][1])]

        animations = []
        for k in range(max(len(prev_titles[0]), len(next_titles[0]))):
            prev_title = prev_titles[0][k] if len(prev_titles[0]) > k else Tex(prev_titles[0][k-1].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
            next_title = next_titles[0][k] if len(next_titles[0]) > k else Tex('', font_size=64, substrings_to_isolate=self.substrings_to_isolate)
            animations.append(TransformMatchingTexColorHighlight(prev_title, next_title, fade_transform_mismatches=True))
        animations.append(TransformMatchingLocation(prev_molecules[0], next_molecules[0])) # , key_map=key_map

        n_molecules *= len(self.molecules[0])
        next_purural_sign = Tex('x{}'.format(n_molecules), font_size=48).next_to(next_titles[0], RIGHT)
        for prev_title, prev_molecule in zip(prev_titles[1:], prev_molecules[1:]):
            animations.append(FadeIn(next_purural_sign))
            animations.append(FadeOut(prev_title, target_position=next_purural_sign, scale=0.3))
            animations.append(FadeOut(prev_molecule, target_position=next_purural_sign, scale=0.3))

        self.wait(duration=0.5)
        self.play(*animations, run_time=1)

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

        if len(molecule) == 1:
            title = VMobject()
            for title_line in molecule[0][0].split('\n'):
                title.add(Tex(title_line, font_size=64, substrings_to_isolate=self.substrings_to_isolate))
            title.arrange(DOWN).to_edge(UP)
            next_titles = [title]
            next_purural_sign = Tex('x{}'.format(n_molecules) if n_molecules > 1 else '', font_size=48).next_to(next_titles[0], RIGHT)
            next_molecules = [ChemObject(molecule[0][1])]

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
                
            for k in range(max(len(prev_titles[0]), len(next_titles[0]))):
                prev_title = prev_titles[0][k] if len(prev_titles[0]) > k else Tex(prev_titles[0][k-1].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
                next_title = next_titles[0][k] if len(next_titles[0]) > k else Tex('', font_size=64, substrings_to_isolate=self.substrings_to_isolate)
                animations2.append(TransformMatchingTexColorHighlight(prev_title, next_title, fade_transform_mismatches=True))

            if key_map := self.key_maps.get(prev_title.tex_string, None):
                key_map = key_map.get(next_title.tex_string, None)

                for n in range(len(prev_molecules[0].submobjects[0].submobjects)):
                    prev_molecules[0].submobjects[0].submobjects[n].key = n

            animations2.extend([
                TransformMatchingLocation(prev_molecules[0], next_molecules[0], key_map=key_map) 
            ])

        elif len(molecule) == 2:
            title1 = VMobject()
            for title_line in molecule[0][0].split('\n'):
                title1.add(Tex(title_line, font_size=48, substrings_to_isolate=self.substrings_to_isolate))
            title1.arrange(DOWN).to_edge(UL)
            title2 = VMobject()
            for title_line in molecule[1][0].split('\n'):
                title2.add(Tex(title_line, font_size=48, substrings_to_isolate=self.substrings_to_isolate))
            title2.arrange(DOWN).to_edge(UR)
            next_titles = [
                title1,
                title2,
            ]
            next_molecules = [
                ChemObject(molecule[0][1]).to_edge(LEFT),
                ChemObject(molecule[1][1]).to_edge(RIGHT),
            ]

            animations1 = []
            is_prev_enzyme_used = False
            for j, (prev_title, next_title, prev_molecule) in enumerate(zip(prev_titles, next_titles, prev_molecules)):
                if prev_title.submobjects[0].tex_string == next_title.submobjects[0].tex_string:
                    continue
                if len(prev_enzyme) == 1 and j != 0 and is_prev_enzyme_used:
                    prev_enzyme = Tex(prev_enzyme, font_size=48).to_edge(DOWN)
                animations1.append(FadeOut(prev_enzyme, target_position=prev_molecules[0] if len(prev_titles) == 1 else prev_molecule, scale=0.5))
                is_prev_enzyme_used = True

            if len(prev_molecules) == 1 and (prev_molecule_parts_to_separate := self.molecules_parts_to_separate.get(prev_title[0].tex_string)):
                animations1.append(FadeOut(prev_molecule))

                prev_molecules_partial = []
                for prev_molecule_part in prev_molecule_parts_to_separate:
                    prev_molecule_partial = ChemObject(self.molecules[i][0][1]).next_to(prev_molecule, ORIGIN)
                    
                    ids_to_remove = sorted([*prev_molecule_part['atoms'], *prev_molecule_part['bonds']], reverse=True)
                    
                    for n in range(len(prev_molecule_partial.submobjects[0].submobjects)):
                        prev_molecule_partial.submobjects[0].submobjects[n].key = n

                    for id_to_remove in ids_to_remove:
                        prev_molecule_partial.submobjects[0].submobjects.pop(id_to_remove)

                    prev_molecules_partial.append(prev_molecule_partial)
                    animations1.append(FadeIn(prev_molecule_partial))

            animations2 = []
            for j, (next_title, next_molecule) in enumerate(zip(next_titles, next_molecules)):
                if len(prev_titles) == 1 and j != 0:
                    prev_title = VMobject()
                    prev_title.add(Tex(prev_titles[0].submobjects[0].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).next_to(prev_titles[0], ORIGIN))
                    prev_molecule = ChemObject(self.molecules[i][0][1]).next_to(prev_molecule, ORIGIN)
                else:
                    prev_title = prev_titles[0] if len(prev_titles) == 1 else prev_titles[j]
                    prev_molecule = prev_molecules[0] if len(prev_titles) == 1 else prev_molecules[j]

                for k in range(max(len(prev_title), len(next_title))):
                    prev_title = prev_title[k] if len(prev_title) > k else Tex(prev_title[k-1].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
                    next_title = next_title[k] if len(next_title) > k else Tex('', font_size=64, substrings_to_isolate=self.substrings_to_isolate)
                    animations2.append(TransformMatchingTexColorHighlight(prev_title, next_title))

                print('Matching molecules | Reactant: [yellow]{}[/yellow], Product: [yellow]{}[/yellow]'.format(prev_title.tex_string, next_title.tex_string))

                if key_map := self.key_maps.get(prev_title.tex_string, None):
                    key_map = key_map.get(next_title.tex_string, None)

                if len(prev_molecules) == 1 and prev_molecule_parts_to_separate:
                    animations2.append(TransformMatchingLocation(prev_molecules_partial[j], next_molecule, key_map=key_map))
                else:
                    animations2.append(TransformMatchingLocation(prev_molecule, next_molecule, key_map=key_map))

        if len(byreaction) > 0 and len(byreaction[0]) != 0:
            for byreactant, byproduct in zip(byreactants_group, byproducts_group):
                animations2.append(TransformMatchingTexColorHighlight(byreactant, byproduct, fade_transform_mismatches=True))

        self.play(*animations1, run_time=1)
        self.play(*animations2, run_time=1.5)

        if len(molecule) > 1 and molecule[0][0] == molecule[1][0]:
            title = molecule[0][0]
            prev_titles = next_titles
            prev_molecules = next_molecules
            titles = VMobject()
            titles.add(Tex(molecule[0][0], font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP))
            next_titles = [titles]
            next_molecules = [ChemObject(molecule[0][1])]

            animations = []
            for k in range(max(len(prev_titles[0]), len(next_titles[0]))):
                prev_title = prev_titles[0][k] if len(prev_titles[0]) > k else Tex(prev_titles[0][k-1].tex_string, font_size=64, substrings_to_isolate=self.substrings_to_isolate).to_edge(UP)
                next_title = next_titles[0][k] if len(next_titles[0]) > k else Tex('', font_size=64, substrings_to_isolate=self.substrings_to_isolate)
                animations.append(TransformMatchingTexColorHighlight(prev_title, next_title, fade_transform_mismatches=True))
            animations.append(TransformMatchingLocation(prev_molecules[0], next_molecules[0])) # , key_map=key_map

            n_molecules *= len(molecule)
            next_purural_sign = Tex('x{}'.format(n_molecules), font_size=48).next_to(next_titles[0], RIGHT)
            for prev_title, prev_molecule in zip(prev_titles[1:], prev_molecules[1:]):
                animations.append(FadeIn(next_purural_sign))
                animations.append(FadeOut(prev_title, target_position=next_purural_sign, scale=0.3))
                animations.append(FadeOut(prev_molecule, target_position=next_purural_sign, scale=0.3))

            self.wait(duration=0.5)
            self.play(*animations, run_time=1)

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

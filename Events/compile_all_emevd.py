import os
from soulstruct.emevd import EMEVD
from soulstruct.emevd.constants import *
from soulstruct.dcx import DCX


DSR_EMEVD_DIRECTORY = 'G:/Steam/steamapps/common/DARK SOULS REMASTERED/event'


def create_superhot_event_slots():
    with open('event_ids.txt') as f:
        output = []
        for line in f:
            enemy_id = line.strip()
            output.append(f'SuperhotEnemy({len(output)}, {enemy_id})')
    with open('event_ids_funcs.txt', 'w') as f:
        f.write('\n'.join(output))


def replace_missing_event_ids(*starts_of_ranges):
    range_index = 0
    current_start = starts_of_ranges[range_index]
    current_id = current_start
    with open('event_ids_vanilla.txt') as f:
        output = []
        all_lines = [int(line.strip()) for line in f.readlines()]
        for old_id in all_lines:
            if old_id == -1:
                # Give new ID, if free.
                if current_id in all_lines:
                    range_index += 1
                    try:
                        current_start = starts_of_ranges[range_index]
                    except IndexError:
                        raise ValueError("Out of ranges.")
                    current_id = current_start
                output.append(str(current_id))
                current_id += 1
            else:
                output.append(str(old_id))
    with open('event_ids.txt', 'w') as f:
        f.write('\n'.join(output))


def compile_emevd():

    print('\nCompiling EMEVD...\n')

    for game_map in ALL_MAPS:
        emevd_name = game_map.file_name

        evs_path = os.path.join(os.path.dirname(__file__), emevd_name + '.evs')
        emevd_path = os.path.join(DSR_EMEVD_DIRECTORY, emevd_name + '.emevd.dcx')

        emevd = EMEVD(evs_path)
        emevd.write_verbose(os.path.join('built_verbose', emevd_name + '.verbose.txt'))
        emevd_dcx = DCX(emevd.pack())
        emevd_dcx.write(emevd_path)

        print(f'Compiled {emevd_name}.')

    print('\nAll EMEVD compiled.')


if __name__ == '__main__':
    # replace_missing_event_ids(1800600)
    # create_superhot_event_slots()
    compile_emevd()

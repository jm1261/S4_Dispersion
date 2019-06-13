import os
import sys
import numpy as np
from shutil import copy


def config_dir_path():
    '''
    Asigns directory path for all data, allowing user input without
    code file path alterations.
    The current working directory (cwd) will then contain all data to
    be analysed. A directory is created name "Put_Data_Here".
    The function waits for user to place data in the folder e.g.
    "hs_img_000", "power_spectrum.csv", "experimental_settings.txt"
    from GMR X.
    Once data is present, the function returns the "Put_Data_Here"
    directory as the main directory and then directory paths can be
    asigned.
    Args:
        The function requires no arguments but will not work unless data
        is present in the new (created) directory and awaits user input.
    '''
    root = os.getcwd()
    main_dir = os.path.join(root, 'Put_Data_Here')
    check_dir_exists(main_dir)

    while len(os.listdir(main_dir)) == 0:
        print('Place data into "Put_Data_Here" folder with this code')
        print('Once complete, restart code')
        os.sys.exit(0)

    else:
        print('Data present in "Put_Data_Here", ensure it is correct\n')
        input('Press enter to continue...\n')

    print('Data set(s) to be examined:')
    print(os.listdir(main_dir))
    print('\n')
    return main_dir


def check_dir_exists(dir_name):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_name: <string> directory path
    '''
    if os.path.isdir(dir_name) is False:
        os.mkdir(dir_name)


def sim_settings(sim_dict):
    '''
    Takes a dictionary containing simulation parameters and generate a
    parameter range for structure's periodicity, structure size, and film
    thickness.
    Args:
        dim_dict: <dictionary> dictionary containing simulation parameters
    Returns:
        period, radius, thickness as python ranges
    '''
    period = range(sim_dict['Period'][0],
                   sim_dict['Period'][1],
                   sim_dict['Period'][2])

    radius = range(sim_dict['Radius'][0],
                   sim_dict['Radius'][1],
                   sim_dict['Radius'][2])

    thickness = range(sim_dict['Film Thickness'][0],
                      sim_dict['Film Thickness'][1],
                      sim_dict['Film Thickness'][2])

    return period, radius, thickness


def get_filename(file_path):
    '''
    Takes a file name path and splits on '/' to obtain only the file name.
    Splits the file name from extension and returns just the user asigned
    file name as a string.
    Args:
        file_name: <string> path to file
    '''

    return os.path.splitext(os.path.basename(file_path))[0]


def dispersion_in(file_path):
    '''
    Reads in raw txt dispersion file using numpy with a tab delimiter.
    Also utilises filename function to determine a file_name.
    Args:
        file_path: <string> file path
    Returns:
        wav, ref_ind, ext_cof (wavelength, refractive index, extinction
        coefficient), file_name
    '''
    file_name = get_filename(file_path)
    if 'vase' in file_name:
        wav, ref_ind, ext_cof = np.genfromtxt(file_path,
                                              delimiter='\t',
                                              skip_header=2,
                                              unpack=True)
    else:
        wav, ref_ind, ext_cof = np.genfromtxt(file_path,
                                              delimiter='\t',
                                              skip_header=1,
                                              usecols=(0, 2, 6),
                                              unpack=True)

    return wav, ref_ind, ext_cof, file_name


def sim_in(file_string, main_dir):
    '''
    Reads in a simulation output txt file from S4 using the directory
    path specified in simulation_out function.
    Args:
        file_string: <string> name of the simulation txt file
        main_dir: <string> directory path to root
    '''
    txt_dir_name = '_'.join(file_string.split('_')[0:3]) + '_Txts'
    file_path = os.path.join(main_dir,
                             txt_dir_name,
                             file_string)

    wav, trans, refl = np.genfromtxt(file_path,
                                     delimiter='\t',
                                     unpack=True)
    return wav, trans, refl


def sim_out(file_name, txt_file, main_dir):
    '''
    Takes the file name from the dispersion file, the output txt file from
    S4 and the root directory and moves all outputted files into the correct
    results folder.
    Args:
        file_name: <string> file name of dispersion file
        txt_file: <string> txt outfile path
        main_dir: <string> root directory
    '''
    name_split = file_name.split('_')
    name_join = '_'.join(name_split[0:-2])
    txt_dir_name = f'{name_join}_Txts'
    txt_dir = os.path.join(main_dir, txt_dir_name)
    check_dir_exists(txt_dir)
    copy(txt_file, txt_dir)
    os.remove(txt_file)


def file_sort(dir_name):
    '''
    Numerically sort a directory containing a combination of string file names
    and numerical file names
    Args:
        dir_name: <string> directory path
    '''
    return sorted(os.listdir(dir_name))


def extract_files(dir_name, file_string):
    '''
    Stack file names in a directory into an array. Returns data files array.
    Args:
        dir_name: <string> directory path
        file_string: <string> string contained within desired files
    '''
    dir_list = file_sort(dir_name)
    return [a for a in dir_list if file_string in a]


def update_progress(progress):
    '''
    Function to display to terminal or update a progress bar according to
    value passed.
    Args:
        progress: <float> between 0 and 1. Any int will be converted
                  to a float. Values less than 0 represent a 'Halt'.
                  Values greater than or equal to 1 represent 100%
    '''
    barLength = 50  # Modify this to change the length of the progress bar
    status = " "

    if isinstance(progress, int):
        progress = float(progress)

    if not isinstance(progress, float):
        progress = 0
        status = 'Error: progress input must be float\r\n'

    if progress < 0:
        progress = 0
        status = 'Halt...\r\n'

    if progress >= 1:
        progress = 1
        status = 'Done...\r\n'

    block = int(round(barLength * progress))
    progress_str = '♠' * block + '-' * (barLength - block)
    text = f'\rPercent: [{progress_str}] {(progress * 100):.0f}% {status}'
    sys.stdout.write(text)
    sys.stdout.flush()

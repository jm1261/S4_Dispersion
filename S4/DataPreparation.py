import os
import decimal
import S4.InputOutput as io
import csv
from shutil import copy


def drange(a, z, jump):
    '''
    Allows the creation of a decimal range.
    Args:
        a: <float, int> starting point
        z: <float, int> finishing point
        jump: <float, int> step size
    '''
    while a < z:
        yield float(a)
        a += decimal.Decimal(jump)


def radius_sweep(main_dir,
                 file_name,
                 sim_params):
    '''
    '''
    csv_out_path = os.path.join(main_dir, 'Csvs')
    io.check_dir_exists(csv_out_path)

    periods, radii, thicknesses = io.sim_settings(sim_params)

    fill_factors = []

    for period in periods:
        for thickness in thicknesses:

            transmission_outfile = (f'{file_name}_'
                                    f'{sim_params["Harmonics"]}_'
                                    f'{period}_'
                                    f'{thickness}_'
                                    f'{sim_params["Top"][0]}_'
                                    f'radius_transmission'
                                    f'.csv')

            reflection_outfile = (f'{file_name}_'
                                  f'{sim_params["Harmonics"]}_'
                                  f'{period}_'
                                  f'{thickness}_'
                                  f'{sim_params["Top"][0]}_'
                                  f'radius_reflection'
                                  f'.csv')

            ffs = []
            with open(transmission_outfile, 'a', newline='') as outfile:
                with open(reflection_outfile, 'a', newline='') as outfile2:

                    for radius in radii:
                        file_string = (f'{file_name}_'
                                       f'{sim_params["Harmonics"]}_'
                                       f'{period}_'
                                       f'{thickness}_'
                                       f'{radius}_'
                                       f'{sim_params["Top"][0]}'
                                       f'.txt')

                        wav, trans, refl = io.sim_in(file_string=file_string,
                                                     main_dir=main_dir)

                        fill_factor = ((2 * radius) / period) / period
                        ffs.append(fill_factor)

                        ## make a blank string ##
                        trans_string = ''
                        ## loop through the array ##
                        for x in trans:
                            ## add the string values x to trans_string ##
                            trans_string = f'{trans_string} {x},'
                        ## use txt write to write trans_string, without the ##
                        ## final comma, strip the spaces and add new line ##
                        outfile.write(trans_string[0:-1].strip() + '\n')
                        refl_string = ''
                        for y in refl:
                            refl_string = f'{refl_string} {x},'
                        outfile2.write(refl_string[0:-1].strip() + '\n')

                outfile.close()
                outfile2.close()

                copy(transmission_outfile, csv_out_path)
                copy(reflection_outfile, csv_out_path)

                os.remove(transmission_outfile)
                os.remove(reflection_outfile)
                fill_factors.append(ffs)

    return fill_factors


def thickness_sweep(main_dir,
                    file_name,
                    sim_params):
    '''
    '''
    csv_out_path = os.path.join(main_dir, 'Csvs')
    io.check_dir_exists(csv_out_path)

    periods, radii, thicknesses = io.sim_settings(sim_params)

    thickness_vals = []

    for period in periods:
        for radius in radii:

            transmission_outfile = (f'{file_name}_'
                                    f'{sim_params["Harmonics"]}_'
                                    f'{period}_'
                                    f'{radius}_'
                                    f'{sim_params["Top"][0]}_'
                                    f'thickness_transmission'
                                    f'.csv')

            reflection_outfile = (f'{file_name}_'
                                  f'{sim_params["Harmonics"]}_'
                                  f'{period}_'
                                  f'{radius}_'
                                  f'{sim_params["Top"][0]}_'
                                  f'thickness_reflection'
                                  f'.csv')

            thicks = []
            with open(transmission_outfile, 'a', newline='') as outfile:
                with open(reflection_outfile, 'a', newline='') as outfile2:

                    for thickness in thicknesses:
                        file_string = (f'{file_name}_'
                                       f'{sim_params["Harmonics"]}_'
                                       f'{period}_'
                                       f'{thickness}_'
                                       f'{radius}_'
                                       f'{sim_params["Top"][0]}'
                                       f'.txt')

                        wav, trans, refl = io.sim_in(file_string=file_string,
                                                     main_dir=main_dir)

                        thick = thickness / period
                        thicks.append(thick)

                        ## make a blank string ##
                        trans_string = ''
                        ## loop through the array ##
                        for x in trans:
                            ## add the string values x to trans_string ##
                            trans_string = f'{trans_string} {x},'
                        ## use txt write to write trans_string, without the ##
                        ## final comma, strip the spaces and add new line ##
                        outfile.write(trans_string[0:-1].strip() + '\n')
                        refl_string = ''
                        for y in refl:
                            refl_string = f'{refl_string} {x},'
                        outfile2.write(refl_string[0:-1].strip() + '\n')

                outfile.close()
                outfile2.close()

                copy(transmission_outfile, csv_out_path)
                copy(reflection_outfile, csv_out_path)

                os.remove(transmission_outfile)
                os.remove(reflection_outfile)
                thickness_vals.append(thicks)

    return thickness_vals


def period_sweep(main_dir,
                 file_name,
                 sim_params):
    '''
    '''
    csv_out_path = os.path.join(main_dir, 'Csvs')
    io.check_dir_exists(csv_out_path)

    periods, radii, thicknesses = io.sim_settings(sim_params)

    period_vals = []

    for thickness in thicknesses:
        for radius in radii:

            transmission_outfile = (f'{file_name}_'
                                    f'{sim_params["Harmonics"]}_'
                                    f'{thickness}_'
                                    f'{radius}_'
                                    f'{sim_params["Top"][0]}_'
                                    f'period_transmission'
                                    f'.csv')

            reflection_outfile = (f'{file_name}_'
                                  f'{sim_params["Harmonics"]}_'
                                  f'{thickness}_'
                                  f'{radius}_'
                                  f'{sim_params["Top"][0]}_'
                                  f'period_reflection'
                                  f'.csv')

            periodss = []
            with open(transmission_outfile, 'a', newline='') as outfile:
                with open(reflection_outfile, 'a', newline='') as outfile2:

                    for period in periods:
                        file_string = (f'{file_name}_'
                                       f'{sim_params["Harmonics"]}_'
                                       f'{period}_'
                                       f'{thickness}_'
                                       f'{radius}_'
                                       f'{sim_params["Top"][0]}'
                                       f'.txt')

                        wav, trans, refl = io.sim_in(file_string=file_string,
                                                     main_dir=main_dir)

                        periodss.append(period)

                        ## make a blank string ##
                        trans_string = ''
                        ## loop through the array ##
                        for x in trans:
                            ## add the string values x to trans_string ##
                            trans_string = f'{trans_string} {x},'
                        ## use txt write to write trans_string, without the ##
                        ## final comma, strip the spaces and add new line ##
                        outfile.write(trans_string[0:-1].strip() + '\n')
                        refl_string = ''
                        for y in refl:
                            refl_string = f'{refl_string} {x},'
                        outfile2.write(refl_string[0:-1].strip() + '\n')

                outfile.close()
                outfile2.close()

                copy(transmission_outfile, csv_out_path)
                copy(reflection_outfile, csv_out_path)

                os.remove(transmission_outfile)
                os.remove(reflection_outfile)
                period_vals.append(periodss)

    return period_vals

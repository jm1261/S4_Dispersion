import os
import S4.InputOutput as io
import S4.DataPreparation as dprep
from shutil import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

root = io.config_dir_path()
dispersion_dir = os.path.join(root, 'Dispersions')
l_script = "S4_lua.lua"

sim_params = {
    'Harmonics' : 225,
    'Period' : [300, 601, 10],
    'Radius' : [50, 151, 10],
    'Film Thickness' : [100, 151, 10],
    'Top' : ['Water', 1.3325, 7.2792e-9, 0],
    'Substrate' : ['Silica', 1.4649, 0.0017953, 0],
    'Wav Range' : [740, 780, 0.5]
}

periods, radii, thicknesses = io.sim_settings(sim_params)
data_files = io.extract_files(dir_name=dispersion_dir,
                              file_string='.txt')

for selected_file in data_files:
    file = os.path.join(dispersion_dir, selected_file)
    if 'H_20_' in file:
        wav, ref_ind, ext_cof, file_name = io.dispersion_in(file)
        print(f'\nNow processing: {file_name}')

        for thickness in thicknesses:
            for radius in radii:

                print('\nProcessing:'
                      f' radius {radius}nm'
                      f' thickness {thickness}nm')

                for index, period in enumerate(periods):
                    mat2 = '_'.join(file_name.split('_')[0:2])
                    txt_outfile = (str(file_name) + '_' +
                                   str(sim_params['Harmonics']) + '_' +
                                   str(period) + '_' +
                                   str(thickness) + '_' +
                                   str(radius) + '_' +
                                   str(sim_params['Top'][0]) +
                                   '.txt')
                    output = ' >> ' + txt_outfile

                    x_range = dprep.drange(sim_params['Wav Range'][0],
                                           sim_params['Wav Range'][1],
                                           sim_params['Wav Range'][2])
                    for x in x_range:
                        n = np.interp(x=x, xp=wav, fp=ref_ind)
                        k = np.interp(x=x, xp=wav, fp=ext_cof)

                        args = ('harmonics = '+str(sim_params['Harmonics'])+
                                '; period = '+str(period)+
                                '; hole_radius = '+str(radius)+
                                '; wavelength = '+str(x)+
                                '; mat1 = '+str(sim_params['Top'][0])+
                                '; mat1_n = '+str(sim_params['Top'][1])+
                                '; mat1_k = '+str(sim_params['Top'][2])+
                                '; mat1_thick = '+str(sim_params['Top'][3])+
                                '; mat2 = '+str(mat2)+
                                '; mat2_n = '+str(n)+
                                '; mat2_k = '+str(k)+
                                '; mat2_thick = '+str(thickness)+
                                '; mat3 = '+str(sim_params['Substrate'][0])+
                                '; mat3_n = '+str(sim_params['Substrate'][1])+
                                '; mat3_k = '+str(sim_params['Substrate'][2])+
                                '; mat3_thick = '+str(sim_params['Substrate'][3]))

                        os.system('S4 -a ' +"\""+ args +"\" "+ l_script + output)
                        io.update_progress(index / len(periods))

                    io.sim_out(file_name=file_name,
                               txt_file=txt_outfile,
                               main_dir=root)

        for index, selected_file in enumerate(data_files):
            file = os.path.join(dispersion_dir, selected_file)
            wav, ref_ind, ext_cof, file_name = io.dispersion_in(file)
            print(f'\nNow processing: {file_name}')

            fill_factors = dprep.radius_sweep(main_dir=root,
                                              file_name=file_name,
                                              sim_params=sim_params)
            thickness_vals = dprep.thickness_sweep(main_dir=root,
                                                   file_name=file_name,
                                                   sim_params=sim_params)
            period_vals = dprep.period_sweep(main_dir=root,
                                             file_name=file_name,
                                             sim_params=sim_params)
            io.update_progress(index / len(data_files))

        csv_dir = os.path.join(root, 'Csvs')
        results_dir = os.path.join(root, 'Results')
        io.check_dir_exists(results_dir)
        data_files = io.extract_files(dir_name=csv_dir,
                                      file_string='.csv')

        wav = dprep.drange(sim_params['Wav Range'][0],
                           sim_params['Wav Range'][1],
                           sim_params['Wav Range'][2])

        for index, selected_file in enumerate(data_files):
            file = os.path.join(csv_dir, selected_file)
            file_name = io.get_filename(file)
            data = np.genfromtxt(file,
                                 delimiter=',')

            if 'radius' in file_name:

                #period = file_name.split('_')[6]
                #fill_factors = []
                #for radius in radii:
                #    fill_factors.append(int(radius) / int(period))
                fig, ax = plt.subplots(1, 1, figsize=[10,7])
                cax = ax.imshow(X=data,
                                cmap=plt.cm.viridis,
                                vmin=data.min(),
                                vmax=data.max(),
                                extent=[sim_params['Wav Range'][0],
                                        sim_params['Wav Range'][1],
                                        max(radii),
                                        min(radii)],
                                 aspect='equal')
                cbar = fig.colorbar(cax)
                cbar.ax.set_ylabel('Intensity [au]', fontsize=16)
                ax.set_xlabel('Wavelength [nm]', fontsize=16)
                ax.set_ylabel('Hole Radius [nm]', fontsize=16)
                ax.set_title(' '.join(file_name.split('_')), fontsize=16)
                fig.tight_layout()

                out_name = f'{file_name}.png'
                out_path = os.path.join(results_dir, out_name)
                plt.savefig(out_path)

                fig.clf()
                plt.close(fig)

            elif 'period' in file_name:

                fig, ax = plt.subplots(1, 1, figsize=[10,7])
                cax = ax.imshow(X=data,
                                cmap=plt.cm.viridis,
                                vmin=data.min(),
                                vmax=data.max(),
                                extent=[sim_params['Wav Range'][0],
                                        sim_params['Wav Range'][1],
                                        max(periods),
                                        min(periods)],
                                 aspect='equal')
                cbar = fig.colorbar(cax)
                cbar.ax.set_ylabel('Intensity [au]', fontsize=16)
                ax.set_xlabel('Wavelength [nm]', fontsize=16)
                ax.set_ylabel('Period [nm]', fontsize=16)
                ax.set_title(' '.join(file_name.split('_')), fontsize=16)
                fig.tight_layout()

                out_name = f'{file_name}.png'
                out_path = os.path.join(results_dir, out_name)
                plt.savefig(out_path)

                fig.clf()
                plt.close(fig)

            elif 'thickness' in file_name:

                fig, ax = plt.subplots(1, 1, figsize=[10,7])
                cax = ax.imshow(X=data,
                                cmap=plt.cm.viridis,
                                vmin=data.min(),
                                vmax=data.max(),
                                extent=[sim_params['Wav Range'][0],
                                        sim_params['Wav Range'][1],
                                        max(thicknesses),
                                        min(thicknesses)],
                                 aspect='equal')
                cbar = fig.colorbar(cax)
                cbar.ax.set_ylabel('Intensity [au]', fontsize=16)
                ax.set_xlabel('Wavelength [nm]', fontsize=16)
                ax.set_ylabel('Film Thickness [nm]', fontsize=16)
                ax.set_title(' '.join(file_name.split('_')), fontsize=16)
                fig.tight_layout()

                out_name = f'{file_name}.png'
                out_path = os.path.join(results_dir, out_name)
                plt.savefig(out_path)

                fig.clf()
                plt.close(fig)

            io.update_progress(index / len(data_files))

    else:
        print('File Skipped')

# Benchmark against analytical solutions
# 1) fft coordinatae calculation: compare spot size
# 2) propagation compare beam size at rayleigh range

import matplotlib.pyplot as plt
import numpy as np

import laser_beam as lb

coord_unit = "mm"
#coord_unit = "inch"
# coord_unit = "furlong"

width_x = 1
width_y = width_x
pixel_size = width_x * 0.08
wavelength = 1000e-9        # in 'm'

focal_length = 100e-3

# convert width to SI for rayleigh range calculation,
waist = 0.5 *lb.rescale_by_units(width_x, unit_data=coord_unit, unit_target='m')

# calculate focus size
focus_size = 2 * wavelength * focal_length / (np.pi * waist) # in 'm'

# calculate rayleigh range
raileigh_range = np.pi*waist**2/wavelength

# calculate beam size at rayleigh range
beam_size_rayleigh = 2*waist*np.sqrt(2)

print(f"Beam width: {width_x}({coord_unit}), wavelength: {wavelength}m")
print(f"Raileigh range: {raileigh_range}m")

# --- define beam ---
beam_nf_I_1 = lb.create_beam_xy(
    type="Gauss",
    label="Near Field",
    name = "Intensity",
    units = "arb.u.",
    func_params={
        'width_x': width_x,
        'width_y': width_y,
    },
    axis_unit=coord_unit,
    axis_pixelsize=pixel_size,
    axis_x_N=101,
    axis_y_N=101,
)

# --- do the math ---
# calculate E-field from Intensity
beam_nf_E_1 = lb.Int_to_Efield(beam_nf_I_1)

# calculate far-field by fourier transform
beam_ff_E_1 = lb.fft_xy(beam_nf_E_1,label="Far-Field")

# append secondary coordinates to far-field (angle and focus size)
beam_ff_E_1 = lb.append_secondary_rec_coordinates(beam_ff_E_1,wavelength=wavelength,focal_length=focal_length)

# convert from E-Field to Intensity
beam_ff_I_1 = lb.Efield_to_Int(beam_ff_E_1)

# propagate
beam_ff_E_2 = lb.propagate(beam_ff_E_1,wavelength=wavelength,distance=raileigh_range)

# convert back to spatial space
beam_nf_E_2 = lb.fft_xy(beam_ff_E_2,direction='inverse',label="Near-Field Propagated")

# convert back to Intensity
beam_nf_I_2 = lb.Efield_to_Int(beam_nf_E_2)

# calculate statistic
beam_nf_I_1 = lb.set_statistics(beam_nf_I_1)
beam_ff_I_1 = lb.set_statistics(beam_ff_I_1)
beam_nf_I_2 = lb.set_statistics(beam_nf_I_2)

beam_size_nf = beam_nf_I_1.coords['x'].attrs['spread']*4
beam_size_ff = np.real(beam_ff_I_1.coords['x_focus'].attrs['spread']*4) # ignore tiny imaginary part from numerical errors
ff_cood_unit = beam_ff_I_1.coords['x_focus'].attrs['units']

print(f"Near-field beam size (D4σ): {beam_size_nf:.3f}{coord_unit}")
print(f"Far-field beam size (D4σ): {beam_size_ff:.3f}{ff_cood_unit}")
print(f"Expected far-field beam size (D(1/e2)): {focus_size*1e6:.3f}μm")

beam_size_nf_prop = np.real(beam_nf_I_2.coords['x'].attrs['spread']*4) # ignore tiny imaginary part from numerical errors
beam_size_nf_prop = lb.rescale_by_units(beam_size_nf_prop, unit_data=coord_unit, unit_target=coord_unit)
beam_size_rayleigh = lb.rescale_by_units(beam_size_rayleigh, unit_data='m', unit_target=coord_unit)
print(f"Near-field beam size after propagation (D4σ): {beam_size_nf_prop:.3f}{coord_unit}")
print(f"Expected near-field beam size after propagation D(1/e2)): {beam_size_rayleigh*1e3:.3f}{coord_unit}")

titel_ff = f"Far Field \n num: {beam_size_ff:.1f}({ff_cood_unit}), anal: {focus_size*1e6:.1f}μm"
titel_nf_prop = f"Near Field Propagated \n num: {beam_size_nf_prop:.3f}({coord_unit}), anal: {beam_size_rayleigh:.3f}{coord_unit}"

# --- Figures ---   

fig,ax = plt.subplots(1, 3,figsize=(18,4))

lb.plot_2D(beam_nf_I_1, ax=ax[0])
#lb.plot_2D(beam_ff_I_1, ax=ax[1],titel=titel_ff,secondary_axis='focus size')
lb.plot_2D(beam_ff_I_1, ax=ax[1],titel=titel_ff)
lb.plot_2D(beam_nf_I_2, ax=ax[2],titel=titel_nf_prop)

plt.show()
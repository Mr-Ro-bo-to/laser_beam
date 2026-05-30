import laser_beam as lb

import matplotlib.pyplot as plt

# file2 = script_dir / "data" / "2026_04_13_PLST7_MP_M2_100p_430mJ" / "130mm.bgData"
file = 'tests\Data\Ophir_Camera.bgData'

beam =  lb.load_bgdata_ophir_as_dataarray(file)

beam_cropped = lb.crop(beam,
    x=(-0.8, -0.2, 'mm', 'center'),
    y=(-0.45, 0.15, 'mm', 'center'),
    )

fig,ax = plt.subplots(1, 2, figsize=(12,6))

lb.plot_2D(
    beam,
    ax = ax[0],
    )

lb.plot_2D(
    beam_cropped,
    title='Far Field',
    plot_unit_x='μm',
    # plot_unit_y ='μm',
    ax = ax[1],
    )

plt.tight_layout()
plt.show()
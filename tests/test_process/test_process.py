import matplotlib.pyplot as plt

import laser_beam as lb

beam = lb.create_beam_xy(
    label = 'Input Beam',
    func_params={
        'width_x': 10,
        'width_y': 15,
    },
    axis_unit='mm',
    axis_x_N=200,
    axis_y_N=200,
)

beam_cropped = lb.crop(beam,
    x=(-4,4,'cm'),
    y=(-4,4,'cm'),
    label = 'Cropped Beam',
    #calc_statistics = False,
    )


beam_red = lb.cross_section(beam,
    y=(-10,10,'mm'),
    label = 'Lineout',
    method='sum',
    #overlay_label = 'lineout',
    calc_statistics=False,
    )


fig,ax = plt.subplots(1, 2,figsize=(12,4))

lb.plot_2D(beam,
    #titel = 'My Very Fancy Beam',  
    #log_scale=True,
    #plot_units='m',
    #plot_units_brackets=('{','}'),
    #overlays_show=False,
    ax= ax[0],
    )

lb.plot_2D(beam_cropped,
    ax=ax[1],

    )

plt.tight_layout()
plt.show()
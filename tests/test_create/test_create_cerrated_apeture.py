import matplotlib.pyplot as plt

import laser_beam as lb




beam_0_0 = lb.create_beam_xy(
    type="SeratedAperture",
)

beam_0_1 = lb.create_beam_xy(
    type="SeratedAperture",
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_0_2 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 60,
            'radius': 10,
            'n_edge': 15,
            'n_corner': 5,
            'depth': 5,
            'inverted': True
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_1_0 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 60,
            'radius': 30,
            'n_corner': 20,
            'depth': 5,
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_1_1 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'x0': 10,
            'y0':-5,
            'orientation': 20,
            'amplitude': 2,
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_1_2 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 60,
            'radius': 0,
            'n_edge': 30,
            'depth': 5,
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_2_0 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 60,
            'radius': 0,
            'n_edge': 0,
            'n_corner': 0,
            'depth': 5,
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_2_1 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 60,
            'radius': 10,
            'n_edge': 0,
            'n_corner': 0,
            'depth': 5,
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)

beam_2_2 = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 60,
            'radius': 10,
            'n_edge': 15,
            'n_corner': 5,
            'depth': 60,
        },
    axis_unit="mm",
    axis_pixelsize=0.1,
    axis_x_N=1000,
    axis_y_N=1000,
)



beam_x_x = lb.create_beam_xy(
    type="SeratedAperture",
    func_params={
            'size': 4,
            'radius': 0.5,
            # 'amplitude': 100,
            # 'x0': 1,
            # 'y0': 2,
            # 'orientation': 10,
            'inverted': True
        },
        axis_unit="mm",
        axis_pixelsize=0.025,
        axis_x_N=500,
        axis_y_N=500,
)

# fig,ax = plt.subplots(3, 3,figsize=(12,8), constrained_layout=True)
fig,ax = plt.subplots(3, 3,figsize=(12,8))

lb.plot_2D(beam_0_0,ax=ax[0,0],titel="Aperture",x_label_show=False,cbar_label_show=False)
lb.plot_2D(beam_0_1,ax=ax[0,1],titel="Best Aperture",x_label_show=False,y_label_show=False,cbar_label_show=False)
lb.plot_2D(beam_0_2,ax=ax[0,2],titel="Bestest Aperture",x_label_show=False,y_label_show=False)

lb.plot_2D(beam_1_0,ax=ax[1,0],titel_show=False,x_label_show=False,cbar_label_show=False)
lb.plot_2D(beam_1_1,ax=ax[1,1],titel_show=False,x_label_show=False,y_label_show=False,cbar_label_show=False)
lb.plot_2D(beam_1_2,ax=ax[1,2],titel_show=False,x_label_show=False,y_label_show=False)


lb.plot_2D(beam_2_0,ax=ax[2,0],titel_show=False,cbar_label_show=False)
lb.plot_2D(beam_2_1,ax=ax[2,1],titel_show=False,y_label_show=False,cbar_label_show=False)
lb.plot_2D(beam_2_2,ax=ax[2,2],titel_show=False,y_label_show=False)

plt.tight_layout()
plt.show()
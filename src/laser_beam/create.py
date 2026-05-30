"""
Docstring for laser_beam.create
"""
import numpy as np
import xarray as xr

# import all functions from all modules in laser_beam
from laser_beam.utils import gauss_2D, supergauss_round_2D, supergauss_square_2D, square_2D, ellipse_2D, serrated_aperture, squircle_2D
from laser_beam.utils import gauss_1D, cosine_1D, hyperbola_1D
#from laser_beam.utils import convert_wavelength_2_frequency
#from laser_beam.visualize import plot_2D

__all__ = ['create_beam_xy','create_beam_2D']

# create beam with 2 dimensions
def create_beam_1D(
    label: str = "My Laser Beam",
    type = "Gauss",
    function = None,
    func_params = {},

    name = "Intensity",
    units = "arb.u.",

    axis_N: int = 100,
    axis_unit: str = "px",
    axis_pixelsize: float = 1.0,
    dim = 'x',      
    ) -> xr.DataArray:
    """
    Parameters
    ----------

    type : str, default 'Gauss', options {'Gauss'}.
        Identifier for the 2D profile generatorr

    dim : str, default 'x'
        Name of the  dimension in the xarray object.

    """

    # Define coordinate arrays
    axis = axis_pixelsize * (np.arange(axis_N) - (axis_N - 1) / 2)

    # calculate data based on type
    if type == 'Gauss':
        data = gauss_1D(axis, **func_params)
    elif type == 'Cosine':
        data = cosine_1D(axis, **func_params)
    elif type == 'Hyperbola':
        data = hyperbola_1D(axis, **func_params)
    elif type == 'Custom':
        if not callable(function):
            raise TypeError("'function' must be callable for Custom type")
        data = function(axis, **func_params)
    else:
        raise ValueError(f"Unknown beam type: {type}")
    
    
    beam = xr.DataArray(
        data,
        dims=[dim,],
        coords={
            dim: (dim, axis, {'units': axis_unit})
        },
        name=name,
        attrs={'units': units,
               'label': label,
        },
    )
    return beam

# create beam with coordinates x and y
def create_beam_xy(
    type= "Gauss",
    label="My Beam",
    func_params = {},
    name = "Intensity",
    units = "arb.u.",
    axis_unit="px",
    axis_pixelsize=1,
    axis_x_N: int =100,
    axis_y_N: int =100,
    # wavelength: float = None,
    ) -> xr.DataArray:
    """
    Parameters
    ----------
    
    type : str, default 'Gauss', options {'Gauss', 'SuperGaussRound', 'SuperGaussSquare', 'Elipse', 'Square', 'Squircle', 'SeratedAperture'}.
        Identifier for the 2D profile generatorr

    wavelength
    """
    

    beam = create_beam_2D(
        label = label,
        type = type,
        func_params = func_params,
        name = name,
        units = units,
        axis_1_N = axis_x_N,
        axis_2_N = axis_y_N,
        axis_1_unit = axis_unit,
        axis_2_unit = axis_unit,
        axis_1_pixelsize = axis_pixelsize,
        axis_2_pixelsize =axis_pixelsize,
        dim_1 = 'x',        
        dim_2 = 'y',
    )

    # if wavelength is not None:
    #     wavelength *= 1e-9
    #     frequency = convert_wavelength_2_frequency(wavelength)

    #     beam = beam.expand_dims("f", axis=-1) #
    #     beam = beam.assign_coords(f=("f", [frequency], {"units": "Hz"}))

    return beam

# create beam with 2 dimensions
def create_beam_2D(
    label: str = "My Laser Beam",
    type = "Gauss",
    func_params = {},

    name = "Intensity",
    units = "arb.u.",

    axis_1_N: int = 100,
    axis_2_N: int = 100,
    axis_1_unit: str = "px",
    axis_2_unit: str = "px",
    axis_1_pixelsize: float = 1.0,
    axis_2_pixelsize: float = 1.0,
    dim_1 = 'x',        
    dim_2 = 'y',
    ) -> xr.DataArray:
    """
    Parameters
    ----------

    type : str, default 'Gauss', options {'Gauss', 'SuperGaussRound', 'SuperGaussSquare', 'Ellipse', 'Square', 'SeratedAperture'}.
        Identifier for the 2D profile generatorr

    dim_1 : str, default 'x'
        Name of the first spatial dimension in the xarray object (many functions expect 'x').

    dim_2 : str, default 'y'
        Name of the second spatial dimension in the xarray object (many functions expect 'y').
    """

    # Define coordinate arrays
    # define x and y axis
    axis_1 = axis_1_pixelsize * (np.arange(axis_1_N) - (axis_1_N - 1) / 2)
    axis_2 = axis_2_pixelsize * (np.arange(axis_2_N) - (axis_2_N - 1) / 2)

    # create meshgrid
    X, Y = np.meshgrid(axis_1, axis_2,indexing='ij')  # note the indexing='ij' for x,y order

    # calculate data based on type
    if type == "Gauss":
        data = gauss_2D(X, Y, **func_params)
    elif type == "SuperGaussRound":
        data = supergauss_round_2D(X, Y, **func_params)
    elif type == "SuperGaussSquare":
        data = supergauss_square_2D(X, Y, **func_params)
    elif type == "Ellipse": # ToDo: decide naming 'Circle' vs 'Ellipse'
        data = ellipse_2D(X,Y,**func_params)
    elif type == "Square": # ToDo: decide naming 'Square' vs 'Rectangular'
        data = square_2D(X,Y,**func_params)
    elif type == "Squircle":
        data = squircle_2D(X,Y, **func_params)
    elif type == "SeratedAperture":
        data = serrated_aperture(X,Y,**func_params)
    else:
        raise ValueError(f"Unknown beam type: {type}")
    
    
    beam = xr.DataArray(
        data,
        dims=[dim_1, dim_2],
        coords={
            dim_1: (dim_1, axis_1, {'units': axis_1_unit}),
            dim_2: (dim_2, axis_2, {'units': axis_2_unit}),
        },
        name=name,
        attrs={'units': units,
               'label': label,
        },
    )
    return beam



if __name__ == "__main__":
    # test laser_beam.create module
    print("Testing laser_beam.create module...")

    import laser_beam as lb
    import matplotlib.pyplot as plt

    def my_weird_beam(x, a=1, b=1):
        return b* np.cos(a*x)/x

    beam_1D = create_beam_1D(
        label = 'Voltage Distribution',
        type = 'Cosine',
        func_params={
            'w': 0.1,
        }
    )

    lb.plot_1D(
        beam_1D,
        legend_show=False)

    beam = create_beam_xy(
        type="Squircle",
        label="Test Rounded Polygone ",
        func_params={
            'width_x': 4,
            'width_y': 4,
            'radius': 1,
            # 'orientation': 20,
            # 'x0': 1,
            # 'inverted': True,
        },
        axis_unit="mm",
        axis_pixelsize=0.1,
    )

    
    # lb.plot_2D(beam)

    #print(beam)

    plt.tight_layout()
    plt.show()
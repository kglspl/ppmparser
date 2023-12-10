# About PPM Parser

Python class for parsing [PPM files](https://scrollprize.org/tutorial3#rendering-the-segment).

Requirements:
- numpy

# Usage

## Get the x/y/z/nx/ny/nz for a given u/v

```py
with PPMParser(ppm_filename).open() as ppm:
    print(ppm.get_3d_coords(1000, 2000)
```

Note that this operation is very fast because PPMParser uses file seek operation to read the correct coordinates.

## Traverse over ppm
```py
with PPMParser(ppm_filename).open() as ppm:
    for imx, imy, x, y, z, nx, ny, nz in ppm.read_next_coords(skip_empty=True):
        print(x, y, z)
```

## Using step

We often want to get only every n-th point in both x and y direction. Parameter `step` allows us to do this:
```py
with PPMParser(ppm_filename, step=4).open() as ppm:
    for imx, imy, x, y, z, nx, ny, nz in ppm.read_next_coords(skip_empty=True):
        print(imx, imy)  # note that you need to multiply both with 4 to get the original coordinates
```

To avoid possible mistakes, we can use `im_shape()` like this:
```py
with PPMParser(ppm_filename).open() as ppm:
    a = np.zeros(ppm.im_shape(), dtype=...)
    for imx, imy, x, y, z, nx, ny, nz in ppm.read_next_coords(skip_empty=True):
        a[imx, imy] = ...
```

Or we can let PPMParser allocate numpy array for us:
```py
with PPMParser(ppm_filename).open() as ppm:
    a = ppm.im_zeros(dtype=...)
    for imx, imy, x, y, z, nx, ny, nz in ppm.read_next_coords(skip_empty=True):
        a[imx, imy] = ...
```

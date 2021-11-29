import numpy as np

def gaus(x, h):
    const_g = 4 * np.log(2)
    return ((const_g**(1/2)) / (np.pi**(1/2) * h)) * np.exp(-const_g * (x/h)**2)

def y_multi(x_val, step, xy_merge, H):
    y_val = 0
    xy_idx = 0
    for xy_idx in range (0, xy_merge.shape[0]):
        if xy_merge[xy_idx, 0] > (x_val * step - 10) and xy_merge[xy_idx, 0] < (x_val * step + 10):
            y_val = y_val + xy_merge[xy_idx, 1] * (gaus((x_val * step - xy_merge[xy_idx, 0]), H[xy_idx, 0])+ 0.5*gaus((x_val * step - xy_merge[xy_idx, 0]), H[xy_idx, 0]))
    return y_val
import argparse
import numpy as np
import pandas as pd


MIN_POINTS = 5 # The minimum number of data points before a vehicle is considered


def get_axle_offset(p, lt, rt):
    """
    Computes the lane offset of the vehicle from the fixed point along the axle axis.

    p: Fixed point [x,y]
    lt: List of [x,y] coordinates of left tire of vehicle
    rt: List of [x,y] coordinates of right tire of vehicle

    TODO: These things would probably improve accuracy:
    Remove frames with unusual x/y values
    Compute best fit line for left and right tires
    Remove frames with coordinates which are far from the lines
    """
    # Compute travel: best fit line for midpoints, expressed as a vector
    midpoints = (lt + rt) /2
    mid_m, mid_b = np.polynomial.polynomial.Polynomial.fit(midpoints[:,0], midpoints[:,1], 1)   # Best fit line for center points
    travel = [1, mid_m]
    # Compute center: average of the midpoints
    center = np.average(midpoints, axis=0)
    # Compute axle: average of the vectors from left tire to right tire
    axle = np.average(rt - lt, axis=0)
    # Compute v: vector from center to fixed point
    v = center - p

    a = (v[0]*travel[1] - v[1]*travel[0]) / (axle[0]*travel[1] - axle[1]*travel[0])
    v_axle = a * axle
    axle_offset = (v_axle[0]**2 + v_axle[1]**2) ** 0.5
    return axle_offset


def get_vehicle_offsets(path):
    """
    Parses a CSV file to get axle offsets for each vehicle

    `path`: Path to CSV file

    Returns dict of vehicle offsets in terms of pixels.
    """
    offsets = dict()
    vals = pd.read_csv(path)
    p = np.average(vals[['anchor_point_x', 'anchor_point_y']], axis=0)
    vehicles = vals.groupby('vehicle_id')
    for vId, vIdVals in vehicles:
        if vIdVals.shape[0] >= MIN_POINTS:
            lt = vIdVals[['left_tire_x', 'left_tire_y']]
            rt = vIdVals[['right_tire_x', 'right_tire_y']]
            offset = get_axle_offset(p, lt.values, rt.values)
            offsets[vId] = offset
    return offsets


if __name__ == "__main__":
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument(
    #     'path',
    #     help='path to CSV file to read'
    # )
    # argparser.add_argument(
    #     '--scale',
    #     default=1.0,
    #     type=float,
    #     help='scaling factor for offsets; recommended units are meters/pixel; default is no scale'
    # )
    # args = argparser.parse_args()
    
    path = "data_DWARF_20230928141941573.csv"
    scale = 0.00349

    offsets = get_vehicle_offsets(path)
    if not offsets:
        print("No offsets could be detected.")
    for vId, offset in offsets.items():
        print(offset  * scale)

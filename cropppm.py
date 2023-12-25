import argparse
import os
import struct

import ppmparser


def get_arguments():
    parser = argparse.ArgumentParser(usage="%(prog)s [OPTION] [FILE]...", description="Crop PPM.")
    parser.add_argument("--input", "-i", help="input PPM file name", required=True)
    parser.add_argument("--output", "-o", help="output PPM file name; if not supplied, input file base name will be used as prefix")
    parser.add_argument("--roi", help="region of interest in x0-x1,y0-y1 notation (e.g. '0-1000,0-700'); start coordinate is inclusive, end is exclusive", required=True)
    parser.add_argument("--stride", help="stride with which output PPM should be constructed", type=int)
    return parser.parse_args()


def construct_output_filename(input_filename):
    raise Exception('Not implemented yet')


def parse_roi(roi):
    axes_rois = roi.split(',')
    start_x, end_x = axes_rois[0].split('-')
    start_y, end_y = axes_rois[1].split('-')
    start_x, end_x, start_y, end_y = int(start_x), int(end_x), int(start_y), int(end_y)
    print(f'ROI in input coordinates: X: {start_x}-{end_x}, Y: {start_y}-{end_y}')
    return start_x, end_x, start_y, end_y


def write_ppm_header(f, width, height):
    # example header:
    # 00000000: 7769 6474 683a 2031 3733 3831 0a68 6569  width: 17381.hei
    # 00000010: 6768 743a 2031 3335 3133 0a64 696d 3a20  ght: 13513.dim:
    # 00000020: 360a 6f72 6465 7265 643a 2074 7275 650a  6.ordered: true.
    # 00000030: 7479 7065 3a20 646f 7562 6c65 0a76 6572  type: double.ver
    # 00000040: 7369 6f6e 3a20 310a 3c3e 0a00 0000 0000  sion: 1.<>......
    s = f"width: {width}\nheight: {height}\ndim: 6\nordered: true\ntype: double\nversion: 1\n<>\n"
    f.write(s.encode('ascii'))


if __name__ == '__main__':
    args = get_arguments()

    print(f'Input file: {args.input}')
    output_file = args.output if args.output else construct_output_filename(args.input)
    print(f'Output file: {output_file}')
    if os.path.exists(output_file):
        raise Exception('Output file exists, cowardly refusing to overwrite it.')

    stride = 1 if args.stride is None else args.stride
    print(f'Stride: {stride}')

    start_x, end_x, start_y, end_y = parse_roi(args.roi)
    width = (end_x - start_x) // stride + 1
    height = (end_y - start_y) // stride + 1

    # note that we will not use PPMParser's step, instead we will control stride ourselves:
    with ppmparser.PPMParser(args.input, None).open() as input_ppm, \
        open(output_file, 'wb') as output_f:

        write_ppm_header(output_f, width, height)

        for imx in range(start_x, end_x, stride):
            for imy in range(start_y, end_y, stride):
                x, y, z, nx, ny, nz = input_ppm.get_3d_coords(imx, imy)
                buf = struct.pack('<dddddd', x, y, z, nx, ny, nz)
                output_f.write(buf)

    print(f'Output written to: {output_file}')
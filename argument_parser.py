import argparse


def custom_integer(x):
    value = int(x)
    if 25 <= value <= 2500:
        return value
    raise argparse.ArgumentTypeError(f'{x}: is not a valid integer')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Learning to parse arguments')
    parser.add_argument('-bb', '--bounding_boxes', default=0,
                        type=int, choices=[0, 1], help='Display the bounding boxes')
    parser.add_argument('-f', '--feed', default=0,
                        type=int, choices=[0, 1], help='Display the feeds')
    parser.add_argument('-os', '--occupation_stamp', default=0,
                        type=int, choices=[0, 1], help='Write the occupation stamp to frame')
    parser.add_argument('-ts', '--time_stamp', default=1,
                        type=int, choices=[0, 1], help='Write the time stamp to frame')
    parser.add_argument('-r', '--record', default=0,
                        type=int, choices=[0, 1], help='Record any motion that is tracked')
    parser.add_argument('-ut', '--unoccupied_ticks', default=50,
                        type=custom_integer, help='The amount of ticks buffer between occupied and unoccupied statuses (25 <= x <= 2500)')
    args = parser.parse_args()

    if args.bounding_boxes is not None:
        print(f'-bb: {bool(args.bounding_boxes)}')
    if args.feed is not None:
        print(f'-f: {bool(args.feed)}')
    if args.occupation_stamp is not None:
        print(f'-os: {bool(args.occupation_stamp)}')
    if args.time_stamp is not None:
        print(f'-ts: {bool(args.time_stamp)}')
    if args.record is not None:
        print(f'-r: {bool(args.record)}')
    if args.unoccupied_ticks is not None:
        print(f'-ut: {args.unoccupied_ticks}')

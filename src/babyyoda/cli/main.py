import matplotlib
import babyyoda
import argparse
import re
from histoprint import print_hist

from babyyoda.Histo1D import HISTO1D_V2
from babyyoda.Histo2D import HISTO2D_V2


def main():
    # argument parsing
    parser = argparse.ArgumentParser(description="Printing tool for BabyYoda")
    # argument -m for matching
    parser.add_argument("-m", "--matching", help="Matching string")
    # argument -M for inverse matching
    parser.add_argument("-M", "--inverse-matching", help="Inverse matching string")
    # Add positional arguments for the operation (plot or print) and the files
    parser.add_argument(
        "operation", choices=["plot", "print"], help="Specify 'plot' or 'print' action."
    )
    # default argument list of files
    parser.add_argument("files", nargs="+", help="Files to print")

    args = parser.parse_args()

    for f in args.files:
        aos = babyyoda.read(f)
        for k, v in aos.items():
            if args.matching and re.search(args.matching, k) is None:
                continue
            if (
                args.inverse_matching
                and re.search(args.inverse_matching, k) is not None
            ):
                continue

            if isinstance(v, HISTO1D_V2) or isinstance(v, HISTO2D_V2):
                if args.operation == "print":
                    print(k)
                    print_hist(v, summary=True, title=v.title())
                if args.operation == "plot":
                    v.plot()
                    matplotlib.pyplot.show()
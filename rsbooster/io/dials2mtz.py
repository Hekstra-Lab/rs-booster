#!/usr/bin/env python
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import glob


from reciprocalspaceship.io import read_dials_stills


def get_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "dirnames",
        type=str,
        nargs="+",
        help="diffBragg.stills_process output folder(s) with *integrated.refls",
    )
    parser.add_argument("mtz", type=str, help="output mtz name")
    parser.add_argument(
        "--ucell",
        default=None,
        nargs=6,
        required=True,
        type=float,
        help="unit cell params (default will be average experiment crystal)",
    )
    parser.add_argument("--symbol", type=str, default=None, required=True)
    parser.add_argument("--verbose", action="store_true", help="show some stdout")
    parser.add_argument("--extra-cols", dest="extra_cols", nargs="+", type=str, default=None, help="attemp to pull in additional columns")
    parser.add_argument("--ext", type=str, default="integrated.refl", help="read files with this extension")
    parser.add_argument("--tag", type=str, default=None, help="only select files containing this string")
    return parser


def print_refl():
    parser = ArgumentParser()
    parser.add_argument("reflfile", type=str, help="path to a integrated.refl file")
    args = parser.parse_args()
    from reciprocalspaceship.io import print_refl_info
    print_refl_info(args.reflfile)


def _write(ds, mtzname, verbose=False):
    """write the RS dataset to mtz file"""
    if verbose:
        print(f"Writing MTZ {mtzname} ...")
    ds.write_mtz(mtzname)
    if verbose:
        print("Done writing MTZ.")


def get_fnames(dirnames, verbose=False, optional_tag=None, ext="integrated.refl"):
    """

    Parameters
    ----------
    dirnames: list of str, folders to search for files
    verbose: bool, whether to print stdout
    optional_tag: str, only select files whose names contain this string
    ext: str, only select files ending with this string

    Returns
    -------
    list of filenames
    """
    fnames = []
    for dirname in dirnames:
        fnames += glob.glob(dirname + f"/*{ext}")
    if verbose:
        print(f"Found {len(fnames)} files")
    if optional_tag is not None:
        fnames = [f for f in fnames if optional_tag in f]
        if verbose:
            print(f"Selected {len(fnames)} files with {optional_tag} in the name.")
    if not fnames:
        raise IOError(f"No filenames were found for loading with dirnames={dirnames}, optional_tag={optional_tag}, and ext={ext}")
    return fnames


def ray_main():
    parser = get_parser()
    parser.add_argument("--numjobs", default=10, type=int, help="number of workers!")
    args = parser.parse_args()

    fnames = get_fnames(args.dirnames, args.verbose, optional_tag=args.tag, ext=args.ext)
    ds = read_dials_stills(fnames, unitcell=args.ucell, spacegroup=args.symbol, numjobs=args.numjobs,
                           parallel_backend="ray", extra_cols=args.extra_cols, verbose=args.verbose, 
                           mtz_dtypes=True)
    _write(ds, args.mtz, args.verbose)


def mpi_main():
    parser = get_parser()
    args = parser.parse_args()
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    fnames = get_fnames(args.dirnames, args.verbose, optional_tag=args.tag, ext=args.ext)
    ds = read_dials_stills(fnames, unitcell=args.ucell, spacegroup=args.symbol, parallel_backend="mpi",
                           extra_cols=args.extra_cols, verbose=args.verbose, comm=comm
                           mtz_dtypes=True)
    if comm.rank == 0:
        _write(ds, args.mtz, args.verbose)


if __name__ == "__main__":
    ray_main()

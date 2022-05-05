from setuptools import setup, find_packages

setup(
    name="efxtools",
    version="0.0.3",
    author="Jack B. Greisman",
    author_email="greisman@g.harvard.edu",
    packages=find_packages(),
    description="",
    install_requires=["reciprocalspaceship", "matplotlib", "seaborn"],
    entry_points={
        "console_scripts": [
            "efxtools.extrapolate=efxtools.esf.extrapolate:main",
            "efxtools.scaleit=efxtools.scaleit.scaleit:main",
            "efxtools.internal_diffmap=efxtools.diffmaps.internaldiffmap:main",
            "efxtools.ccsym=efxtools.stats.ccsym:main",
            "efxtools.ccanom=efxtools.stats.ccanom:main",
            "efxtools.ccpred=efxtools.stats.ccpred:main",
            "efxtools.diffmap=efxtools.diffmaps.diffmap:main",
            "efxtools.precog2mtz=efxtools.io.precog2mtz:main",
            "efxtools.find_peaks=efxtools.realspace.find_peaks:find_peaks",
            "efxtools.find_difference_peaks=efxtools.realspace.find_peaks:find_difference_peaks",
        ]
    },
)

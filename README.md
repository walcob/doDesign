# doDesign
Quick script for running fixed backbone design using PyRosetta

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This script requires the user to have a license and copy of PyRosetta version 4.  Licensing is free for academic and non-profit institutions and is available to commercial users for a fee.  Please see [PyRosetta](http://pyrosetta.org/dow) for more details.

### How to use

Simply download and run doDesign.py in your terminal.  There are several command-line arguments that doDesign.py takes.  You can find more details about those by executing

```
/usr/bin/python doDesign.py -h
```
which will yield the following description:
```
usage: doDesign.py [-h] [-f input.pdb] [-res RESFILE] [-o output] [-j JOBS]
                   [--pymol] [-sfxn SFXN]

optional arguments:
  -h, --help    show this help message and exit
  -f input.pdb  input PDB file for design
  -res RESFILE  resfile to use for design
  -o output     output file stem (don't include the .pdb)
  -j JOBS       number of times to perform design (default: 1)
  --pymol       Outputs structures to PyMOL instance (default: False)
  -sfxn SFXN    ScoreFunction to use for design (default: ref2015)
```

For more info on how to create resfiles please see the [Rosetta Documentation](https://www.rosettacommons.org/manuals/archive/rosetta3.5_user_guide/d1/d97/resfiles.html).  To use the PyMOL output, you must also run the script ```PyMOL-RosettaServer.py``` (included with PyRosetta) within an instance of PyMOL before running this script.

```
run PyMOL-RosettaServer.py
```

If not supplied, the options will be set to their default values.  Options without a default value are mandatory.

## Example
Let's take, for example, the Trp-cage protein (pdb code 1L2Y) and save it as ```1L2Y.pdb```

We want to redesign every residue of the protein to allow substitution with any other amino acid.  To do this, create a resfile ```1L2Y.res``` with the following content:

```
ALLAA
start
```

If we want to generate 300 structures and monitor our output in PyMOL we could use doDesign as follows:
```
/usr/bin/python doDesign.py -f 1L2Y.pdb -res 1L2Y.res -o 1L2Y_out -j 300 --pymol
```

Our PyMOL instance should now be displaying our new structures and they should be output as pdb files with the name ```1L2Y_out_n.pdb``` where n is a number corresponding to which of the 300 structures it is.

An additional file, ```1L2Y_out.fasc``` will be generated, summarizing the energy of each design.
## Authors

* **Benjamin Walcott** - [walcob](https://github.com/walcob)

## Acknowledgments

* RosettaCommons

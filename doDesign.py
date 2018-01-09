#!/usr/bin/env python

from pyrosetta import *
from rosetta import *
#Fixbb imports
from pyrosetta.rosetta.core.pack.task import *
from pyrosetta.rosetta.core.pack.task import parse_resfile
from pyrosetta.rosetta.protocols.simple_moves import PackRotamersMover
from pyrosetta.rosetta.core.scoring.constraints import ResidueTypeLinkingConstraint
from pyrosetta.rosetta.core.scoring import *
import argparse


# protocols.moves.AddPyMOLObserver(test_pose,True)

def main():
    # initialize argument parser
    parser = argparse.ArgumentParser()
    # input pdb -f
    parser.add_argument('-f',dest="pdb",metavar="input.pdb",help="input PDB file for design")
    # input resfile -res
    parser.add_argument('-res',help='resfile to use for design',dest='resfile')
    # output pdb extension -o
    parser.add_argument('-o',help='output file stem (don\'t include the .pdb)',metavar="output",dest='output')
    # number of times you want to perform design -j
    parser.add_argument('-j',help='number of times to perform design (default: 1)',default=1,dest='jobs',type=int)
    # use PyMOL mover --pymol
    parser.add_argument("--pymol",help="Outputs structures to PyMOL instance (default: False)",action="store_true")
    # scorefunction choice -sfxn
    parser.add_argument('-sfxn',help='ScoreFunction to use for design (default: ref2015)',default="ref2015")
    # parse the arguments
    args = parser.parse_args()
    # Run Fixbb
    fixbb(args.pdb,args.resfile,args.output,args.jobs,args.sfxn,args.pymol)
    
def fixbb(pdb,resfile,output,jobs=1,sfxn = "ref2015",pymol = False):
    # Initialize Rosetta
    init()
    # Create a pose from pdb
    pose = Pose()
    pose_from_file(pose,pdb)
    
    # Create a copy of pose for testing
    testPose = Pose()
    testPose.assign(pose)
    
    # Setup ScoreFunction    
    scorefxn = create_score_function(sfxn)
    
    # Setup Fixbb design
    designPack = TaskFactory.create_packer_task(testPose)
    parse_resfile(testPose,designPack,resfile)
    packMover = PackRotamersMover(scorefxn,designPack)
    
    # Setup PyJobDistributor
    jd = PyJobDistributor(output,jobs,scorefxn)
    
    # PyMOL observer
    if pymol: protocols.moves.AddPyMOLObserver(testPose,True)
    
    # Perform Fixbb Design
    counter = 0 # For pretty output
    while not jd.job_complete:
        # Reset testPose
        testPose.assign(pose)
        counter += 1
        # rename pose for pretty output to PyMOL
        testPose.pdb_info().name("%s_%i"%(output,counter))
        packMover.apply(testPose)
        # output decoy
        jd.output_decoy(testPose)
        
if __name__ == '__main__': main()
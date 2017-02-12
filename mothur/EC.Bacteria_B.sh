#!/bin/bash
#PBS -k o
#PBS -l nodes=1:ppn=16,vmem=500gb,walltime=72:00:00
#PBS -M mmuscare@indiana.edu,lennonj@indiana.edu
#PBS -m abe
#PBS -j oe
cd /N/dc2/projects/Lennon_Sequences/2017_EvolutionCanyon/
module load gcc/4.9.2
module load boost/1.52.0
module load mothur/1.39.0
mothur EC.Bacteria_B.Batch

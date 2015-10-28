#!/bin/bash

#input file of cds for all genomes = cds.fasta each sequence i.d. should be the genome i.d. followed by a "_" and unique 
#locus tag, e.g. ">genome1_locus123"

#find cds clusters = 'genes'
usearch -cluster_fast cds.fasta -id 0.60 -centroids centroids.fasta -consout cons.fasta -sort size -uc clusters.uc

#sort clusters
sort -nk2 clusters.uc > clusters_sorted.uc

#make a table of results, pangenome.txt
python ~/s/gene-matrix-from-uclust2.py clusters_sorted.uc pangenome.txt 95

#annotate the list of cds
python ~/s/cds_annotation.py centroids.fasta nr cds.blast p 1e-5

#the title colum of the cds.blast output can then be directly inserted into pangenome.txt (following sorting 
#to ensure names match-up)

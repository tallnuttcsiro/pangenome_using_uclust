import os
import re
import glob
import sys
import subprocess	

#T. Allnutt, CSIRO, 2015
#script to parse the uclust .uc file and make a table of clusters with their %identity
#usage: gene-matrix-from-uclust2.py clusters_sorted.uc pangenome.txt 60
#nb '95' is the identiy threshold below which presence of a gene is not scored

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
			  
			  
f = open(sys.argv[1],'r')

g = open(sys.argv[2],'w')

id_thresh=float(sys.argv[3])

#shared_tot=int(sys.argv[3])

data = {}
hitlist=[]
c=1
ct=0
n=0
for line in f:
	k = line.split("\t")
	if k[0]<>"S":
		
		hit=k[8].split("_")[0] #nb the "_" separates the cds number from the genome id, so only score the genome id as a hit
		if hit not in hitlist:
			hitlist.append(hit)
	
	
		if k[0]=="C":
			n=0
			ct=ct+1	
			cds = k[8]
			data[cds]={} #new cluster
			data[cds][hit]=float(1) #self identity
			print "cluster",ct,cds	
		if k[0]=="H":
			id = float(k[3])/100
			
			if id*100>id_thresh:
				n=n+1
				print "cluster",ct,cds,n, id
				if hit not in data[cds].keys():				
					data[cds][hit]=id
					
				elif id>data[cds][hit]: #keep highest id only
				
					data[cds][hit]=id
		
	
print "writing"
hitlist.sort(key=tokenize)		

title="\t"+"\t".join(str(p)for p in hitlist)+"\n"
g.write(title)
output=""
for i in data.keys():
	c=c+1
	output = output+i
	for j in hitlist:
		if j in data[i].keys():
			output = output +"\t"+str(data[i][j])
		else:
			output = output +"\t"+"0"
	g.write(output+"\n")
	output=""
	

	
		
















	

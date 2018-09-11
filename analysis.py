from PBSMA import *
from OS_helper import *
import os

######## Script constants. Don't change!!!! ########
reverse_primer_dir = "Primer/Reverse_Primer/"
forward_primer_dir = "Primer/Forward_Primer/"
probe_dir = "Probe/"
check_fasta_dir = ["Human", "Animal", "Both"] # Directories that should contain fasta files
######## Script constants. Don't change!!!! ########

FASTA_root_dir = "Influenza A virus M gene"
job_title = "M_gene_WHO2017_p8"
max_mutation_cnt = 5
query_dir = probe_dir

inp = raw_input("Please enter the FASTA root pathway ( default "+ FASTA_root_dir +" ) :: ").strip()

if len(inp) != 0 :
	FASTA_root_dir = inp

if not checkDirExistinCWD(FASTA_root_dir) :
	print "FASTA root directory doesn't exist ... The program will exit here. "
	sys.exit(1)

inp = raw_input("Please enter the Job title ( default "+ job_title +" ) :: ").strip()

if len(inp) != 0 :
	job_title = inp

inp = raw_input("Please enter the type of query ( default forward, you can also input reverse or probe ) :: ").strip()

if len(inp) == 0 or inp == "forward" :
	query_dir = forward_primer_dir
elif inp == "probe" :
	query_dir = probe_dir
elif inp == "reverse" :
	query_dir = reverse_primer_dir
else :
	print "Unknow input ... The script will end here ... "
	sys.exit(0)

tag = startTimer(None)

FASTA_root_dir = os.path.join(getCurrentDir(),FASTA_root_dir)
query_dir = os.path.join(FASTA_root_dir, query_dir)
query_file = listFilesOfGivenExt(query_dir,"fasta")

if len(query_file) < 1 :
	print "Query file cannot be found ... The script will end here ... "
	sys.exit(0)
else :
	query_file = query_file[0]

fasta_dir = checkDir(FASTA_root_dir, check_fasta_dir)

fts = getFileTimeStamp()
createDirAtCWD(fts)

chDir(FASTA_root_dir)

res={}
alignCnt={}
PBS={}
misCnt={}

for i in range(len(check_fasta_dir)) :
	if fasta_dir[i] :
		chDir(check_fasta_dir[i])
		for d in listOnlyDir(getCurrentDir()):
			chDir(d)
			for fa in listFilesOfGivenExt(getCurrentDir(), "fasta") :
				align_res = runBLAST(query_dir, query_file, getFileName(fa))
				dummy, dummy2, res[getFileName(fa)] = calMismatch(align_res)
				alignCnt[getFileName(fa)] = len(dummy)
				misCnt[getFileName(fa)] = calMismatchCount(dummy, max_mutation_cnt)
				PBS[getFileName(fa)] = primerBindingSite(align_res)
			chDir("..")
		chDir("..")

chDir("..")
chDir(fts)

with open("README", "w") as f :
	f.write("Job title : " + job_title +"\n")
	f.write("Maximum mutation count : " + str(max_mutation_cnt) +"\n")
	f.write("query_dir : " + query_dir +"\n")
	f.write("query_file : " + query_file +"\n")
	f.write("FASTA_root_dir : " + FASTA_root_dir +"\n")

for p in PBS :
	with open("PBS_"+str(p)+".ra", "w") as f : # ra for raw alignment
		for l in PBS[p] :
			f.write(l+"\n")
	f.close()

def getYear(s) :
	s = s.split('_')[2]
	if s == 'ALL' :
		s = -1
	return s

def getStrain(s) :
	return s.split('_')[1]

def getGeneSeg(s) :
	return s.split('_')[-1]

with open("MC_"+job_title+".csv", "w") as f :
	mutation_cnt_header=range(max_mutation_cnt+1)
	for i in range(len(mutation_cnt_header)):
		mutation_cnt_header[i] = str(mutation_cnt_header[i]) + " mismatch"
	mutation_cnt_header.append("more than "+str(max_mutation_cnt)+" mismatch")
	mutation_cnt_header=",".join(mutation_cnt_header)
	f.write("IAV Strain, Gene Seg, Year, Total number of sequence,"+mutation_cnt_header+"\n")
	MCList=[]
	for mc in misCnt:
		sumMC=sum(misCnt[mc])
		MCList.append( [ getStrain(mc), getGeneSeg(mc), getYear(mc), sumMC, misCnt[mc] ]  )
	MCList.sort(key=lambda x:x[2], reverse=True)
	MCList.sort(key=lambda x:x[1], reverse=True)
	MCList.sort(key=lambda x:x[0], reverse=True)
	for i in range(len(MCList)):
		if MCList[i][2] == -1 :
			MCList[i][2] = "ALL"
		f.write(",".join( [ str(ele) for ele in MCList[i][:-1] ] + [ str(ele) + "("+ str(round((float(ele)/MCList[i][3]*100), 2)) +")" for ele in MCList[i][-1] ] )+"\n")

f.close()

chDir("..")

endTimer(tag)

sys.exit(0)

from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
import os

Sym2Base = {
	'A': ["A"],
	'T': ['T'],
	'C': ['C'],
	'G': ['G'],
	'U': ['U'],
	'W': ['A','T'],
	'S': ['C','G'],
	'M': ['A','C'],
	'K': ['G','T'],
	'R': ['A','G'],
	'Y': ['C','T'],
	'B': ['C','G','T'],
	'D': ['A','G','T'],
	'H': ['A','C','T'],
	'V': ['A','C','G'],
	'N': ['A','T','C','G'],
	'Z': [],
	'-': []
}

BASES = ['A','T','C','G', 'U']

def anyMatch(l1,l2) :
	for i in l1 :
		if i in l2 :
			return True
	return False

def runBLAST(primer_dir, primer_file, db_name):

	Alignment_Result = {}

	cmd = NcbiblastnCommandline(
		query=os.path.join(primer_dir,primer_file),
		max_hsps=1,
		db=db_name,
		evalue=0.1,
		num_alignments=99999,
		word_size=5,
		outfmt=5,
		strand="plus",
		out="my_blast.xml"
	)

	stdout, stderr = cmd()
	result_handle = open("my_blast.xml")
	blast_records = NCBIXML.read(result_handle)

	for alignment in blast_records.alignments:
		for hsp in alignment.hsps:
			Alignment_Result[alignment.title] = {
				"identities": hsp.identities,
				"QLength": len(hsp.query),
				"query": hsp.query.upper(),
				"sbjct": hsp.sbjct.upper(),
				"evalue": hsp.expect,
				"match pattern": hsp.match,
				"MismatchCnt": int(str(hsp.match).count(' '))
			}

			if len(hsp.query) != len(hsp.sbjct) :
				Alignment_Result[alignment.title]["identities"] = -1
			else :
				for i in range(len(hsp.query)) :
					if hsp.sbjct[i] in BASES :
						if hsp.sbjct[i] in Sym2Base[hsp.query[i]] :
							Alignment_Result[alignment.title]["identities"] += 1
					else :
						if anyMatch(Sym2Base[hsp.query[i]], Sym2Base[hsp.sbjct[i]]) :
							Alignment_Result[alignment.title]["identities"] += 1
				Alignment_Result[alignment.title]["MismatchCnt"] = len(hsp.query) - Alignment_Result[alignment.title]["identities"]

			if len(hsp.query) != len(hsp.sbjct) or len(hsp.query) != len(hsp.match) :
				print alignment.title
				print hsp.query
				print hsp.match
				print hsp.sbjct
				print "Not the same ..."
	try :
		os.remove("my_blast.xml")
	except:
		pass

	return Alignment_Result

def calMismatch(Alignment_Result) :
	res={}
	average_mismatch=[0,0]
	for ar in Alignment_Result :
		mismatch = Alignment_Result[ar]["QLength"]-Alignment_Result[ar]["identities"]
		res[ar] = mismatch
		average_mismatch[0] += mismatch
		average_mismatch[1] += 1
	return Alignment_Result, res, float(average_mismatch[0])/average_mismatch[1]

def primerBindingSite(Alignment_Result) :
	pbs = []
	for ar in Alignment_Result :
		pbs.append(str(Alignment_Result[ar]["sbjct"]))
	return pbs

def calMismatchCount(Alignment_Result, max_mismatch=5) :
	cnt=[0]*(max_mismatch+2)
	for ar in Alignment_Result :
		if Alignment_Result[ar]["MismatchCnt"] > max_mismatch :
			cnt[max_mismatch+1] += 1
		else :
			cnt[Alignment_Result[ar]["MismatchCnt"]] += 1
	return cnt

if __name__=="__main__" :
	pass
else :
	print "Importing PBSMA"

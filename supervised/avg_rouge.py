'''
	Generate average scores, top 5, worse 5 for any given score
'''
import sys
import yaml
from prettytable import PrettyTable

''' Output
+-----------------+-----------+---------+---------+-----------+---------+---------+-----------+---------+---------+
|        #        |  rouge-1  |    .    |    ..   |  rouge-2  |     .   |    ..   |  rouge-l  |    .    |   ..    |
+-----------------+-----------+---------+---------+-----------+---------+---------+-----------+---------+---------+
|        #        | precision |  recall |  fscore | precision |  recall |  fscore | precision |  recall |  fscore |
|       CRF       |  0.34078  | 0.38644 | 0.35105 |  0.16195  | 0.17172 | 0.15945 |  0.30432  | 0.34368 | 0.29736 |
|      letsum     |  0.27676  | 0.40822 | 0.29818 |  0.06866  | 0.11241 | 0.07327 |  0.25286  | 0.37165 | 0.2356  |
+-----------------+-----------+---------+---------+-----------+---------+---------+-----------+---------+---------+
'''

def averaged(scores, rougex, metric):
	'''
		Rougex is which rouge, metric is f / p / r
	'''
	l = list()
	for case in scores:
		l.append( scores[case][rougex][metric] )

	av = sum(l) / len(l)
	return round(av, 5)


def avg_rouge(results_file):
	with open(results_file, 'r') as f:
		txt = f.readlines()

	scores = {}
	skipped_files = 0
	for line in txt:
		t = list( filter( None, line.split(' ') ) )
		arrow = t.index('=>')
		score = ''.join( t[ arrow+1 : ] ).rstrip()
		file = t[arrow-1]

		if score == 'Skipped':
			skipped_files += 1
			# print(file)
			continue
		scores[file] = yaml.load(score)

	print(len(scores))
	print('Skipped', skipped_files)
	print(len(scores) + skipped_files)

	pt = PrettyTable()
	pt.field_names = ['#', 'rouge-1', '.', '..', 'rouge-2', ' .', ' ..', 'rouge-l', '. ', '.. ']
	pt.add_row(['#', 'precision', 'recall', 'fscore', 'precision', 'recall', 'fscore', 'precision', 'recall', 'fscore'])

	p1, p2, pl = averaged(scores, 'rouge-1', 'p'), averaged(scores, 'rouge-2', 'p'), averaged(scores, 'rouge-l', 'p')
	r1, r2, rl = averaged(scores, 'rouge-1', 'r'), averaged(scores, 'rouge-2', 'r'), averaged(scores, 'rouge-l', 'r')
	f1, f2, fl = averaged(scores, 'rouge-1', 'f'), averaged(scores, 'rouge-2', 'f'), averaged(scores, 'rouge-l', 'f')

	out = [results_file, p1, r1, f1, p2, r2, f2, pl, rl, fl]
	pt.add_row(out)
	# print(pt)
	print ( '\t'.join([str(x) for x in out]) )


if __name__ == '__main__':
	if len(sys.argv) > 1:
		file = sys.argv[1]
	else:
		file = input('Enter file to average out')
	avg_rouge(file)
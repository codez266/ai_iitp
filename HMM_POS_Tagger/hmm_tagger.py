import sys
import numpy as np
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import os

emission_probs = {}
tag_counts = {}
transition_probs = {}
acc_list = []
macro_f1 = []
micro_f1 = []
weighted_f1 = []
macro_f1_class = []


def custom_evaluation(pred_file, gold_file):
	instances = 0.0
	correct = 0.0
	with open(pred_file,'r') as reader:
		with open(gold_file,'r') as reader2:
			while 1:
				pred = reader.readline()
				if not pred:
					break
				words_pred = pred.split(' ')
				words_gold = reader2.readline().split(' ')
				#print(str(len(words_gold))+' '+str(len(words_pred)))
				instances += len(words_gold)
				for i in xrange(len(words_pred)):
					if words_pred[i] in words_gold[i] or words_gold[i] in words_pred[i]:
						correct += 1.0

	print (correct/instances)

def print_cm(cm, labels, file, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    file.write('Confusion Matrix:\n')
    columnwidth = max([len(x) for x in labels]+[5]) # 5 is value length
    empty_cell = " " * columnwidth
    for i, label1 in enumerate(labels):
        file.write("    %{0}s".format(columnwidth) % label1,)
        for j in range(len(labels)): 
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            file.write(cell,)
        file.write('\n')


def evaluation(pred_file, gold_file, flag, directory):
	f = open(os.path.join(directory, 'results'+str(flag)+'.txt'), 'w')
	gold = []
	pred = []
	with open(pred_file,'r') as reader:
		for line in reader:
			words = line.split(' ')
			for word in words:
				pred.append(word)
	with open(gold_file,'r') as reader2:
		for line in reader2:
			words = line.split(' ')
			for word in words:
				gold.append(word)

	labels = []
	for key in tag_counts:
		labels.append(key)

	f.write("Macro-Averaged F1: "+str(f1_score(gold, pred, average='macro'))+'\n')
	macro_f1.append(f1_score(gold, pred, average='macro'))
	f.write("Accuracy: "+str(accuracy_score(gold, pred))+'\n')
	acc_list.append(accuracy_score(gold, pred))
	f.write("Micro-Averaged F1: "+str(f1_score(gold, pred, average='micro'))+'\n')
	micro_f1.append(f1_score(gold, pred, average='micro'))
	f.write("Weighted-Averaged F1: "+str(f1_score(gold, pred, average='weighted'))+'\n')
	weighted_f1.append(f1_score(gold, pred, average='weighted'))
	f.write("Macro-Averaged F1 by class:\n "+str(f1_score(gold, pred, average=None))+'\n')
	macro_f1_class.append(f1_score(gold, pred, average=None))
	cm = confusion_matrix(gold, pred, labels)

	# then print it in a pretty way
	print_cm(cm, labels, f)

	f.close()

def calculate(file):
	instances = 0.0
	with open(file,'r') as reader:
		for line in reader:
			instances += 1.0
			line = "strt_START "+line.strip()+" stp_STOP"
			splited = line.strip().split(' ')
			for splitter in splited:
				if '_' not in splitter:
					continue
				word = splitter.split('_')[0]
				tag = splitter.split('_')[1]
				if tag in tag_counts:
					tag_counts[tag] += 1.0
				else:
					tag_counts[tag] = 1.0
				if word in emission_probs:
					if tag in emission_probs[word]:
						emission_probs[word][tag] += 1.0
					else:
						emission_probs[word][tag] = 1.0
				else:
					emission_probs[word] = {}
					emission_probs[word][tag] = 1.0

			for i in range(1,len(splited)):
				if '_' not in splited[i]:
					continue
				if '_' not in splited[i-1]:
					first_tag = splited[i-2].split('_')[1]
				else:
					first_tag = splited[i-1].split('_')[1]
				second_tag = splited[i].split('_')[1]
				bigram = first_tag+' '+second_tag
				if bigram in transition_probs:
					transition_probs[bigram] += 1.0
				else:
					transition_probs[bigram] = 1.0

	#print emission_probs
	#print tag_counts
	#print transition_probs

	for key in emission_probs:
		for subkey in emission_probs[key]:
			emission_probs[key][subkey] /= tag_counts[subkey]

	for key in transition_probs:
		words = key.strip().split(' ')
		transition_probs[key] /= tag_counts[words[0]]
	
	#print emission_probs
	#print transition_probs


def viterbi_tagger(file, flag, directory):
	f = open(os.path.join(directory, 'pred_tags'+str(flag)+'.txt'), 'w')
	with open(file, 'r') as reader:
		for line in reader:
			line = "strt "+line.strip()
			dp = {}
			bp = {}
			words = line.strip().split(' ')
			n = len(words)
			dp[0] = {}
			dp[0]['START'] = 1.0
			for i in range(1,n):
				dp[i] = {}
				bp[i] = {}
				if words[i] not in emission_probs:
					emission_probs[words[i]] = {}
					emission_probs[words[i]]['NP'] = 1.0
				for tag in emission_probs[words[i]]:
					max_prob = float("-inf")
					most_prob_tag = ''
					for prev_tag in emission_probs[words[i-1]]:
						bigram = prev_tag+' '+tag
						trans_prob = 0.0
						if bigram in transition_probs:
							trans_prob = transition_probs[bigram]
						tag_prob = dp[i-1][prev_tag] * trans_prob * emission_probs[words[i]][tag]
						if(tag_prob > max_prob):
							max_prob = tag_prob
							most_prob_tag = prev_tag
					dp[i][tag] = max_prob
					bp[i][tag] = prev_tag


			final_max_prob = float("-inf")
			ending_tag = ''
			for prev_tag in emission_probs[words[n-1]]:
				bigram = prev_tag+' STOP'
				trans_prob = 0.0
				if bigram in transition_probs:
					trans_prob = transition_probs[bigram]
				tag_prob = dp[n-1][prev_tag] * trans_prob
				if tag_prob > final_max_prob:
					final_max_prob = tag_prob
					ending_tag = prev_tag

			
			original_sequence = ending_tag
			#print original_sequence
			tag_ahead = ending_tag
			for i in range(n-2, 0, -1):
				#print tag_ahead
				tag_ahead = bp[i+1][tag_ahead]
				original_sequence += ' '+tag_ahead

			tags = original_sequence.split(' ')
			tag_sequence = ''
			for i in range(len(tags)-1, -1, -1):
				tag_sequence += tags[i]+' '
			f.write(tag_sequence+'\n')

	f.close()



if __name__ == '__main__':
	instances = 0
	with open(str(sys.argv[1]), 'r') as reader:
		for line in reader:
			instances += 1


	for i in xrange(5):
		count = 0
		directory = 'Cross_Validation'+str(i)
		if not os.path.exists(directory):
			os.makedirs(directory)
		train_file = open(os.path.join(directory, 'train_file'+str(i)+'.txt'), 'w')
		test_file = open(os.path.join(directory, 'test_file'+str(i)+'.txt'), 'w')
		test_gold = open(os.path.join(directory, 'test_gold'+str(i)+'.txt'), 'w')
		with open(str(sys.argv[1]), 'r') as reader:
			for line in reader:
				count += 1
				if count >= (instances*i)/5 and count < (instances*(i+1))/5:
					words = line.strip().split(' ')
					for word in words:
						if '_' in word:
							test_file.write(word.split('_')[0]+' ')
							test_gold.write(word.split('_')[1]+' ')
					test_file.write('\n')
					test_gold.write('\n')
				else:
					train_file.write(line)

		train_file.close()
		test_gold.close()
		test_file.close()
		calculate(os.path.join(directory, 'train_file'+str(i)+'.txt'))
		viterbi_tagger(os.path.join(directory, 'test_file'+str(i)+'.txt'), i, directory)
		evaluation(os.path.join(directory, 'pred_tags'+str(i)+'.txt'), os.path.join(directory, 'test_gold'+str(i)+'.txt'), i, directory)
		#custom_evaluation('pred_tags.txt', 'test_gold.txt')
	f = open('final_results.txt', 'w')

	f.write("Macro-Averaged F1: "+str(float(sum(macro_f1))/len(macro_f1))+'\n')
	f.write("Accuracy: "+str(float(sum(acc_list))/len(acc_list))+'\n')
	f.write("Micro-Averaged F1: "+str(float(sum(micro_f1))/len(micro_f1))+'\n')
	f.write("Weighted-Averaged F1: "+str(float(sum(weighted_f1))/len(weighted_f1))+'\n')
	avg = [float(sum(col))/len(col) for col in zip(*macro_f1_class)]
	f.write("Macro-Averaged F1 by class:\n "+str(avg)+'\n')
	f.close()
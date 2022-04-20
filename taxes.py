#!/usr/bin/python3
def my_is_decimal(string):
	for i in string:
		if not ('0' <= i <= '9' or i == '.'):
			return False
	return True
		
def get_thresholds():
	global exonerated
	thresholds = [(0, 0, 0)]
	read_flag = 0
	try:
		fd = open("brackets.txt")
		line_count = 1
		while 1:
			line = fd.readline()
			if line == "":
				break
			if '\n' in line:
				line = line[:-1]
			items = line.split()
			if items[0] == "exonerated" and len(items) > 1 and my_is_decimal(items[1]):
				exonerated = float(items[1])
				line_count += 1
				continue
			if len(items) != 3:
				print("line {}: wrong number of items, have {} instead of 3".format(line_count, len(items)))
				read_flag = 1
				raise Exception('file syntax error')
			for i in items:
				flag = 0
				if not my_is_decimal(i):
					if not i == "inf":
						print("one of the fields in your input is not a number")
						flag = 1
						break
			if flag == 1:
				raise Exception('file syntax error')
			min = float(items[0])
			if min < thresholds[len(thresholds) - 1][1]:
				print("line {}: lower bracket is lower than previous upper bracket".format(line_count))
				read_flag = 1
				raise Exception('file syntax error')
			max = float(items[1])
			if max < min:
				print("line {}: upper bracket is lower than lower bracket".format(line_count))
				read_flag = 1
				raise Exception('file syntax error')
			perc = float(items[2])
			if perc < 0:
				print("line {}: negative percentage".format(line_count))
				read_flag = 1
				raise Exception('file syntax error')
			thresholds.append((min, max, perc))
			line_count += 1
		return thresholds[1:]
	
	except:
		if read_flag == 1:
			print("problem in 'thresholds.taxes' ")
		else:
			print("file 'thresholds.taxes' not found")
		inpt = input("Do you want to input thresholds manually ? (y / n): ")
		while (inpt.upper() != "Y" and inpt.upper() != "N"):
			inpt = input("type in a 'y' for yes or 'n' for no and press enter")
		if inpt.upper() == 'N':
			print("exiting...")
			exit()
		
		while 1:
			inpt = input("input threshold in the following pattern:\n'min max percentage'\npress 'enter' on an empty line to finish input\n")
			if inpt == "":
				break
			line = inpt.split()
			flag = 0
			for i in line:
				if not my_is_decimal(i):
					if not i == "inf":
						print("one of the fields in your input is not a number")
						flag = 1
						break
			if flag == 1:
				continue
			if len(line) != 3:
				print("incorrect number of items in input")
				continue
			min = float(line[0])
			if min < thresholds[len(thresholds) - 1][1]:
				print("lower bracket is lower than previous upper bracket")
				continue
			max = float(line[1])
			if max < min:
				print("upper bracket is lower than lower bracket")
				continue
			perc = float(line[2])
			if perc < 0:
				print("negative percentage")
				continue
			thresholds.append((min, max, perc))
		inpt = input("is there an exonerated amount ?: ")
		if my_is_decimal(inpt):
			exonerated = float(inpt)
		fd = open("brackets.txt", "w+")
		fd.write("exonerated {}\n".format(exonerated))
		for i in thresholds[1:-1]:
			fd.write("{} {} {}\n".format(i[0], i[1], i[2]))
		fd.write("{} {} {}\n".format(thresholds[-1][0], thresholds[-1][1], thresholds[-1][2]))	
		return thresholds[1:]

if __name__ == '__main__':
	exonerated = 0
	thresholds = get_thresholds()
	exit()
	while 1:
		gross = input('enter your gross salary: (empty to quit program): ')
		if input == "":
			print("exiting...")
			exit()
		currency = "€"
		while not my_is_decimal(gross):
			gross = input('enter your gross salary (must be a number): ')
		gross = float(gross)
		gross_step = gross - exonerated
		if gross < exonerated:
			net = gross
			print("no taxes under {}{}".format(exonerated, currency))
			continue
		net = exonerated
		for i in thresholds:
			if gross_step > i[1]:
				net += (i[1] - i[0]) * (1 - (i[2] / 100))
			else:
				net += (gross_step - i[0]) * (1- (i[2] / 100))
				break
		print("net income = {}".format(net))
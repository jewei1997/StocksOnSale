with open("SnP500.txt", 'r') as reader:
    line = reader.readline()
    count = 0
    while line != '':
        line = reader.readline()
        if "external text" in line and not "sec.gov" in line:
            line = line[:len(line)-5]
            last_carrot_idx = -1
            while line[last_carrot_idx] != '>':
                last_carrot_idx-=1
            print(line[last_carrot_idx+1:])
            count+=1

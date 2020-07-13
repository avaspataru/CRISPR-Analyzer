#extract the doench guides as wu-crispr needs them (26 nucleotides)
INPUT_FILE_NAME = "Doench-2014.csv"


# Used for extracting the guide from the CSV format
GUIDE_INDEX = 1
GUIDE_START_POS = 10
GUIDE_LEN = 23

with open(INPUT_FILE_NAME, 'r') as fRead, open('Doench-Wu-Crispr.txt', 'w+') as fWrite:

    # read each line - file contains header and blank footer - then break apart by comma
    for line in [x.split(',') for x in fRead.read().split('\n')[1:-1]]:
        pos = line[1].find(line[0])
        fWrite.write(line[1][pos:pos+26]+'\n')

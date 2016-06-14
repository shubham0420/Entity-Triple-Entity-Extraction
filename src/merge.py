import glob,os

"""read_files = glob.glob("/home/nitin/Desktop/test/*.txt")
with open("wiki_merged.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())"""

"for rename"
#converting txt to json for dbpedia files
for filename in glob.iglob(os.path.join("/home/nitin/Desktop/attrib/", '*.txt')):
	os.rename(filename, filename[:-4] + '.json')

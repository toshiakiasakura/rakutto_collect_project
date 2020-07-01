import zipfile
import lxml
import glob
from lxml import etree


PATH = "/Users/shun/Desktop/excel_editing/excel_hacking_3.xlsx"


def main():
	O_FILE = PATH.replace(".xlsx", "")


	with zipfile.ZipFile(PATH) as zf:
	    zf.extractall(O_FILE)

	path2xml = O_FILE + "/xl/drawings/*.xml"
	paths = glob.glob(path2xml)
	for path in paths :
		tree = etree.parse(path)
		pathOutput = path[:-4] + "_pp.xml"
		tree.write(pathOutput, pretty_print=True)

if __name__ == "__main__":
	main()
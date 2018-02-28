# redundancyChecker.py
# Jiamin Li
# Reads all the files in a specified directory
# and prints a report of the lines that are
# identical in any pair of lines
# -------------------------------------
# File 1: <f1>
# File 2: <f2>
# Number of identical lines: <n>
# -------------------------------------
# *** <line_num_f1> < line_num_f2> <line_contents>
# *** <line_num_f1> < line_num_f2> <line_contents>

import os

class File():

    # Constructor
    # @name | name of the file
    # @lines | a list of tuples containing each line's content and its line number
    #                                               e.g [(1, "hello"), (2, "line2")]
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def get_name(self):
        return self.name

    # Returns a list of all the file's lines without the line numbers
    # Useful for comparing lines
    def get_lines(self):
        lines = (line[1] for line in self.lines)
        return lines

    # Gets the line number associated with a string line
    # @index | the line number
    def get_line_num(self, index):
        return str(self.lines[index][0]) 

########################################################
# Opens and reads each line in a file, cleans text     #
# Creates a list of File objects with attributes       #
########################################################

def create_file_set(validFiles):
    fileSet = [] # Contains a list of file objects
    
    for fileName in validFiles: # O(n^2)
        file = open(fileName, "r")
        lines = [(index, line.strip())
                 for index, line in enumerate(file, start=1)] # Strip white space + index each line (including empty lines)
        lines[:] = [line for line in lines if line[1] != ''] # Now we can remove empty lines from the list
        fileSet.append(File(fileName, lines))
        file.close()
        
    return fileSet


############################################################
# Takes in two file objects and compares lines for matches #
############################################################

def compare_lines(file1, file2):
    matched = [(i, j, line1) # O(n^2)
               for i, line1 in enumerate(file1.get_lines())
                    for j, line2 in enumerate(file2.get_lines())
                       if (line1 == line2)]
    
    return matched
                


def main():
    # Get path
    path = input("Type in directory path > ").strip()

    # Get a list of .py, .csv, or .txt file names in the specified directory and "store" in generator object
    validFiles = (fileName for fileName in os.listdir(path) if
                  ((".py" in fileName) or (".csv" in fileName) or (".txt" in fileName)))
    
    # Create a set of file objects with attributes (e.g. names, lines)
    fileSet = create_file_set(validFiles)

    ########################################################
    # Iterates over all possible file combinations
    # If identical lines are found, then print out report
    ########################################################
    
    print()
    for i in range(0, len(fileSet)): # O(n^3)
        for j in range(i+1, len(fileSet)):
            file1 = fileSet[i]
            file2 = fileSet[j]
            matched = compare_lines(file1, file2)
            if len(matched) != 0: # Number of identical lines
                # Print out report
                print("File 1: "+file1.get_name())
                print("File 2: "+file2.get_name())
                print("Number of identical lines: "+str(len(matched)))
                print("-------------------------------------")
                for line in matched:
                    print("***", end=" ")
                    print(file1.get_line_num(line[0])+", "+file2.get_line_num(line[1]), end=" ")
                    print("\""+line[2]+"\"")
        
                print("")

main()

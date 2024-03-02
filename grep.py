'''Usage: grep [options] pattern filename'''
import sys 
import re

'''Function to take the pattern and prepare it for grep to work as expected'''
def preparePattern(pattern, wordOnly=False):
    #the .*{pattern}*. wrapper is required to match the default of grep that
    #checks for the substring inside any string no mattern what surrounds the pattern.
    insideSurround = '.*'
    outsideSurround = '.*'

    #wordboundry check
    if wordOnly:
        insideSurround = insideSurround + r'\b'
        outsideSurround = r'\b' + outsideSurround

    return insideSurround +  pattern + outsideSurround
arguments = sys.argv
i = 1 # A index for where the pattern file starts

#finding and seting up flags
caseInsensitive, lineCount, invert, wordOnly = False, False, False, False
if '-i' in arguments:
    caseInsensitive = True
    i += 1
if '-c' in arguments:
    lineCount = True
    i += 1
if '-v' in arguments:
    invert = True
    i += 1
if '-w' in arguments:
    wordOnly = True
    i += 1

pattern = sys.argv[i]
pattern = preparePattern(pattern, wordOnly)
files = sys.argv[i+1:] #all the file names
lc = 0 #line count variable. used lc for convention

for file in files:
    with open(file, 'r') as f:
        lineLst = f.readlines()
        lineLst = [i.strip() for i in lineLst]
        for line in lineLst:
            result = None
            #matching the file through regex. 

            if(caseInsensitive):
                result = re.match(pattern, line, re.IGNORECASE)
            else:
                result = re.match(pattern, line)
            
            if invert:
                condition = result is None
            else:
                condition = result is not None

            if condition:
                lc += 1
                if not lineCount:
                    print(line) # Won't print lines if -l option is enabled
if (lineCount): 
    print(lc)

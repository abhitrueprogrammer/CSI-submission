'''Usage: grep [options] pattern filename'''
import sys 
import re

'''Function to take the pattern and prepare it for grep to work as expected'''
def preparePattern(pattern, wordOnly=False):
    #the .*{pattern}*. wrapper is required to match the default of grep that
    #checks for the substring inside any string no mattern what surrounds the pattern.
    inside_surround = '.*'
    outside_surround = '.*'

    #wordboundry check
    if wordOnly:
        inside_surround = inside_surround + r'\b'
        outside_surround = r'\b' + outside_surround

    return inside_surround +  pattern + outside_surround
arguments = sys.argv
i = 1 # A index for where the pattern file starts

#finding and seting up flags
case_insensitive, line_count, invert, word_only = False, False, False, False
if '-i' in arguments:
    case_insensitive = True
    i += 1
if '-c' in arguments:
    line_count = True
    i += 1
if '-v' in arguments:
    invert = True
    i += 1
if '-w' in arguments:
    word_only = True
    i += 1

pattern = sys.argv[i]
pattern = preparePattern(pattern, word_only)
files = sys.argv[i+1:] #all the file names
lc = 0 #line count variable. used lc for convention

for file in files:
    with open(file, 'r') as f:
        line_lst = f.readlines()
        line_lst = [i.strip() for i in line_lst]
        for line in line_lst:
            result = None
            #matching the file through regex. 

            if(case_insensitive):
                result = re.match(pattern, line, re.IGNORECASE)
            else:
                result = re.match(pattern, line)
            
            if invert:
                condition = result is None
            else:
                condition = result is not None

            if condition:
                lc += 1
                if not line_count:
                    print(line) # Won't print lines if -l option is enabled
if (line_count): 
    print(lc)

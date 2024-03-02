'''Usage: python3 grep [options] pattern filename'''
'''Example: python3 grep.py -n -w clear GOL.c grep.py'''
import sys 
import re
import os
'''Function to take the pattern and prepare it for grep to work as expected'''
'''Input: pattern and optionally status of word_only'''
'''Output: prepared string. '''
def preparePattern(pattern, word_only=False):
    #the .*{pattern}*. wrapper is required to match the default of grep that
    #checks for the substring inside any string no mattern what surrounds the pattern.
    inside_surround = '.*'
    outside_surround = '.*'

    #Adds wordboundry check if only word option is enabled
    if word_only:
        inside_surround = inside_surround + r'\b'
        outside_surround = r'\b' + outside_surround

    return inside_surround +  pattern + outside_surround
'''Check if file doesn't exist'''
'''Input: list of files'''
'''Return: File name that doesn't exist else 0'''
def fileNotExist(fileList):
    for file in fileList:
        if not( os.path.exists(os.path.join(os.getcwd(), file))):
            return file
    return 0
arguments = sys.argv
i = 1 # A index for where the pattern file starts

#finding and seting up flags
case_insensitive = show_only_matching_lc = invert = word_only = show_line_count = show_file_name = directory =lines_after =lines_before = False
if '-i' in arguments:
    case_insensitive = True
    i += 1
if '-c' in arguments:
    show_only_matching_lc = True
    i += 1
if '-v' in arguments:
    invert = True
    i += 1
if '-w' in arguments:
    word_only = True
    i += 1
if '-n' in arguments:
    show_line_count = True
    i += 1
if '-r' in arguments:
    i+=1
    directory = True
   
if '-A' in arguments:
    i+=2
    indexLine = arguments.index('-A') +1
    lines_after = int(arguments[indexLine])
if '-B' in arguments:
    i+=2
    indexLine = arguments.index('-B') +1
    lines_before = int(arguments[indexLine])
if '-C' in arguments:
    i+=2
    indexLine = arguments.index('-C') +1
    lines_after = int(arguments[indexLine])
    lines_before = int(arguments[indexLine])

pattern = sys.argv[i]
pattern = preparePattern(pattern, word_only)

#if -r set than search the directory that's mentioned as the first argument 
if directory:
    files = [f"./{sys.argv[i+1]}/" + filename for filename in os.listdir(sys.argv[i+1])]
    files = files + sys.argv[i+2:]
else:
    files = sys.argv[i+1:] #all the file names
ghostFile = fileNotExist(files)
if(ghostFile):
    print(f"ERROR: {ghostFile} doesn't exist")
    exit()
#need to show filenames if multiple files are included
if(len(files) > 1):
    show_file_name = True
found_instances_n = 0 #line count variable. used lc for convention

for file in files:
    with open(file, 'r') as f:
        lc = 0 #short for line count. Following the convention ;)
        line_lst = f.readlines()
        line_lst = [i.strip() for i in line_lst]
        for i in range(len(line_lst)):
            lc += 1
            #matching the file through regex. 
            
            if(case_insensitive):
                result = re.match(pattern, line_lst[i], re.IGNORECASE)
            else:
                result = re.match(pattern, line_lst[i])
            
            if invert:
                condition = result is None
            else:
                condition = result is not None

            if condition:
                found_instances_n += 1
                if not show_only_matching_lc: # Won't print lines if -c option is enabled
                    #printing if -B is enabled
                    if lines_before:
                        extraLineIndex = i - lines_before
                        if extraLineIndex < 0:
                            extraLineIndex = 0
                        for j in range(extraLineIndex, extraLineIndex + lines_before):
                            if(show_file_name):
                                print(file, end=":")
                            print(line_lst[j])
                    #Major Printing
                    if(show_file_name):
                        print(file, end=":")
                    if(show_line_count):
                        print(lc, end=":")
                    print(line_lst[i]) 

                    #printing if -A is enabled
                    if lines_after:
                        extraLineIndex = i + lines_after
                        if extraLineIndex > len(line_lst):
                            extraLineIndex = len(line_lst)
                        for j in range(extraLineIndex - lines_after, extraLineIndex):
                            if(show_file_name):
                                print(file, end=":")
                            print(line_lst[j])
                    if lines_after or lines_before:
                        print("---")
if (show_only_matching_lc): 

    print(found_instances_n)

import re
from pathlib import Path


def read_s1p(path):
    comments = get_comments(path)
    option = get_option(path)

    file = open(path)
    content = file.read()
    file.close()

    content = content.split('\n')


    #remove all empy lines
    content = list(filter(None, content))
    #remove all lines that doesnt start with number
    content = [line for line in content if line[0].isnumeric()]
    n_columns = len(re.findall(r'\S+',content[0])) #number of columns = number of spaces + newline
    print(n_columns)
    n_rows = len(content)

    data = [[0 for _ in range(n_rows)] for _ in range(n_columns)] 
    
    s1p_regex = r"-?\d+\.?\d+(?:e?[-+]?\d+)?" 
    #sorry for that, i will explain:
    #match all patterns that  have
    # a minus signal - (or not) and after
    # one or more digits and after
    #a dot . (or not) and after
    #one or more digits and after
    #an 'e' (or not) and after
    # a minus or plus signal -/+ (or not) and after
    # one or more digits 

    #this will match any of the this examples:
    # 1000000
    #1000.000
    # -100.0e+6

    for n_line in range(len(content)):
        values = re.findall(s1p_regex,content[n_line])
        print(values)
       # print(values[0])
        for n in range(n_columns):
            data[n][n_line] = float(values[n])
            


    return [option, comments, data]

def get_comments(path):
    
    file = open(path)
    content = file.read()
    file.close()

    content = content.split('\n')

    comments = [line[1:] for line in content if '!' in line]

    return comments


def get_option(path):
    file = open(path)
    content = file.read()
    file.close()

    if '#' in content:
        options = content[content.index('#') : content.index('\n', content.index('#'))]
    else:
        return []
    
    options = re.findall(r'[^#\s+]+' ,options) #find all non space and non # characters sequences
    return options


def write_s1p(path, option, comments, data):

    file = path.open(mode='w')

    
    for com in comments:
        file.write('!')
        file.write(com + '\n')
    
    file.write('# ')
    for opt in option:  
        file.write(opt + ' ')

    file.write('\n')
    
    
    for nrows in range(len(data[0])):
        for ncol in range(len(data)):

            file.write(str(data[ncol][nrows]))
            file.write('\t')

        file.write('\n')

    file.close()

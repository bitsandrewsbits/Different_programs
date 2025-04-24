#Y0UR_EnglishV0CABULARY - version 1_3
#A program can help you write and repeat your english word in this vocabulary

import functions as fns

#Main part of programm            
words_file = open('Y0UR_ENglish_W0RD5.txt', 'at')
words_file.close()

words_read = open('Y0UR_ENglish_W0RD5.txt', 'rt')

if len(words_read.readlines()) == 0:
    print('Y0UR vocabulary is empty! Let\'s filling it.')
    print(f'Welcome to Y0UR English V0vabulary {fns.version}!\nThis program can help you to repeating and styding new english words.')
    print('Before starting, read instraction - press i')
    words_read.close()
    
    fns.execute_vocabulary('Y0UR_ENglish_W0RD5.txt')
else:
    words_read.close()
    
    fns.execute_vocabulary('Y0UR_ENglish_W0RD5.txt')

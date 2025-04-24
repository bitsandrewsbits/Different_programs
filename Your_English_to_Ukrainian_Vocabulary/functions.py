#Functions for main programm

import datetime
import random
from re import match

version = '1_3'

def show_instruction():
    print('Commands in programm:\n' + '-' * len('Commands in programm:'))
    print('|1)press i - to instruction\n|2)press show - to read all words in your dictionary')
    print('|3)press w - to write words to vocabulary\n|4)press show some - to show you some word')
    print('|5)press d - to delete word from dictionary\n|6)press amount - to show amount of words in your vocabulary')
    print('|6)press test - to checking how you known english words from your vocabulary')
    print('|7)press lastdate - to show you last writted date in your vocabulary')

def check_word_in_vocabulary(vocab_file, writed_word):
    with open(vocab_file, 'rt') as r_file:
        for line in r_file:
            vocabulary_word = line.split(' ')[0]
            if writed_word == vocabulary_word:
                return True

    return False

def write_str_date(your_date):  #format - DayMonthYear(for instance, 10102021)
    return f'{your_date[:2]}-{your_date[2:4]}-{your_date[-4:]}'

def convert_str_to_date(str_date):
    day = int(str_date[:2])
    month = int(str_date[2:4])
    year = int(str_date[-4:])
        
    return datetime.datetime(year, month, day)

#function for store all dates in your vocabulary-file
def collect_all_vocabulary_dates(vocab_file):
    dates_list = []
    with open(vocab_file, 'rt') as r_f:
        for line in r_f:
            if 'DATE' in line:
                dates_list.append(line)

    return dates_list

#fuct thar return the last date in your vacabulary(if you forgot it)
def get_last_writed_date(vocabulary_file):
    last_writed_date = collect_all_vocabulary_dates(vocabulary_file)[-1].split(' ')[1][:-6]

    return last_writed_date

def adding_words_to_vocabulary(write_file):
    voc_write = open(write_file, 'at')
    today_date = datetime.datetime.now().strftime('%d%m%Y')

    #answer the question - want to set or not set some date for your vocabulary
    # if you answered Yes(press Y, y or yes) - you can set your date
    # if you answered No (press N, n or no) - setting currect date(today, when was program was executed)
    while True:
        set_user_date = input('Are you want set your date?[press y/n or nothing to set today date]: ')
        if set_user_date.lower() == 'y' or set_user_date.lower() == 'yes':
            user_date = input('Input your date[DayMonthYear]: ')
            if convert_str_to_date(user_date) > convert_str_to_date(today_date):
                print('!' * len('Your date is in the future! Try again.'))
                print('Your date is in the future! Try again.')
                print('!' * len('Your date is in the future! Try again.'))
            else:
                #set and write date
                u_date = convert_str_to_date(user_date).strftime('%d%m%Y')
                writed_date = write_str_date(u_date)
                w_date = f'=====DATE: {writed_date}=====\n'
                
                if w_date in collect_all_vocabulary_dates(write_file):
                    print('Your vocabulary has already this date!\n' + '*' * 30)
                    break
                else:
                    voc_write.write(w_date)
                    break
                
        #set current date - today date
        elif set_user_date == '' or set_user_date.lower() == 'n' or set_user_date.lower() == 'no':
            today_date = datetime.datetime.now().strftime('%d-%m-%Y')
            if get_last_writed_date(write_file) == today_date:
                print('=' * 30 + f'\nToday you have already added new words to vocabulary! Good!')
                print('You continuing to add new words...')
                print('=' * 30)
                break
            else:
                voc_write.write(f'=====DATE: {today_date}=====\n')
                break

    while True:
        user_word = input('Enter your ENGLISH word [or press e - to stop adding words]: ')
        
        if user_word == 'e':
            print('Main menu')
            break
        elif check_word_in_vocabulary(write_file, user_word) == False:
            word_translation = input(f'Enter translation of word "{user_word}": ')
            voc_write.write(f'{user_word} ---> {word_translation}\n')
        else:
            print('=' * len(f'English word\"{user_word}\" was added early!'))
            print(f'English word\"{user_word}\" was added early!')
            print('=' * len(f'English word\"{user_word}\" was added early!'))

    voc_write.close()

#this function read dict file and return new file without removed word
def remove_word_from_vocabulary(read_file, target_word):
    with open(read_file, 'rt') as r_file:
        for word_str in r_file:
            if target_word == word_str.split(' ')[0]:
                current_words_file = open(read_file, 'rt')
                #creating list only with english words
                tmp_list = current_words_file.readlines()
                
                current_words_file.close()
                
                res_new_file = open('Y0UR_ENglish_W0RD5.txt', 'wt')
                
                #now we overwritting vocabulary file
                for line in tmp_list:
                    if line.split('--->')[0][:-1] == target_word:
                        continue
                    res_new_file.write(line)
                    
                res_new_file.close()
                break
    return True

def show_all_dict_words(read_file):
    print('====Y0UR V0CABULARY====\n')

    with open(read_file, 'rt') as r_file:
        for word_str in r_file:
            print(word_str[:-1])
    print('\n')

def show_some_word(read_file, target_word):
    with open(read_file, 'rt') as r_file:
        for word_str in r_file:
            if word_str.split('--->')[0][:-1] == target_word:
                print(f'\nEnglish word: {target_word}')
                translation_word = word_str.split('--->')[1][1:-1]
                print(f'Translation: {translation_word}\n')

def amount_words_in_vocabulary(read_file):
    amount_words = 0
    with open(read_file, 'rt') as r_file:
        for line in r_file:
            if 'DATE' in line:
                continue
            amount_words += 1
            
    return amount_words

def start_testing_your_memory(your_vocab):
    #creating dictionary of words: {[words]: [translation]}
    words_dict = {}
    #creating list only with english words from your vocabulary
    words_list_for_choicing = [line.split(' ')[0] for line in open(your_vocab, 'rt').readlines() if 'DATE' not in line]
    
    with open(your_vocab, 'rt') as r_file:
        for line in r_file:
            if 'DATE' not in line:
                words_dict[line.split('--->')[0][:-1]] = line.split('--->')[1][1:-1]

    while True:
        word_number = random.randint(0, len(words_list_for_choicing) - 1)
        target_word = words_list_for_choicing[word_number]
        
        user_answer = input(f'Enter translation of word \"{target_word}\" [or press e - to exit from tested mode]: ')

        if user_answer == 'e':
            print('returning to Main menu...\nMain Menu')
            break

        for word in words_dict:
            if user_answer in words_dict[target_word]:
                print('GOOD! you are right!')
                break
            else:
                print(f'NO! right answer is - {words_dict[target_word]}')
                print('Try again.')
                break

#Amount words per month
def get_words_dict(word_file):
    res_dict = {}
    tmp_year = 0
    tmp_month = 0
    with open(word_file) as read_f:
        for line in read_f:
            if 'DATE' in line:
                date = match(r'.*(\S+)-(\S+)-(\S+)[=]{5}', line)
                if tmp_year != date.group(3) or tmp_month != date.group(2):
                    res_dict[(int(date.group(2)), int(date.group(3)))] = []
                    tmp_year = date.group(3)
                    tmp_month = date.group(2)
            else:
                res_dict[int(tmp_month), int(tmp_year)].append(line)
                
    return res_dict
            
def amount_and_words_per_month(words: dict, input_month: int, input_year: int):
    amount_words = 0
    for date in words:
        if date == (input_month, input_year):
            for line in words[date]:
                amount_words += 1
                print(line)
    print(f'{"=" * 30}\nAmount words by month {input_month} {input_year} year = {amount_words}')
#=====================================
    
def execute_vocabulary(dict_file):
    while True:
        user_action = input('Enter your command\n[press command or e - to exit]: ')

        if user_action == 'e':
            print('Bye. See you later)')
            break
        elif user_action == 'i':
            show_instruction()
        elif user_action == 'w':
            adding_words_to_vocabulary(dict_file)
        elif user_action == 'show':
            show_all_dict_words(dict_file)
        elif user_action == 'lastdate':
            print('=_' * 20)
            print(f'Last writted date in your vocabulary: {get_last_writed_date(dict_file)}')
            print('_=' * 20)
        elif user_action == 'd':
            while True:
                user_word = input('Enter word for deleting[or e - to exit from deleting]: ')
                if user_word == 'e':
                    print('Main menu:')
                    break
                else:
                    remove_word_from_vocabulary(dict_file, user_word)
        elif user_action == 'show some':
            while True:
                user_word = input('Enter what word you want find[or e - to exit from searshing]: ')
                if user_word == 'e':
                    print('Main menu:')
                    break
                else:
                    show_some_word(dict_file, user_word)
        elif user_action == 'amount':
            print(f'\nT0TAL amount words in your vocabulary = {amount_words_in_vocabulary(dict_file)}\n')
        elif user_action == 'month':
            user_month = int(input('Enter month: '))
            user_year = int(input('Enter year: '))
            amount_and_words_per_month(get_words_dict(dict_file), user_month, user_year)
        elif user_action == 'test':
            print('Okey. Now we checking your knowledges how you know english words!')
            print('Ready? Okey. Go!')
            start_testing_your_memory(dict_file)

if __name__ == '__main__':
    print('Test Mode')
    start_testing_your_memory('Y0UR_ENglish_W0RD5.txt')
    print(get_words_dict('test_words_file.txt'))
    amount_and_words_per_month(get_words_dict('test_words_file.txt'), 10, 2021)

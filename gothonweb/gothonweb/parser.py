#!/usr/bin/python


class ParserError(Exception):
    pass
    

class Sentence(object):

    def __init__(self, num, subject, verb, obj):
        # remember we take ('noun','princess') tuples and convert them
        self.number = num[1]
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = obj[1]

    def parsed_sentence(self):
        sentence = []
        if self.number != 'error':
            sentence.append(str(self.number))
        if self.subject != 'error':
            sentence.append(self.subject)
        if self.verb != 'error':
            sentence.append(self.verb)
        if self.object != 'error':
            sentence.append(self.object)

        # have to join these to make sentence and than check that
        final_sentence = ' '.join(sentence)
        return final_sentence


# Takes the tuple from list than value from that tuple and returns it
def peek(word_list):
    if word_list:
        word = word_list[0]
        return word[0]
    else:
        return None
        
def match(word_list, expecting):
    if word_list:
        word = word_list.pop(0)

        if word[0] == expecting:
            return word
        else:
            return None
    else:
        return None

# takes the scanned list and type to match
# iterating through the peek returned value.
# It's called first on >every fuction< and removes
# the stop words continuesly until it did'nt find that next word.
def skip(word_list, word_type):
    while peek(word_list) == word_type:
        match(word_list, word_type)
        

class Parser_core():

    def parse_verb(self, word_list):
        skip(word_list, 'stop')
        skip(word_list, 'error')

        if peek(word_list) == 'verb':
            return match(word_list, 'verb')
        else:
            raise ParserError("Expected a verb next.")
            

    def parse_object(self, word_list):
        skip(word_list, 'stop')
        skip(word_list, 'error')
        next_word = peek(word_list)

        if next_word == 'noun':
            return match(word_list, 'noun')
        elif next_word == 'direction':
            return match(word_list, 'direction')
        else:
            raise ParserError("Expected a noun or direction next.")


    def parse_subject(self, word_list):
        skip(word_list, 'stop')
        skip(word_list, 'error')
        next_word = peek(word_list)

        if next_word == 'noun':
            return match(word_list, 'noun')
        elif next_word == 'verb':
            return ('noun', 'player')
        else:
            raise ParserError("Expected a verb next.")

    def parse_number(self, nums):
        next_word = peek(nums)
        if next_word == 'number':
            return match(nums, 'number')

    def num_check(self, word_list):
        nums = []
        index_num = []
        for n in word_list:
            if n[0] == 'number':
                nums.append(n)
                index_num.append(word_list.index(n))

        for num in nums:
            word_list.remove(num)
        return nums

    def parse_sentence(self, word_list):

        num_list = self.num_check(word_list)
        if num_list:
            num = self.parse_number(num_list)
        else:
            num = ('error', 'error')
    
        try:
            subj = self.parse_subject(word_list)
        except ParserError:
            subj = ('error', 'error')

        try:
            verb = self.parse_verb(word_list)
        except ParserError:
            verb = ('error', 'error')

        try:
            obj = self.parse_object(word_list)
        except ParserError:
            obj = ('error', 'error')

        return Sentence(num, subj, verb, obj)

# testing
# ss = Parser_core()
# rv = ss.parse_sentence([('stop', 'really'),
#                         ('noun', 'code'), 
#                         ('number', 404),
#                         ('number', 200),
#                         ('stop', 'dude'), 
#                         ('verb', 'is'), 
#                         ('noun', 'awesome!')])
# print rv.subject
# print rv.verb
# print rv.object
# print rv.number
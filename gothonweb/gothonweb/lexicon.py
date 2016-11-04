lexicon = {
    'tell': 'noun',
    'a': 'verb',
    'joke': 'noun',
    'dodge': 'noun',
    'shoot': 'noun',
    '0132': 'number',
    '2': 'number',
    'slowly': 'noun',
    'place': 'verb',
    'the': 'stop',
    'bomb': 'noun',
    'throw': 'noun',
    'in': 'stop',
    'him': 'stop',
    'freaky': 'stop',
}


def scan(sentence):

    words = sentence.split()
    result = []

    for word in words:
        if word in lexicon:
            try:
               pair = (lexicon[word], word)
               result.append(pair)
    
            except ValueError:
                try:
                    pair = (lexicon[word.lower()], word.lower())
                    result.append(pair)
            
                except KeyError:
                    pair = (lexicon[word.upper()], word.upper())
                    result.append(pair)

        else:
            pair = ('error', str(word))
            result.append(pair)

    return result


# experiment on converting int to English numbers
num_in_eng = {
            1: 'One',
            2: 'Two',
            3: 'Three',
            4: 'Four',
            5: 'Five'
            }
            
def conversion(string_num):
    converted = num_in_eng[int(string_num)]

    return converted


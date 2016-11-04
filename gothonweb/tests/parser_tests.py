from nose.tools import *
from gothonweb import parser

def setup():
	global y
	y = parser.Parser_core()

def test_Sentence():
	x = parser.Sentence(('number', '3'), ('noun', 'we'), ('verb', 'are'), ('noun', 'DedSec'))

	assert_equal(x.subject, 'we')
	assert_equal(x.verb, 'are')
	assert_equal(x.object, 'DedSec')


def test_peek():
	assert_equal(parser.peek([('noun', 'DedSec'), 
								('verb', 'was'), 
								('noun', 'here')]), 'noun')

def test_match():
	# this is more readable i think
	result = parser.match([('noun', 'DedSec'), 
							('verb', 'was'), 
							('noun', 'here')], 'noun')
	assert_equal(result, ('noun', 'DedSec'))

def test_skip():
	assert_equal(parser.skip([('noun', 'DedSec'), 
								('stop', 'was'), 
								('noun', 'here')], 'stop'), None)

def test_parse_verb():

	# first checking LHS=RHS
	assert_equal(y.parse_verb([('verb', 'DedSec'),
								('stop', 'was'),
								('noun', 'here')]), ('verb', 'DedSec'))

	# second checking that exception get raised on passing wrong arguments
	assert_raises(parser.ParserError, y.parse_verb, [('noun', 'DedSec'),
														('stop', 'was'), 
														('noun', 'here')])

def test_parse_object():

	assert_equal(y.parse_object([('direction', 'north'),
										('stop', 'is'),
										('noun', 'san fransisco bay')]),
										 ('direction', 'north'))

	assert_raises(parser.ParserError, y.parse_object, [('stop', 'are'),
														('verb', 'these'),
														('noun', 'apples')])

def test_parse_subject():
	assert_equal(y.parse_subject([('noun', 'We'),
									('stop', 'are'),
									('noun', 'DedSec')]), ('noun', 'We'))
	testing_words = [('stop', 'me')]
	assert_raises(parser.ParserError, y.parse_subject, testing_words)

def test_parse_sentence():
	x = y.parse_sentence([('number', 01000),
							('noun', 'we'),
							('verb', 'are'),
							('noun', 'DedSec')])

	assert_equal(x.number, 01000)
	assert_equal(x.subject, 'we')
	assert_equal(x.verb, 'are')
	assert_equal(x.object, 'DedSec')

def test_num_check():
	object_ = parser.Parser_core()
	num_exist_check = object_.num_check([('number', 0132), ('verb', 'me')])
	assert_equal(num_exist_check, [('number', 0132)])

	parse_num = object_.parse_number(num_exist_check)
	assert_equal(parse_num, ('number', 0132))
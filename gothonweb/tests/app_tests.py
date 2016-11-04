from nose.tools import *
from bin.app import app
from tools import assert_response
from bin import model


def test_index():
    # check that we get a 404 on the /none URL
    # app is app.py's variable
    resp = app.request("/none")
    assert_response(resp, status="404")

    # test our first GET request to /
    resp = app.request("/")
    assert_response(resp)

    resp = app.request("/game")
    assert_response(resp)

    # can't test because of sessions
    # make sure default values work for the form
    # resp = app.request("/game", method="POST")
    # # contains not working with status 303, because of 303 the data is gone i think
    # assert_response(resp, contains=None, status="303")

    # #test that we get expected values
    # data = {'action': 'tell'}
    # resp = app.request("/game", method="POST", data=data)
    # assert_response(resp, contains=None, status="303")

def test_GameEngine_POST():
    final_sentence = ' '.join(['what', 'None', 'hell'])
    assert_equal(final_sentence, 'what None hell')

# model module tests
def test_db_exist():
    user_ex = model.user_exist("usa")
    assert_equal(user_ex, True)

    user_ex = model.user_exist("shami")
    assert_equal(user_ex, False)

def test_signin():
    signin = model.signin("shami", "saif")
    assert_equal(signin, "shami")

    signin = model.signin("sama", "saif")
    assert_equal(signin, None)

# it will insert data in my original database, have to workout how to create a
# temporary database for testing
# def test_insert_score():
#     # score = model.scores()
#     in_sc = model.insert_score(55, 'hello')
#     assert_equal(in_sc, 14)

    
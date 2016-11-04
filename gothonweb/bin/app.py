import web
import model
from web import form
from gothonweb import map
from gothonweb import lexicon, parser

urls = (
    '/game', 'GameEngine',
    '/', 'Index',
    '/account', 'Account',
    '/signin', 'Signin',
    '/signout', 'Signout',
    '/imgupload', 'ImgUpload'
)

app = web.application(urls, globals())

# little hack so that the debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store, initializer={'room': None, 'username': None, 'guess': 10})
    web.config._session = session

else:
    session = web.config._session

render = web.template.render('templates/', base="layout")

class Index(object):


    form = form.Form(
        form.Textbox("Name", 
            form.notnull,
            class_="form-control", 
            description=None,
            placeholder="Your Name",
            ),
        form.Password("pass1", 
            class_="form-control", 
            description=None,
            placeholder="Password"),
        form.Password("pass2", 
            class_="form-control", 
            description=None,
            placeholder="Password Again"),
        validators = [form.Validator("Password did'nt match", lambda i: i.pass1 == i.pass2),
                        form.Validator("User name already exist! Try something else.", lambda x: model.user_exist(x.Name))]
        )

    

    def GET(self):
        register = self.form()
        players_data = model.scores()
        return render.login(register, notify=None, players_data=players_data)

    # for submission of signup form only
    def POST(self):
        register = self.form()
        if not register.validates():
            players_data = model.scores()
            return render.login(register, notify=None, players_data=players_data)

        # incomming = web.input('Name', 'pass1')
        
        # this is used to "setup" the session with starting values
        session.room = map.START
        session.username = register.d.Name
        model.signup(register.d.Name, register.d.pass1)
        raise web.seeother("/game")


# for submission of signin form
# signin check if user is registered
class Signin(object):
    def POST(self):
        register = Index.form()

        incomming = web.input('signin_name', 'signin_pass')
        
        user_login_check = model.signin(incomming.signin_name, incomming.signin_pass)
        if user_login_check:

            session.room = map.START
            session.username = incomming.signin_name
            raise web.seeother("/game")
        else:
            players_data = model.scores()
            return render.login(register, notify='User name or Password not correct!', players_data=players_data)



class GameEngine(object):
    def GET(self):
        if session.room and session.username:
            regd_users = model.users()
            player_score = model.show_score(session.username)
            id_ = model.user_id(session.username)
            piclink = model.piclink(id_)
            return render.show_room(room=session.room, user=session.username, score=player_score, piclink=piclink, guesses=session.guess)
        else:
            # why is there here? do you need it?
            # yes if someone tries to directly go to the /game url without setting the session
            # or session.room is None
            return render.you_died(death=map.death())
            # raise web.seeother('/')

    def POST(self):
        form = web.input(action='shoot!')

        # submit to lexicon for analyze it
        word_list = lexicon.scan(form.action)
        # making object for class in parser module
        parser_object = parser.Parser_core()
        # submit the lexicon data to parser
        parsed_sentence = parser_object.parse_sentence(word_list)
        final_sentence = parsed_sentence.parsed_sentence()
        
        
        # there is a bug here, can you fix it?
        # if form.action is not in the dict then it returns None
        # when it comes to the last room it wont direct to died on submitting anything
        if session.room and session.room.name != "The End" and form.action and session.room.name == 'Laser Weapon Armory' and session.guess <= 10 and form.action != '0132':
            session.guess -= 1
            if session.guess <= 0:
                session.room = session.room.go(final_sentence)

        elif session.room and session.room.name != "The End" and form.action:
            # have to change the room.go parameter
            session.room = session.room.go(final_sentence)
            score = 20
            model.insert_score(score, session.username)
            score += 30
            session.guess = 10
        elif session.room.name == "The End":
            session.room = map.START

        raise web.seeother("/game")


class Account(object):
    def GET(self):
        id_ = model.user_id(session.username)
        piclink = model.piclink(id_)
        return render.account(name=session.username, piclink=piclink)

    def POST(self):
        id_ = model.user_id(session.username)
        model.del_account(id_)
        session.kill()
        raise web.seeother("/")

class Signout(object):
    def POST(self):
        session.kill()
        raise web.seeother("/")

class ImgUpload(object):
    def POST(self):
        id_ = model.user_id(session.username)
        x = web.input(photo={})
        filedir = 'static/profilepic'
        if 'photo' in x:
            # replace the backslash file system path to / filesystem
            filepath = x.photo.filename.replace('\\','/')
            # just select filename from the full path of file
            filename = filepath.split('/')[-1]
            ext = filename.split('.')[-1]
            # creates the file where the uploaded file should be stored
            fout = open(filedir +'/'+ str(id_) + '.' + ext,'wb')
            # writes the uploaded file to the newly created file
            fout.write(x.photo.file.read())
            path = filedir + '/' + str(id_) + '.' + ext
            model.updatepic(path, id_)
            fout.close()
        raise web.seeother("/account")


if __name__ == "__main__":
    app.run()
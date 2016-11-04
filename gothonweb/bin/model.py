import web

db = web.database(dbn='sqlite', db='users.db')

def users():
    return db.select('users', order='id')

def signup(name, password):
    db.insert('users', name=name, _pass=password, gothonweb=0)

def del_account(id):
    db.delete('users', where="id=$id", vars=locals())

# checks if the user exist in db
def user_exist(name):
    user_check = users()
    for user in user_check:
        if user.name == name:
            return False
            break
    else:
        return True

def user_id(name):
    user = users()
    for user_data in user:
        if user_data.name == name:
            return user_data.id

def signin(name, _pass):
    user = users()
    name_exist = None
    pass_exist = None
    for user_name in user:
        if user_name.name == name:
            name_exist = user_name.name
            if user_name._pass == _pass:
                pass_exist = True
    if name_exist and pass_exist:
        return name_exist
    else:
        return None

def scores():
    return db.select('users', order="gothonweb DESC", limit=10)

def show_score(name):
    user = users()
    for user_data in user:
        if user_data.name == name:
            return user_data.gothonweb

def insert_score(score, name):
    user = users()
    for user_data in user:
        if user_data.name == name:
            _id = user_data.id
            score += int(user_data.gothonweb)
            db.update('users', where="id=%d"%_id, gothonweb=score)

def piclink(id):
    user = users()
    for user_data in user:
        if user_data.id == id:
            return user_data.piclink

def updatepic(link, id):
    db.update('users', where="id=%d"%id, piclink=link)
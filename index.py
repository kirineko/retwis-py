import bottle
import settings
import session
import time
from convert import to_dict, to_list, to_set, to_string
from model import User, Post, Timeline

r = settings.r


def islogin():
    sess = session.Session(bottle.request, bottle.response)

    if sess.is_new():
        return False
    else:
        return User(sess['id'])

@bottle.get('/')
@bottle.view('index')
def index():
    user = islogin()
    if user:
        res = {
            'username': user.username,
            'posts': user.posts(),
            'followers': user.followers(),
            'following': user.following(),
            'followers_num': user.followers_num(),
            'following_num': user.following_num()
        }
        return res
    else:
        bottle.redirect('/signup')

@bottle.get('/timeline')
@bottle.view('timeline')
def timeline():
    user = islogin()
    if user:
        res = {
            'username': user.username,
            'posts': Timeline.posts(),
            'users': User.users()
        }
        return res

    bottle.redirect('/')

@bottle.get('/<username>')
@bottle.view('profile')
def profile(username):
    login_user = islogin()
    user = User.find_by_username(username)
    if user and login_user:
        res = {
            'username': user.username,
            'loginname': login_user.username,
            'followers': user.followers(),
            'following': user.following(),
            'followers_num': user.followers_num(),
            'following_num': user.following_num(),
            'posts': user.posts(),
            'isfollowing': login_user.isfollowing(user)
        }
        return res
    
    bottle.redirect('/')

@bottle.get('/<loginname>/follow/<username>')
def follow(loginname, username):
    login_user = User.find_by_username(loginname)
    user = User.find_by_username(username)
    if login_user and user:
        login_user.add_following(user)
        bottle.redirect('/{}'.format(user.username))
    bottle.redirect('/')

@bottle.get('/<loginname>/unfollow/<username>')
def unfollow(loginname, username):
    login_user = User.find_by_username(loginname)
    user = User.find_by_username(username)
    if login_user and user:
        login_user.remove_following(user)
        bottle.redirect('/{}'.format(user.username))
    bottle.redirect('/')

@bottle.get('/mentions/<username>')
@bottle.view('mentions')
def mentions(username):
    login_user = islogin()
    user = User.find_by_username(username)
    if login_user and user:
        res = {
            'username': user.username,
            'loginname': login_user.username,
            'isfollowing': login_user.isfollowing(user),
            'posts': user.mentions()
        }
        return res
    
    bottle.redirect('/')


@bottle.get('/signup')
@bottle.view('signup')
def signup():
    return dict()


@bottle.post('/signup')
@bottle.view('signup')
def signup():
    username = bottle.request.POST['username']
    password = bottle.request.POST['password']

    user = User.create(username, password)
    if user:
        sess = session.Session(bottle.request, bottle.response)
        sess['id'] = user.id
        sess.save()

        bottle.redirect('/')
    
    return dict()

@bottle.post('/login')
@bottle.view('signup')
def login():
    username = bottle.request.POST['username']
    password = bottle.request.POST['password']

    user = User.find_by_username(username)
    if user:
        if user.password == password:
            sess = session.Session(bottle.request, bottle.response)
            sess['id'] = user.id
            sess.save()

            bottle.redirect('/')
    
    return dict()

@bottle.get('/logout')
def logout():
    sess = session.Session(bottle.request, bottle.response)
    sess.invalided()
    bottle.redirect('/')


@bottle.post('/post')
def post():
    user = islogin()
    if user:
        content = bottle.request.POST['content']
        Post.create(user, content)
        bottle.redirect('/')
    else:
        bottle.redirect('/signup')

@bottle.get('/public/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='public/')

bottle.run(reloader=True)



import bottle
import settings
import session

r = settings.r


def islogin():
    sess = session.Session(bottle.request, bottle.response)

    if sess.is_new():
        return False
    else:
        print(sess['id'])
        return True

@bottle.get('/')
@bottle.view('index')
def index():
    if islogin():
        return dict()
    else:
        bottle.redirect('/signup')

@bottle.get('/signup')
@bottle.view('signup')
def signup():
    return dict()


@bottle.post('/signup')
@bottle.view('signup')
def signup():
    username = bottle.request.POST['username']
    password = bottle.request.POST['password']

    uid = r.hget('users', username)
    if not uid:
        uid = r.incr('user:uid')
        udata = {
            'username': username,
            'password': password
        }
        r.hmset('user:{}'.format(uid), udata)
        r.hset('users', username, uid)

        sess = session.Session(bottle.request, bottle.response)
        sess['id'] = uid
        sess.save()

        bottle.redirect('/')
    
    return dict()

bottle.run(reloader=True)



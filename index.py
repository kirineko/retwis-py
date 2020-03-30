import bottle
import settings
import session
import time
from convert import to_dict, to_list, to_set, to_string

r = settings.r


def islogin():
    sess = session.Session(bottle.request, bottle.response)

    if sess.is_new():
        return False
    else:
        return sess['id']

@bottle.get('/')
@bottle.view('index')
def index():
    uid = islogin()
    if uid:
        username = to_string(r.hget('user:{}'.format(uid), 'username'))
        posts_id = to_list(r.lrange('user:{}:timeline'.format(uid), 0, 9))
        
        posts = {}
        for pid in posts_id:
            post = to_dict(r.hgetall('post:{}'.format(pid)))
            post['username'] = to_string(r.hget('user:{}'.format(post['userid']), 'username'))
            posts[pid] = post

        followers = to_list(r.smembers('user:{}:followers'.format(uid)))
        followers = [to_string(r.hget('user:{}'.format(uid), 'username')) for uid in followers]
        followers_num = r.scard('user:{}:followers'.format(uid))

        following = to_list(r.smembers('user:{}:following'.format(uid)))
        following = [to_string(r.hget('user:{}'.format(uid), 'username')) for uid in following]
        following_num = r.scard('user:{}:following'.format(uid))

        res = {
            'username': username,
            'posts': posts,
            'followers': followers,
            'following': following,
            'followers_num': followers_num,
            'following_num': following_num
        }
        return res
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

@bottle.post('/login')
@bottle.view('signup')
def login():
    username = bottle.request.POST['username']
    password = bottle.request.POST['password']

    uid = r.hget('users', username).decode('utf-8')
    if uid:
        upassword = r.hget('user:{}'.format(uid), 'password').decode('utf-8')

        if upassword == password:
            sess = session.Session(bottle.request, bottle.response)
            sess['id'] = uid
            sess.save()

            bottle.redirect('/')
    
    return dict()


@bottle.post('/post')
def post():
    uid = islogin()
    if uid:
        content = bottle.request.POST['content']
        pid = r.incr('post:uid')
        pdata = {
            'userid': uid,
            'content': content,
            'posttime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        r.hmset('post:{}'.format(pid), pdata)

        r.lpush('user:{}:timeline'.format(uid), pid)
        r.lpush('user:{}:posts'.format(uid), pid)
        r.lpush('timeline', pid)
        r.sadd('posts:id', pid)
        bottle.redirect('/')
    else:
        bottle.redirect('/signup')

@bottle.get('/public/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='public/')

bottle.run(reloader=True)



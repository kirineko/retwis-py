from __future__ import annotations
from typing import Optional
import settings
from convert import to_dict, to_list, to_set, to_string
import time

r = settings.r

class User:
    def __init__(self, id : int):
        self.id = int(id)
        udata = to_dict(r.hgetall('user:{}'.format(self.id)))
        self.username = udata['username']
        self.password = udata['password']

    @staticmethod
    def find_by_id(id: int) -> Optional[User]:
        if r.exists('user:{}'.format(int(id))):
            return User(int(id))
        return None

    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        uid = r.hget('users', username)
        if uid:
            return User(int(uid))
        return None

    @staticmethod
    def create(username: str, password: str) -> Optional[User]:
        uid = r.hget('users', username)
        if not uid:
            uid = r.incr('user:uid')
            udata = {
                'username': username,
                'password': password
            }
            r.hmset('user:{}'.format(uid), udata)
            r.hset('users', username, uid)
            return User(int(uid))
        return None

    def posts(self) -> List[Post]:
        posts_id = to_list(r.lrange('user:{}:timeline'.format(self.id), 0, 9))
        return [Post(pid) for pid in posts_id]
        
    def followers(self) -> List[User]:
        followers = to_list(r.smembers('user:{}:followers'.format(self.id)))
        return [User(uid) for uid in followers]

    def following(self) -> List[User]:
        following = to_list(r.smembers('user:{}:following'.format(self.id)))
        return [User(uid) for uid in following]

    def followers_num(self) -> int:
        return r.scard('user:{}:followers'.format(self.id))

    def following_num(self) -> int:
        return r.scard('user:{}:following'.format(self.id))

class Post:
    def __init__(self, id: int):
        self.id = id
        pdata = to_dict(r.hgetall('post:{}'.format(self.id)))
        self.userid = pdata['userid']
        self.content = pdata['content']
        self.posttime = pdata['posttime']

    @staticmethod
    def find_by_id(id: int) -> Optional[Post]:
        if r.sismember('posts:id', int(id)):
            return Post(int(id))
        return None

    @staticmethod
    def create(user: User, content: str) -> Post:
        pid = r.incr('post:uid')
        pdata = {
            'userid': user.id,
            'content': content,
            'posttime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        r.hmset('post:{}'.format(pid), pdata)

        r.lpush('user:{}:timeline'.format(user.id), pid)
        r.lpush('user:{}:posts'.format(user.id), pid)
        r.lpush('timeline', pid)
        r.sadd('posts:id', pid)
        return Post(int(pid))

    @property
    def username(self):
        return to_string(r.hget('user:{}'.format(self.userid), 'username'))

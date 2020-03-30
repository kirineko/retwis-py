<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retiws</title>
    <link rel="stylesheet" href="/public/css/screen.css">
    <link rel="stylesheet" href="/public/css/custom.css">
</head>
<body>
    <div class="container">
        <div id="header" class="span-24">
            <div class="span-12">
                <br>
                <h1>Retiws</h1>
            </div>

            <div class="span-12 last right-align">
                <br>
                <br>
                <a href="/">home</a> |
                <a href="/mentions/{{username}}">mentions</a> |
                <a href="/{{username}}">{{username}}</a> |
                <a href="/timeline">timeline</a> |
                <a href="/logout">logout</a>
            </div>

            <hr>
        </div>

        <div class="span-24">
            <div class="span-16">
                <div id="updateform" class="box">
                    <form action="/post" method="post">
                        {{username}}, what's on your mind?
                        <textarea name="content" id="" cols="70" rows="3"></textarea>
                        <br>
                        <input type="submit" value="Update">
                    </form>
                </div>

                <div id="posts" class="span-15">
                    % for id, post in posts.items():
                    <div class="post">
                        <strong>{{ post['username'] }}</strong>
                        {{ post['content'] }}
                        <div class="date">{{ post['posttime'] }}</div>
                    </div>
                    % end
                </div>
            </div>

            <div class="span-7 last">
                <div class="box">
                    <h4>Followers: {{ followers_num }}</h4>
                    <ul class="user-list">
                        % for user in followers:
                        <li>{{ user }}</li>
                        % end
                    </ul>
                </div>

                <div class="box">
                    <h4>Following: {{ following_num }}</h4>
                    <ul class="user-list">
                        % for user in following:
                        <li>{{ user }}</li>
                        % end
                    </ul>
                </div>
            </div>
        </div>

        <div class="span-24 last right-align">
            <hr>
            This site is a twitter clone written by Python and Redis. copyright @kirineko.
        </div>
    </div>
</body>
</html>
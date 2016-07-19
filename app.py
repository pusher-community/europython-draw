import os
import random
from flask import Flask, request, jsonify, abort

from pusher import Pusher

pusher = Pusher(
    app_id='226984',
    key='87d7bf07035146dd4fa7',
    secret=os.environ['PUSHER_SECRET'],
    cluster='eu',
    ssl=True
)

app = Flask(__name__)

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/pusher/auth", methods=['POST'])
def auth():
    auth = pusher.authenticate(
        channel=request.form.get(u'channel_name'),
        socket_id=request.form.get(u'socket_id'),

        custom_data={
            u'user_id': request.form.get(u'socket_id'),
            u'user_info': {}
        }
    )
    return jsonify(auth)

@app.route("/slide")
def slide():
    return app.send_static_file('slide.html')


@app.route("/broadcast", methods=['POST'])
def broadcast():
    secret_token = request.form.get(u'SECRET_TOKEN') or None;
    event = request.form.get(u'EVENT') or None;

    if secret_token == None or event == None or secret_token != os.environ['PASSWORD']:
        return abort(403)

    chatroom_users = pusher.users_info(u'presence-demo')[u'users']
    user_ids = [user[u'id'] for user in chatroom_users]
    winner = random.choice(user_ids)

    pusher.trigger(u'presence-demo', event, { u'id': winner })

    print event, { u'id': winner }

    return "ok"

if __name__ == "__main__":
    app.run()

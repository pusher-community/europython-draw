import os
from flask import Flask, request, jsonify
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


if __name__ == "__main__":
    app.run()

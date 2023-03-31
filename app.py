from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class Channel:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.threads = []

    def add_thread(self, thread):
        self.threads.append(thread)

class Thread:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

class Message:
    def __init__(self, content, author):
        self.content = content
        self.author = author

channels = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/channels', methods=['POST'])
def create_channel():
    data = request.get_json()
    channel = Channel(data['name'], data['description'])
    channels[channel.name] = channel
    return jsonify(channel_name=channel.name, description=channel.description)

@app.route('/channels/<channel_name>/threads', methods=['POST'])
def create_thread(channel_name):
    channel = channels[channel_name]
    data = request.get_json()
    thread = Thread(data['title'], data['author'])
    channel.add_thread(thread)
    return jsonify(title=thread.title, author=thread.author)

@app.route('/channels/<channel_name>/threads/<thread_title>/messages', methods=['POST'])
def create_message(channel_name, thread_title):
    channel = channels[channel_name]
    thread = next(t for t in channel.threads if t.title == thread_title)
    data = request.get_json()
    message = Message(data['content'], data['author'])
    thread.add_message(message)
    return jsonify(content=message.content, author=message.author)

def main():
    app.run()

if __name__ == '__main__':
    main()

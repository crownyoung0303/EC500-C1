import hw2
import os
import flask


app = flask.Flask(__name__)
@app.route('/')
def form():
	return flask.render_template('form.html')


@app.route('/submitted', methods=['POST'])
def hw2_form():
    name = flask.request.form['name']
    hw2.get_all_tweets(name)
    hw2.writefile(name)
    return flask.render_template('hw2_form.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
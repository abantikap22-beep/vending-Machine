import webbrowser
from threading import Timer
from flask import Flask, render_template, request, session, redirect, url_for
from dfa_logic import process_note

app = Flask(__name__)
app.secret_key = "dfa-vending-secret-key"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/menu', methods=['GET'])
def menu():
    current_total = session.get('current_total', 0)
    current_item = session.get('current_item', '')
    current_state = session.get('current_state', 'q0')

    return render_template(
        'menu.html',
        current_total=current_total,
        current_item=current_item,
        current_state=current_state
    )


@app.route('/insert', methods=['POST'])
def insert():
    item = request.form['item']
    note_input = request.form['note']

    try:
        note = int(note_input)
    except ValueError:
        result = {
            "status": "REJECTED",
            "dfa_state": "q_reject",
            "message": "Please enter one valid note like 2, 5, 10, 20, 50, or 100."
        }
        return render_template('result.html', result=result)

    current_total = session.get('current_total', 0)

    current_item = session.get('current_item')
    if current_item and current_item != item and current_total > 0:
        current_total = 0

    result = process_note(item, current_total, note)

    if result["status"] == "WAITING":
        session['current_item'] = item
        session['current_total'] = result['total']
        session['current_state'] = result['dfa_state']
        return render_template(
            'menu.html',
            current_total=result['total'],
            current_item=item,
            current_state=result['dfa_state'],
            result=result
        )

    session.clear()
    return render_template('result.html', result=result)


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('menu'))


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)
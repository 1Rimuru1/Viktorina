from random import randint, shuffle
from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts import *
import os

quiz = 1
last_question = 0
counter = 0


def index():
    global counter
    session['counter'] = 0
    session['quiz'] = 1
    session['last_question'] = 0
    session['total'] = 0
    session['answers'] = 0
    return '<a href="/test">Викторины</a>'
#    redirect(url_for('test'))



def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    print(answer)
    if check_answer(quest_id, answer):
        session['answers'] += 1



def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template('test.html',
            question = question[1], quest_id = question[0],
            answers_list = answers_list)

def test():
    if not ('quiz' in session) or int (session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_question_after(
                session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

def anectod():
    return "<h1> anectod = — Дети, сегодня у нас в классе новый ученик! Ну что же вы растерялись? Бейте его!!! </h1>"

def buttons():
    return "<a href='/anectod'>  смешной анктод </a>"

def result():
    redirect(url_for('result'))
    return render_template('result.html', total = session['total'], answers = session['answers'])

app = Flask(__name__, template_folder=os.getcwd())
app.config['SECRET_KEY'] = "VeryStrongKey"
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test', 'test', test,
                methods=['POST', 'GET'])
app.add_url_rule('/result', 'result', result)
app.add_url_rule('/anectod', 'anectod', anectod)
app.add_url_rule('/buttons', 'buttons', buttons)
app.add_url_rule('/', 'index', index,
                methods=['POST', 'GET'])
app.run(debug = True)

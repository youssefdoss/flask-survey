from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def show_home_page():
    '''Brings the user to the home page with a start button'''

    return render_template(
        'survey_start.html',
        title=survey.title,
        instructions=survey.instructions)


@app.post('/begin')
def start_survey():
    '''Redirects user to first survey question page'''

    return redirect('/questions/0')


@app.get('/questions/<question_number>')
def show_first_question(question_number):
    '''Brings the user to the first survey question page'''
    question_number = len(responses)

    return render_template(
        'question.html',
        prompt=survey.questions[question_number].prompt,
        choices=survey.questions[question_number].choices)


@app.post('/answer')
def handle_answer():
    '''Adds answer to responses list and redirects to next question,
    or sends the user to the thank you page'''

    responses.append(request.form['answer'])

    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')

    else:
        return redirect('/thank_you')


@app.get('/thank_you')
def show_completed_page():
    '''Displays the completion page with questions and answers'''
    questions = survey.questions

    return render_template(
        'completion.html',
        questions=questions,
        responses=responses)

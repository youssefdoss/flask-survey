from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def show_home_page():
    '''Brings the user to the home page with a start button'''

    return render_template(
        # You can just inject the entire survey and specify properties in the HTML
        'survey_start.html',
        title=survey.title,
        instructions=survey.instructions)


@app.post('/begin')
def start_survey():
    '''Redirects user to first survey question page'''
    session['responses'] = []

    return redirect('/questions/0')


@app.get('/questions/<question_number>')
def show_first_question(question_number):
    '''Brings the user to the first survey question page'''
    correct_question_number = len(session['responses'])

    if correct_question_number == len(survey.questions):

        flash("Hey dummy that question is invalid")
        return redirect('/thank_you')
    elif correct_question_number == int(question_number):
        
        return render_template(
            'question.html',
            prompt=survey.questions[correct_question_number].prompt,
            choices=survey.questions[correct_question_number].choices)
    else:
        flash("Why can't you just follow instructions you absolute monster")
        return redirect(f'/questions/{correct_question_number}')


@app.post('/answer')
def handle_answer():
    '''Adds answer to responses list and redirects to next question,
    or sends the user to the thank you page'''

    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses

    if len(session['responses']) < len(survey.questions):
        return redirect(f'/questions/{len(session["responses"])}')

    else:
        return redirect('/thank_you')


@app.get('/thank_you')
def show_completed_page():
    '''Displays the completion page with questions and answers'''
    questions = survey.questions

    return render_template(
        'completion.html',
        questions=questions,
        # You can get session and cookie values directly in the Jinja template
        responses=session['responses'])

from flask import render_template, url_for, request
from app import webapp
import json



def load_question_as_obj():
    with open('app/questions/questions.json') as f:
        data = json.load(f)
    return data


#################################################################

@webapp.route('/',methods=['GET','POST'])
def show_questionnaire():
    questionnaire = load_question_as_obj()
    if request.method == 'GET':
        return render_template('form.html', questionnaire=questionnaire)
    else:
        submissions = dict()
        form = request.form
        for name, values in form.lists():
            if name == 'submit' or name.endswith('.other'):
                continue
            valid = name.startswith('q')
            if valid:
                try:
                    n = int(name[1:None])
                except ValueError:
                    valid = False
            if not valid:
                return "invalid submission parameters", 400
            submissions[n] = filter(any,
                ((s.strip(), form.get('%s.%s.other' % (name, s.strip())))
                 for s in values))

        error = False
        errormsgs = questionnaire['messages']['error']

        for i, q in enumerate(questionnaire['questions']):
            s = submissions.get(i, [])
            required = q.get('required')
            other_opt = q.get('other_option')
            values = list(v[0] for v in s)
            # empty required field error
            empty_required = bool(required) and not any(values)
            # empty "other" field error
            empty_other = (bool(other_opt) and
                           any(True for v, o in s if v == other_opt and not o))
            if empty_required or empty_other:
                q['error'] = errormsgs['required']
            if values:
                q['value'] = values[0]
                q['values'] = values
            if other_opt:
                other_vals = filter(None, (o for v, o in s if v == other_opt))
                if other_vals:
                    q['other_value'] = other_vals[0]
            # validate option values
            invalid = (bool(values) and 'options' in q and
                       any(True for v in values if v not in q['options']))
            if invalid:
                q['error'] = errormsgs['invalid']
            error = error or empty_required or empty_required or invalid
        if error:
            return render_template("form.html", questionnaire=questionnaire)
        else:
            return str(form)


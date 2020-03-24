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
            question_list_dict = get_questions()
            course_list_dict = get_courses()
            # print(len(question_list_dict))
            # print(len(course_list_dict))
            answer = form.to_dict(flat=False)
            print("User Submitted Answer")
            print(answer)
            del answer["submit"]
            answer_tags = set()
            question_counter = 0
            for i in answer:
                current_question_select_tag_dict = question_list_dict[question_counter]["tags"]
                selected_options = answer[i]
                for each_option in selected_options:
                    if each_option in current_question_select_tag_dict:
                        answer_tags = answer_tags|set(current_question_select_tag_dict[each_option])
                question_counter+=1

            print("User Selected Tags:")
            print(answer_tags)


            #get all the tags that the user selected, now search for which courses has the tags
            for course in course_list_dict:
                if course["course_type"] == "EB" or course["course_type"] == "ET":
                    num_tags = len(course["tags"])
                    selected_num_tags = 0
                    for each_tag in course["tags"]:
                        if each_tag in answer_tags:
                            selected_num_tags +=1
                    course["course_score"] = round(selected_num_tags*1.0/num_tags,2)
                elif course["course_type"] == "EC":
                    num_tags = len(course["tags"])
                    selected_num_tags = 0
                    for each_tag in course["tags"]:
                        if each_tag in answer_tags:
                            selected_num_tags +=1
                    course["course_score"] = round(1-selected_num_tags*1.0/num_tags,2)
                else:
                    pass

            print("Calculated Course Score:")
            for course in course_list_dict:
                print(course)
            MC = []
            EC = []
            EB = []
            ET = []
            #sort the course to different list
            for course in course_list_dict:
                if course["course_type"] == "MC":
                    MC.append(course)
                elif course["course_type"] == "EC":
                    EC.append(course)
                elif course["course_type"] == "EB":
                    EB.append(course)
                elif course["course_type"] == "ET":
                    ET.append(course)
                else:
                    print("Not in list")

            MC = sorted(MC, reverse=True, key=lambda course_obj: course_obj["course_score"])
            EC = sorted(EC, reverse=True, key=lambda course_obj: course_obj["course_score"])
            EB = sorted(EB, reverse=True, key=lambda course_obj: course_obj["course_score"])
            ET = sorted(ET, reverse=True, key=lambda course_obj: course_obj["course_score"])

            Selected_Tags = str(answer_tags)

            #"Submitted Answers=\n" + str(form) + "\nUser Selected Tags\n" + str(answer_tags) + "\nCalculated Course Scores:\n" +str(ranked_course)
            return render_template("result.html", Selected_Tags = Selected_Tags ,MC = MC, EC = EC, EB = EB, ET = ET)
def get_questions():
    with open('app/questions/questions.json') as f:
        data = json.load(f)
    # print(data)
    return data["questions"]

def get_courses():
    with open('app/questions/courses.json') as f:
        data = json.load(f)
    # print(data)
    return data["courses"]

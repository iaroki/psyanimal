import json
from bottle import route, run, template, request, error

with open('questions.json', 'r') as jsonfile:
    questions_dict = json.load(jsonfile)

@route('/')
def ddt():
    return template('''
        <!DOCTYPE html>
        <html><head><meta charset="utf-8"><title>Тест "Несуществующее животное"</title></head>
        <body bgcolor="#558000">
        <h1>Тест Несуществующее животное</h1><br>
        <h4>
        <form action="/" method=post>
            Имя: <input name="name" type="text" />
            Описание: <input name="desc" type="text" /><br><br>
            % for key in sorted(questions_dict.keys()):
                <input type="checkbox" name="question" value="{{key}}"> {{questions_dict[key][0]}}<br>
            % end
            <br>
            <input value="Проверить" type="submit" />
        </h3>
        </form></body></html>
    ''', questions_dict=questions_dict)

@route('/', method='POST')
def ddt_result():
    name = request.forms.get('name')
    desc = request.forms.get('desc')
    data = request.forms.getall('question')
    return template('''
        <!DOCTYPE html>
        <html><head><meta charset="utf-8"><title>Тест "Несуществующее животное"</title></head>
        <body bgcolor="#558000">
        <h3>Имя: {{name}}<br>
        Описание: {{desc}}<br></h3>
        <ul>
        % for key in data:
            <li><b>{{questions_dict[key][0]}}</b><br>
            {{questions_dict[key][1]}}</li>
        %end
        </ul>
        <br>
        <form action="http://127.0.0.1:9999">
            <input type="submit" value="Назад" />
        </form>
        </body></html>
        ''', name=name.encode('iso-8859-1'), desc=desc.encode('iso-8859-1'), data=data, questions_dict=questions_dict)

@error(404)
def error404(error):
    return 'Nothing here, sorry'

run(host='localhost', port=9999, reloader=True, debug=False)
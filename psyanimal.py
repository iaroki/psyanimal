import sys
import json
import codecs
from threading import Thread
from bottle import route, run, template, request, error, static_file
from cefpython3 import cefpython as cef

with codecs.open('questions.json', 'r', encoding='utf-8') as jsonfile:
    questions_dict = json.load(jsonfile)

@route('/<filename:re:.*\.(css|ico)>')
def send_static(filename):
    return static_file(filename, root='./')

@route('/')
def ddt():
    return template('''
        <!DOCTYPE html>
        <html><head><meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>Тест "Несуществующее животное"</title></head>
        <h1>Тест Несуществующее животное</h1><br>
        <form action="/" method=post>
            <h3>
            Имя: <input name="name" type="text" />
            Описание: <input name="desc" type="text" /><br><br>
            </h3>
            <h4>
            % for key in sorted(questions_dict.keys()):
                <input type="checkbox" name="question" value="{{key}}"> {{questions_dict[key][0]}}<br>
            % end
            </h4>
            <br>
            <input value="Проверить" type="submit" />
        </form></body></html>
    ''', questions_dict=questions_dict)

@route('/', method='POST')
def ddt_result():
    name = request.forms.get('name')
    desc = request.forms.get('desc')
    data = request.forms.getall('question')
    return template('''
        <!DOCTYPE html>
        <html><head><meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>Тест "Несуществующее животное"</title></head>
        <h3>Имя: {{name}}<br>
        Описание: {{desc}}<br></h3>
        <ul>
        % for key in data:
            <li><b>{{questions_dict[key][0]}}</b><br>
            {{questions_dict[key][1]}}</li>
        % end
        </ul>
        <br>
        <form action="http://0.0.0.0:9999">
            <input type="submit" value="Назад" />
        </form>
        </body></html>
        ''', name=name.encode('iso-8859-1'), desc=desc.encode('iso-8859-1'), data=data, questions_dict=questions_dict)

@error(404)
def error404(error):
    return 'Nothing here, sorry'

t = Thread(target=run, kwargs=dict(host='localhost', port=9999))
t.daemon = True
t.start()

sys.excepthook = cef.ExceptHook
cef.initialize()
cef.CreateBrowserSync(url='localhost:9999')
cef.MessageLoop()
cef.Shutdown()

#run(host='0.0.0.0', port=9999, reloader=True, debug=False)


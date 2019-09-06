
# from flask_script import Manager
# from app import app
# from flask_migrate import MigrateCommand

# app.config['JSON_AS_ASCII'] = False
# manager = Manager(app)
# manager.add_command('Base',MigrateCommand)

# if __name__ == '__main__':
#     # manager.run()
#     app.config['JSON_AS_ASCII'] = False
#     app.run(host='198.168.6.56', port=5000)



from flask_script import Manager
from app import app
from gevent import monkey, pywsgi

monkey.patch_all()

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('198.168.6.56', 5000), app)
    server.serve_forever()
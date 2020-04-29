# CornerstoneScaffold
### require
```shell script
pip install -r requirements.txt
```

### start up
common start
```shell script
python app.py
```
gunicorn start 
```shell script
gunicorn -c wsgi/config.py app:app
```
ps:
status debug=False daemon=True if you want stop run command
```shell script
kill `cat log/gunicorn.pid`
```

### Config 
config/config.py
FLASK_CONF=default|dev|prod|docker
ps:
if you need config from env just Make a class all attr get from 
like this, and Update ConfigInstanceFactory. (will make it graceful.)
```python
import os
class FooConfig:
    ATTR1=os.environ.get('attr1')
    ATTR2=os.environ.get('attr2')
    ATTR3=os.environ.get('attr3')
```

### Docker
```shell script
export DOCKER_BUILDKIT=1
docker build .
```

### for developer
register your module in folder ExtendRegister
```text
ExtendRegister
|-__init__.py
|-register_yourExtend.py
 
```
init_app in folder ApplicationFactory
```python
from flask import Flask
def create_app():
    app = Flask(__name__)
    # register.init_app(app)
    return app

```

### Reference
<https://github.com/yangyuexiong/Flask_BestPractices>   
<https://medium.com/@aidobreen/using-docker-dont-forget-to-use-build-caching-6e2b4f43771e>  
<https://stackoverflow.com/questions/58592259/how-do-you-enable-buildkit-with-docker-compose>   


## Flask简介
Flask诞生于2010年，是Armin ronacher（人名）用Python语言基于Werkzeug工具箱编写的轻量级Web开发框架。它主要面向需求简单的小应用。

Flask本身相当于一个内核，其他几乎所有的功能都要用到扩展（邮件扩展Flask-Mail，用户认证Flask-Login），都需要用第三方的扩展来实现。比如可以用Flask-extension加入ORM、窗体验证工具，文件上传、身份验证等。Flask没有默认使用的数据库，你可以选择MySQL，也可以用NoSQL。其 WSGI 工具箱采用 Werkzeug（路由模块） ，模板引擎则使用 Jinja2 。

可以说Flask框架的核心就是Werkzeug和Jinja2。

Python最出名的框架要数Django，此外还有Flask、Tornado等框架。虽然Flask不是最出名的框架，但是Flask应该算是最灵活的框架之一，这也是Flask受到广大开发者喜爱的原因。
## Flask扩展包
Flask-SQLalchemy：操作数据库；
Flask-migrate：管理迁移数据库；
Flask-Mail:邮件；
Flask-WTF：表单；
Flask-script：插入脚本；
Flask-Login：认证用户状态；
Flask-RESTful：开发REST API的工具；
Flask-Bootstrap：集成前端Twitter B

## 安装
### 创建一个虚拟环境
本系统默认是python 3.7.1

```
mkdir myproject
cd myproject
python -m env flask_ennv
```
激活虚拟环境：

`source flask_env/bin/activate`
或者
`. flask_env/bin/activate`

退出虚拟环境：

`deactivate`

### 安装Flask
`pip install Flask`

## 快速上手小例子
### 创建flask01.py
```
from flask import Flask
# 创建一个该类的实例,第一个参数是应用模块或者包的名称
app = Flask(__name__)

# 使用 route() 装饰器来告诉 Flask 触发函数的 URL
@app.route('/')
def hello_world():
    return "Hello, World!"
```
可以使用 flask 命令或者 python 的 -m 开关来运行这个应用。在 运行应用之前，需要在终端里导出 FLASK_APP 环境变量。FLASK_APP 环境变量中储存的是模块的名称，运行 flask run 命令就 会导入这个模块。

```
export FLASK_APP=[路径]/hello.py
flask run
```
如果需要打开所有开发功能（包括调试模式），那么要在运行服务器之前导出 FLASK_ENV 环境变量并把其设置为 development。

```
export FLASK_ENV=development
flask run
```
### url_for()
url_for() 函数用于构建指定函数的 URL。它把函数名称作为第一个 参数。它可以接受任意个关键字参数，每个关键字参数对应 URL 中的变量。未知变量 将添加到 URL 中作为查询参数。

```
from flask import Flask, escape, url_for
# 创建一个该类的实例,第一个参数是应用模块或者包的名称
app = Flask(__name__)

# 使用 route() 装饰器来告诉 Flask 触发函数的 URL
@app.route('/')
def index():
    return "index"

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
```
### 渲染模版
使用 render_template() 方法可以渲染模板，只要提供模板名称和需要 作为参数传递给模板的变量就行了。
Flask 会在 templates 文件夹内寻找模板。因此，如果你的应用是一个模块， 那么模板文件夹应该在模块旁边；如果是一个包，那么就应该在包里面。

```
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

```
创建templates文件夹，并在其中创建hello.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello from Flask</title>
</head>
<body>

{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}

</body>
</html>
```

### Flask创建app对象
#### 初始化参数
```
import_name: 
static_url_path:
static_folder: 默认‘static’
template_folder: 默认‘templates’
```
```
from flask import Flask

app = Flask(__name__,
            static_url_path="/python",  #访问静态资源的url前缀，默认值是static
            static_folder="static", # 静态文件的目录，默认就是static
            template_folder="templates", # 模版文件的额目录，默认是templates
            )

@app.route("/")
def index():
    """定义视图函数"""
    return "hello flask"

if __name__ == '__main__':
    # 启动flask程序
    app.run()
```
### 配置参数
```
app.config.from_pyfile(“yourconfig.cfg”) 或
app.config.from_object()
```
```
from flask import Flask

app = Flask(__name__,
            static_url_path="/python",  #访问静态资源的url前缀，默认值是static
            static_folder="static", # 静态文件的目录，默认就是static
            template_folder="templates", # 模版文件的额目录，默认是templates
            )
# 配置参数的使用
# 1、使用配置文件,创建config.cfg，写入DEBUG=True
# app.config.from_pyfile("config.cfg")

# 2、使用对象配置参数
class Config(object):
    DEBUG = True
app.config.from_object(Config)

# 3、直接操作config的字典对象
app.config["DEBUG"] = True

@app.route("/")
def index():
    """定义视图函数"""
    return "hello flask"

if __name__ == '__main__':
    # 启动flask程序
    app.run()
```
### 在视图读取配置参数
`from flask import current_app # 其中current_app就是app的代理人`

`app.config.get()  或者 current_app.config.get()`
### app.run的参数
`app.run(host=”0.0.0.0”, port=5000)`


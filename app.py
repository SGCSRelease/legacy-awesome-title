# $ pip install flask
from flask import Flask, request, jsonify
# $ pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# $ pip install flask-admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# $ pip install flask-migrate
from flask_migrate import Migrate

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
# pip install pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://awesome:title@localhost/minhoryang'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
admin = Admin(app)  # <-- Admin page Setting!
migrate = Migrate(app, db)

class User(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.String(20), unique=True)
    pwd = db.Column(db.String(20))
    name = db.Column(db.String(10))
    hakbun = db.Column(db.Integer)
    last_login = db.Column(db.String(30))


@app.route("/user/register", methods=["GET", "POST"])
def Register():
    if request.method == "GET":
        return """
        회원가입 기능이 들어갈꺼에요.
        <script src="//code.jquery.com/jquery-1.12.0.min.js"></script>
        <form action="/user/register" method="POST">
            ID: <input type=text class='usr' id=usr name=usr /><br>
            PW: <input type=text id=pwd name=pwd /><br>
            Name: <input type=text id=name name=name /><br>
            Hakbun: <input type=text id=hakbun name=hakbun /><br>
            <input type=submit />
        </form>
        <script>
            $('#usr').change(
                function(){
                    var check_id = "/user/check_id/" + $('.usr').val();
                    $.get(
                        check_id,
                        function (data){
                            alert("쓰셔도 좋습니다.");
                        }
                    ).fail(
                        function (data){
                            alert("겹치는 ID가 있습니다.");
                        }
                    );

                }
            );
        </script>
        """
    else:
        new = User()
        new.usr = request.form['usr']
        new.pwd = request.form['pwd']
        new.name = request.form['name']
        new.hakbun = int(request.form['hakbun'])
        db.session.add(new)
        db.session.commit()
        return "성공하였습니다!"

@app.route("/user/check_id/<id>")
def CheckID(id):
    found = User.query.filter(
            User.usr == id,
    ).first()
    if found:
        return "땡!", 400
    return "굳!"

@app.route("/user/check_hakbun/<hakbun>")
def CheckHakBun(hakbun):
    found = User.query.filter(
            User.hakbun == hakbun,
    ).first()
    if found:
        return "땡!", 400
    return "굳!"













if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

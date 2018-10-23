from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

#Add User Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    #blogs = db.relationship('Blog', backref='owner')

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    valid = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner, valid):
        self.title = title
        self.body = body
        self.owner = owner
        self.valid = True 





#Add Login

@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method =='POST':
        user_name = request.form['user-name']
        password = request.form['password']
        user= User.query.filter_by(user_name = user_name).first()
        print (user)
        if not user_name:
            return redirect('/signup')
        elif user_name and not user:
            flash('user does not exist')
            return redirect ('/login')
        elif password==user.password:
            session['user'] = user.user_name
            flash('welcome back, '+ user.user_name)
            return redirect('/blog')
        elif password !=user.password:
            flash('invalid password')
            return redirect ('/login')
        


    return render_template('login.html')

#Add Sign Up
@app.route('/signup', methods= ['POST', 'GET'])
def signup():
    if request.method=='POST':
        user_name=request.form['user-name']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            flash('user already exists')
            return redirect ('/signup')
        elif len(user_name) <3 or len(password)<3:
            flash('invalid username or password')
            return redirect ('/signup')
        elif not user_name or not password or not verify:
            flash('one or more fields invalid')
            return redirect ('/signup')
        elif password!=verify:
            flash('''passwords don't match''')
            return redirect ('/signup')
        else:
            user = User(user_name=user_name, password = password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.user_name
            return redirect('/add-a-blog-entry')
    return render_template('signup.html')
    
#add log out

@app.route('/main-blog-page')
def main_blog_page():
    return redirect('/blog')

@app.route('/add-a-blog-entry', methods= ['POST', 'GET'])
def add_a_blog_entry():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        owner=User.query.filter_by(user_name=session['user']).first()
        new_blog = Blog(blog_title, blog_body, owner, True)
        if not blog_title:
            #entry = Blog.query.filter_by(body=blog_body).first()
            return render_template('blogentry.html', body= blog_body, error= "Be sure to enter both a title and a body")
        if not blog_body: 
            return render_template('blogentry.html', title= blog_title, error= "Be sure to enter both a title and a body")
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()
        last_post = blogs[-1]
        id = str(last_post.id)
        return redirect('/blog?id=' + id )
    return render_template('/blogentry.html')    
    
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(title, owner, True)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(valid=True).all()
    id = request.args.get('id')

    if id:
        blog_post = Blog.query.filter_by(id=id).first()
        return render_template('blogsingleentry.html', title= blog_post.title, body= blog_post.body)
    
    return render_template('blog.html',title="Build a Blog", blogs=blogs, id=id)

 
@app.before_request
def require_login():
    allowed_routes=['blog', 'login', 'signup', 'main-blog-page']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

if __name__ == '__main__':
    app.run()
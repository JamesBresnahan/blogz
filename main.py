from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    valid = db.Column(db.Boolean)

    def __init__(self, title, body, valid):
        self.title = title
        self.body = body
        self.valid = True 

#@app.before_request
#def require_login():
#    allowed_routes=['login', 'register']
#    if request.endpoint not in allowed_routes and 'email' not in session:
#        return redirect('/login')
    

@app.route('/main-blog-page')
def main_blog_page():
    return redirect('/blog')

@app.route('/add-a-blog-entry', methods= ['POST', 'GET'])
def add_a_blog_entry():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body, True)
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
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(title, owner, True)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(valid=True).all()
    print (request.args)
    id = request.args.get('id')

    if id:
        blog_post = Blog.query.filter_by(id=id).first()
        return render_template('blogsingleentry.html', title= blog_post.title, body= blog_post.body)
    
    return render_template('blog.html',title="Build a Blog", blogs=blogs, id=id)

if __name__ == '__main__':
    app.run()
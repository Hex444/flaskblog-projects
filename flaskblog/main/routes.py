from flask import Blueprint
from flask import render_template, request, Blueprint
from flaskblog.models import Post
main=Blueprint('main', __name__)

# posts = [
#     {
#         "author": "max tennyson",
#         "title": "blog post 1",
#         "content": "blueprints of the omnitrix spread through the entire universe, the entire multiverse at danger",
#         "date_posted": "2 Feb, 2022"
#     },
#     {
#         "author": "Sherlock, a great thought to be dead detective",
#         "title": "blog post 2",
#         "content": "Rohit Ghosh caught to be stealing doughnuts from dunkin doughnuts, fined for $2000",
#         "date_posted": "3 Feb, 2022"
#     }
# ]

@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)

@main.route("/about")
def about():
    return render_template("about.html", title="about")
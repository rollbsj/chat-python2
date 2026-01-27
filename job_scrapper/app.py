from flask import Flask, render_template, request
from scrapper import search_incruit 
from file import save_to_csv
from os

app = Flask(__name__) 
page_num= 2

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/search")
def search(): 

    keyword = request.args.get("keyword")
    jobs = search_incruit(keyword, page_num)
    return render_template("search.html", keyword = keyword, jobs = jobs)

@app.route("/download")
def download():
    keyword = request.args.get("keyword")
    jobs = search_incruit(keyword, page_num)
    save_to_csv(jobs)

if __name__ == "__main__":
    app.run()
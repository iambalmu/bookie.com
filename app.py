from flask import Flask,render_template,request
import pickle
import numpy as np

final_rb = pickle.load(open('final1.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top50')
def top50():
    return render_template('top50.html',
                           book_name=list(final_rb['Book-Title'].values),
                           author=list(final_rb['Book-Author'].values),
                           image=list(final_rb['Image-URL-S'].values),
                           votes=list(final_rb['num_ratings'].values),
                           rating=list(final_rb['avg_rating'].values))

if __name__=='__main__':
    app.run(debug=True)



from flask import Flask,render_template,request
import pickle
import numpy as np

bk= pickle.load(open('bk.pkl','rb'))
book=pickle.load(open('books.pkl','rb'))
final_fil=pickle.load(open('final.pkl','rb'))
sim=pickle.load(open('similarity_scores.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top50')
def top50():
    return render_template('top50.html',
                           book_name=list(bk['Title'].values),
                           author=list(bk['authors'].values),
                           image=list(bk['image'].values),
                           link=list(bk['previewLink'].values),
                           date=list(bk['publishedDate'].values),
                           summary=list(bk['description'].values),
                           categories=list(bk['categories'].values)
                           )

@app.route('/recommend')
def recommend_ui():
      return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(final_fil.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(sim[index])), key=lambda x: x[1], reverse=True)[1:20]
    k=sorted(list(enumerate(sim[index])), key=lambda x: x[1], reverse=True)[0]
    data = []
    for i in similar_items:
        item = []
        temp_df = book[book['Book-Title'] == final_fil.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)


    data2=[]
    temp_df2 = book[book['Book-Title'] == final_fil.index[k[0]]]
    data2.append(list(temp_df2.drop_duplicates('Book-Title')['Book-Title'].values))
    print(data)
    k=data2[0][0]
    print(k)
    return render_template('recommend.html',data=data,k=k)

@app.route('/find_books',methods=['post'])
def find():
    user_input = request.form.get('user_input')
    index = np.where(final_fil.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(sim[index])), key=lambda x: x[1], reverse=True)[0:1]
    k=sorted(list(enumerate(sim[index])), key=lambda x: x[1], reverse=True)[0]
    data = []
    for i in similar_items:
        item = []
        temp_df = book[book['Book-Title'] == final_fil.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        data.append(item)



    print(data)

    return render_template('find.html',data=data)

@app.route('/find')
def author():
    return render_template('find.html')

@app.route('/connect')
def connectwithme():
    return render_template('connect.html')

if __name__=='__main__':
    app.run(debug=True)



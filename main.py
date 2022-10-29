from flask import Flask, jsonify, request
from storage import liked_articles, not_liked_articles, all_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-articles")
def get_article():
    movies_data = {
        'url': all_articles[0][11],
        'title': all_articles[0][12],
        'text': all_articles[0][13],
        'lang': all_articles[0][14],
        'total_events': all_articles[0][15]
    }
    return jsonify({
        'data': movies_data,
        'status': 'success'
    })

#assuming the user liked the article so we are removing it from the list
@app.route("/liked-article", methods = ['POST'])
def liked_article():
    #getting the info at 0 index
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0) #deleting from all_articles

    return jsonify({
        'status': 'success'
    }), 201

#assuming the user didn't like the article so we are removing it from the list
@app.route("/unliked-article", methods = ['POST'])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)

    return jsonify({
        'status': 'sucess'
    }), 201

@app.route("/popular-articles")
def popular_articles():
    articles_data = []
    for article in output:
        #creating a custom dictionary of the key value for the data that we must've received from the demographic filtering and finally we are returning the list of custom dictionary we created for our 20 most popular articles
        _d = {
            'url': article[0],
            'title': article[1],
            'text': article[2],
            'lang': article[3],
            'total_events': article[4]
        }
        articles_data.append(_d)
    return jsonify({
        'data': articles_data,
        'status': 'success'
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    #iterating over all the liked articles
    for liked_article in liked_articles:
        #giving the movie 19th column (title) as an argument to the getrecommendations() and saving all the data into a list all_recommended
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
        #to remove the duplicates and also to sort the movies
        import itertools
        all_recommended.sort()
        all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))
        article_data = []
        for recommended in all_recommended:
            _d = {
                'url': recommended[0],
                'title': recommended[1],
                'text': recommended[2],
                'lang': recommended[3],
                'total_events': recommended[4]
            }
            article_data.append(_d)
        return jsonify({
            'data': article_data,
            'status': 'success'
        }), 200

if __name__ == '__main__':
    app.run()
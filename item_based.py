import pandas as pd
from sklearn.neighbors import NearestNeighbors

def fill_df(df, user_id):

    df1 = df.copy()

    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(df.values)
    distances, indices = knn.kneighbors(df.values, n_neighbors=3)

    user_index = df.columns.tolist().index(user_id)
    number_neighbors = 3

    for m, t, in list(enumerate(df.index)):
        if df.iloc[m, user_index] == 0:
            sim_movies = indices[m].tolist()
            movie_distances = distances[m].tolist()

            if m in sim_movies:
                id_movie = sim_movies.index(m)
                sim_movies.remove(m)
                movie_distances.pop(id_movie)
            #if m is not in sim_movies, then all sim_movies have distance = 0
            #so we can just remove 1 as they are all the same
            else:
                sim_movies = sim_movies[:n_neighbors-1]
                movie_distances = movie_distances[:n_neighbors-1]
            
            movie_similarity = [1-x for x in movie_distances]
            movie_similarity_copy = movie_similarity.copy()
            nominator = 0

            for s in range(0, len(movie_similarity)):
                if df.iloc[sim_movies[s], user_index] == 0:
                    # if the rating of the similar movie is 0 then no need to use it in calculations
                    if len(movie_similarity_copy) == (number_neighbors -1):
                        movie_similarity_copy.pop(s)
                    else:
                        movie_similarity_copy.pop(s-(len(movie_similarity)-len(movie_similarity_copy)))
                    
                else:
                    nominator = nominator + movie_similarity[s]*df.iloc[sim_movies[s],user_index]

            if len(movie_similarity_copy) > 0:
                if sum(movie_similarity_copy) > 0:
                    predicted_r = nominator/sum(movie_similarity_copy)
                else:
                    predicted_r = 0
                
            else:
                predicted_r = 0
            
            df1.iloc[m, user_index] = predicted_r
    return df1
    
def recommend_movies(user, df, df1, num_recommended_movies):

    print(f'The list of the movies {user} has watched')

    for m in df[df[user] > 0][user].index.tolist():
        print(m)

    
    print('')

    recommended_movies = []

    for m in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        if predicted_rating > 3:
            recommended_movies.append((m, str(predicted_rating)))

    sorted_rm = sorted(recommended_movies, key=lambda x:x[1], reverse=True)

    print('The sorted movies: ')
    rank = 0
    for movie in sorted_rm[:num_recommended_movies]:
        print(f'{rank}: {movie[0]} -predicted rating: {movie[1]}')
        rank += 1
    return recommended_movies


import pandas as pd
from sklearn.neighbors import NearestNeighbors

data={
        'user_0': [0,3,0,5,0,0,4,5,0,2],
        'user_1': [0,0,3,2,5,0,4,0,3,0],
        'user_2': [3,1,0,3,5,0,0,4,0,0],
        'user_3': [4,3,4,2,0,0,0,2,0,0],
        'user_4': [2,0,0,0,0,4,4,3,5,0],
        'user_5': [1,0,2,4,0,0,4,0,5,0],
        'user_6': [2,0,0,3,0,4,3,3,0,0],
        'user_7': [0,0,0,3,0,2,4,3,4,0],
        'user_8': [5,0,0,0,5,3,0,3,0,4],
        'user_9': [1,0,2,0,4,0,4,3,0,0]}
indices = ['movie_0', 'movie_1', 'movie_2', 'movie_3',
'movie_4', 'movie_5', 'movie_6', 'movie_7', 'movie_8', 'movie_9']
df = pd.DataFrame(index=indices, columns=data, data=data)

df1 = df.copy()

knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)
distances, indices = knn.kneighbors(df.values, n_neighbors=3)

user_index = df.columns.tolist().index('user_4')
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
    
def recommend_movies(user, num_recommended_movies):

    print(f'The list of the movies {user} has watched')

    for m in df[df[user] > 0][user].index.tolist():
        print(m)
    
    print('')

    recommended_movies = []

    for m in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        recommended_movies.append((m, predicted_rating))

    sorted_rm = sorted(recommended_movies, key=lambda x:x[1], reverse=True)

    print('The sorted movies: ')
    rank = 0
    for movie in sorted_rm[:num_recommended_movies]:
        print(f'{rank}: {movie[0]} -predicted rating: {movie[1]}')
        rank += 1

recommend_movies('user_4', 5)

import streamlit as st
import pickle
import pandas as pd

# Cargar el modelo
with open('./Data/metadata.pkl', 'rb') as metadata_f:
    metadata = pickle.load(metadata_f)

with open('./Data/gower.pkl', 'rb') as gower_f:
    gower = pickle.load(gower_f)

def recommend_games(game_input,metadata_selected,gower_dist_matrix, n=5):

    #Le paso el nombre del juego que tiene que si o si estar en meta (mi universo de juegos) y el n de recomendaciones. Default 4 

    try:
        # Buscar juegos cuyos nombres contengan la cadena de búsqueda en metadata_selected
        matching_games = metadata_selected[metadata_selected['name'].str.contains(game_input, case=False)].copy()

        if not matching_games.empty:
            # Si el juego está en metadata_selected, obtener su índice
            game_index = matching_games.index[0]
            #print(game_index, metadata_selected[metadata_selected['name']==game_input],matching_games)

            # Obtener los juegos más similares
            similarity_score = list(enumerate(gower_dist_matrix[game_index]))
            similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=False)
            similarity_score = similarity_score[1:n]

            # Retornar los nombres de los juegos utilizando el DataFrame meta
            game_indices = [i[0] for i in similarity_score]
            return metadata_selected[['name']].iloc[game_indices]

        else:
            print("Realizando una busqueda más amplia. Espere por favor.No se encontro su juego")
            
    except IndexError:
        # Si ocurre un IndexError, imprime un mensaje y devuelve None o un DataFrame vacío
        print(f"No se encontraron juegos que contengan '{game_input}'.")
        return None


def main():
    st.title('Streamlit App')

    user_imput = st.text_input('Ingrese el el nombre del juego:', '')

    if st.button('Predecir'):
        if user_imput:
            game_imput = str(user_imput)
            recomended = recommend_games(game_imput,metadata,gower,20)

            recomend_df = pd.DataFrame(recomended)  

            st.subheader('Recomendaciones:')
            st.write(recomend_df)

        else:
            st.warning('Ingrese un juego válido .')

if __name__ == '__main__':
    main()
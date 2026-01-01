import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Initialize session state
if 'show_id_input' not in st.session_state:
    st.session_state.show_id_input = False

if 'show_recipe_details' not in st.session_state:
    st.session_state.show_recipe_details = False

if 'show_similar_button' not in st.session_state:
    st.session_state.show_similar_button = False

if 'show_similar_input' not in st.session_state:
    st.session_state.show_similar_input = False


@st.cache_data
def load_data(path):
    return pd.read_parquet(path)

recipes_ingtag = load_data('/Users/snehauppu/Documents/PythonProjects/RecipeRecommendationSystem/recipes_ingtag.parquet')
recipes_steps = load_data('/Users/snehauppu/Documents/PythonProjects/RecipeRecommendationSystem/recipes_steps.parquet')
recipes_final = load_data('/Users/snehauppu/Documents/PythonProjects/RecipeRecommendationSystem/recipes_final.parquet')

st.image('/Users/snehauppu/Documents/PythonProjects/RecipeRecommendationSystem/Image.jpeg', use_container_width = True)
st.title('Recipe Search & Recommendations')

tag_options = ['60-minutes-or-less', '30-minutes-or-less', '15-minutes-or-less', 'meat', 'poultry', 'vegetables', 
               'fruit', 'pasta-rice-and-grains', 'dietary', 'healthy', 'low-carb', 'low-sodium', 'low-saturated-fat', 'low-calorie', 
               'low-cholesterol', 'low-fat', 'low-sugar', 'beginner-cook', 'sweet', 'savory']

tags_selected = st.multiselect('Please select any tags for a meal you are interested in.', tag_options)

def all_tags_present(item_tags, selected):
    return all(string in item_tags for string in selected)

recipes_rec = recipes_ingtag.copy()
if tags_selected:
    recipes_rec['tag_match'] = recipes_rec['tags'].apply(all_tags_present, selected=tags_selected)
        
ing_selected = st.text_input('Please enter ingredients you have on hand')
ing_selected = ing_selected.split(',')

def check_ingredients(ingredients_col):
    ingredients = ing_selected
    ings_matched = ingredients_col
    
    ingredients_str = ' '.join(str(ing).lower() for ing in ings_matched)
    
    for item in ingredients:
        item = item.strip('s')
        if item not in ingredients_str:
            return False

    return True

search = st.button('Search for Matching Recipes')
if search:
    recipes_rec = recipes_ingtag.copy()

    if tags_selected:
        recipes_rec['tag_match'] = recipes_rec['tags'].apply(all_tags_present, selected=tags_selected)
        recipes_rec = recipes_rec[recipes_rec['tag_match'] == True]

    if ing_selected:
        recipes_rec['ing_match'] = recipes_rec['ingredients'].apply(check_ingredients)
        recipes_rec = recipes_rec[recipes_rec['ing_match'] == True]

    st.session_state.search_results = recipes_rec
    st.session_state.show_id_input = True

    recipes_id = recipes_rec['id'].values
    recipes_steps_rec = recipes_steps[recipes_steps['id'].isin(recipes_id)][['id', 'name', 'description']]
    st.write(recipes_steps_rec)

if st.session_state.show_id_input:
    id_num = st.number_input('Enter the ID of the recipe you are interested in', value=0)
    get_recipe = st.button('Get Recipe')
    if get_recipe and id_num != 0:
        recipe = recipes_steps[recipes_steps['id'] == id_num]
        rec_name = recipe['name'].values[0]
        rec_steps = recipe['steps'].values[0]
        rec_ingredients = recipe['ingredients'].values[0]
        link_name = rec_name.replace(' ', '-')
        link_url = f'https://www.food.com/recipe/{link_name}-{id_num}'
        
        st.write(f"Link to Recipe: {link_url}")
        st.write(f"Recipe Name: {rec_name.title()}")
        st.write(f"Ingredients: {rec_ingredients}")
        
        for i, step in enumerate(rec_steps, 1):
            st.write(f"Step {i}: {step.capitalize()}")

        st.session_state.show_similar_button = True

        

# Get similar recipes
if st.session_state.show_similar_button:
    sim = st.button('Take a look at some similar recipes')
    if sim:
        rec_feat = recipes_final[recipes_final['id'] == id_num]
        rec_feat = rec_feat.drop(columns=['id']).values.reshape(1, -1)

        cosine_sim = cosine_similarity(rec_feat, recipes_final.drop(columns=['id']))
        sim_scores = list(zip(recipes_final['id'].values, cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        rec_indices = [i[0] for i in sim_scores]

        recs = recipes_steps[recipes_steps['id'].isin(rec_indices)][['id', 'name', 'description']]
        st.write(recs)

        st.session_state.show_similar_input = True


if st.session_state.show_similar_input:
    d_num = st.number_input('If any of those interest you, enter the ID here', value=0)
    get_recipe = st.button('Get the Recipe')
    if get_recipe and d_num != 0:
        recipe = recipes_steps[recipes_steps['id'] == d_num]
        rec_name = recipe['name'].values[0]
        rec_steps = recipe['steps'].values[0]
        rec_ingredients = recipe['ingredients'].values[0]
        link_name = rec_name.replace(' ', '-')
        link_url = f'https://www.food.com/recipe/{link_name}-{d_num}'
        st.write(f"Link to Recipe: {link_url}")
        st.write(f"Recipe Name: {rec_name.title()}")
        st.write(f"Ingredients: {rec_ingredients}")
        
        for i, step in enumerate(rec_steps, 1):
            st.write(f"Step {i}: {step.capitalize()}")

        
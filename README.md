
# Recipe Recommendation System

This is a **Streamlit-based Recipe Recommendation System** that allows users to find recipes based on:

- Tags (e.g., vegetarian, 30-minutes-or-less)
- Ingredients

Enter the ingredients you have and get the recipes that can be made wth those ingredients.

The app also suggests **similar recipes** using cosine similarity on preprocessed recipe features.

---

## Project Overview

This project demonstrates how **content-based filtering** can be used to build a recipe recommendation engine using tags, ingredients, and textual data.

The backend is implemented in **Python**, the model is developed and preprocessed in a Jupyter Notebook, and the application is deployed using **Streamlit**.

---

## Tools Used

- **Python**
- **Pandas** for data cleaning and transformation
- **Scikit-learn** for cosine similarity
- **Streamlit** for interactive frontend
- **Jupyter Notebook / Colab** for preprocessing

---

## Dataset

This project uses the **[Food.com Recipes Dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-interactions)** from Kaggle.

Please download the following file from Kaggle and place them in your working directory:
- `RAW_recipes.csv`

These files are cleaned and converted to `.parquet` format as part of the preprocessing.

---

##  How It Works

1. The user selects a tag or ingredient from a dropdown menu and enter the ingredients he wants to use.
2. The system filters recipes that match the selected tag(s) and ingredient(s) and displays them
3. Cosine similarity is calculated on preprocessed recipe vectors.
4. The app displays:
   - Matching recipes
   - Similar recipe suggestions

---

## Steps to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/Sui-Generis-14/Recipe_Recommendation_System.git
cd Recipe_Recommendation_System
```
### 2. Install Dependencies
```bash
pip install pandas streamlit scikit-learn
```
### 3. Download the Dataset
Go to Kaggle and download:
> RAW_recipes.csv

### 4. Generate Required .parquet Files
Run the preprocessing script:
```bash
python recipe_recommendation.py
```
This will create:
- recipes_ingtag.parquet
- recipes_steps.parquet
- recipes_final.parquet

These files must be present to run the app.

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```

You'll be able to:
- Choose recipe tags
- Get recipe matches
- View 10 similar recipes

## Folder Structure
```bash
RecipeRecommendationSystem/
├── recipe_recommendation.py          # Streamlit app
├── RecipeRecommendationSystem.ipynb  # Preprocessing and ML logic
├── *.parquet                         # Large data files (excluded)
├── .gitignore                        # Excludes large files
└── README.md                         # This file
```
## Future Enhancements:
- Add calorie and nutrition filters
- Include recipe images from external APIs
- Add fuzzy ingredient matching
- Deploy on Streamlit Cloud


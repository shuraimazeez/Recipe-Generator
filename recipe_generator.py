import streamlit as st
import random
from collections import defaultdict
from PIL import Image
import requests
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="AI Chef Master",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS (you'll need to create a style.css file or remove this if not needed)
try:
    local_css("style.css")
except:
    pass

class RecipeGenerator:
    def __init__(self):
        # Expanded knowledge base for recipe generation
        self.cuisines = {
            'italian': {
                'proteins': ['chicken', 'beef', 'fish', 'pork', 'tofu', 'shrimp', 'mussels'],
                'carbs': ['pasta', 'risotto', 'polenta', 'bread', 'gnocchi', 'focaccia'],
                'vegetables': ['tomatoes', 'zucchini', 'eggplant', 'spinach', 'mushrooms', 'artichokes', 'arugula'],
                'spices': ['basil', 'oregano', 'rosemary', 'garlic', 'parsley', 'thyme', 'sage'],
                'cooking_methods': ['saute', 'bake', 'simmer', 'grill', 'braise', 'roast'],
                'signature': ['olive oil', 'parmesan cheese', 'balsamic vinegar', 'mozzarella', 'prosciutto'],
                'image': 'https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            'indian': {
                'proteins': ['chicken', 'lamb', 'fish', 'chickpeas', 'lentils', 'paneer', 'tofu'],
                'carbs': ['rice', 'naan', 'roti', 'puri', 'dosa', 'paratha'],
                'vegetables': ['potatoes', 'cauliflower', 'spinach', 'eggplant', 'okra', 'peas', 'beans'],
                'spices': ['cumin', 'turmeric', 'coriander', 'garam masala', 'chili', 'cardamom', 'mustard seeds'],
                'cooking_methods': ['curry', 'tandoori', 'fry', 'steam', 'bhuna', 'dum'],
                'signature': ['ghee', 'yogurt', 'tamarind', 'coconut milk', 'mango powder'],
                'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            'mexican': {
                'proteins': ['chicken', 'beef', 'pork', 'beans', 'tofu', 'shrimp', 'chorizo'],
                'carbs': ['tortillas', 'rice', 'corn', 'tacos', 'tostadas', 'tamales'],
                'vegetables': ['peppers', 'onions', 'tomatoes', 'avocado', 'zucchini', 'squash', 'jalapenos'],
                'spices': ['cumin', 'chili powder', 'paprika', 'oregano', 'cilantro', 'epazote', 'achiote'],
                'cooking_methods': ['grill', 'fry', 'stew', 'bake', 'sear', 'barbacoa'],
                'signature': ['lime', 'sour cream', 'cheese', 'avocado', 'salsa verde'],
                'image': 'https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            'japanese': {
                'proteins': ['salmon', 'tuna', 'chicken', 'tofu', 'pork', 'beef', 'shrimp'],
                'carbs': ['rice', 'noodles', 'udon', 'soba', 'ramen'],
                'vegetables': ['seaweed', 'daikon', 'mushrooms', 'cabbage', 'spinach', 'bamboo shoots'],
                'spices': ['soy sauce', 'mirin', 'sake', 'ginger', 'wasabi', 'sesame'],
                'cooking_methods': ['stir-fry', 'simmer', 'grill', 'deep-fry', 'steam'],
                'signature': ['miso paste', 'dashi', 'pickled ginger', 'nori', 'bonito flakes'],
                'image': 'https://images.unsplash.com/photo-1553621042-f6e147245754?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            }
        }
        
        self.meal_types = ['breakfast', 'lunch', 'dinner', 'dessert', 'snack']
        self.dietary_restrictions = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'nut-free', 'low-carb']
        self.difficulty_levels = ['easy', 'medium', 'hard']
    
    def generate_recipe(self, cuisine=None, meal_type=None, dietary=None, difficulty=None):
        # If no cuisine specified, pick one randomly
        if not cuisine:
            cuisine = random.choice(list(self.cuisines.keys()))
        
        # Get the cuisine profile
        profile = self.cuisines[cuisine]
        
        # Generate recipe name
        cooking_method = random.choice(profile['cooking_methods'])
        protein = random.choice(profile['proteins'])
        name = f"{cooking_method.title()} {protein} {cuisine.title()}"
        
        # Adjust for dietary restrictions
        ingredients = []
        if dietary == 'vegetarian':
            proteins = [p for p in profile['proteins'] if p not in ['chicken', 'beef', 'pork', 'lamb', 'fish']]
        elif dietary == 'vegan':
            proteins = [p for p in profile['proteins'] if p not in ['chicken', 'beef', 'pork', 'lamb', 'fish']]
            profile['signature'] = [s for s in profile['signature'] if s not in ['cheese', 'yogurt', 'sour cream']]
        else:
            proteins = profile['proteins']
        
        # Select ingredients based on difficulty
        if difficulty == 'easy':
            num_ingredients = random.randint(4, 6)
            num_spices = 1
        elif difficulty == 'medium':
            num_ingredients = random.randint(6, 8)
            num_spices = 2
        else:  # hard
            num_ingredients = random.randint(8, 10)
            num_spices = 3
        
        ingredients.append(random.choice(proteins))
        ingredients.append(random.choice(profile['carbs']))
        ingredients.extend(random.sample(profile['vegetables'], min(2, len(profile['vegetables']))))
        ingredients.extend(random.sample(profile['spices'], num_spices))
        ingredients.append(random.choice(profile['signature']))
        
        # Generate instructions based on difficulty
        steps = [
            f"Prepare all ingredients by cleaning and chopping as needed."
        ]
        
        if difficulty == 'easy':
            steps.extend([
                f"Heat a pan and {cooking_method} the {ingredients[0]} with {ingredients[3]} for flavor.",
                f"Cook the {ingredients[1]} according to package instructions.",
                f"Combine all ingredients and cook for {random.randint(5, 15)} minutes.",
                f"Garnish with {ingredients[-1]} and serve."
            ])
        elif difficulty == 'medium':
            steps.extend([
                f"Marinate the {ingredients[0]} with {', '.join(random.sample(profile['spices'], 2))} for {random.randint(15, 30)} minutes.",
                f"In a large pan, {cooking_method} the {ingredients[0]} until golden brown.",
                f"Add {', '.join(ingredients[2:4])} and cook for {random.randint(5, 10)} minutes.",
                f"Meanwhile, prepare the {ingredients[1]} separately.",
                f"Combine all components and simmer for {random.randint(5, 10)} minutes.",
                f"Adjust seasoning and garnish with {ingredients[-1]} before serving."
            ])
        else:  # hard
            steps.extend([
                f"Prepare a marinade with {', '.join(random.sample(profile['spices'], 3))} and coat the {ingredients[0]}. Let sit for {random.randint(30, 120)} minutes.",
                f"Start by {cooking_method}ing the {ingredients[0]} in batches to ensure even cooking.",
                f"In a separate pan, caramelize the {random.choice(profile['vegetables'])} with {random.choice(profile['spices'])}.",
                f"Prepare a sauce by combining {random.choice(profile['signature'])}, {random.choice(profile['spices'])}, and {random.choice(['broth', 'cream', 'coconut milk'])}.",
                f"Cook the {ingredients[1]} using a specialized technique (like pilaf for rice or al dente for pasta).",
                f"Layer all components in a serving dish and bake for {random.randint(10, 20)} minutes for flavors to meld.",
                f"Finish with a garnish of {ingredients[-1]} and serve with accompaniments."
            ])
        
        # Generate cooking time based on difficulty
        if difficulty == 'easy':
            cook_time = f"{random.randint(10, 30)} minutes"
        elif difficulty == 'medium':
            cook_time = f"{random.randint(30, 60)} minutes"
        else:
            cook_time = f"{random.randint(1, 3)} hours"
        
        # Format the recipe
        recipe = {
            'name': name,
            'cuisine': cuisine.title(),
            'meal_type': meal_type if meal_type else 'Any',
            'dietary': dietary if dietary else 'None',
            'difficulty': difficulty if difficulty else 'medium',
            'cook_time': cook_time,
            'ingredients': ingredients,
            'instructions': steps,
            'image_url': profile['image']
        }
        
        return recipe

def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

def main():
    # Initialize recipe generator
    generator = RecipeGenerator()
    
    # Sidebar for inputs
    with st.sidebar:
        st.title("🍳 AI Chef Master")
        st.markdown("Generate custom recipes based on your preferences!")
        
        cuisine = st.selectbox(
            "Choose a cuisine",
            ["Any"] + list(generator.cuisines.keys()),
            index=0
        )
        
        meal_type = st.selectbox(
            "Meal type",
            ["Any"] + generator.meal_types,
            index=0
        )
        
        dietary = st.selectbox(
            "Dietary restrictions",
            ["None"] + generator.dietary_restrictions,
            index=0
        )
        
        difficulty = st.selectbox(
            "Difficulty level",
            ["Any"] + generator.difficulty_levels,
            index=0
        )
        
        generate_btn = st.button("Generate Recipe", type="primary")
    
    # Main content area
    st.title("Your Custom Recipe")
    
    if generate_btn:
        with st.spinner("Cooking up your perfect recipe..."):
            # Generate recipe
            recipe = generator.generate_recipe(
                cuisine if cuisine != "Any" else None,
                meal_type if meal_type != "Any" else None,
                dietary if dietary != "None" else None,
                difficulty if difficulty != "Any" else None
            )
            
            # Display recipe
            col1, col2 = st.columns([1, 2])
            
            with col1:
                img = load_image_from_url(recipe['image_url'])
                if img:
                    st.image(img, caption=recipe['cuisine'], use_column_width=True)
                else:
                    st.image("https://via.placeholder.com/400x300?text=Food+Image", use_column_width=True)
                
                st.subheader("Recipe Info")
                st.markdown(f"""
                **Cuisine:** {recipe['cuisine']}  
                **Meal Type:** {recipe['meal_type']}  
                **Dietary:** {recipe['dietary']}  
                **Difficulty:** {recipe['difficulty'].title()}  
                **Cooking Time:** {recipe['cook_time']}
                """)
            
            with col2:
                st.markdown(f"## {recipe['name']}")
                
                with st.expander("Ingredients", expanded=True):
                    for ingredient in recipe['ingredients']:
                        st.markdown(f"- {ingredient}")
                
                with st.expander("Instructions", expanded=True):
                    for i, step in enumerate(recipe['instructions'], 1):
                        st.markdown(f"{i}. {step}")
            
            # Add a nice divider
            st.markdown("---")
            
            # Feedback section
            st.subheader("Enjoy your meal!")
            st.markdown("Did you like this recipe? Let us know!")
            
            feedback_cols = st.columns(3)
            with feedback_cols[0]:
                st.button("😍 Loved it!")
            with feedback_cols[1]:
                st.button("😐 It's okay")
            with feedback_cols[2]:
                st.button("😞 Not for me")
    
    else:
        st.info("👈 Select your preferences and click 'Generate Recipe' to get started!")
        st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
                caption="Let's cook something delicious!", use_column_width=True)

if __name__ == "__main__":
    main()
# Import python packages
import streamlit as st


# Write directly to the app
st.title('🥤 Customize Your Smoothie! 🥤')
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake (depending on your setup)
# Option 1: Use get_active_session if available


# Option 2: Use st.connection if your Streamlit supports it
# cnx = st.connection("snowflake")
# session = cnx.session()

# Load data from Snowflake


# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    st.write(my_insert_stmt)

st.stop()

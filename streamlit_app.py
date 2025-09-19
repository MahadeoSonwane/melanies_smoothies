# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App Title
st.title(":cup_with_straw: Customize Your Smoothie")
st.write("Choose the fruits you want in your custom Smoothie! 🥤")

# Input: Smoothie Name
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Create Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# If user selected ingredients
if ingredients_list:
    # Join ingredients with commas
    ingredients_string = ",".join(ingredients_list)

    st.write("Your selected ingredients:", ingredients_string)

    # SQL insert statement (parameterized for safety)
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES (?, ?)
    """

    # Submit order button
    if st.button("Submit Order"):
        if not name_on_order:
            st.error("⚠️ Please enter a name for your Smoothie before submitting.")
        else:
            # Insert order safely
            session.sql(my_insert_stmt, (ingredients_string, name_on_order)).collect()

            # Success message
            st.success(f"✅ Your Smoothie is ordered, {name_on_order}!", icon="🥤")

            # Show last 5 orders (optional)
            recent_orders = session.table("smoothies.public.orders").limit(5)
            st.subheader("📝 Recent Orders")
            st.dataframe(recent_orders)

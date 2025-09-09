import streamlit as st


# Title and description
st.title('🥤 Customize Your Smoothie! 🥤')
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake using st.connection

session = cnx.session()

# Query fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(my_dataframe, use_container_width=True)

# Convert dataframe column to list for multiselect options
fruit_options = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

# Multiselect for up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

my_insert_stmt = None

if ingredients_list:
    # Create a space-separated string of chosen fruits
    ingredients_string = ' '.join(ingredients_list)
    st.write('Ingredients chosen:', ingredients_string)

    # Prepare SQL insert statement safely with placeholders
    # Note: Streamlit Snowflake API doesn't support parameterized queries directly
    # So be mindful of SQL injection if inputs come from untrusted sources
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write('SQL statement:')
    st.code(my_insert_stmt)

# Button to submit the order
time_to_insert = st.button('Submit Order')

if time_to_insert:
    if not name_on_order:
        st.error("Please enter a name for your Smoothie before submitting.")
    elif not ingredients_list:
        st.error("Please select at least one ingredient before submitting.")
    else:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered! ✅')
        except Exception as e:
            st.error(f"Error submitting order: {e}")

st.stop()

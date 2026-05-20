# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Create Snowflake session

st.title("🥤 Customize Your Smoothie! 🥤")

# Description text
st.write(
    """
Choose the fruits you want in your custom Smoothie!
"""
)


name_on_order = st.text_input("Name on smoothie: ")
st.write("The name on your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


Ingredients_list = st.multiselect(
    'choose up to 5 ingradients:',
     my_dataframe,
     max_selections = 5
    )

if Ingredients_list:
    ingredients_string = ''

    for fruit_chosen in Ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """' )"""

    st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
    

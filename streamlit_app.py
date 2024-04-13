# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

NAME_ON_ORDER = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', NAME_ON_ORDER)

# from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# --st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,max_selections=5)

# st.write('You selected:', options)
if ingredients_list:
    ingredients_string=''
    # NAME_ON_ORDER=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen +'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon"+ fruit_chosen)
        fv_df= st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    # st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""
            # 

    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
st.success('Your Smoothie is ordered!',icon="✅")




# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col




# Write directly to the app
st.title("Example Streamlit App 2 :crown:")
st.write(
    """Hello, order your own **Smoothie!**
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name of your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ing_list=st.multiselect('Choose up to 5 ing.',my_dataframe,max_selections=5) 

if ing_list:
    ing_string = ''

    for fruit in ing_list:
        ing_string += fruit
        ing_string += ' '

    #st.write(ing_string)

   
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ing_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')

    if time_to_insert:

        session.sql(my_insert_stmt).collect()   
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")



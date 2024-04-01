# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas
st.dataframe = pd_df

ing_list=st.multiselect('Choose up to 5 ing.',my_dataframe,max_selections=5) 

if ing_list:
    ing_string = ''

    for fruit in ing_list:
        ing_string += fruit
        ing_string += ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader = fruit+' nutrition info'
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        #st.text(fruityvice_response)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True) 

    #st.write(ing_string)

   
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ing_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')

    if time_to_insert:

        session.sql(my_insert_stmt).collect()   
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")


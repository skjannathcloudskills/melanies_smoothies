# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)



# option = st.selectbox(
#     "What is your favourate fruit",
#     ("Banana", "Straw berries", "Peaches"),
#     index=None,
#     placeholder="Select contact method...",
# )

# st.write("Your favourate fruit is :", option)




name_on_order = st.text_input("Name on smoothie : ")
st.write("The Name on smoothie will be ", name_on_order)
cnx = st.connection("snowflake")
session=cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list=st.multiselect('Choose upto 5 ingredients :',my_dataframe,
                              max_selections=5)
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)


    ingredients_string=''
    for fruit_chosen in ingredient_list:
        ingredients_string+=fruit_chosen+' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' ,'"""+name_on_order+"""')"""


    # st.write(my_insert_stmt)
    
    time_to_insert=st.button('Submit Order')    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!,' +name_on_order, icon="✅")
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

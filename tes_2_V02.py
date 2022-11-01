import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)
menu=["HOME", "WEATHER", "RECIPES", "MOVIES", "CALCULATOR", "TOP_SITES", "IMAGE_VIEW"]
choice=st.sidebar.selectbox("MENU", menu)

def find_current_weather(city):
    API_KEY_weather = "97ab0b877cfca467f9406ee30e8ae357"
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_weather}&units=metric"
    weather_data = requests.get(base_url).json()
    try:
        general = weather_data['weather'][0]['main']
        icon_id = weather_data['weather'][0]['icon']
        temperature = round(weather_data['main']['temp'])
        humidity = weather_data['main']['humidity']
        icon = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    except KeyError:
        st.error("City Not Found")
        st.stop()
    return general, temperature, humidity, icon


def food_Recipes(maxCalories, minProtein, minCarbs, maxCarbs, maxFat, number):
    url = "https://api.spoonacular.com/recipes/findByNutrients"

    querystring = {"minProtein": minProtein,
                   "minCarbs": minCarbs,
                   "maxCalories": maxCalories,
                   "maxCarbs": maxCarbs,
                   "number": number,
                   "maxFat": maxFat
                   }
    headers = {
        "x-api-key": "fc7125d5cf8945e6bbe8d134d928dcbe",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    recipe = requests.request("GET", url, headers=headers, params=querystring)
    recipe_data = recipe.json()
    for i in range(int(number)):
        title = recipe_data[i]['title']
        image = recipe_data[i]['image']
        calories = recipe_data[i]['calories']
        protein = recipe_data[i]['protein']
        carbs = recipe_data[i]['carbs']
        fat = recipe_data[i]['fat']

    return carbs, title, image, calories, protein, fat


def movies(title):
    API_KEY_MOVIE = "68cbf863"
    url = f"http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY_MOVIE}"

    querystring = {"t": title,
                   }

    movie = requests.request("GET", url, params=querystring)
    movie_data = movie.json()
    Title = movie_data['Title']
    Poster = movie_data['Poster']
    Released = movie_data['Released']
    Genre = movie_data['Genre']
    imdbRating = movie_data['imdbRating']

    return Title, Poster, Released, Genre, imdbRating

def cal_aws(x,y,op):
    url = "https://x367frdk9j.execute-api.eu-central-1.amazonaws.com/add1/add_numbers"

    querystring = {"x": x,
                   "y": y,
                   "op": op
                   }

    response_data = requests.request("GET", url, params=querystring)
    data = response_data.json()
    return data


def main():
    if choice == "HOME":
        st.title("THIS IS TASK 1 FOR CEI_521")
        col1,col2=st.columns(2)
        st.subheader("My name is Rafaellos Leontiou and i have created six applications and deployed them "
                     "through **streamlist** ")
        st.subheader("The applications are :")
        st.text("1. Weather App: Using online server")
        st.text("2. Recipes App: Using online server")
        st.text("3. Movies App: Using online server")
        st.text("4. Calculator App: Using serverless aws lambda functions")
        st.text("5. Top sites App: Using serverless aws lambda functions")
        st.text("6. Weather App: Using serverless aws lambda functions")
        st.caption("****************************************")
        st.caption("YOU CAN HAVE ACCESS TO THESE APPLICATION FROM THE MENU ON THE LEFT SIDE")
        st.caption("****************************************")

    elif choice == 'WEATHER':

        st.title("Find the Weather")
        st.caption("****************************************")
        st.text("This is the application where you can check the weather at limassol at any time")
        st.text("By pressing the button you are sending request to OpenWeatherMap")
        st.caption("The app has as output :")
        st.caption("Temperature")
        st.caption("Humidity")
        st.caption("Icon of the weather")
        st.caption("****************************************")
        #city = st.text_input("The Weather at Limassol at this moment is").lower()
        st.subheader("The Weather at Limassol at this moment is")
        city="limassol"
        if st.button("Show me the weather"):
         general, temperature,humidity, icon = find_current_weather(city)
         st.metric(label="Temperature", value=f"{temperature}°C")
         st.metric(label="humidity", value=f"{humidity}%")
         st.write(general)
         st.image(icon)

    elif choice == 'RECIPES':
        st.title("Nutrients")
        st.caption("****************************************")
        st.text("This is the application where you can check recipes based on the macros requirements")
        st.text("It is optional to fill the field bellow but by filling them you will receive better results")
        st.text("By pressing the button you are sending request to spoonacular")
        st.caption("The app has as output :")
        st.caption("Title")
        st.caption("Icon")
        st.caption("Protein ")
        st.caption("Fats ")
        st.caption("Carbs ")
        st.caption("****************************************")
        maxCalories = st.text_input("maxCalories") or 1000
        minProtein = st.text_input("minProtein") or 0
        minCarbs = st.text_input("Min Carbs") or 0
        maxCarbs = st.text_input("Max Carbs") or 100
        maxFat = st.text_input("maxFat") or 100
        number = st.text_input("number") or 1

        if st.button("Find Recipe"):
            carbs,title,image,calories,protein,fat = food_Recipes(maxCalories,minProtein,minCarbs,maxCarbs,maxFat,number)
            st.metric(label="Title", value=f"{title}")
            st.image(image, channels="RGB", output_format="auto")
            st.metric(label="Calories", value=f"{calories}Kcal")
            st.metric(label="Protein", value=f"{protein}")
            st.metric(label="Fat", value=f"{fat}")
            st.metric(label="Carbs", value=f"{carbs}")

    elif choice == 'MOVIES':
        st.title("Movies")
        st.caption("****************************************")
        st.text("This is the application where you can check movies details")
        st.text("By pressing the button you are sending request to omdb")
        st.caption("The app has as output :")
        st.caption("Title")
        st.caption("Poster")
        st.caption("Released ")
        st.caption("Genre ")
        st.caption("imdbRating ")
        st.caption("****************************************")
        title = st.text_input("title")

        if st.button("Find Movie"):
            Title, Poster, Released, Genre, imdbRating = movies(title)
            st.metric(label="Title", value=f"{Title}")
            st.image(Poster, channels="RGB", output_format="auto")
            st.metric(label="Released", value=f"{Released}")
            st.metric(label="Genre", value=f"{Genre}")
            st.metric(label="imdbRating", value=f"{imdbRating}")

    elif choice == 'CALCULATOR':
        st.title("Calculator")
        st.caption("****************************************")
        st.text("This is a simple calculator")
        st.text("This app was developed using aws lamda serveless functions")
        st.caption("****************************************")
        col1,col2=st.columns((1,2))
        x=0
        y=0
        op=0
        with col1:
            with st.form(key='calc', clear_on_submit=True):
                x=st.text_input("Give first number")
                y=st.text_input("Give second number")
             #op=st.text_input("Give oper")
                if st.checkbox("+"):
                    op="add"
                    op_vis= "+"
                if st.checkbox("-"):
                    op="sub"
                    op_vis = "-"
                if st.checkbox("*"):
                    op="mult"
                    op_vis = "*"
                if st.checkbox("/"):
                    op="div"
                    op_vis = "/"

                if st.form_submit_button("Calculate"):
                    data = cal_aws(x, y, op)
                    #st.text(f"{x} " f"{op_vis} " f"{y}" " = " f"{data}")
                    if type(data) == str:
                        st.metric(label="ANSWER", value=f"{data}")
                    else:
                        st.metric(label="ANSWER", value=f"{data:.2f}")


    elif choice == 'TOP_SITES':
        url = " https://suvv7evrcqmabqgsp7ahpxbny40jkwwf.lambda-url.eu-central-1.on.aws/"
        response_data = requests.request("GET", url)
        data= response_data.json()
        google=data["google"]
        youtube = data["youtube"]
        facebook = data["facebook"]
        twitter = data["twitter"]
        wikipedia = data["wikipedia"]
        instagram = data["instagram"]
        yahoo = data["yahoo"]
        amazon = data["amazon"]
        reddit = data["reddit"]


        st.title("MONTHLY VISIT IN TOP SITES")
        st.caption("****************************************")
        st.text("THIS SECTION IS WHERE YOU CAN SE DETAILS FOR THE TOP VISITED SITES OF THE YEAR")
        st.text("INCLUDING TABLES,CHARTS,VALUES")
        st.caption("*****----THIS APP DOESN'T NEED ANY INTERACTION WITH THE USER----*****")
        st.caption("****************************************")
        col1, col2 = st.columns((2, 5))
        with col1:
            result=pd.DataFrame({
                'SITE': ["google", "youtube", "facebook", "twitter", "wikipedia", "instagram", "yahoo", "amazon", "reddit"],
                'VISITS (Billions)': [google, youtube, facebook, twitter, wikipedia, instagram,
                                        yahoo, amazon, reddit],
        })

            result.index += 1
            pd.options.display.float_format = '{:, .2f}Billions'.format
            st.write(result)
        with col2:
            st.bar_chart(result, x="SITE", y="VISITS (Billions)")
        with col1:
            st.header("AVERAGE-MIN-MAX RESULTS")
            result_total = result["VISITS (Billions)"].describe()
            st.write(result_total)
            result_mean=result["VISITS (Billions)"].mean()
            result_min = result["VISITS (Billions)"].min()
            result_max = result["VISITS (Billions)"].max()


        with col2:
            st.header("")
            st.header("")
            st.header("")
            st.metric(label="AVERAGE", value=f"{result_mean:.2f}")
            st.metric(label="MIN", value=f"{result_min:.2f}")
            st.metric(label="MAX", value=f"{result_max:.2f}")

    elif choice == 'IMAGE_VIEW':
        from PIL import Image
        from io import BytesIO

        url = "https://2d0ji63236.execute-api.eu-central-1.amazonaws.com/v3/pdf2imagebucket?"

        querystring = {
            "file": "CEI521.png"
                }

        response_data = requests.request("GET", url, params=querystring)
        img = Image.open(BytesIO(response_data.content))


        st.title("IMAGE VIEW APP FROM S3 BUCKET")
        st.caption("****************************************")
        st.text("THIS SECTION IS WHERE YOU CAN SEE AN IMAGE THAT IS STORED IN A S3 BUCKET AND THROUGH ")
        st.text("AWS LAMBDA FUNCTION IT IS DIPLAYED HERE")
        st.caption("*****----THIS APP DOESN'T NEED ANY INTERACTION WITH THE USER----*****")
        st.caption("****************************************")


        st.image(img)


if __name__ == '__main__':
    main()



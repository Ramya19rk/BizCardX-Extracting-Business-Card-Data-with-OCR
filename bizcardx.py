import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import mysql.connector
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re

# Streamlit Page Creation

st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR",
                   layout="wide",
                   initial_sidebar_state="expanded"
                  )
st.markdown("<h1 style='text-align: center; color: blue;'>BizCardX: Extracting Business Card Data with OCR</h1>",
            unsafe_allow_html=True)

# Creating Background

def setting_bg():
    st.markdown(f""" <style>.stApp {{
                    background:url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGeZlHZnlm_zGcOLg7yzdK0ELW2WWZ2OUhJw&usqp=CAU");
                    background-size: cover}}
                </style>""", unsafe_allow_html=True)
setting_bg()

# Creating option menu in the side bar

selected = option_menu("Menu", ["Home", "Upload & Extract", "Modify"],
                icons = ["house","cloud-upload","pencil-square"],
                default_index = 0,
                orientation="horizontal",       
                 styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "-2px", "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#6495ED"}})

# INITIALIZING THE EasyOCR READER

reader = easyocr.Reader(['en'])

# MySQL Table Connection

config = {'host' : 'localhost',
              'user' : 'root',
              'password' : 'xxxxx',
              'database' : 'bizcardxs'}

conn = mysql.connector.connect(**config)

cursor = conn.cursor()

create_query = '''CREATE TABLE IF NOT EXISTS card_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    Company_Name VARCHAR(255),
                    Card_Holder_Name VARCHAR(255),
                    Designation VARCHAR(255),
                    Mobile_Number VARCHAR(255),
                    Email_Address VARCHAR(255),
                    Website_url VARCHAR(255),
                    Area VARCHAR(255),
                    City VARCHAR(255),
                    State VARCHAR(255),
                    Pincode VARCHAR(255),
                    Image_Path LONGBLOB
);
'''

cursor.execute(create_query)

conn.commit()

# Home Menu

if selected == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.image("/Users/arul/Downloads/home.jpg")
        st.markdown("## :green[**Technology Used :**] Python,easy OCR, Streamlit, SQL, Pandas")
    with col2:
         st.markdown("## :green[**About :**] BusinessCard OCR App is a streamlined solution for efficiently managing business card information. It seamlessly integrates OCR technology, a user-friendly Streamlit interface, and database storage to offer users a hassle-free experience in organizing and storing business card details.")
         st.markdown(" ")
         st.markdown("## :green[**Technical Details:**]")
         st.markdown("## **Image Processing:** Utilize image processing techniques for enhanced OCR accuracy.")
         st.markdown("## **Scalability:** Designed to handle a growing number of entries efficiently.")

# Upload and Extract Menu

if selected == "Upload & Extract":
    if st.button(":blue[Already stored data]"):
        cursor.execute(
            "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Address,Website_url,Area,City,State,Pincode from card_data")
        updated_df = pd.DataFrame(cursor.fetchall(),
                                  columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                           "Email_Address",
                                           "Website_url", "Area", "City", "State", "Pincode"])
        st.write(updated_df)
    st.subheader(":blue[Upload a Business Card]")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])
    
    if uploaded_card is not None:

        def save_card(uploaded_card):
            # Define the directory path
            uploaded_cards_dir = os.path.join(os.getcwd(), "uploaded_cards")

            # Create the directory if it doesn't exist
            if not os.path.exists(uploaded_cards_dir):
                os.makedirs(uploaded_cards_dir)

            # Save the uploaded card
            with open(os.path.join(uploaded_cards_dir, uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())

        save_card(uploaded_card)

        def image_preview(image, res):
            #print("Contents of res:", res)
            
            for item in res:
                if isinstance(item, tuple) and len(item) >= 3:
                    bbox, text, prob = item[:3]  # Ensure at least three values in the tuple
                    # unpack the bounding box
                    (tl, tr, br, bl) = bbox
                    tl = (int(tl[0]), int(tl[1]))
                    tr = (int(tr[0]), int(tr[1]))
                    br = (int(br[0]), int(br[1]))
                    bl = (int(bl[0]), int(bl[1]))
                    cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                    cv2.putText(image, text, (tl[0], tl[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                #else:
                   # print("Unexpected format for OCR result:", item)

            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)

        # DISPLAYING THE UPLOADED CARD
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))

                # easy OCR
        saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
        result = reader.readtext(saved_img, detail=0, paragraph=False)

        
         # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData


        data = {"Company_Name": [],
                "Card_Holder_Name": [],
                "Designation": [],
                "Mobile_Number": [],
                "Email_Address": [],
                "Website_url": [],
                "Area": [],
                "City": [],
                "State": [],
                "Pincode": [],
                "Image_Path": img_to_binary(saved_img)
                }


        def get_data(res):
            for ind, i in enumerate(res):

                # To get WEBSITE_URL
                if "www " in i.lower() or "www." in i.lower():
                    data["Website_url"].append(i)
                elif "WWW" in i:
                    data["Website_url"] = res[4] + "." + res[5]

                # To get EMAIL ID
                elif "@" in i:
                    data["Email_Address"].append(i)

                # To get MOBILE NUMBER
                elif "-" in i:
                    data["Mobile_Number"].append(i)
                    if len(data["Mobile_Number"]) == 2:
                        data["Mobile_Number"] = " & ".join(data["Mobile_Number"])

                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["Company_Name"].append(i)
                
                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["Card_Holder_Name"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["Designation"].append(i)

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["Area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["Area"].append(i)

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*', i)
                if match1:
                    data["City"].append(match1[0])
                elif match2:
                    data["City"].append(match2[0])
                elif match3:
                    data["City"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["State"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["State"].append(i.split()[-1])
                if len(data["State"]) == 2:
                    data["State"].pop(0)

                # To get PINCODE
                if len(i) >= 6 and i.isdigit():
                    data["Pincode"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["Pincode"].append(i[10:])


        get_data(result)   
        #print(len(res))    
        
        # FUNCTION TO CREATE DATAFRAME
        def create_df(data):
            df = pd.DataFrame(data)
            return df


        df = create_df(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                querry = """INSERT INTO card_data(Company_Name,
                                                Card_Holder_Name,
                                                Designation,
                                                Mobile_Number,
                                                Email_Address,
                                                Website_url,
                                                Area,
                                                City,
                                                State,
                                                Pincode,
                                                Image_Path)
                                                
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                cursor.execute(querry, tuple(row))
                conn.commit()
                st.success("#### Uploaded to database successfully!")

        if st.button(":blue[View updated data]"):
            cursor.execute("select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Address,Website_url,Area,City,State,Pincode from card_data")
            updated_df = pd.DataFrame(cursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                   "Email_Address",
                                                   "Website_url", "Area", "City", "State", "Pincode"])
            st.write(updated_df)
            
# Modify MENU

if selected == "Modify":
    st.subheader(':blue[You can view , Edit or Delete the extracted data in this app]')
    select = option_menu(None,
                         options=["EDIT", "DELETE"],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#6495ED"}})

    if select == "EDIT":
        st.markdown(":blue[Edit the data here]")

        try:
            cursor.execute("SELECT Card_Holder_Name FROM card_data")
            result = cursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.markdown("#### Update or modify any data below")
                cursor.execute(
                "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Address,Website_url,Area,City,State,Pincode FROM card_data WHERE Card_Holder_Name=%s",
                (selected_card,))
                result = cursor.fetchone()

                # DISPLAYING ALL THE INFORMATIONS
                Company_Name = st.text_input("Company_Name", result[0])
                Card_Holder_Name = st.text_input("Card_Holder_Name", result[1])
                Designation = st.text_input("Designation", result[2])
                Mobile_Number = st.text_input("Mobile_Number", result[3])
                Email_Address = st.text_input("Email_Address", result[4])
                Website_url = st.text_input("Website", result[5])
                Area = st.text_input("Area", result[6])
                City = st.text_input("City", result[7])
                State = st.text_input("State", result[8])
                Pincode = st.text_input("Pincode", result[9])


                if st.button(":blue[Commit changes to DB]"):


                   # Update the information for the selected business card in the database
                    cursor.execute("""UPDATE card_data SET Company_Name=%s,
                                                           Card_Holder_Name=%s,
                                                           Designation=%s,
                                                           Mobile_Number=%s,
                                                           Email_Address=%s,
                                                           Website_url=%s,
                                                           Area=%s,
                                                           City=%s,
                                                           State=%s,
                                                           Pincode=%s
                                        WHERE Card_Holder_Name=%s""", (Company_Name, Card_Holder_Name, Designation, Mobile_Number, Email_Address, Website_url, Area, City, State, Pincode,
                    selected_card))
                    conn.commit()
                    st.success("Information updated in database successfully.")

            if st.button(":blue[View updated data]"):
                cursor.execute(
                    "SELECT Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Address,Website_url,Area,City,State,Pincode FROM card_data")
                updated_df = pd.DataFrame(cursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                   "Email_Address",
                                                   "Website_url", "Area", "City", "State", "Pincode"])
                st.write(updated_df)

        except:
            st.warning("There is no data available in the database")

    if select == "DELETE":
        st.subheader(":blue[Delete the data]")
        try:
            cursor.execute("SELECT Card_Holder_Name FROM card_data")
            result = cursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
                st.write("#### Proceed to delete this card?")
                if st.button("Yes Delete Business Card"):
                    cursor.execute(f"DELETE FROM card_data WHERE Card_Holder_Name='{selected_card}'")
                    conn.commit()
                    st.success("Business card information deleted from database.")

            if st.button(":blue[View updated data]"):
                cursor.execute(
                    "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Address,Website_url,Area,City,State,Pincode from card_data")
                updated_df = pd.DataFrame(cursor.fetchall(),
                                            columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                    "Email_Address",
                                                    "Website_url", "Area", "City", "State", "Pincode"])
                st.write(updated_df)

        except:
            st.warning("There is no data available in the database")

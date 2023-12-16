# BizCardX-Extracting-Business-Card-Data-with-OCR

Problem Statement: Develop an OCR-based solution, BizCardX, to efficiently extract and organize business card data, facilitating seamless digital integration and contact management.

NAME : RAMYA KRISHNAN A

BATCH: DW75DW76

DOMAIN : DATA SCIENCE

DEMO VIDEO URL : https://www.linkedin.com/posts/ramyakrishnan19_introducing-bizcardx-transforming-business-activity-7138380957367078913-kwYf?utm_source=share&utm_medium=member_desktop

Linked in URL : www.linkedin.com/in/ramyakrishnan19

# Project Overview

BizCardX streamlines the extraction and organization of business card details, providing a user-friendly interface through Streamlit. The project focuses on leveraging Optical Character Recognition (OCR) technology to extract information from uploaded business card images.

# Technology Stack

•	Streamlit: The web application framework used for creating interactive and data-driven pages.
 
•	OCR Technology: Employing Optical Character Recognition for accurate extraction of text from business card images.
 
•	Database: Storing and managing business card data in a backend database.

# Libraries

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

# Features

# Home

•	Overview of the project and technical details.

•	Insight into the technologies utilized in the development of the Streamlit page.

<img width="1438" alt="Screenshot 2023-12-07 at 9 24 31 AM" src="https://github.com/Ramya19rk/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/145639838/f4f1adeb-f000-4d1a-a1e8-be72071e8cd3">


# Upload and Extract

•	Upload business card images.

•	Display extracted details in a tabular format.

•	View already inserted data.

•	Upload card details to the database for future reference.

<img width="1440" alt="Screenshot 2023-12-07 at 9 24 40 AM" src="https://github.com/Ramya19rk/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/145639838/1f85b170-fd85-4bb6-b3b9-b283c75d15e5">


# Modify

Edit
•	Modify and update existing business card details.

•	Commit changes to the database.

Delete

•	Select a cardholder's name from the dropdown.

•	Confirm deletion by clicking "Yes, delete business card."

•	View updated data in the database.

<img width="1440" alt="Screenshot 2023-12-07 at 9 24 51 AM" src="https://github.com/Ramya19rk/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/145639838/49337e49-80f4-4130-acb9-c47df5e15384">


# Getting Started

Clone the repository.

Install dependencies using pip install -r requirements.txt.

Run the Streamlit app: streamlit run app.p

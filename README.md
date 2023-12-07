# BizCardX-Extracting-Business-Card-Data-with-OCR

Problem Statement: Develop an OCR-based solution, BizCardX, to efficiently extract and organize business card data, facilitating seamless digital integration and contact management.

NAME : RAMYA KRISHNAN A

BATCH: D98

DOMAIN : DATA SCIENCE

DEMO VIDEO URL : 

Linked in URL : www.linkedin.com/in/ramyakrishnan19

# Features

OCR Extraction: Utilizes Optical Character Recognition to extract text data from business card images.

Output Organization: Provides a structured and organized output format for the extracted information.

Image Format Support: Supports various image formats commonly used for business cards.

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


import streamlit as st
from PIL import Image
import base64
from pathlib import Path

headAndCss ='''
	<head>
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
		<meta charset="utf-8" />
		<meta name="description" content="This is a chatbot for Sri Sri Gurudev." />
		<meta name="keywords" content="AOL Sri Sri Gurudev chat QnA" />
	</head>
	<style>
		:root {
			--primary-color: #884EA0;

			--primary-bg: #FFFFFF;
			--secondary-bg: #5E1675;
		}
		.subHead {
			color: var(--primary-color);
			font-size: 20px;
			margin-top: 10px;
			margin-bottom: 2px;
		}
		.title {
			color: #FFE6E6; 
			text-align: center;
			font-size: 50px;
			font-weight: 600;
		}
		.desc {
			color: white;
			text-align: justify;
			font-size: 20px;
		}
		.center _img {
			display: block;
			margin-left: auto;
			margin-right: auto;
			width: 50%;
		}

		[data-testid="stChatInputTextArea"] { 
			color: white; 
			caret-color: white;
		} 
		[data-testid="stChatInputSubmitButton"] { 
			color: white; 
		} 
		.st-emotion-cache-134p1bi > svg {
			color: white;
		}
		[data-testid="baseButton-header"] > svg {
			color: white;
		}
		<!-- User chat -->
		.st-emotion-cache-1c7y2kd {
			display: flex;
			align-items: flex-start;
			gap: 0.5rem;
			padding: 1rem;
			border-radius: 0.5rem;
			background-color: var(--secondary-bg);
		}
	</style>
'''

title ='''
	<div classname='title'>
		Ask Sri Sri
	<div/>
'''
desc ='''
	<div classname='desc'>
		Ask anything! The knowledge from Gurudev's QnA is used to answer. You will be blessed with an answer practically by him.
	<div/>
'''

# Images
def img_to_bytes(img_path):
	img_bytes = Path(img_path).read_bytes()
	encoded = base64.b64encode(img_bytes).decode()
	return encoded
def img_to_html(img_path):
	img_html = "<img src='data:image/png;base64,{}' alt='aol logo' class='center_img'>".format(
		img_to_bytes(img_path)
	)
	return img_html

# st.markdown(img_to_html('streamlit-logo-secondary-colormark-darktext.png'), unsafe_allow_html=True)
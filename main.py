import cv2
import streamlit as st
import numpy as np
from PIL import Image


def color_transfer(source, target):
	source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
	target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

	# compute color statistics for the source and target images
	(lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
	(lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

	# subtract the means from the target image
	(l, a, b) = cv2.split(target)
	l -= lMeanTar
	a -= aMeanTar
	b -= bMeanTar

	# add in the source mean
	l += lMeanSrc
	a += aMeanSrc
	b += bMeanSrc

	# merge the channels together and convert back to the RGB color
	# space, being sure to utilize the 8-bit unsigned integer data
	# type
	transfer = cv2.merge([l, a, b])
	transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

	# return the color transferred image
	return transfer

def image_stats(image):

	# compute the mean and standard deviation of each channel
	(l, a, b) = cv2.split(image)
	(lMean, lStd) = (l.mean(), l.std())
	(aMean, aStd) = (a.mean(), a.std())
	(bMean, bStd) = (b.mean(), b.std())

	# return the color statistics
	return (lMean, lStd, aMean, aStd, bMean, bStd)


def main_loop():

    st.title("COLOR CHANGE CHARM🪄")
    st.text("Color transfer app 📱🧙")

    source_file = st.file_uploader("Upload Source Image", type=['jpg', 'png', 'jpeg'])
    target_file = st.file_uploader("Upload Target Image", type=['jpg', 'png', 'jpeg'])
    if source_file is None:
        return None

    source_image = Image.open(source_file)
    source_image = np.array(source_image)
    target_image = Image.open(target_file)
    target_image = np.array(target_image)

    processed_image = color_transfer(source_image, target_image)

    st.image(processed_image)


if __name__ == '__main__':
    main_loop()






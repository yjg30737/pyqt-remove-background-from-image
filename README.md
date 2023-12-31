# pyqt-remove-background-from-image
Python desktop app example of remove background from image with OpenCV, PyTorch

You need <b>CUDA</b> to run this.

## Requirements
* pillow - to save the image
* opencv-python - to handle the image file as numpy array and apply Gaussian Blur to make border smooth
* torch - to use CUDA
* torchvision - To use deeplab V3 (prominent image segmenation model made by Google)

## How to Run
1. clone this repo.
2. `pip install -r requirements.txt` to download necessary packages
3. python main.py

## After Running
![image](https://github.com/yjg30737/pyqt-remove-background-from-image/assets/55078043/5cbda5a8-31d3-4ca2-acbe-21f32b4fc1de)
1. First find the path which including images you want to remove the background.
- This package has the sample folder to make you get proper images (which is generated by Stable Diffusion) more conviniently.
2. Press "Remove Background and Save!" button. It will make a backup folder and save original images to it and remove the background from the images in folder.

## Result
<img src="https://github.com/yjg30737/pyqt-remove-background-from-image/assets/55078043/6cce690f-391f-45b6-84e5-e3fff0add25e" width="400" height="400">
<img src="https://github.com/yjg30737/pyqt-remove-background-from-image/assets/55078043/47ec52de-1620-4e1c-b88d-89c6b097d5e2" width="400" height="400">


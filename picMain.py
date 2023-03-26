from lobe import ImageModel
from TakePic import takePic

model = ImageModel.load("hoohacksTensorFlow")

# OPTION 1: Predict from an image file
# result = model.predict_from_file('path/to/file.jpg')

# OPTION 2: Predict from an image url
# result = model.predict_from_url('http://url/to/file.jpg')
# OPTION 3: Predict from Pillow image
from PIL import Image

# img = Image.open('dorito.png')
# img = Image.open('can2.jpg')
takePic()

# i = input("type anything:")
img = Image.open("saved_img.png")

result = model.predict(img)

# Print top prediction
print(result.prediction)

# Print all classes
for label, confidence in result.labels:
    print(f"{label}: {confidence*100}%")

# Visualize the heatmap of the prediction on the image 
# this shows where the model was looking to make its prediction.
# heatmap = model.visualize(img)
# heatmap.show()
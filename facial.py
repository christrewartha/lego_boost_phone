import cv2
import numpy as np
from google.cloud import vision_v1p3beta1 as vision

# Initialize the client
client = vision.ImageAnnotatorClient()

# Load the image
image = cv2.imread('path_to_your_image.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert the image to bytes
_, encoded_image = cv2.imencode('.jpg', image)
image_content = vision.types.Image(content=encoded_image.tobytes())

# Detect faces in the image
response = client.face_detection(image_content)
faces = response.face_annotations

# Draw bounding boxes around detected faces
for face in faces:
    box = face.bounding_poly.vertices
    cv2.rectangle(image, (box[0].x, box[0].y), (box[2].x, box[2].y), (255, 0, 0), 2)

# Display the image with bounding boxes
cv2.imshow('Faces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import easyocr
import cv2
from ultralytics import YOLO
import streamlit as st
from PIL import Image


st.title("ANPR on Image")

#st.text('upload your image:')

# Create a file uploader widget
uploaded_file = st.file_uploader("upload your image:", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Read the uploaded image
    image = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(image, caption='Uploaded Image')
    image_rgb = image.convert("RGB")
    image_rgb.save("saved_image.jpg", format="JPEG")
    frame = cv2.imread("saved_image.jpg")
    model = YOLO("../runs/detect/train/weights/best.pt")
    results = model(frame, save=True)
    print(results)
    if not results[0]:

        st.subheader("No plate detected!")
    else:
        trt = False
        while not trt:
            with st.spinner("Processing..."):
                for result in results[0].boxes.data.tolist():
                    reader = easyocr.Reader(['en'], gpu=True)
                    x1, y1, x2, y2, score, _ = result
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cropped_img = frame[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite('test.jpg', cropped_img)
                    image = Image.open('test.jpg')

                    st.image(image, caption='Image Caption')

                    # lp_crop_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

                    easyocr_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                    res = reader.readtext(easyocr_image)
                    if not res:
                        print("Tuple does not have at least two elements.")

                    else:
                        a, b, c = res[0]
                        print(b)

                        st.write("Extracted number is:", str(b))
                        st.write("with confidence score:",str(c))
                        print(c)
                trt = True







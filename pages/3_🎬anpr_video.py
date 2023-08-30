import easyocr
import cv2
from ultralytics import YOLO
import streamlit as st
from utils import update_csv
import tempfile
import os


st.title("ANPR on Video")

# Create a file uploader widget for videos
uploaded_file = st.file_uploader("Upload your video", type=["mp4", "avi"])

if "value_set" not in st.session_state:
        st.session_state.value_set = True

if st.session_state.value_set:

    if uploaded_file is not None:
        st.video(uploaded_file)

        # Create a temporary file to store the uploaded video
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()


        # Create a VideoCapture object using the temporary file's path
        cap = cv2.VideoCapture(temp_file.name)
        if not cap.isOpened():
            st.error("Error: Could not open video.")

        model = YOLO('yolov8n.pt')
        lp_detector = YOLO("runs/detect/train/weights/best.pt")
        reader = easyocr.Reader(['en'], gpu=True)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Define the codec and create a VideoWriter object
        output_path = 'output_video.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        ret = True

        frame_nbr = 0
        with st.spinner("Processing..."):
            while ret:
                    # Read a frame from the camera
                    ret, frame = cap.read()
                    if ret and frame_nbr % 10 == 0:
                        results = model.track(frame, persist=True)
                        for result in results[0].boxes.data.tolist():
                            print(result)

                            x1, y1, x2, y2, id, score, label = result
                            if score > 0.5 and label == 2:
                                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                                text_x = int(x1)
                                text_y = int(y1) - 10
                                cv2.putText(frame, str(id), (text_x, text_y),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                cropped_img = frame[int(y1):int(y2), int(x1):int(x2)]
                                cv2.imwrite('frame.jpg', frame)
                                cv2.imwrite('cropped_image.jpg', cropped_img)
                                plates = lp_detector(cropped_img)
                                for plate in plates[0].boxes.data.tolist():
                                    if score > 0.6:
                                        x1, y1, x2, y2, score, _ = plate
                                        cv2.rectangle(cropped_img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                                        lp_crop = cropped_img[int(y1):int(y2), int(x1):int(x2)]
                                        lp_crop_gray = cv2.cvtColor(lp_crop, cv2.COLOR_BGR2GRAY)

                                        ocr_res = reader.readtext(lp_crop_gray)
                                        if not ocr_res:
                                            print("Tuple does not have at least two elements.")

                                        else:
                                            entry = {'id': id, 'number': ocr_res[0][1], 'score': ocr_res[0][2]}
                                            update_csv(entry)

                            out.write(frame)

                            cv2.imshow('frame', frame)
                    frame_nbr += 1

                    # Break the loop if the 'q' key is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            out.release()

            cap.release()
            cv2.destroyAllWindows()
            st.session_state.value_set=False



if not st.session_state.value_set:

    # Video csv Download
    st.header("Video File Download")
    st.download_button(label="Download CSV", data="output.csv", file_name="output.csv", key="csv")

    # Video File Download Button
    st.header("Video File Download")
    # Add a download button

    video_file = open("output_video.mp4", "rb")
    video_bytes = video_file.read()
    video_file.close()
    st.download_button(
                label="Click to Download",
                data=video_bytes,
                file_name=os.path.basename("output_video.mp4"),
                mime="video/mp4", )




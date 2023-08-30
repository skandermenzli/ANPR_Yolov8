# Automatic number plate recognition with YOLOV8
<img src="https://github.com/skandermenzli/ANPR_Yolov8/blob/main/assets/plates.jpg">
This repository demonstrates using YOLOV8 with easyOCR to create an ANPR streamlit app. It provides an interface where u can either upload an image of car and it will detect the license plate and return it's number.
or you can upload a video and it will track all cars detect license plate and returns new tracking video and a csv file containing the cars ids and their license plate number

## App Pics

<img src="https://github.com/skandermenzli/ANPR_Yolov8/blob/main/assets/img_screen.PNG">



https://github.com/skandermenzli/ANPR_Yolov8/assets/80335572/cfe23ca8-a65b-4077-8277-a01c2d1e6a29



## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/anpr-streamlit-yolo.git
   ```
2. Navigate to the project directory:
```bash
  cd ANPR_Yolov8
   ```
3. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Usage

run streamlit app:
```bash
streamlit run app.py
```

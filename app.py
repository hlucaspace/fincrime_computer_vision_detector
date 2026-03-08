import streamlit as st
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import base64

load_dotenv()

api_key = os.getenv("ROBOFLOW_API_KEY")

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key = api_key
)

st.title ("FinCrime Document Detector")
st.write ("Upload a document to scan for potential fraud indicators")


# Initiate uploading on the page
uploaded_file = st.file_uploader("Choose a document image:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    draw = ImageDraw.Draw(image)
    st.write("Document received. Scanning...")

    with open("temp_img.jpeg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open("temp_img.jpeg", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    result = CLIENT.infer(image_base64, model_id="bank-c0uup/5")


    predictions = result["predictions"]

    expected_fields = [
        "signature",
        "account_number",
        "amount_digits",
        "amount_letter",
        "cheque_number",
        "DateIss",
        "IssueBank",
        "ReceiverName"
    ]



    st.subheader("Scan Results")

    missing_count = 0
    uncertain_count = 0
    detected_count = 0

    for field in expected_fields:
        best_confidence = 0

        for p in predictions:
            if p["class"] == field:
                if p["confidence"] > best_confidence:

                    best_confidence = p["confidence"]
                    x = p["x"]
                    y = p["y"]
                    w = p["width"]
                    h = p["height"]

                    x0 = x - (w/2)
                    y0 = y - (h/2)
                    x1 = x + (w/2)
                    y1 = y + (h/2)


        if best_confidence == 0:
            st.error(f"MISSING: {field} not detected. Flag for review!")
            missing_count += 1
        elif best_confidence >=0.65:
            st.success(f"DETECTED: {field}. Confidence {best_confidence:.0%}")
            detected_count += 1
            draw.rectangle([x0, y0, x1, y1], outline="green", width=3)
            draw.text((x0, y0 - 10), field, fill="green")
        else:
            st.warning (f"UNCLEAR: {field} with low confidence {best_confidence:.0%}")
            uncertain_count += 1
            draw.rectangle([x0, y0, x1, y1], outline="orange", width=3)
            draw.text((x0, y0 - 10), field, fill="black")


    st.subheader("Document Scan Visualisation")
    st.image(image, caption="Detected Fields", use_container_width=True)

    st.subheader("Overall Risk Assessment")

    if missing_count >= 3:
        st.error(f"HIGH RISK: {missing_count} fields missing — recommend rejecting document")
    elif missing_count >= 1 or uncertain_count >= 2:
        st.warning(
            f"MEDIUM RISK: {missing_count} fields missing, {uncertain_count} uncertain — recommend manual review")
    else:
        st.success(f"LOW RISK: Document appears complete — {detected_count} fields verified")

    st.write(f"Inference time: {result['time']:.3f} seconds")
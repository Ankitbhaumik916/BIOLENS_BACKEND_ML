import base64
import grpc
from clarifai_grpc.grpc.api import service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import os
os.environ["CLARIFAI_PAT"] = "41376528601e49738ff0ae42ebf00d86"


# Establish connection with Clarifai API
channel = grpc.insecure_channel("api.clarifai.com")
stub = service_pb2_grpc.V2Stub(channel)

def detect_food(image_path):
    """Detects food items in an image using Clarifai API."""
    try:
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()

        # Convert image to Base64
        base64_img = base64.b64encode(image_bytes).decode("utf-8")

        # Create API request
        request = service_pb2.PostModelOutputsRequest(
            model_id="food-item-recognition",  # Food recognition model
            inputs=[{"data": {"image": {"base64": base64_img}}}]
        )

        # Send request to Clarifai API
        response = stub.PostModelOutputs(request, metadata=(("authorization", f"Key {API_KEY}"),))

        # Process the response
        if response.status.code == status_code_pb2.SUCCESS:
            print("\ Food Items Detected:")
            for concept in response.outputs[0].data.concepts:
                print(f"{concept.name} ({concept.value * 100:.2f}%)")
        else:
            print(" Error:", response.status.description)
    except FileNotFoundError:
        print("Error: The file was not found. Please check the image path.")

# Get image path from the user
image_path = input(" Enter the image path: ").strip()
detect_food(image_path)

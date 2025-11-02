from google import genai
from google.genai import types
import re
import cv2

#Checks if a camera is connected and accessible.Returns if camera is connected, or if it not connected
def func_camera_check():

    try:
        cap = cv2.VideoCapture(0)
    except:
        pass

    try:
        if not cap.isOpened():
            cap.release()
            print("No camera detected or camera is not accessible.")
            return "No camera detected or camera is not accessible."
        else:
            print("Camera detected and accessible!")
            return "Camera detected and accessible!"
            
    except:
        print("Could not connect to camera")
        return "Could not connect to camera"
    
#Takes a pic with the attached camera
def func_camera_pic():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return "Error: Could not open webcam."
    else:
        # Read a single frame from the camera
        ret, frame = cap.read()

        if ret:
            # Save the captured image
            cv2.imwrite("captured_image.jpg", frame)
            # Release the camera
            cap.release()
            cv2.destroyAllWindows()
            print("Image captured successfully as captured_image.jpg")
            return "Image captured successfully as captured_image.jpg"
        else:
            cap.release()
            cv2.destroyAllWindows()    
            print("Error: Could not read frame from webcam.")
            return "User asked to take a pic using the attached cam. But coudl not read frame from webcam."    

 
#Opens the attached camera
def func_camera_open():

    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened. Press 'q' to quit.")

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # If the frame was not read successfully, break the loop
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the captured frame
        cv2.imshow('Webcam Feed', frame)

        # Wait for a key press for 1 millisecond
        # If 'q' is pressed, break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return "Webcam was opened. The user asked to quit. The Webcam was stopped"

#The function takes a picture. Saves it. Then calls LLM with the saved image to identify it
def func_camera_identify():

    ##Check if camera is opern
    try:
        cap = cv2.VideoCapture(0)
    except:
        pass

    try:
        if not cap.isOpened():
            cap.release()
            print("No camera detected or camera is not accessible.")
            return "No camera detected or camera is not accessible."
        else:
            ## Take a pic
            # Read a single frame from the camera
            ret, frame = cap.read()

            if ret:
                # Save the captured image
                cv2.imwrite("captured_image.jpg", frame)
                # Release the camera
                cap.release()
                cv2.destroyAllWindows()
            else:
                cap.release()
                cv2.destroyAllWindows()    
                print("Error: Could not read frame from webcam.")
                return "User asked to take a pic using the attached cam. But coudl not read frame from webcam."              



            ##Identify image
            with open('captured_image.jpg', 'rb') as f:
                image_bytes = f.read()

            
            response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
                ),
                'What is this an image of?'
            ]
            )

            print(response.text)
            return "User asked to identify the object. This was the response " + response.text
            
    except:
        print("Could not connect to camera")
        return "Could not connect to camera"



# A dictionary to map function names (strings) to function objects
function_map = {
    "func_check_camera": func_camera_check,
    "func_pic_camera": func_camera_pic,
    "func_vid_camera": func_camera_open,
    "func_identify_camera": func_camera_identify,  
}

## Use in the System prompt to relate a users question to the name of the funciton
question_json = "{" \
"'Is this computer connected to a camera':'func_check_camera'," \
"'Take a pic using the camera':'func_pic_camera'," \
"'Start the webcam':'func_vid_camera'" \
"'Identify this object:'func_identify_camera'" \
"}"

client = genai.Client(api_key=<enter your API KEY>)
chat = client.chats.create(model="gemini-2.5-flash",
                           config=types.GenerateContentConfig(
                               thinking_config=types.ThinkingConfig(thinking_budget=0),
                               system_instruction="You function as you are supposed to, as an LLM. Check if the user's query matches any of the keys in this json file " + question_json + ". If it does , then output on the value correspoinding to the key. If it does not then replay as you normally would")
                           )


while True:
    print("\n\n---------------------------------------")
    question = input("Ask your question (q to quit):")
    print("\n\n")
    if question == "q":
        break
    result = chat.send_message(question)
    print(result.text)
    pattern = r"\bfunc_\w+"
    if  re.findall(pattern, result.text):
        
        func_name = re.findall(pattern, result.text)
        #print(func_name)
        func = function_map[func_name[0]]
        function_ouput = func()
        if function_ouput:
            result = chat.send_message(function_ouput)
            print(result.text)
    else:
        print(result.text)

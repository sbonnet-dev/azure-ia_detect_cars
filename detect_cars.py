import cv2
import requests

API_KEY = "XXXXXXXXXXXXXXXXXXX"

OBJECT_DETECTION_URL = "https://computer-visio.cognitiveservices.azure.com/vision/v3.0/detect"

video = cv2.VideoCapture("video.mp4")

def draw_boxes(image, objects):
    for object in objects:
        x = object['rectangle']['x']
        y = object['rectangle']['y']
        w = object['rectangle']['w']
        h = object['rectangle']['h']

        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 255), 2)

while True:
    success, image = video.read()

    if not success:
        break

    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

    headers = {'Ocp-Apim-Subscription-Key': API_KEY, 'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Objects'}

    response = requests.post(OBJECT_DETECTION_URL, headers=headers, params=params, data=image_bytes)
    response.raise_for_status()

    analysis = response.json()

    car_count = 0
    for object in analysis['objects']:
        if object['object'] == 'car':
            car_count += 1

    draw_boxes(image, [obj for obj in analysis['objects'] if obj['object'] == 'car'])

    cv2.putText(image, f"Cars: {car_count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Video", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

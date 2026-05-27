import cv2
import mediapipe as mp

mp_face = mp.solutions.face_mesh

face_mesh = mp_face.FaceMesh()

def detect_cheating(frame):

    if frame is None:
        return "Camera not detected"

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "⚠ No face detected"

    if len(results.multi_face_landmarks) > 1:
        return "⚠ Multiple faces detected"

    return "✅ Candidate verified"

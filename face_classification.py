import face_recognition
import cv2
import math
from tqdm import tqdm
from moviepy.editor import *


def fetch_face_recognition_frames(face_image_path, video_path):
    image = face_recognition.load_image_file(face_image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    process = True
    video = cv2.VideoCapture(video_path)
    fps = math.ceil(video.get(cv2.CAP_PROP_FPS))
    frames = []
    frame_count = 0
    i = 1
    pbar = tqdm(total=int(video.get(cv2.CAP_PROP_FRAME_COUNT)))

    while video.isOpened():
        pbar.update(i)
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1
        resize_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
        if process:
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            # face_names = []
            for image_encoding in face_encodings:
                matches = face_recognition.compare_faces([face_encoding], image_encoding)
                # print(matches)
                if True in matches:
                    frames.append(frame_count)
                    # print("foundmatches")

        process = not process

        # cv2.imshow('<ediaPipe Face Detection with WEBCAM', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == 7:
            break
    # print(frames)
    return frames, fps


def get_clip_times(frame_list, fps=24):
    start_index = 0
    clips = []
    for i in range(1, len(frame_list)):
        if frame_list[i] - frame_list[i - 1] > 6:
            sub_clip = (frame_list[start_index] // fps, frame_list[i - 1] // fps + 1)
            clips.append(sub_clip)
            start_index = i
        else:
            continue
    else:
        sub_clip = (frame_list[start_index] // fps, frame_list[len(frame_list) - 1] // fps + 1)
        clips.append(sub_clip)
    return clips


def create_final_edit(original_file_name, clip_times, output_path):
    clips = []
    for clip in clip_times:
        new_clip = VideoFileClip(original_file_name).subclip(clip[0], clip[1])
        clips.append(new_clip)
    final_edit = concatenate_videoclips(clips)
    final_edit.write_videofile(output_path)


def edit_video(video_path, face_image_path):
    filename, extension = os.path.splitext(video_path)
    frames, fps = fetch_face_recognition_frames(face_image_path=face_image_path, video_path=video_path)
    clip_times = get_clip_times(frames, fps)
    # print(clip_times)
    output_path = f'{filename}_final.mp4'
    create_final_edit(video_path, clip_times, output_path)
    return output_path

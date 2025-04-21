import cv2
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np

def timestamp_from_frame(frame_num, fps):
    total_seconds = int(frame_num / fps)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}m{seconds:02d}s"

def ensure_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def delete_previous_screenshots(folder, prefix):
    files = [f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith(".png")]
    for f in files:
        os.remove(os.path.join(folder, f))
    if files:
        print(f"🗑️ Borradas {len(files)} capturas anteriores para: {prefix}")

def extract_screenshots(video_path, output_dir, threshold=0.95):
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Borrar capturas anteriores del mismo video
    delete_previous_screenshots(output_dir, video_name)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    success, prev_frame = cap.read()
    frame_num = 0
    count = 1

    if not success:
        print(f"❌ No se pudo leer el video: {video_path}")
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        score, _ = ssim(prev_gray, gray, full=True)

        if score < threshold:
            timestamp = timestamp_from_frame(frame_num, fps)
            filename = f"{video_name}_{count:03d}_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            print(f"→ Guardado: {filename}")
            prev_gray = gray
            count += 1

        frame_num += 1

    cap.release()
    print(f"📸 Finalizado: {video_name}")

def remove_similar_images(folder, prefix, similarity_threshold=0.98):
    files = sorted([f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith(".png")])
    if not files:
        print(f"⚠️ No hay imágenes para revisar con prefijo {prefix}")
        return

    print(f"🧹 Limpiando capturas similares para: {prefix}")

    prev_img = cv2.imread(os.path.join(folder, files[0]), cv2.IMREAD_GRAYSCALE)
    keep = [files[0]]

    for i in range(1, len(files)):
        curr_path = os.path.join(folder, files[i])
        curr_img = cv2.imread(curr_path, cv2.IMREAD_GRAYSCALE)
        score, _ = ssim(prev_img, curr_img, full=True)

        if score < similarity_threshold:
            keep.append(files[i])
            prev_img = curr_img
        else:
            os.remove(curr_path)
            print(f"🗑️ Eliminada: {files[i]}")

    print(f"✅ Quedaron {len(keep)} capturas para {prefix}")

def main():
    video_dir = "videos"
    output_dir = "screenshots"
    ensure_dirs(video_dir, output_dir)

    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    if not video_files:
        print("❌ No se encontraron videos en la carpeta 'videos'.")
        return

    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        print(f"\n📹 Procesando: {video_file}")
        extract_screenshots(video_path, output_dir)
        prefix = os.path.splitext(video_file)[0]
        remove_similar_images(output_dir, prefix)

if __name__ == "__main__":
    main()
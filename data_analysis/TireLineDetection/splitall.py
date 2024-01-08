import cv2
import glob
import os



CLIPS_DIR="data_analysis/TireLineDetection/data/videos"  #path to the directory with mp4 videos
FRAMES_DIR="data_analysis/TireLineDetection/data/frames"  #path to the directory for frames


if __name__ == "__main__":
    for path in glob.glob(CLIPS_DIR + '/*.mp4'):
        capture = cv2.VideoCapture(path)
        
        vid = path.split('/')[-1].split('.')[0]
        print(vid)
        outDir = os.path.join(FRAMES_DIR, vid)
        os.makedirs(outDir, exist_ok=True)

        frameNr = 0
        success, frame = capture.read()
        while (success):
            cv2.imwrite(os.path.join(outDir, f'{frameNr:05}.png'), frame)
            frameNr = frameNr+1
            success, frame = capture.read()

        capture.release()

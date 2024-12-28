import cv2
import os
import glob
import numpy as np

def extract_and_plot_orb_features(input_dir, output_video, max_features=3000, frame_rate=30):
    """
    Extracts ORB features from a sequence of images and visualizes them, saving the output as a video.

    Args:
        input_dir (str): Directory containing input images.
        output_video (str): Path to save the output video file.
        max_features (int): Maximum number of ORB features to detect.
        frame_rate (int): Frame rate of the output video.
    """
    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=max_features)
    
    # Get list of images sorted by filename
    image_paths = sorted(glob.glob(os.path.join(input_dir, "*.jpg")) + glob.glob(os.path.join(input_dir, "*.png")))
    
    if not image_paths:
        print("No images found in the directory.")
        return
    
    # Read the first image to get dimensions
    first_image = cv2.imread(image_paths[0])
    height, width, layers = first_image.shape

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
    video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    for idx, image_path in enumerate(image_paths):
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error reading image {image_path}. Skipping.")
            continue

        # Convert to grayscale for ORB
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect ORB keypoints
        keypoints = orb.detect(gray, None)
        
        for kp in keypoints:
            kp.size *= 0.05

        # Draw keypoints on the image
        output_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Add frame to the video
        video_writer.write(output_image)

        print(f"Processed frame {idx + 1}/{len(image_paths)}: {image_path}")

    # Release the video writer
    video_writer.release()
    print(f"Video saved to {output_video}")

# Parameters
input_directory = "..\datasets\KITTI_sequence_1\image_l"  # Replace with the path to your image directory
output_video_path = "orb_features_video.mp4"  # Replace with your desired video output path

# Run the script
extract_and_plot_orb_features(input_directory, output_video_path)

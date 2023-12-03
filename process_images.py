import argparse
import os
import subprocess
import pwd

def run_docker_container(batch_id, batch_start, batch_end, pipeline_file, output_dir, image_dir, memory, cellprofiler_version, verbose):
    """
    Run a Docker container for processing a batch of images.

    :param batch_id: ID of the batch.
    :param batch_start: Starting index of the image batch.
    :param batch_end: Ending index of the image batch.
    :param pipeline_file: Path to the CellProfiler pipeline (.cppipe) file.
    :param output_dir: Parent output directory where the analysis results will be saved.
    :param image_dir: Path to the directory containing input images.
    :param memory: Memory requirement for the Docker container.
    :param cellprofiler_version: Version of CellProfiler to use.
    :param verbose: Print verbose information if True.
    """
    batch_output_dir = os.path.join(output_dir, batch_id)
    os.makedirs(batch_output_dir, exist_ok=True)

    # Get the current user's UID and GID
    current_user = pwd.getpwuid(os.getuid())
    uid = current_user.pw_uid
    gid = current_user.pw_gid

    # Construct the Docker container run command with the user's UID and GID and specified CellProfiler version
    cmd = [
        "docker", "run",
        "--name", f"cellprofiler_{batch_id}",
        "--memory", memory,
        "--cpus", "1",
        "--rm",
        "-dit",
        "-v", f"{pipeline_file}:/pipeline.cppipe:ro",
        "-v", f"{batch_output_dir}:/output",
        "-v", f"{image_dir}:/input:ro",
        "-u", f"{uid}:{gid}",
        f"cellprofiler/cellprofiler:{cellprofiler_version}",
        "cellprofiler", "-c", "-r", "-p", "/pipeline.cppipe",
        "-f", str(batch_start),
        "-l", str(batch_end - 1),
        "-o", "/output",
        "-i", "/input",
        "--conserve-memory", "True"
    ]

    if verbose:
        print(" ".join(cmd))

    # Run the Docker container
    subprocess.run(cmd, check=True)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run CellProfiler using Docker containers on batches of images.")
    parser.add_argument("pipeline_file", help="Path to the CellProfiler pipeline (.cppipe) file.")
    parser.add_argument("output_dir", help="Parent output directory where the analysis results will be saved.")
    parser.add_argument("image_dir", help="Path to the directory containing input images.")
    parser.add_argument("--batch-size", type=int, default=32, help="Number of images to process in each batch.")
    parser.add_argument("--num-channels", type=int, default=4, help="Number of channels in the images.")
    parser.add_argument("--memory", default="16G", help="Memory requirement for the Docker container.")
    parser.add_argument("--cellprofiler-version", default="4.2.6", help="Version of CellProfiler to use.")
    parser.add_argument("--verbose", action="store_true", help="Print verbose information.")
    args = parser.parse_args()

    # Convert paths to absolute paths
    pipeline_file = os.path.abspath(args.pipeline_file)
    output_dir = os.path.abspath(args.output_dir)
    image_dir = os.path.abspath(args.image_dir)

    # Verify the pipeline_file is a valid .cppipe file
    _, extension = os.path.splitext(pipeline_file)
    if extension.lower() != ".cppipe":
        raise ValueError("Invalid pipeline file. Please provide a valid CellProfiler pipeline file with .cppipe extension.")

    # Check if the image directory exists
    if not os.path.isdir(image_dir):
        raise FileNotFoundError(f"Image directory '{image_dir}' not found. Please provide a valid image directory.")

    # Create the parent output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    image_list = os.listdir(image_dir)
    total_images = len(image_list) // args.num_channels + 1

    print(f"Total images found: {total_images}")

    # Process images in batches using Docker containers
    for i in range(0, total_images, args.batch_size):
        batch_start = i
        batch_end = min(i + args.batch_size, total_images)
        batch_id = str(i // args.batch_size + 1).zfill(3)

        # Run the current batch as a Docker container
        run_docker_container(
            batch_id, batch_start, batch_end, pipeline_file, output_dir, image_dir,
            args.memory, args.cellprofiler_version, args.verbose
        )

        if args.verbose:
            print(f"Container cellprofiler_{batch_id} started.")

    print("Docker containers started for image processing.")

if __name__ == "__main__":
    main()

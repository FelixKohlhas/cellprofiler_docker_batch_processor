# CellProfiler Docker Batch Processor

This script facilitates the processing of image batches using CellProfiler within Docker containers. It is particularly useful for parallelizing the analysis of large image datasets. The script divides the image dataset into batches, runs CellProfiler in Docker containers for each batch, and saves the analysis results in a specified output directory.

## Prerequisites

- [Docker](https://www.docker.com/) installed and running.
- CellProfiler Docker image. The script uses the official `cellprofiler/cellprofiler` Docker image. You can customize the CellProfiler version by providing the appropriate `--cellprofiler-version` argument.

## Usage

```bash
python process_images.py <pipeline_file> <output_dir> <image_dir> [--options]
```

### Arguments

- `pipeline_file`: Path to the CellProfiler pipeline (.cppipe) file.
- `output_dir`: Parent output directory where the analysis results will be saved.
- `image_dir`: Path to the directory containing input images.

### Options

- `--batch-size`: Number of images to process in each batch (default: 32).
- `--num-channels`: Number of channels in the images (default: 4).
- `--memory`: Memory requirement for the Docker container (default: "16G").
- `--cellprofiler-version`: Version of CellProfiler to use (default: "4.2.6").
- `--verbose`: Print verbose information.

### Example

#### Process images
```bash
python process_images.py /path/to/pipeline.cppipe /path/to/output /path/to/images --batch-size 64 --num-channels 3 --memory 8G --cellprofiler-version 4.3.0 --verbose
```

#### Merge output
```sh
python merge_output.py output/* merged/
```

## Notes

- The script automatically verifies the validity of the provided CellProfiler pipeline file and the existence of the image directory.
- Each batch is processed in a separate Docker container, allowing for parallel execution.
- The results for each batch are saved in individual directories within the specified output directory.

**Note:** Ensure that the user running the script has the necessary permissions to interact with Docker and access the provided directories.

Feel free to customize the script and Docker command parameters based on your specific requirements.
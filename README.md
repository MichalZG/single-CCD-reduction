![superredukcjabratku](https://github.com/janandrzejewski/single-CCD-reduction/assets/67760124/4857955a-ba36-4a31-92ac-9ba2dcdd8773)
# Single-CCD-Reduction
Single-CCD-Reduction script is designed for reducing a single astronomical image from the command line. 
It performs essential preprocessing steps such as bias, dark, and flat-field corrections

## Requirements

- Python 3.10.8+
- Ccdproc 2.3.2+
- Astropy 5.2+

## Installation

1. Ensure that you have Python 3.10.8 or a later version installed.

2. Install the required packages by running the following commands in your terminal or command prompt:

   ```bash
   pip install ccdproc>=2.3.2
   pip install astropy>=5.2



## Usage
To start use:
```commandline
python app.py -d /path/to/ccd_image_file -md /path/to/master_dark_frame -mb /path/to/master_bias_frame -mf /path/to/master_flat_frame
```
| Argument | Required | Description |
| ---- | ---- | ---------------------------- |
| -d, --dir  | Yes  | Path to the CCD image file to be processed    |
| -md, --master_dark  | No  | Path to the Master dark frame file  |
| -mb, --master_bias | No  | Path to the Master bias frame file  |
| -mf, --master_flat  | No   |  Path to the Master flat frame file.      |

### Output
The processed CCD image file will be saved with the suffix "_out" in the `pipeline_out` folder within the same directory as the input file.


## Development

Imports are organized with `isort`.

Code is formatted with `black`.

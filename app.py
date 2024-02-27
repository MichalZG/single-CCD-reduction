import argparse
import logging
import os
from datetime import datetime

import ccdproc as ccdp
import numpy as np
from astropy import units as u
from astropy.io import fits
from astropy.nddata import CCDData
from astropy.stats import mad_std

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger()


def log(message, *args):
    now = datetime.now()
    formatted_time = now.strftime("[%Y-%m-%dT%H:%M:%S.%f]")
    logging.info("%s  " + message, formatted_time, *args)


def astro_reduction(args):
    ccd_file = CCDData(
                fits.getdata(args.dir), meta=fits.getheader(args.dir), unit="adu"
            )
    m_bias = CCDData(
        fits.getdata(args.master_bias),
        meta=fits.getheader(args.master_bias),
        unit="adu",
    )
    m_flat = CCDData(
        fits.getdata(args.master_flat),
        meta=fits.getheader(args.master_flat),
        unit="adu",
    )
    m_dark = CCDData(
        fits.getdata(args.master_dark),
        meta=fits.getheader(args.master_dark),
        unit="adu",
    )
    bias_subtracted = ccdp.subtract_bias(ccd_file, m_bias)

    dark_subtracted = ccdp.subtract_dark(
                    bias_subtracted,
                    m_dark,
                    exposure_time="EXPTIME",
                    exposure_unit=u.adu,
                    scale=True,
                )
    ccd_file = ccdp.flat_correct(
                    dark_subtracted, m_flat, min_value=0.01
                )
    ccd_file.meta["HISTORY"] = "Bias corrected"
    ccd_file.meta["HISTORY"] = "Dark corrected"
    ccd_file.meta["HISTORY"] = "Flat corrected"
    ccd_file.data = np.rint(ccd_file) #round values to nearest integer
    ccd_file.data = ccd_file.data.astype(np.uint16)
    file_name = os.path.splitext(os.path.basename(args.dir))[0]
    directory = os.path.dirname(args.dir)
    new_path = os.path.join(directory, "pipeline_out", f"{file_name}_out.fits")
    os.makedirs(os.path.join(directory, "pipeline_out"), exist_ok=True)
    ccd_file.write(new_path, overwrite=True)
    


def parse_args():
    parser = argparse.ArgumentParser(description="Reduce astro images")
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        help="directory containing FITS images or a PHOT filepath",
        required=True,
    )
    parser.add_argument(
        "-md",
        "--master_dark",
        type=str,
        default="master_dark.fits",
        help="The Master dark",
    )
    parser.add_argument(
        "-mb",
        "--master_bias",
        type=str,
        default="master_bias.fits",
        help="The Master bias",
    )
    parser.add_argument(
        "-mf",
        "--master_flat",
        type=str,
        default=None,
        help="The master flat",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    astro_reduction(args)


if __name__ == "__main__":
    main()

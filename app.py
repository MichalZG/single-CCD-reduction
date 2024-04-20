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



def open_master_bias(master_bias_path):
    m_bias = CCDData(
        fits.getdata(master_bias_path),
        meta=fits.getheader(master_bias_path),
        unit="adu",
    )
    return m_bias

def open_master_dark(master_dark_path):
    m_dark = CCDData(
        fits.getdata(master_dark_path),
        meta=fits.getheader(master_dark_path),
        unit="adu",
    )
    return m_dark

def open_master_flat(master_flat_path):
    m_flat = CCDData(
        fits.getdata(master_flat_path),
        meta=fits.getheader(master_flat_path),
        unit="adu",
    )
    return m_flat


def astro_reduction(im_dir, m_dark, m_bias, m_flat):
    ccd_file = CCDData(
                fits.getdata(im_dir), meta=fits.getheader(im_dir), unit="adu"
            )

    if m_bias is not None:
        ccd_file = ccdp.subtract_bias(ccd_file, m_bias)
        ccd_file.meta["HISTORY"] = "Bias corrected"

    if m_dark is not None:
        ccd_file = ccdp.subtract_dark(
                        ccd_file,
                        m_dark,
                        exposure_time="EXPTIME",
                        exposure_unit=u.adu,
                        scale=True,
                    )
        ccd_file.meta["HISTORY"] = "Dark corrected"

    if m_flat is not None:
        ccd_file = ccdp.flat_correct(
                        ccd_file, m_flat, min_value=0.01
                    )
        ccd_file.meta["HISTORY"] = "Flat corrected"

    ccd_file.data = np.rint(ccd_file.data)
    ccd_file.data = ccd_file.data.astype(np.uint16)

    file_name = os.path.splitext(os.path.basename(im_dir))[0]
    directory = os.path.dirname(im_dir)
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
    m_bias = open_master_bias(args.master_bias)
    m_dark = open_master_dark(args.master_dark)
    m_flat = open_master_flat(args.master_flat)

    astro_reduction(args.dir, m_dark, m_bias, m_flat)


if __name__ == "__main__":
    main()

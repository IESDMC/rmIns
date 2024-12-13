# This program is provided by the IESDMC team.
# usage: python rmIns_for_sac_mseed.py <path to SAC or MiniSEED file> <path to StationXML file>
# author: hjc
# 2024-11-22 ver. 1.0

import os
import sys
import numpy as np
from obspy import read, read_inventory


def detect_format(filepath):
    """
    Detect the data format.

    :param filepath: Path to the seismic data file.
    :return: Tuple containing the format of the data ("MSEED" or "SAC")
             and the encoding type if applicable.
    """
    try:
    # Read the file to get the format
        st = read(filepath, headonly=True)
        data_format = st[0].stats._format.upper()

        encoding = None
        if data_format == "MSEED":
            # Get the encoding for MiniSEED
            encoding = st[0].stats.mseed.encoding
        elif data_format == "SAC":
            encoding = None  # SAC does not have an encoding attribute

        return data_format, encoding
    except Exception as e:
        raise ValueError(f"Error determining file format: {e}")


def remove_instrument_response(input_data_path, xml_path, output_units):
    """
    Remove the instrument response.
    Processed files will be saved in the same format as the input.

    :param input_data_path: Path to the input data file (SAC or MiniSEED).
    :param xml_path: Path to the instrument response StationXML file.
    """
    # Detect the input file format
    input_format, input_encoding = detect_format(input_data_path)

    # Load seismic data
    print(f"Loading seismic data: {input_data_path}")
    st = read(input_data_path)

    # Load the full inventory (StationXML)
    print(f"Loading full inventory: {xml_path}")
    full_inventory = read_inventory(xml_path)

    # Ensure output directory exists
    output_folder = "./Output/"
    #os.makedirs(output_folder, exist_ok=True)

    # Process each trace in the stream
    for tr in st:
        network = tr.stats.network
        station = tr.stats.station
        location = tr.stats.location
        channel = tr.stats.channel

        # Select the relevant part of the inventory
        print(f"Selecting inventory for station: {station}, channel: {channel}")
        try:
            selected_inventory = full_inventory.select(
                network=network, station=station, location=location, channel=channel
            )
        except Exception as e:
            print(f"Error selecting inventory for trace {tr.id}: {e}. Skipping.")
            continue

        # Remove the instrument response
        try:
            print(f"Removing instrument response for trace {tr.id}")
            tr.remove_response(inventory=selected_inventory, output=output_units, pre_filt=None)
            
            # Ensure data type compatibility for MiniSEED
            if input_format == "MSEED":
                print(tr.data.dtype)
                # Determine appropriate encoding based on dtype
                if tr.data.dtype == np.int16:
                    encoding = "INT16"
                elif tr.data.dtype == np.int32:
                # Use STEIM2 for integer data (compressed format)
                    encoding = "STEIM2"
                elif tr.data.dtype == np.float32:
                    encoding = "FLOAT32"
                elif tr.data.dtype == np.float64:
                # FLOAT64 is not supported in MiniSEED; must downcast
                    print(f"Warning: Converting FLOAT64 to FLOAT32 for trace {tr.id}")
                    tr.data = tr.data.astype(np.float32)
                    encoding = "FLOAT32"
                else:
                    raise ValueError(f"Unsupported data type {tr.data.dtype} for MiniSEED")

                # Set the encoding for writing
                tr.stats.mseed.encoding = encoding
                print(f"Encoding set for trace {tr.id}: {encoding}")

                tr.write(os.path.join('./Output/', f"{station}.{channel}_rmIns_{output_units}.mseed"),
                         format=input_format)
            else:
                tr.write(os.path.join(output_folder, f"{station}.{channel}_rmIns_{output_units}.sac"),
                         format=input_format)
            print(f"Processed file saved: {station}_{channel}_rmIns.{input_format.lower()}")

        except Exception as e:
            print(f"Error removing instrument response for trace {tr.id}: {e}. Skipping.")
            continue


if __name__ == "__main__":
    # input param check
    try:
        if len(sys.argv) != 4:
            print("Usage: python script.py <path to SAC or MSEED> <path to StationXML file> <output unit>\nNote: output unit must be one of ACC VEL DISP")
            sys.exit(1)

        # input param check
        input_data_path = sys.argv[1]
        xml_path = sys.argv[2]
        output_units = sys.argv[3].upper()

        if output_units not in ['ACC', 'VEL', 'DISP']:
            raise FileNotFoundError(f"Error: output unit is wrong, please check the input parameter.")
        if not os.path.isfile(input_data_path):
            raise FileNotFoundError(f"Error: can't found the input data file: '{input_data_path}', please ensure the input data file.")

        if not os.path.isfile(xml_path):
            raise FileNotFoundError(f"Error: can't found the xml file:'{xml_path}', please ensure the xml path.")
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    print('st rmIns')
    try:
        remove_instrument_response(input_data_path, xml_path, output_units)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)



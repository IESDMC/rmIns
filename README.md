# README.md

## rmIns_for_sac_mseed_with_yaml.py

### Required Environment:
- Python 3.6+

### Required Modules:
- [ObsPy](https://docs.obspy.org/)
- [PyYAML](https://pypi.org/project/PyYAML/)

### Author:
HJC  
IESDMC  
Version: 1.0  
Date: 2024-12-11

### Functionality:
Removes the instrument response from seismic waveform data and outputs the corrected waveform file.

### Usage:
```bash
python rmIns_for_sac_mseed_with_yaml.py
```
**Example:**  
```bash
python rmIns_for_sac_mseed_with_yaml.py
```

### Notes:
1. No parameters are required for execution; users only need to modify the `rmIns_config.yaml` configuration file.
2. Both `rmIns_config.yaml` and `rmIns_for_sac_mseed_with_yaml.py` must be placed in the same directory.
3. The instrument response file must be in XML format ([details here](https://www.fdsn.org/xml/station/)).
4. Using individual station instrument response files can speed up processing. Refer to the documentation for `README-split_xml_station.py` for details on obtaining instrument response files.

### Example YAML File:
```yaml
# Configuration file for rmIns_for_sac_mseed_with_yaml.py
# Pay attention to the path format for different operating systems (Windows: '\', Linux: '/')
RmIns_config:
    input_data: './SAC/2024.055.04.36.08.0000.TW.ALS.10.EHZ.D.SAC'  # Path to the seismic waveform file
    xml: './xml/ALS.xml'  # Path to the instrument response file
    output_units: 'VEL'  # Output unit after instrument response removal (must be one of [ACC, VEL, DISP], representing acceleration, velocity, and displacement in meters)
    output_format: 'MSEED'  # Output file format (must be one of [MSEED, SAC, DEFAULT]; DEFAULT retains the input file format)
    output_folder: './'  # Path for output files; ensure the folder exists and the path is correct
```

---

## rmIns_for_sac_mseed.py

### Required Environment:
- Python 3.6+

### Required Modules:
- [ObsPy](https://docs.obspy.org/)

### Author:
HJC  
IESDMC  
Version: 1.0  
Date: 2024-12-11

### Functionality:
Removes the instrument response from seismic waveform data and outputs the waveform file in the same format as the input.

### Usage:
```bash
python rmIns_for_sac_mseed.py <seismic_data_file_path> <instrument_response_file_path> <output_physical_quantity>
```
**Example:**  
```bash
python rmIns_for_sac_mseed.py evt.mseed station.xml VEL
```

### Notes:
1. Parameters within `< >` are mandatory.
2. The output physical quantity must be one of [ACC, VEL, DISP], representing acceleration, velocity, and displacement in meters.
3. The instrument response file must be in XML format ([details here](https://www.fdsn.org/xml/station/)).
4. Using individual station instrument response files can speed up processing. Refer to the documentation for `README-split_xml_station.py` for details on obtaining instrument response files.

---

## split_xml_station.py

### Required Environment:
- Python 3.6+

### Required Modules:
- [ObsPy](https://docs.obspy.org/)

### Author:
HJC  
IESDMC  
Version: 1.0  
Date: 2024-12-11

### Functionality:
Splits an instrument response file into individual station response files and saves them in a newly created `xml` directory.

### Usage:
```bash
python split_xml_station.py <stationXML>
```
**Example:**  
```bash
python split_xml_station.py stationXML
```

### Notes:
1. Both `stationXML` and `split_xml_station.py` must be placed in the same directory.
2. The instrument response file must be in XML format ([details here](https://www.fdsn.org/xml/station/)).
3. The individual station instrument response files will be stored in a newly created `xml` directory. Ensure that the directory name does not conflict with existing folders. Users do not need to create the directory; the script will handle this automatically.

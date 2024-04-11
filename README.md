# Dataset dump

This folder contains a dataset dump of the test bench data of the KNF pump FR30. The files contain

 - **X.pkl**: Contains measurement data, split into 1s unshuffled windows at a sampling rate of 10kHz. The data is stored as a 3D numpy array with the shape (n_windows, n_features, window_size). The semantics of the sensors can be found in the yaml below, where the order of sensors corresponds to the indices of the numpy array.
 - **y.pkl**: Contains a binary label describing weather the measurement window does contain a defect (1) or not (0), according to the judgement multiple experts. The label is stored as a 1D numpy array with the shape (n_windows,).
 - **meta.pkl**: Contains additional metadata about the measurement windows. The metadata is stored as a list of dictionaries, where each dictionary contains the metadata for one measurement window.


## Dataset Parameters:

To generate this dump, the following parameters where used:

```yaml
dataset:
  name: sliced
  window_size: 100_000
  window_stride: 10 # make 10kHz data
  hop_size: 50_000
  seed: 123
  path: FR30_0_Serie_lifetime_tests_data_split_100kHz_v4
  index_mapping: device_id
  training_condition:
    key: device_infos/defect 1
    values: [
        "valve torn",
        "diaphragm",
        "leakage",
        "bearing",
        "brushes",
        #"motor mounting", only used for testing
      ]
  columns:
    [
      Beschleunigung_Horizontal_58,
      Beschleunigung_Vertikal_60,
      CAN_Flow,
      Druck_DS_P2,
      Druck_SS_P1,
      Strom,
    ]
  meta_columns:
    - time
  scaler_type: none
  scaler_num_samples: 10000
  num_workers: 20
  label:
    name: avg_expert_ttf
    expert_columns:
      - "device_infos/defectstart cs"
      - "device_infos/defectstart st"
      - "device_infos/defectstart ls"
    per_time_step: false
  feature_extractor:
    name: raw
  flatten: false
  meta_filter:
    "device_infos/defect 1":
      [
        "valve torn",
        "diaphragm",
        "leakage",
        "bearing",
        "brushes",
        #"motor mounting",
      ]
  meta_mapping:
    "device_infos/defect 1":
      "valve ss torn": "valve torn"
      "valve torn": "valve torn"
      "diaphragm torn": "diaphragm"
      "diaphragm": "diaphragm"
      "leakage": "leakage"
      "lose water": "leakage"
      "bearing b blocked": "bearing"
      "bearing b": "bearing"
      "bearing a": "bearing"
      "brushes blocked": "brushes"
      "brushes": "brushes"
      "motor mounting": "motor mounting"
```
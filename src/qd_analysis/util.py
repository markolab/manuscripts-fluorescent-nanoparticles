import numpy as np
import pandas as pd
import os


def load_example_frames(
    base_dir,
    bground_dir="_bground",
    frame_range=range(2000, 2500),
    segmentation_dir="_segmentation_tau-0-pretrain",
    bground_subtract_fluorescence=True,
    load_cameras=None,
    load_dct={},
): 
    from markovids.vid.io import read_frames_multicam
    import h5py
    import warnings
    import cv2
    import glob

    if load_cameras is not None:
        cam_names = load_cameras
    else:
        cam_names = sorted(glob.glob(os.path.join(base_dir, "*-fluorescence.avi")))
        cam_names = [
            os.path.basename(
                os.path.splitext(_cam_name.replace("-fluorescence", ""))[0]
            )
            for _cam_name in cam_names
        ]
    fluorescence_fnames = {
        _cam_name: os.path.join(base_dir, f"{_cam_name}-fluorescence.avi")
        for _cam_name in cam_names
    }
    reflectance_fnames = {
        _cam_name: os.path.join(base_dir, f"{_cam_name}-reflectance.avi")
        for _cam_name in cam_names
    }
    fluorescence_dct = {v: k for k, v in fluorescence_fnames.items()}
    reflectance_dct = {v: k for k, v in reflectance_fnames.items()}

    # load_dct= {}
    fluorescence_timestamps = pd.read_csv(
        os.path.join(base_dir, "timestamps-fluorescence.txt"), sep="\s+"
    )  # note that we're already aligned by frame idx now...
    read_frames = {
        _cam: np.array(list(frame_range)).astype("int32") for _cam in cam_names
    }

    with warnings.catch_warnings():
        # warnings.simplefilter("ignore", UserWarning)
        # not that we're not undistorting here...
        fluorescence_raw_frames = read_frames_multicam(
            fluorescence_dct, read_frames
        )
        use_frames_reflectance = read_frames_multicam(
            reflectance_dct, read_frames
        )

    use_masks = {}
    for _cam in cam_names:
        segmentation_path = os.path.join(
            base_dir, segmentation_dir, f"{_cam}-reflectance.hdf5"
        )
        with h5py.File(segmentation_path) as f:
            use_masks[_cam] = f["labels"][frame_range]
            # use_masks[_cam] = use_masks[_cam]

    if bground_subtract_fluorescence:
        bgrounds = {}
        for _cam, _fname in fluorescence_fnames.items():
            use_fname = os.path.splitext(os.path.basename(_fname))[0]
            bground_path = os.path.join(base_dir, bground_dir, f"{use_fname}.hdf5")
            with h5py.File(bground_path, "r") as f:
                rolling_bgrounds = f["bground"][()]
                idxs = f["frame_idxs"][()]
            bgrounds[_cam] = {}
            bgrounds[_cam]["bground"] = rolling_bgrounds
            bgrounds[_cam]["idxs"] = idxs

        use_frames_fluo = {}
        for _cam, _frames in fluorescence_raw_frames.items():
            bground_sub = np.zeros(_frames.shape, dtype="int16")
            for i, (_idx, _frame) in enumerate(zip(frame_range, _frames)):
                use_bground = np.argmin(np.abs(bgrounds[_cam]["idxs"] - _idx))
                bground_sub[i] = np.clip(
                    _frame - bgrounds[_cam]["bground"][use_bground], 0, 255
                )
            use_frames_fluo[_cam] = bground_sub.astype("uint8")
    else:
        use_frames_fluo = fluorescence_raw_frames
        for _cam, _frames in use_frames_fluo.items():
            use_frames_fluo[_cam] = _frames.astype("uint8")
        bgrounds = None

    for _cam, _params in load_dct.items():
        if _cam not in load_cameras:
            continue
        for i in range(len(use_frames_fluo[_cam])):
            use_frames_fluo[_cam][i] = cv2.undistort(
                use_frames_fluo[_cam][i],
                _params["intrinsic_matrix"],
                _params["distortion_coeffs"],
            )
        for i in range(len(use_frames_reflectance[_cam])):
            use_frames_reflectance[_cam][i] = cv2.undistort(
                use_frames_reflectance[_cam][i],
                _params["intrinsic_matrix"],
                _params["distortion_coeffs"],
            )
        for i in range(len(use_masks[_cam])):
            use_masks[_cam][i] = cv2.undistort(
                use_masks[_cam][i],
                _params["intrinsic_matrix"],
                _params["distortion_coeffs"],
            )
        if bgrounds is not None:
            for i in range(len(bgrounds[_cam]["bground"])):
                bgrounds[_cam]["bground"][i] = cv2.undistort(
                    bgrounds[_cam]["bground"][i],
                    _params["intrinsic_matrix"],
                    _params["distortion_coeffs"],
                )

    return (
        use_frames_fluo,
        use_frames_reflectance,
        use_masks,
        fluorescence_timestamps,
        bgrounds,
    )



def clean_df(
    df,
    exp_types={},
    subject_typos={},
    regexs_hours=["(\d+)h", "(\d+) hrs", "(\d+) hr", "(\d+) post"],
    regexs_days=["(\d+) days"],
    chk_fields=["notes", "session"],
    exclude_subjects=[],
    exclude_dates=[],
):

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["base_filename"] = df["filename"].apply(os.path.basename)
    df["camera"] = df["base_filename"].str.extract(r"(Basler-[\d|A-Z]+-[\d|A-Z]+)\-")
    df["subject"] = df["subject"].str.lower()

    for k, v in subject_typos.items():
        df["subject"] = df["subject"].replace(k, v)
    df["hours"] = np.nan
    for _regex_hours in regexs_hours:
        for _field in chk_fields:
            session_hours = (
                df.loc[df["hours"].isnull()][_field]
                .str.extract(_regex_hours)
                .astype("float")
            )
            df.loc[session_hours.index, "hours"] = session_hours.values

    for _regex_days in regexs_days:
        for _field in chk_fields:
            session_hours = (
                df.loc[df["hours"].isnull()][_field]
                .str.extract(_regex_days)
                .astype("float")
                * 24
            )
            df.loc[session_hours.index, "hours"] = session_hours.values

    # in case it's in session notes
    # session_hours = df.loc[df["hours"].isnull()]["session"].str.extract("(\d+) hr").astype("float")
    # df.loc[session_hours.index,"hours"] = session_hours.values
    df.loc[df["subject"].str.contains("vehicle|blank"), "hours"] = 0.0  # previously nan
    df["exp_type"] = "null"
    for k, v in exp_types.items():
        df.loc[df["subject"].str.contains(k), "exp_type"] = v
    df.loc[df["filename"].str.contains("timecourse_02"), "exp_type"] = df.loc[df["filename"].str.contains("timecourse_02"), "exp_type"].apply(lambda x: x + "_v2")
    df.loc[df["filename"].str.contains("timecourse_03"), "exp_type"] = df.loc[df["filename"].str.contains("timecourse_03"), "exp_type"].apply(lambda x: x + "_v2")
    df["days"] = np.round(df["hours"] / 24)
    df = df.loc[~df["subject"].isin(exclude_subjects)].copy()
    for _exclude_date in exclude_dates:
        dt = pd.to_datetime(_exclude_date)
        df = df.loc[df["start_time"].dt.floor("d") != dt].copy()
    return df
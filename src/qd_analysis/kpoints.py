import numpy as np

def get_pairwise_l2(df, x_key="x", y_key="y"):
    from scipy.spatial.distance import pdist
    if len(df) > 1:
        matrix = df[[x_key,y_key]].values
        distances = pdist(matrix)
        return np.max(distances)
    else:
        return np.nan

def get_pairwise_qd_l2(df, x_key="x", y_key="y"):
    xa = df.loc[df["labeler"] != "qd"].dropna()
    xb = df.loc[df["labeler"] == "qd"].dropna()
    results = {} 
    if (len(xa) > 0) and (len(xb) > 0):
        for i in range(len(xa)):
            # we should only have one point for labeler...
            labeler = xa["labeler"].iat[i]
            pt = xa.iloc[i][[x_key,y_key]].values
            pt2 = xb[[x_key,y_key]].values
            results[labeler] = pt - pt2
        return results
    else:
        return None
        # return [np.nan, np.nan]
from typing import List, Optional, Tuple
import numpy as np

__VALID_LIAD_MODE__ = ["forward"]  # ["forward", "central", "spline"]
__VALID_MAX_MODE__ = ["naive", "lehmer"]
__VALID_PTP_MODE__ = ["naive", "interdecile"]
__VALID_REDUCE_MODE__ = ["all", "attribute", "sample", "none"]

def _validate_za_shape(
    z: np.ndarray,
    a: np.ndarray,
    reg_dim: Optional[List] = None,
    min_size: int = None
) -> Tuple[np.ndarray, np.ndarray, List]:

    assert 2 <= a.ndim <= 3
    assert 2 <= z.ndim <= 3

    if a.ndim == 2:
        a = a[:, None, :]
    
    if z.ndim == 2:
        z = z[:, None, :]
        
    n_samples_a, n_attr, n_interp_a = a.shape
    n_samples_z, n_features, n_interp_z = z.shape
    
    assert n_samples_a == n_samples_z
    assert n_interp_a == n_interp_z
        
    if reg_dim is not None:
        n_attr = a.shape[-1]
        n_features = z.shape[-1]
        assert len(reg_dim) == n_attr
        assert min(reg_dim) >= 0
        assert max(reg_dim) < n_features
        
        z = z[:, reg_dim, :]
    else:
        assert n_attr <= n_features
        if n_attr != n_features:
            z = z[:, :n_attr, :]
        
    if min_size is not None:
        assert n_interp_a >= min_size

    return z, a


def finite_diff(z: np.ndarray, a: np.ndarray, order: int = 1, mode: str = "forward", return_list: bool = False):

    rets = []
    
    for _ in range(order):
        if mode == "forward":
            da = np.diff(a, n=1, axis=-1)
            dz = np.diff(z, n=1, axis=-1)

            a = da / dz
            z = 0.5(z[..., :-1] + z[..., 1:])
            
            rets.append((a, z))
        else:
            raise NotImplementedError

    if return_list:
        return rets
    else:
        return a, z


def liad(z: np.ndarray, a: np.ndarray, order: int = 1, mode: str = "forward", return_list: bool = False):

    if mode in ["forward", "central"]:
        rets = finite_diff(z, a, order, mode, return_list=return_list)
    else:
        #TODO: add spline interpolation derivatives
        raise NotImplementedError

    return rets

def lehmer_mean(x: np.ndarray, p: float):
    
    if p == 1.0:
        den = 1.0
    else:
        den = np.power(x, p-1.0)
    num = x * den
    
    return np.sum(num, axis=-1)/np.sum(den, axis=-1)
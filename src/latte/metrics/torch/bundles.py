from typing import List, Optional, Union
from torchmetrics import MetricCollection

import numpy as np

from ..torch.disentanglement import (
    MutualInformationGap,
    DependencyAwareMutualInformationGap,
    DependencyBlindMutualInformationGap,
    DependencyAwareLatentInformationGap,
)
from ..torch.interpolatability import Smoothness, Monotonicity

# Note: We use `MetricCollection` from TorchMetrics for better efficiency, instead of a `TorchMetricWrapper` around a `MetricBundle`.


class DependencyAwareMutualInformationBundle(MetricCollection):
    def __init__(
        self, reg_dim: Optional[List] = None, discrete: bool = False,
    ):
        # need to set `fill_reg_dim=True` for same `reg_dim` behaviour with other metrics
        super().__init__(
            metrics={
                "MIG": MutualInformationGap(
                    reg_dim=reg_dim, discrete=discrete, fill_reg_dim=True
                ),
                "DMIG": DependencyAwareMutualInformationGap(
                    reg_dim=reg_dim, discrete=discrete
                ),
                "XMIG": DependencyBlindMutualInformationGap(
                    reg_dim=reg_dim, discrete=discrete
                ),
                "DLIG": DependencyAwareLatentInformationGap(
                    reg_dim=reg_dim, discrete=discrete
                ),
            }
        )


class LiadInterpolatabilityBundle(MetricCollection):
    def __init__(
        self,
        reg_dim: Optional[List] = None,
        liad_mode: str = "forward",
        max_mode: str = "lehmer",
        ptp_mode: Union[float, str] = "naive",
        reduce_mode: str = "attribute",
        liad_thresh: float = 1e-3,
        degenerate_val: float = np.nan,
        nanmean: bool = True,
        clamp: bool = False,
        p: float = 2.0,
    ):
        super().__init__(
            metrics={
                "smoothness": Smoothness(
                    reg_dim=reg_dim,
                    liad_mode=liad_mode,
                    max_mode=max_mode,
                    ptp_mode=ptp_mode,
                    reduce_mode=reduce_mode,
                    clamp=clamp,
                    p=p,
                ),
                "monotonicity": Monotonicity(
                    reg_dim=reg_dim,
                    liad_mode=liad_mode,
                    reduce_mode=reduce_mode,
                    liad_thresh=liad_thresh,
                    degenerate_val=degenerate_val,
                    nanmean=nanmean,
                    clamp=clamp,
                    p=p,
                ),
            }
        )

<p align=center><img width="50%" src="https://raw.githubusercontent.com/karnwatcharasupat/latte/main/assets/logo.png"/></p>
<p align=center><b>Cross-framework Python Package for Evaluation of Latent-based Generative Models</b></p>

[![Documentation Status](https://readthedocs.org/projects/latte/badge/?version=latest)](https://latte.readthedocs.io/en/latest/?badge=latest)
[![CircleCI](https://circleci.com/gh/karnwatcharasupat/latte/tree/main.svg?style=shield)](https://circleci.com/gh/karnwatcharasupat/latte/tree/main)
[![codecov](https://codecov.io/gh/karnwatcharasupat/latte/branch/main/graph/badge.svg)](https://codecov.io/gh/karnwatcharasupat/latte/branches/main)
[![CodeFactor](https://www.codefactor.io/repository/github/karnwatcharasupat/latte/badge/main)](https://www.codefactor.io/repository/github/karnwatcharasupat/latte/overview/main)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/latte-metrics.svg)](https://badge.fury.io/py/latte-metrics)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5786402.svg)](https://doi.org/10.5281/zenodo.5786402)


# Latte

Latte (for _LATent Tensor Evaluation_) is a cross-framework Python package for evaluation of latent-based generative models. Latte supports calculation of disentanglement and controllability metrics in both PyTorch (via TorchMetrics) and TensorFlow.


## Installation

For developers working on local clone, `cd` to the repo and replace `latte` with `.`. For example, `pip install .[tests]`

```console
pip install latte-metrics           # core (numpy only)
pip install latte-metrics[pytorch]  # with torchmetrics wrapper
pip install latte-metrics[keras]    # with tensorflow wrapper
pip install latte-metrics[tests]    # for testing
```

### Running tests locally
```
pip install .[tests]
pytest tests/ --cov=latte
```

## Example

### Functional API
```python
import latte
from latte.functional.disentanglement.mutual_info import mig
import numpy as np

latte.seed(42)

z = np.random.randn(16, 8)
a = np.random.randn(16, 2)

mutual_info_gap = mig(z, a, discrete=False, reg_dim=[4, 3])
```


### Modular API
```python
import latte
from latte.metrics.core.disentanglement import MutualInformationGap
import numpy as np

latte.seed(42)

mig = MutualInformationGap()

# ... 
# initialize data and model
# ...

for data, attributes in range(batches):
  recon, z = model(data)

  mig.update_state(z, attributes)

mig_val = mig.compute()
```

### TorchMetrics API
```python
import latte
from latte.metrics.torch.disentanglement import MutualInformationGap
import torch

latte.seed(42)

mig = MutualInformationGap()

# ... 
# initialize data and model
# ...

for data, attributes in range(batches):
  recon, z = model(data)

  mig.update(z, attributes)

mig_val = mig.compute()
```

### Keras Metric API
```python
import latte
from latte.metrics.keras.disentanglement import MutualInformationGap
from tensorflow import keras as tfk

latte.seed(42)

mig = MutualInformationGap()

# ... 
# initialize data and model
# ...

for data, attributes in range(batches):
  recon, z = model(data)

  mig.update_state(z, attributes)

mig_val = mig.result()
```


## Documentation

https://latte.readthedocs.io/en/latest

## Method Chart for Modular API

TorchMetrics: https://torchmetrics.readthedocs.io/en/latest/pages/implement.html

Keras Metric: https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Metric

Torch/Keras wrapper will
1. convert torch/tf types to numpy types (and move everything to CPU)
2. call native class methods
3. if there are return values, convert numpy types back to torch/tf types


|      | Native  |TorchMetrics | Keras Metric |
| :--- | :--- | :---        | :---         |
| base class | `latte.metrics.LatteMetric` | `torchmetrics.Metric` | `tf.keras.metrics.Metric` |
| super class | `object` | `torch.nn.Module` | `tf.keras.layers.Layer` |
| adding buffer | `self.add_state` | `self.add_state` | `self.add_weight` |
| updating buffer | `self.update_state` | `self.update` | `self.update_state` |
| resetting buffer | `self.reset_state` | `self.reset` | `self.reset_state` |
| computing metric values | `self.compute` | `self.compute` | `self.result` |

## Supported metrics

🧪 Beta support | ✔️ Stable | 🔨 In Progress | 🕣 In Queue | 👀 KIV |

| Metric                                        | Latte Functional  | Latte Modular | TorchMetrics   | Keras Metric | 
| :---                                          | :--:        | :--:      | :--:       | :--:       |
| _Disentanglement Metrics_                     |
| [📝](https://arxiv.org/abs/1802.04942) Mutual Information Gap (MIG)                          |🧪|🧪|🧪|🧪|
| [📝](https://arxiv.org/abs/2110.05587) Dependency-blind Mutual Information Gap (DMIG)         |🧪|🧪|🧪|🧪|
| [📝](https://www.researchgate.net/publication/356259963_Controllable_Music_Supervised_Learning_of_Disentangled_Representations_for_Music_Generation) Dependency-aware Mutual Information Gap (XMIG)                                                |🧪|🧪|🧪|🧪|
| [📝](https://www.researchgate.net/publication/356259963_Controllable_Music_Supervised_Learning_of_Disentangled_Representations_for_Music_Generation) Dependency-aware Latent Information Gap (DLIG)                                                |🧪|🧪|🧪|🧪|
| [📝](https://arxiv.org/abs/1711.00848) Separate Attribute Predictability (SAP)                |🧪|🧪|🧪|🧪|
| [📝](https://arxiv.org/abs/1802.05312) Modularity                                             |🧪|🧪|🧪|🧪|
| [📝](https://openreview.net/forum?id=Sy2fzU9gl) β-VAE Score    |👀|👀|👀|👀|
| [📝](https://arxiv.org/abs/1802.05983) FactorVAE Score   |👀|👀|👀|👀|
| [📝](https://openreview.net/forum?id=By-7dz-AZ) DCI Score    |👀|👀|👀|👀|
| [📝](https://arxiv.org/abs/1811.00007) Interventional Robustness Score (IRS)   |👀|👀|👀|👀|
| [📝](https://arxiv.org/abs/1910.09772) Consistency   |👀|👀|👀|👀|
| [📝](https://arxiv.org/abs/1910.09772) Restrictiveness   |👀|👀|👀|👀|
| _Interpolatability Metrics_                     |
| [📝](https://www.researchgate.net/publication/356259963_Controllable_Music_Supervised_Learning_of_Disentangled_Representations_for_Music_Generation) Smoothness                                                |🧪|🧪|🧪|🧪|
| [📝](https://www.researchgate.net/publication/356259963_Controllable_Music_Supervised_Learning_of_Disentangled_Representations_for_Music_Generation) Monotonicity                                              |🧪|🧪|🧪|🧪|
| [📝](https://archives.ismir.net/ismir2021/paper/000064.pdf) Latent Density Ratio                                              |🕣|🕣|🕣|🕣|
| [📝](https://arxiv.org/abs/2007.15474) Linearity                                        |👀|👀|👀|👀|

## Bundled metric modules
🧪 Experimental (subject to changes) | ✔️ Stable | 🔨 In Progress | 🕣 In Queue

| Metric Bundle                                 | Latte Functional  | Latte Modular | TorchMetrics   | Keras Metric | Included
| :---                                          | :--: | :--:        | :--:      | :--:       | :---|
| Dependency-aware Disentanglement              |🧪|🧪|🧪|🧪| MIG, DMIG, XMIG, DLIG |
| LIAD-based Interpolatability                  |🧪|🧪|🧪|🧪| Smoothness, Monotonicity |

## Cite 

For individual metrics, please cite the paper according to the link in the 📝 icon in front of each metric.

If you find our package useful please cite us as
```bibtex
@software{
  watcharasupat2021latte,
  author = {Watcharasupat, Karn N. and Lee, Junyoung and Lerch, Alexander},
  title = {{Latte: Cross-framework Python Package for Evaluation of Latent-based Generative Models}},
  url = {https://github.com/karnwatcharasupat/latte}
  doi = {10.5281/zenodo.5786402}
}
```



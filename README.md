## eMACDscore: Extended Morality as Cooperation Dictionary Scoring
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

**eMACDscore** provides a novel extension to existing moral mining tools for the fast and flexible extraction of various moral information metrics from textual input data. eMACDscore adopts the theoretical perspective of [Morality as Cooperation](https://doi.org/10.1007/978-3-319-19671-8_2) and is constructed based on crowd-sourced textual highlights as pioneered with the popular [eMFDscore](https://github.com/medianeuroscience/emfdscore). eMACDscore lets users score documents with multiple Morality as Cooperation Dictionaries and provides various metrics for analyzing moral information. 

When using eMACDscore, please consider giving this repository a star (top right corner) and citing the associated publication (currently in press; will be updated shortly)

eMACDscore is dual-licensed under GNU GENERAL PUBLIC LICENSE 3.0, which permits the non-commercial use, distribution, and modification of the eMACDscore package. Commercial use of the eMACDscore requires an application.

If you have any questions and/or require additional assistance with running the package, feel free to connect directly with the project maintainer, Musa Malik, via their ([LinkedIn](https://www.linkedin.com/in/musainayatmalik/). 

## Install 
**eMACDscore** requires a Python installation (v3.11+). If your machine does not have Python installed, we recommend installing Python by downloading and installing either [Anaconda or Miniconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html) for your OS.

For best practises, we recommend installing eMACDscore into a virtual conda environment. Hence, you should first create a virtual environment by executing the following command in your terminal:

```
$ conda create -n emac python=3.11
```

Once Anaconda/Miniconda is installed activate the env via:

```
$ source activate emac
```

Next, you must install spaCy, which is the main natural language processing backend that emacscore is built on:

```
$ conda install -c conda-forge spacy
$ python -m spacy download en_core_web_sm
``` 

Finally, you can install eMACDscore by copying, pasting, and executing the following command: 

`
pip install https://github.com/medianeuroscience/eMACDscore/archive/master.zip
`

### eMACDscore in Google Colaboratory

eMACDscore can also be run in [google colab](https://colab.research.google.com/notebooks/intro.ipynb). All you need to do is add these lines to the beginning of your notebook, execute them, and then restart your runtime:

```
!pip install https://github.com/medianeuroscience/eMACDscore/archive/master.zip
```

You can then use eMACDscore as a regular python library.

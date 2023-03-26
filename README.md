## emacscore: Extended Morality as Cooperation Dictionary Scoring
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

**emacscore** provides a novel extension to existing moral mining tools for the fast and flexible extraction of various moral information metrics from textual input data. emacscore adopts the theoretical perspective of [Morality as Cooperation](https://doi.org/10.1007/978-3-319-19671-8_2) and is constructed based on crowd-sourced textual highlights as pioneered with the popular [emfdscore](https://github.com/medianeuroscience/emfdscore). **emacscore** lets users score documents with **multiple Morality as Cooperation Dictionaries** and provides various metrics for analyzing moral information. 

**emacscore** is **currently in beta phase**. We do NOT recommend using this tool for research purposes right now. This section will be updated with more information once the beta phase has succesfully concluded.

## Install 
**emacscore** requires a Python installation (v3.7+). If your machine does not have Python installed, we recommend installing Python by downloading and installing either [Anaconda or Miniconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html) for your OS.

For best practises, we recommend installing emacscore into a virtual conda environment. Hence, you should first create a virtual environment by executing the following command in your terminal:

```
$ conda create -n emac python=3.7
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

Finally, you can install emacscore by copying, pasting, and executing the following command: 

`
pip install https://github.com/medianeuroscience/emacscore/archive/master.zip
`

### emacscore in Google Colaboratory

emacscore can also be run in [google colab](https://colab.research.google.com/notebooks/intro.ipynb). All you need to do is add these lines to the beginning of your notebook, execute them, and then restart your runtime:

```
!pip install -U pip setuptools wheel
!pip uninstall spacy
!pip install -v "spacy == 3.4.0"
!python -m spacy download en_core_web_sm
!pip install emacscore-master.zip  #currently need to download as local file as repo is private. will be changed to https:// link in future.
```

You can then use **emacscore** as a regular python library.

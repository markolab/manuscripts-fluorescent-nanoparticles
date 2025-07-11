# High-resolution in vivo kinematic tracking with injectable fluorescent nanoparticles

## Authors
Emine Zeynep Ulutas<sup>1</sup>, Amartya Pradhan<sup>2</sup>, Dorothy Koveal<sup>1</sup>Jeffrey E. Markowitz<sup>1,2#</sup>

<br>

<sup>1</sup>Wallace H. Coulter Department of Biomedical Engineering, Georgia Institute of Technology and Emory University, Atlanta, Georgia, United States<br>
<sup>2</sup>Graduate Program in Neuroscience, Emory Unviersity, Atlanta, Georgia, United States<br>

#Corresponding Author 

<br><br>

# Overview

Pre-processing and panel generation is done using Jupyter notebooks. You will need to have Jupyter or Jupyterlab installed on your machine. 

Much of the analysis was run on an AWS EC2 instance with 64GB of RAM and 16 CPUs, or on Georgia Tech's HPC environment, PACE. 

<br><br>

# Installation

Installation instructions

1. (IF YOU DO NOT HAVE CONDA) Install Miniconda on your machine https://docs.conda.io/en/latest/miniconda.html . On linux you can use these commands in the terminal.
		```bash
		# this example is for linux x86-64
		wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
		bash ~/miniconda.sh
		```
2. Install the environment needed to run JupyterLab and the notebooks.
		```bash
		conda env create -f conda_environments/base_qd_analysis.yml
		```
3. Once Miniconda is installed create the environment used for nearly all notebooks in this repository by running from the command line.
		conda activate base_qd_analysis

4. Install the library needed to run the code by running `pip install -e .` while in the `base_qd_analysis` environment.



<br><br>

# Notebooks/scripts

1. First, open `notebooks/preprocessing/config.toml` and alter the relevant file paths.
2. Next, assuming you have downloaded and unzipped all data from Zenodo, you can run all of the notebooks in `notebooks/panels`.

<br><br><br>

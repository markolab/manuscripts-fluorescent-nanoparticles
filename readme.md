# High-resolution in vivo kinematic tracking with injectable fluorescent nanoparticles

## Authors
Emine Zeynep Ulutas<sup>1</sup>, Amartya Pradhan<sup>2</sup>, Dorothy Koveal<sup>1</sup>Jeffrey E. Markowitz<sup>1,#</sup>

<br>

<sup>1</sup>Wallace H. Coulter Department of Biomedical Engineering, Georgia Institute of Technology and Emory University, Atlanta, Georgia, United States<br>
<sup>2</sup>Graduate Program in Neuroscience, Emory Unviersity, Atlanta, Georgia, United States<br>

#Corresponding Author 

<br><br>

# Overview

Pre-processing and panel generation is done using Jupyter notebooks. You will need to have Jupyter or Jupyterlab installed on your machine. 

Much of the analysis was run on an AWS EC2 instance with 64GB of RAM and 16 CUPS. 

<br><br>

# Installation

Installation instructions

1. (IF YOU DO NOT HAVE CONDA) Install Miniconda on your machine https://docs.conda.io/en/latest/miniconda.html . On linux you can use these commands in the terminal.

		# this example is for linux x86-64
		wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
		bash ~/miniconda.sh
1. We typically install jupyterlab in the base environment with `nb_conda_kernel`

		conda install -c conda-forge jupyterlab ipywidgets
		conda install nb_conda_kernels
		# be sure pip install ipykernel in other environments so they're detected by jupyter
1. Once Miniconda is installed create the environment used for nearly all notebooks in this repository by running from the command line.

		conda create -n particle-tracking python=3.10
		conda activate particle-tracking

1. Install the library needed to run the code by running `pip install -e .` while in the `particle-tracking` environment.



<br><br>

# Notebooks/scripts

1. First, open `analysis_configuration.toml` and alter the relevant file paths.
1. Next, you will need to run all preprocessing notebooks found in `notebooks-preprocessing`.
1. Once you have run all preprocessing notebooks, next run the panel figure generation notebooks in `notebooks-panels`. 
<br><br><br>

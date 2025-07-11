# Datasheet for QD-Pi-120k, version 01

Emine Zeynep Ulutas, Amartya Pradhan, Dorothy Koveal, [Jeffrey Markowtz](http://markolab.org)

## Motivation

### For what purpose was the dataset created?

Tracking movement in small laboratory animals, *e.g.* laboratory mice, is typically done using markerless keypoint trackers; that is, models trained to predict the position of key body parts using images of the surface of the animal. However, these methods can only be as accurate as the data used to train them. Here, we used fluorescent nanoparticles injected into the adipose tissue to precisely mark the location of specific body parts in freely moving mice. 

### Who created the dataset and on behalf of which entity?

The dataset was created by Emine Zeynep Ulutas (Georgia Tech) and Amartya Pradhan (Emory University). 

### Who funded the creation of the dataset?

The effort was funded by research fellowships to Markowitz from the Packard Foundation, Sloan Foundation, and Burroughs Wellcome Fund, seed funding from the McCamish Foundation, and startup funds from Georgia Tech.

## Composition

### What do the instances that comprise the dataset represent?

The instances are xy coordinates of ten body parts imaged across 5 different camera views in freely moving laboratory mice (C57/BL6J, Jackson Laboratories). Cameras (Basler acA2040-90um) outfit with 8 mm focal length lenses (Thorlabs MVL8M1) with a 780 nm longpass filter attached (MidOpt LP780-55) were hardware-synchronized by Arduino and were arrayed in a pentagon formation around a plexiglass arena. Cameras were placed approximately 12 inches from the center of the arena. Mice were illuminated using 660 nm LEDs (Advanced Illumination SL-S100150W-660) and 850 nm LEDs (SL246-850IC) with alternating 23 and 10 ms exposures, respectively. A strip of hair along the back of the mice was shaved to enable fluorescence imaging of particles injected into the back.

### How many instances are there in total?

Version 1 of the dataset has 114,629 instances. Here, 1 instance is 1 frame.

### Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set?

The dataset is a sample of a larger dataset. First, keypoints were predicted in a larger dataset using a model trained to predict keypoint locations from both fluorescence and reflectance data. Then, keypoint locations were verified using fluorescence. Additional thresholds to remove outliers were applied (see https://doi.org/INSERTDOI for more details)

### What data does each instance consist of?

The dataset is released in the slp format (https://github.com/talmolab/sleap). 

### Is there a label or target associated with each instance?

Multiple labels, or xy locations, are associated with each instance (*i.e.*, frame). Here we list all labels with their true names in the dataset given in parentheses. 

1. Left forepaw (foreleg_L)
1. Right forepaw (foreleg_R)
1. Left hindpaw (hindleg_L)
1. Right hindpaw (hindleg_R)
1. Tail tip (tail_tip)
1. Tail middle (tail_middle)
1. Tail base (tail_base)
1. Back bottom (back_bottom)
1. Back middle (back_middle)
1. Back top (back_top)

### Is any information missing from individual instances?

It is possible that keypoint locations are missing from some instances. 

### Are relationships between individual instances made explicit?

The relationships between instances are made explicit in the metadata associated with the slp file, which is stored in the toml format. Here, the video and frame index for each instances is shown.

### Are there recommended data splits (e.g., training, development/validation, testing)?

This depends entirely on the task. In our experience, training/testing on frames pooled across all cameras has worked well.

### Are there any errors, sources of noise, or redundancies in the dataset?

Errors are sure to exist given the size of the dataset. Given the thresholds applied to remove potential outliers, one likely source of noise are keypoints that are present but not properly identified in the dataset. An additional error source is the gap between adjacent fluorescence and reflectance exposures (17.5 ms, due to the short gap between fluorescence and reflectance exposures). The surface of the mouse and the location of the fluroescence markers were combined from alternating exposures, thus there may be displacements between the location of the fluorescence marker and its corresponding body part. Periods of rapid motion were filtered out from the dataset, but errors still likely remain, especially for the tail, which can move much faster than the rest of the mouse's body.


### Is the dataset self-contained, or does it link to or otherwise rely on external resources?

The dataset is self-contained. 

### Does the dataset contain data that might be considered confidential?

No.


### Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?

The dataset contains images of laboratory mice with a strip of hair shaved off of the back. While the mice were spontaneously behaving and presumably not under any stress, these images may still trigger unwelcome emotions.

### Does the dataset relate to people?

No, it only contains images of laboratory mice. 

### Does the dataset identify any subpopulations (e.g., by age, gender)?

N/A

### Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset?

N/A

### Does the dataset contain data that might be considered sensitive in any way (e.g., data that reveals racial or ethnic origins, sexual orientations, religious beliefs, political opinions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history)?

N/A

## Collection Process

###  How was the data associated with each instance acquired?

Mice were briefly anesthetized and injected with biotinylated quantum dots (qdot 800, Thermo Fisher) attached to streptavidin-coated agarose microbeads (Amid). Injections were performed in ten body parts. Then, after mice were ambulatory, they were imaged over multiple <10 minute sessions up to approximately 1 week post-injection in an open-field plexiglass arena.  

### What mechanisms or procedures were used to collect the data?

All the images in the dataset were collected using custom Python software to control our machine vision cameras, [cammy](https://github.com/markolab/cammy). 

### If the dataset is a sample from a larger set, what was the sampling strategy?

From our accompanying manuscript (see [here](https://doi.org/INSERTDOIHERE), 

>...we post-processed keypoint predictions using the following rules. First, we assumed that any large jumps in position between frames indicated a tracking error, so keypoints were excluded if they moved more than 30 pixels (L2 distance) between neighboring frames. Next, to filter outliers, we dimensionally reduced the x and y coordinates of the 10 keypoints (back bottom, back middle, back top, tail base, tail middle, tail tip, left/right fore/hindpaw) using principal components analysis (PCA). Here, we selected the number of PCs required to drop the cumulative mean squared reconstruction error by 90%. Next, we considered a keypoint visible if its keypoint confidence score exceeded 0.2. Of the visible keypoints, we then set thresholds on the minimum amount of fluorescence and the maximum distance to the nearest QD center for the keypoint to be considered valid; both values scaled with keypoint confidence. Less confident keypoints required higher fluorescence and needed to be closer to the nearest QD center. The minimum fluorescence peak linearly scaled from 75 for predictions with a score of 0.7 to 25 for a score of 1.0. The maximum distance scaled from 5 for predictions with a score of 0.7 to 15 for a score of 1.0. To prevent inclusion of frames with large difference between the number of “visible” keypoints and the number of “valid” keypoints, we linearly scaled the number of accepted dropped keypoints (“visible” – “valid”) from 0 for frames with 3 or fewer keypoints to 3 for frames with 10 keypoints. Finally, to exclude frames with outliers, we removed any frames where the distance between any pair of keypoints exceeded 300 pixels. "


### Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?

Emine Zeynep Ulutas (research technician) and Amartya Pradhan (graduate student). Each carried out research as part of their standard duties in the laboratory.

### Over what timeframe was the data collected?

The data were collected between June 10th and June 28th, 2024. 


### Were any ethical review processes conducted?

Yes, all procedures were performed according to Georgia Tech IACUC Protocol (PI Markowitz).

### Did you collect the data from individuals directly, or obtain it via third parties or other sources (e.g., websites)?

The data were all collected directly in PI Markowitz's laboratory at Georgia Tech.

### Were the individuals in question notified about the data collection?

N/A

### Did the individuals in question consent to the collection and use of their data?

N/A

### If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses?

N/A


### Has an analysis of the potential impact of the dataset and its use on data subjects (e.g., a data protection impact analysis) been conducted?

N/A

## Preprocessing/cleaning/labeling


### Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)?

Yes, see above for quote from accompanying manuscript for relevant pre-processing steps.


### Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?

Here, we consider the images "raw" data, and they are contained in the dataset. 

### Is the software used to preprocess/clean/label the instances avail- able?

Yes, the Python code used to generate and clean the dataset can be found [here](https://github.com/markolab/manuscripts-fluorescent-nanoparticles)


## Uses


### Has the dataset been used for any tasks already?

As of this writing, the data has only be used in the associated manuscript published by PI Markowitz's lab.


### Is there a repository that links to any or all papers or systems that use the dataset?

The Zenodo repository that this dataset is deposited in only links to the paper describing the creation for the dataset.


### What (other) tasks could the dataset be used for?

It is possible that this dataset could be used to profile algorithms for automatically disambiguating different body parts on the mouse. Potentially, this data could also be well-suited for training a model to segment the mouse. 

### Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?

Yes. We used mono machine vision cameras in specific positions arranged around the arena. We have not tested how well models trained on this dataset generalized to mouse recordings with different lighting or camera optics.


### Are there tasks for which the dataset should not be used?

We are not presently able to identify tasks for which the dataset should not be used, beyond the vast number of clear misapplications one can imagine. If we learn of problematic uses, we will update this section.


## Distribution


### Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created?

Yes, the dataset will be publicly available.


### How will the dataset will be distributed?

It is distributed via the current repository.


### When will the dataset be distributed?

The dataset will be made publicly available upon publication of the associated manuscript.

### Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?

We have released the dataset under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/), and the associated code in this repository has an Apache 2.0 license.


### Have any third parties imposed IP-based or other restrictions on the data associated with the instances?

No.


### Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?

Not that we are aware.


## Maintenance


### Who is supporting/hosting/maintaining the dataset?

At present, PI Markowitz is responsible for this.


### How can the owner/curator/manager of the dataset be contacted (e.g., email address)?

PI Markowitz can be contacted via his laboratory website (http://markolab.org) or via e-mail (listed on Georgia Tech BME's website)


###  Is there an erratum?

Not at present, but as errors are made aware to us we will be sure to update this section.


### Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)?

While the Zenodo repository will be immutable once it is made public, if errors are found we plan to correct them in the dataset and share the latest version elsewhere to the degree possible.

### If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g., were individuals in question told that their data would be retained for a fixed period of time and then deleted)?

N/A

### Will older versions of the dataset continue to be supported/hosted/maintained?

The Zenodo version of the dataset will be immutable.

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?

Yes, please reach out to PI Markowitz if you are interested.

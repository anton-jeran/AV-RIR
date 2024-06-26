# AV-RIR: Audio-Visual Room Impulse Response Estimation (CVPR 2024)

The inference code of our AV-RIR without CRIP. We provide two versions of our network optimized for RIR estimation and Speech enhancement. We also provide test samples to run the inference code. 

# Requirements

```
Python 3.8+
Cuda 11.0+
PyTorch 1.10+
numpy
pygsound
wavefile
tqdm
gdown
scipy
soundfile
librosa
```

## Trained Model and Test Data
To download the trained model and test data to the appropriate folder structure, run the following command.
```
source download.sh
```

## RIR Estimation
To run RIR estimation inference code. Go to **RIR_Estimation** and run the following command. The **output** folder will be created with the outputs.

```
cd RIR_Estimation/
bash submit_autoencoder.sh --start 2
cd output/autoencoder/symAD_vctk_48000_hop300/test/rir/

```


## Speech Enhancement
To run Speech Enhancement inference code. Go to **Enhancement** and run the following command. The **output** folder will be created with the outputs.

```
cd Enhancement/
bash submit_autoencoder.sh --start 2
cd output/autoencoder/symAD_vctk_48000_hop300/test/clean/
```

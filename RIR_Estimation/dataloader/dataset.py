#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
# Reference (https://github.com/kan-bayashi/ParallelWaveGAN/)

"""PyTorch compatible dataset modules."""

import os
import soundfile as sf
from torch.utils.data import Dataset
from dataloader.utils import find_files
import pickle
from PIL import Image
import numpy as np

class SingleDataset(Dataset):
    def __init__(
        self,
        files,
        query="*.wav",
        load_fn=sf.read,
        return_utt_id=False,
        subset_num=-1,
    ):
        self.return_utt_id = return_utt_id
        self.load_fn = load_fn
        self.subset_num = subset_num
        self.files = files

        self.filenames = self._load_list(files[0], query)
        self.utt_ids = self._load_ids(self.filenames)
        # self.dict_path = os.path.join(files[0], "dictionary.pickle")
        

        # if(len(files)>1):
        #     with open(self.dict_path, 'rb') as f:
        #         self.dictionary = pickle.load(f)


    def __getitem__(self, idx):
        utt_id = self.utt_ids[idx]
        data = self._data(idx)
                
        if self.return_utt_id:
            items = utt_id, data
        else:
            items = data

        return items


    def __len__(self):
        return len(self.filenames)
    
    
    def _read_list(self, listfile):
        filenames = []
        with open(listfile) as f:
            for line in f:
                line = line.strip()
                if len(line):
                    filenames.append(line)
        return filenames
    

    def _load_list(self, files, query):
        if isinstance(files, list):
            filenames = files
        else:
            if os.path.isdir(files):
                filenames = sorted(find_files(files, query,False))
            elif os.path.isfile(files):
                filenames = sorted(self._read_list(files))
            else:
                raise ValueError(f"{files} is not a list / existing folder or file!")
            
        if self.subset_num > 0:
            filenames = filenames[:self.subset_num]
        assert len(filenames) != 0, f"File list in empty!"
        return filenames
    
    
    def _load_ids(self, filenames):
        utt_ids = [
            # os.path.splitext(os.path.basename(f))[0] for f in filenames
            os.path.splitext(f)[0].split("/")[-2:] for f in filenames
        ]
        return utt_ids
    

    def _data(self, idx):
        return self._load_data(self.filenames[idx], self.load_fn)
    

    def _load_data(self, filename, load_fn):
        data=[]

        reverb_path = os.path.join(self.files[0],filename)
        reverb_data, _ = load_fn(reverb_path, always_2d=True) # (T, C)
        # if(len(self.files)>3):
            # reverb_data = reverb_data[0:9600]

            
        reverb_data = reverb_data[0:14400]

        if(reverb_data.shape[-1]==2):
            reverb_data = np.expand_dims(reverb_data[0:14400,0],axis=1)

        
        material_path = os.path.join(self.files[1],filename).replace(".wav",".png")
        image_path = os.path.join(self.files[2],filename).replace(".wav",".png")


        material_image = np.array(Image.open(material_path))
        color_image = np.array(Image.open(image_path))



        data = [reverb_data, material_image, color_image]
        if(len(self.files)>3):
            clean_path = os.path.join(self.files[3],filename)
            rir_path = os.path.join(self.files[4],filename)
        
            clean_data, _ = load_fn(clean_path, always_2d=True) # (T, C)
            rir_data, _ = load_fn(rir_path, always_2d=True) # (T, C)
        
            clean_data =  clean_data[0:9600]
            # rir_data =  rir_data[0:4000]

            rir_data =  rir_data[0:4000]
            # std_value = np.std(rir_data)  * 10
            # std_array = np.repeat(std_value,100).reshape(100,1)
            # rir_data =rir_data/std_value
            # rir_data = np.concatenate([rir_data,std_array])

        # print("rir_data shape  ", rir_data.shape)
        # print("clean_data shape  ", clean_data.shape)
        # print("reverb_data shape  ", reverb_data.shape)


            data = [reverb_data, material_image, color_image, clean_data, rir_data]
        
        return data





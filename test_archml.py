import pandas as pd
import numpy as np
import os
from EQTransformer.core.EqT_utils import cred2
import trainer as eqtt
from archml.helpers import resizer, result_metrics, compare
from archml.models import bilstm_closed



def test_models():

	input_hdf5=None
	input_csv=None
	output_name=None              
	input_dimention=(6000,3)
	cnn_blocks=5
	lstm_blocks=2
	padding='same'
	activation = 'relu'            
	drop_rate=0.1
	shuffle=True 
	label_type='gaussian'
	normalization_mode='std'
	augmentation=True
	add_event_r=0.6
	shift_event_r=0.99
	add_noise_r=0.3
	drop_channel_r=0.5
	add_gap_r=0.2
	scale_amplitude_r=None
	pre_emphasis=False             
	loss_weights=[0.05, 0.40, 0.55]
	loss_types=['binary_crossentropy', 'binary_crossentropy', 'binary_crossentropy']
	train_valid_test_split=[0.85, 0.05, 0.10]
	mode='generator'
	batch_size=200
	epochs=200
	monitor='val_loss'
	patience=12
	multi_gpu=False
	number_of_gpus=4
	gpuid=None
	gpu_limit=None
	use_multiprocessing=True
	model_select = bilstm_closed
	
	args_dict = {
	"input_hdf5": input_hdf5,
	"input_csv": input_csv,
	"output_name": output_name,
	"input_dimention": input_dimention,
	"cnn_blocks": cnn_blocks,
	"lstm_blocks": lstm_blocks,
	"padding": padding,
	"activation": activation,
	"drop_rate": drop_rate,
	"shuffle": shuffle,
	"label_type": label_type,
	"normalization_mode": normalization_mode,
	"augmentation": augmentation,
	"add_event_r": add_event_r,
	"shift_event_r": shift_event_r,
	"add_noise_r": add_noise_r,
	"add_gap_r": add_gap_r,
	"drop_channel_r": drop_channel_r,
	"scale_amplitude_r": scale_amplitude_r,
	"pre_emphasis": pre_emphasis,
	"loss_weights": loss_weights,
	"loss_types": loss_types,
	"train_valid_test_split": train_valid_test_split,
	"mode": mode,
	"batch_size": batch_size,
	"epochs": epochs,
	"monitor": monitor,
	"patience": patience,           
	"multi_gpu": multi_gpu,
	"number_of_gpus": number_of_gpus,           
	"gpuid": gpuid,
	"gpu_limit": gpu_limit,
	"use_multiprocessing": use_multiprocessing,
	"model_select": model_select
	}

	model = eqtt._build_model(args_dict)


	assert len(model.layers) == 142 #97



def test_resizer():
	resizer(data="ModelsAndSampleData/100samples.hdf5",csv="ModelsAndSampleData/100samples.csv",size=50)
	csv100 = pd.read_csv("ModelsAndSampleData/100samples.csv")
	csv50 = pd.read_csv("steadmini_50.csv")

	assert len(csv50) == len(csv100)/2

	os.remove("steadmini_50.csv")
	os.remove('steadmini_50.hdf5')


def test_results_metrics():

	eqt = pd.read_csv("ModelsAndSampleData/X_test_results_EQT.csv")
	test_dict = {'EQT':eqt}
	test_columns = np.array(["model_name","det_recall","det_precision","d_tp","d_fp","d_tn","d_fn","p_recall","p_precision","p_mae","p_rmse","p_tp","p_fp","p_tn","p_fn","s_recall","s_precision","s_mae","s_rmse","s_tp","s_fp","s_tn","s_fn","#events","#noise"])
	result_metrics(test_dict)
	
	csv = pd.read_csv("test_results.csv")
	
	comparison = csv.columns == test_columns
	equal_arrays = comparison.all()

	assert equal_arrays

	os.remove('test_results.csv')

	
def test_compare():
	csv = pd.read_csv("ModelsAndSampleData/test_results.csv")
	a = compare(csv)
	assert a == 'det_recall'




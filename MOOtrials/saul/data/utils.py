import gzip
import os
from random import random
import numpy as np

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import glob

HERE = os.path.dirname(os.path.abspath(__file__))


####################################################################################################################################

# def load_sst_data():
#     """Load the STT raw data.

#     Returns:
#         train_data, test_data, mask: the training data, testing data and surface mask respectively.
#     """
#     dirIn = "/global/cfs/projectdirs/dasrepo/nramachandra/data/new_void_prism/"
    
#     # train_data_raw = np.load(os.path.join(HERE, "sst_var_train.npy"), allow_pickle=True).data
#     train_data_raw = np.load(dirIn + "sst_var_train.npy", allow_pickle=True).data
#     # train_data_raw = np.random.rand(1000, 32, 32) ## random testing
    
#     # test_data_raw = np.load(os.path.join(HERE, "sst_var_test.npy"), allow_pickle=True).data
#     test_data_raw = np.load(dirIn + "sst_var_test.npy", allow_pickle=True).data
#     #test_data_raw = np.random.rand(1000, 32, 32) ## random testing
    
#     # mask = np.load(os.path.join(HERE, "mask.npy"), allow_pickle=True).data   
#     mask = np.load(dirIn + "mask.npy", allow_pickle=True).data    
#     #mask = np.random.rand(1000, 32, 32) ## random testing
    
#     return train_data_raw, test_data_raw, mask


# def prepare_as_seq2seq(data, input_horizon=8, output_horizon=8):

#     total_size = data.shape[0] - (input_horizon + output_horizon)  # Limit of sampling
#     input_seq = []
#     output_seq = []

#     for t in range(0, total_size):
#         input_seq.append(data[t : t + input_horizon, :])
#         output_seq.append(
#             data[t + input_horizon : t + input_horizon + output_horizon, :]
#         )

#     X = np.asarray(input_seq)  # [Samples, timesteps, state length]
#     y = np.asarray(output_seq)  # [Samples, timesteps, state length]

#     return X, y


# def load_data_prepared(n_components=5, input_horizon=8, output_horizon=8):

#     cached_data = f"processed_data_{n_components}_{input_horizon}_{output_horizon}.npz"

#     if not (os.path.exists(cached_data)):
#         train_data, test_data, _ = load_sst_data()

#         # flatten the data
#         train_data_flat = train_data.reshape(train_data.shape[0], -1)
#         test_data_flat = test_data.reshape(test_data.shape[0], -1)

#         train_data_flat = np.concatenate(
#             [train_data_flat, test_data_flat[:700]], axis=0
#         )
#         test_data_flat = test_data_flat[700:]

#         # dimensionality reduction
#         preprocessor = Pipeline(
#             # [("pca", PCA(n_components=n_components)), ("standard", StandardScaler())]
#             [("pca", PCA(n_components=n_components)), ("minmax", MinMaxScaler())]
#         )
#         train_data_reduc = preprocessor.fit_transform(train_data_flat)
#         test_data_reduc = preprocessor.transform(test_data_flat)

#         X_train, y_train = prepare_as_seq2seq(
#             train_data_reduc, input_horizon, output_horizon
#         )
#         X_test, y_test = prepare_as_seq2seq(
#             test_data_reduc, input_horizon, output_horizon
#         )

#         X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

#         # Save
#         data = {
#             "train": (X_train, y_train),
#             "valid": (X_valid, y_valid),
#             "test": (X_test, y_test),
#             "preprocessor": preprocessor,
#         }
#         with gzip.GzipFile(cached_data, "w") as f:
#             np.save(file=f, arr=data, allow_pickle=True)
#     else:
#         # Load (dict)
#         with gzip.GzipFile(cached_data, "rb") as f:
#             data = np.load(f, allow_pickle=True).item()

#         X_train, y_train = data["train"]
#         X_valid, y_valid = data["valid"]
#         X_test, y_test = data["test"]
#         preprocessor = data["preprocessor"]

#     return (X_train, y_train), (X_valid, y_valid), (X_test, y_test), preprocessor



####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def load_data(nSamples, nGrid, train_test_split):
    
    dirIn = '/global/cfs/projectdirs/dasrepo/nramachandra/data/new_void_prism/Data/'

    
    ell_all_files = glob.glob(dirIn+'/*Ellipse*')
    stress_all_files = glob.glob(dirIn+'/*VonMises*')

    ell_all = np.array([np.load(f) for f in ell_all_files])[:nSamples]
    stress_all = np.array([np.load(f) for f in stress_all_files])[:nSamples]
    
    max_stress = np.max(stress_all, axis=(1,2))  ## max stress
    

    vol90 = []  ## high vol region
    for ind in range(stress_all.shape[0]):
        vol90i = np.where(stress_all[ind] > 0.9*max_stress[ind], 1, 0).sum()
        vol90 = np.append(vol90, vol90i)

    target_all = np.vstack([max_stress, vol90]).T

    split = np.int32( train_test_split*ell_all.shape[0] )

    train_data = ell_all[0:split, :, :].astype('float32')
    # train_target = stress_all[0:split, :, :].astype('float32')
    train_target = target_all[0:split].astype('float32')

    test_data = ell_all[split:, :, :].astype('float32')
    # test_target = stress_all[split:, :, :].astype('float32')
    test_target = target_all[split:].astype('float32')

    return (train_data[:, :nGrid, :nGrid], train_target), (test_data[:, :nGrid, :nGrid], test_target)
            
############################################
    
def load_data_prepared(nSamples, nGrid, train_test_split):
    (train_input, train_target), (test_input, test_target) = load_data(nSamples, nGrid, train_test_split)
    
    # RESCALING IMAGES

    tmin = train_input.min()
    
    tmax = train_input.max()
    # print('old min-max:', tmin, tmax)
    train_images = (train_input - tmin) / (tmax - tmin) # Normalize the images to [-1, 1]
    test_images = (test_input - tmin) / (tmax - tmin)
    # print('new min-max:', train_images.min(), train_images.max())

    shape0 = train_images.shape[0]
    swe_train_data = train_images.reshape(shape0, nGrid, nGrid, 1)
    shape0 = test_images.shape[0]
    swe_test_data = test_images.reshape(shape0, nGrid, nGrid, 1)
    
    
    ############################################
    # RESCALING TARGETS

    
    tmin = train_target.min()
    
    tmax = train_target.max()
    # print('old min-max:', tmin, tmax)
    train_target = (train_target - tmin) / (tmax - tmin) # Normalize the images to [-1, 1]
    test_target = (test_target - tmin) / (tmax - tmin)
    # print('new min-max:', train_target.min(), train_target.max())
    
    return (swe_train_data, train_target), (swe_test_data, test_target)



############################################

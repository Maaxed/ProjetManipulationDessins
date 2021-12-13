import numpy as np
import sklearn.model_selection
from utils import load_files, make_a_gif
from model_VAE import get_model, train_and_save_weights
import os

from matplotlib import pyplot as plt

os.environ["CUDA_VISIBLE_DEVICES"]="1"

directory = r'./data'

autoencoder, encoder, decoder = get_model()

def print_mean(data_, categories_):
    categories_unique = np.unique(categories_)
    data_categorised = [data_[categories_ == cat] for cat in categories_unique]
    ultimas = []
    for cat, dat in zip(categories_unique, data_categorised):
        plt.figure(figsize=(14, 4))
        ultimate_mean_image = np.mean(dat, axis=0)
        plt.subplot(1, 3, 1)
        plt.imshow(ultimate_mean_image, cmap="gray", vmin=0, vmax=1)
        plt.title("Mean image of all " + cat)
        plt.axis('off')
        lattent_vectors = encoder.predict(dat)
        mean_data = np.mean(lattent_vectors, axis=0)
        best_data_index = np.argmin([np.dot(lat - mean_data, lat - mean_data) for lat in lattent_vectors], axis=0)
        ultimas.append(lattent_vectors[best_data_index])
        res = decoder.predict(np.array([lattent_vectors[best_data_index]]))[0]
        plt.subplot(1, 3, 2)
        plt.imshow(res, cmap="gray", vmin=0, vmax=1)
        plt.title("Ultimate " + cat)
        plt.axis('off')
        plt.subplot(1, 3, 3)
        plt.imshow(dat[best_data_index], cmap="gray", vmin=0, vmax=1)
        plt.title("Base image for Ultimate " + cat)
        plt.axis('off')
        plt.show()
    return ultimas, categories_unique


def test_each_dimension(encoder, decoder, data, var):
    for k in range(10):
        d = data[k]
        plt.imshow(d, cmap="gray", vmin=0, vmax=1)
        plt.axis('off')
        lattentvector = encoder.predict(np.array([d]))
        show_count = len(lattentvector[0]) 
        print(f"LATTENTVECTOR:{lattentvector}\n\n")

        plt.figure(figsize=(14, 4))
        for i in range(show_count):
            for j in range(len(var)):
                tmp_latt = np.copy(lattentvector)
                tmp_latt[0][i] += var[j]
                res = decoder.predict(tmp_latt)[0]
                plt.subplot(len(var), show_count, 1 + j*show_count + i)
                plt.imshow(res, cmap="gray", vmin=0, vmax=1)
                plt.axis('off')
        plt.tight_layout()
        plt.show()


def transit(ultimas, categories, nb_steps):
    cols = nb_steps + 2
    for ulti1 in range(len(ultimas)-1):
        for ulti2 in range(ulti1+1, len(ultimas)):
            plt.figure(figsize=(14, 4))
            plt.subplot(1, cols, 1)
            plt.imshow(decoder.predict(np.array([ultimas[ulti1]]))[0], cmap='gray', vmin=0, vmax=1)
            plt.title("Ultima " + categories[ulti1])
            plt.axis('off')
            plt.subplot(1, cols, cols)
            plt.imshow(decoder.predict(np.array([ultimas[ulti2]]))[0], cmap='gray', vmin=0, vmax=1)
            plt.title("Ultima " + categories[ulti2])
            plt.axis('off')
            inbetweens = np.linspace(ultimas[ulti1], ultimas[ulti2], nb_steps, endpoint=False)
            ctr = 0
            for inb in inbetweens:
                plt.subplot(1, cols, 2 + ctr)
                ctr += 1
                plt.imshow(decoder.predict(np.array([inb]))[0], cmap='gray', vmin=0, vmax=1)
                plt.axis('off')
            plt.tight_layout()
            plt.show()
            make_a_gif(decoder, ultimas[ulti1], ultimas[ulti2], nb_steps, True)





data, categories = load_files(directory)

print(f"Shape of data: {data.shape}")

train_data, valid_data, train_cat, valid_cat = sklearn.model_selection.train_test_split(data, categories, test_size=0.33)

print("Data ready")

#train_and_save_weights(autoencoder, train_data, valid_data)

load_status = autoencoder.load_weights("weights")

ultimas, categories = print_mean(valid_data, valid_cat)
transit(ultimas, categories, 7)

test_each_dimension(encoder, decoder, valid_data, var = [-4, -3, -2, -1, 0, 1, 2, 3, 4])
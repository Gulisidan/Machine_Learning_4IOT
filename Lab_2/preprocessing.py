import tensorflow as tf
import tensorflow_io as tfio
import IPython


LABELS = ['down', 'go', 'left', 'no', 'right', 'stop', 'up', 'yes']


def get_audio_and_label(filename):
    # tensorflow can manage opening a file, returning a binary string (object is tensorflow
    audio_binary = tf.io.read_file(filename)
    # transform the tensor into a usable format, decoding the file as it is a wav file
    audio, sampling_rate = tf.audio.decode_wav(audio_binary)  # for the examples seens during the lab, our audio files have sampling rate = 16 kHz
    
    # as Label, i take the label that is saved inside the filename (after examples that is my folder, before "_" )
    path_parts = tf.strings.split(filename, '/')
    path_end = path_parts[-1]
    file_parts = tf.strings.split(path_end, '_')
    # to decode this label -> label.numpy().decode()
    label = file_parts[0]
    #print(audio)
    return audio, sampling_rate, label
    
    

def get_spectrogram(filename, downsampling_rate, frame_length_in_s=0.04, frame_step_in_s=0.02):
    # TODO: Write your code here
    audio_binary = tf.io.read_file(filename)
    audio, sampling_rate = tf.audio.decode_wav(audio_binary)

    zero_padding = tf.zeros(sampling_rate - tf.shape(audio), dtype=tf.float32)
    audio_padded = tf.concat([audio, zero_padding], axis=0)
    frame_length = int(frame_length_in_s * sampling_rate.numpy())
    frame_step = int(frame_step_in_s * sampling_rate.numpy())

    stft = tf.signal.stft(
        audio_padded, 
        frame_length=frame_length,
        frame_step=frame_step,
        fft_length=frame_length
    )
    spectrogram = tf.abs(stft)

    path_parts = tf.strings.split(filename, '/')
    path_end = path_parts[-1]
    file_parts = tf.strings.split(path_end, '_')
    label = file_parts[0]

    return spectrogram, sampling_rate, label


def get_log_mel_spectrogram(filename, downsampling_rate, frame_length_in_s=0.04, frame_step_in_s=0.02, num_mel_bins=40, lower_frequency=20, upper_frequency=4000):
    # TODO: Write your code here
    spectogram, sampling_rate, label = get_spectrogram(filename, downsampling_rate, frame_length_in_s, frame_step_in_s)
    num_spectrogram_bins = spectrogram.shape[1]

    linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
        num_mel_bins=num_mel_bins,
        num_spectrogram_bins=num_spectrogram_bins,
        sample_rate=sampling_rate,
        lower_edge_hertz=lower_frequency,
        upper_edge_hertz=upper_frequency
    )
    mel_spectrogram = tf.matmul(spectrogram, linear_to_mel_weight_matrix)

    log_mel_spectrogram = tf.math.log(mel_spectrogram + 1.e-6)

    return log_mel_spectrogram, label


def get_mfccs(filename, downsampling_rate, frame_length_in_s, frame_step_in_s, num_mel_bins, lower_frequency, upper_frequency, num_coefficients):
    # TODO: Write your code herea

    return mfccs, label

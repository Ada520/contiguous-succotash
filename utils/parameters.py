from .functional import *


class Parameters:
    def __init__(self, max_word_len, max_seq_len, word_vocab_size, char_vocab_size):

        self.max_word_len = int(max_word_len)
        self.max_seq_len = int(max_seq_len) + 1  # go or eos token

        self.word_vocab_size = int(word_vocab_size)
        self.char_vocab_size = int(char_vocab_size)

        self.word_embed_size = 300
        self.char_embed_size = 15

        self.encoder_rnn_size = 600
        self.encoder_num_layers = 1

        self.latent_variable_size = 1100

        self.kernels = [(1, 25), (2, 50), (3, 75), (4, 100), (5, 125), (6, 150)]
        self.sum_depth = fold(lambda x, y: x + y, [depth for _, depth in self.kernels], 0)

        self.decoder_dilations = [1, 2, 4, 8, 16]
        self.decoder_kernels = [(1700, self.latent_variable_size + self.word_embed_size, 3),
                                (2400, 1700, 3),
                                (3100, 2400, 3),
                                (4400, 3100, 3),
                                (7000, 4400, 3)]
        self.decoder_num_layers = len(self.decoder_kernels)
        ''' paddings in thin case is necessary to prevent using t+i-th token in t-th token prediction.
            paddings are resized because kernel width is increased when dilation is performed
        '''
        self.decoder_paddings = [Parameters.effective_k(w, self.decoder_dilations[i]) - 1
                                 for i, (_, _, w) in enumerate(self.decoder_kernels)]

    @staticmethod
    def effective_k(k, d):
        """
        :param k: kernel width
        :param d: dilation size
        :return: effective kernel width when dilation is performed
        """
        return k + (k - 1) * (d - 1)
import tensorflow_datasets as tfds
import pickle

def get_dataset():
    builder = tfds.builder('reddit_tifu', data_dir=r'data/reddit_tifu')
    builder.download_and_prepare()
    return builder.as_dataset(split='train')


def get_dataset_df():
    builder = tfds.builder('reddit_tifu', data_dir=r'data/reddit_tifu')
    builder.download_and_prepare()
    dataset = builder.as_dataset(split='train')
    return tfds.as_dataframe(dataset)


def print_rows(dataset, num_rows):
    '''
        Print a limited number of rows
    :param dataset:
    :param num_rows:
    '''
    print(tfds.as_dataframe(dataset.take(num_rows)))


def get_column_names(df_dataset):
    return df_dataset.columns


def decode_columns(df_dataset, columns):
    for column in columns:
        df_dataset[column] = df_dataset[column].str.decode('utf-8')
        print(df_dataset[column].head(10))
    return df_dataset


if __name__ == "__main__":
    dataset = get_dataset()
    df_dataset = get_dataset_df()
    df_dataset = decode_columns(df_dataset, ['documents', 'title', 'tldr'])
    with open('data/reddit_tifu/df_tifu.pkl', 'wb') as f:
        pickle.dump(df_dataset, f)
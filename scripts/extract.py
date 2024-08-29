import argparse
from Bio import SeqIO
from tqdm import tqdm
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    # fasta file; metadata file; output file
    parser.add_argument('-f', '--fasta', type=str, required=True)
    parser.add_argument('-m', '--metadata', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    return parser.parse_args()

def pull_seqs_from_fasta(fasta_file, metadata):
    extracted_seqs = []
    fasta_sequences = SeqIO.parse(fasta_file, 'fasta')
    for seq in tqdm(fasta_sequences):
        seq_name = str(seq.id).strip().split('.')[0] # get epi id
        if seq_name in metadata['renamed_name'].values.tolist():
            seq.id = metadata[metadata['renamed_name'] == seq_name]['name'].values[0]
            seq.description = ''
            extracted_seqs.append(seq)
    return extracted_seqs

def read_metadata(metadata_file):
    if metadata_file.endswith('.csv'):
        metadata = pd.read_csv(metadata_file)
    elif metadata_file.endswith('.tsv'):
        metadata = pd.read_csv(metadata_file, sep='\t')
    else:
        raise Exception('Unknown metadata file format')
    return metadata

def main():
    print('Extracting sequences from fasta file')
    args = parse_args()
    metadata = read_metadata(args.metadata)
    metadata['renamed_name'] = metadata['name'].str.split('_').str[0]
    extracted_seqs = pull_seqs_from_fasta(args.fasta, metadata)
    SeqIO.write(extracted_seqs, args.output, 'fasta')

if __name__ == '__main__':
    main()
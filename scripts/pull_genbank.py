from Bio import Entrez
from tqdm import tqdm
import sys
import time
import pandas as pd

# Set email, Entrez requires a valid email address
Entrez.email = "gardfgra@gdsfgdf.com"

genbank_ids_file = sys.argv[1]
output_file = sys.argv[2]

# List of GenBank names
metadata = pd.read_csv(genbank_ids_file, sep="\t")
genbank_names = metadata["name"].tolist()

# Function to download FASTA files
def download_fasta(genbank_name, output_file):
    try:
        # pull only the HA segment
        search_term = f"dengue  AND {genbank_name.split('_')[0]}"
        genbank_bar.set_description(f"Downloading GenBank FASTA files for {genbank_name}")
        handle = Entrez.esearch(db="nucleotide", term=search_term, retmode="xml")
        record = Entrez.read(handle)
        handle.close()
        
        # If no records are found, skip to the next GenBank name
        if not record['IdList']:
            print(f"No records found for {genbank_name}")
            return
        
        # Get the first record ID (assumption: it is the correct one)
        record_id = record['IdList']
        
        # Fetch the record by ID
        handle = Entrez.efetch(db="nucleotide", id=record_id, rettype="fasta", retmode="text")
        fasta_data = handle.read()
        handle.close()
        
        with open(output_file, "a") as f:
            f.write(fasta_data)
        
        # print(f"FASTA file for {genbank_name} saved successfully.")
    
    except Exception as e:
        raise e


# Download FASTA files for all GenBank names in the list
genbank_bar = tqdm(genbank_names, desc="Downloading GenBank FASTA files")
for name in genbank_bar:
    try:
        download_fasta(name, output_file)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Retrying in 60 seconds...")
        time.sleep(60)
        download_fasta(name, output_file)
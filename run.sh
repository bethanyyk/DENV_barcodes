set -ex

bash data/get-data.sh

nextflow pull https://github.com/gp201/Freyja_pathogen_workflow_v2 -r 'main'

LOC=$(nextflow info gp201/Freyja_pathogen_workflow_v2 | grep "local path")

# delete "local path: " from the string
LOC=${LOC:15}

nextflow -c $LOC/nextflow.config run $LOC/subworkflows/local/nextstrain_data_extraction/main.nf --json_tree $PWD/data/auspice_tree.json -profile mamba

mv output/NEXTSTRAIN_DATA_EXTRACTION_WORKFLOW\:FORMAT_NWK_TREE/tree.nwk .
mv output/NEXTSTRAIN_DATA_EXTRACTION_WORKFLOW\:NEXTSTRAIN_DATA_EXTRACTION/subworkflow_auspice_metadata.tsv metadata.tsv

rm -rf output

# python scripts/pull_genbank.py metadata.tsv data/genbank.fasta
python3 scripts/extract.py --fasta data/genbank.fasta --metadata metadata.tsv --output sequences.fasta

nextflow run https://github.com/gp201/Freyja_pathogen_workflow_v2.git -r 'main' -profile mamba -c config/nextflow.config
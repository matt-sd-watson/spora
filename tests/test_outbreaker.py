import os
from outbreaker import main
import sys
from Bio import SeqIO

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/'))
print(DATA_DIR)

test_reference = os.path.join(DATA_DIR, 'reference', 'ncov_reference.gb')


class TestOutbreaker:
    def test_read_test_focal_fasta(self):
        query_file = os.path.join(DATA_DIR, 'tests/', 'focal_seqs.fa')
        assert len(list(SeqIO.parse(query_file, "fasta"))) == 4
    def test_read_test_background_fasta(self):
        query_file = os.path.join(DATA_DIR, 'tests/', 'background_seqs.fa')
        assert len(list(SeqIO.parse(query_file, "fasta"))) == 6

    def test_run_outputs(self, tmp_path):
        focal_seqs = os.path.join(DATA_DIR, 'tests/', 'focal_seqs.fa')
        background_seqs = os.path.join(DATA_DIR, 'tests/', 'background_seqs.fa')

        args = ['-f', str(focal_seqs), '-b', str(background_seqs), '--rename', '-p', 'pytest',
                '-r', str(test_reference), '-o', str(tmp_path)]

        main.main(sysargs = args)
        output_merged_fasta = os.path.join(tmp_path, 'pytest_renamed.fa')
        assert len(list(SeqIO.parse(output_merged_fasta, "fasta"))) == 10

        new_names = ["pytest_" + str(i) for i in range(1, 11, 1)]
        names_in_fasta = []
        for record in SeqIO.parse(output_merged_fasta, "fasta"):
            names_in_fasta.append(record.id)
        assert names_in_fasta == new_names





        
        





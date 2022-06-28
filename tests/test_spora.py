import os
import sys
from Bio import SeqIO
import subprocess
import pytest


@pytest.fixture(scope = "module")
def get_data_dir():
    return str(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/')))

@pytest.fixture(scope = "module")
def get_alignment_reference(get_data_dir):
    return str(os.path.join(get_data_dir, 'reference', 'ncov_reference.gb'))

@pytest.fixture(scope = "module")
def get_focal_sequences(get_data_dir):
    return str(os.path.join(get_data_dir, 'tests/', 'focal_seqs.fa'))

@pytest.fixture(scope = "module")
def get_background_sequences(get_data_dir):
    return str(os.path.join(get_data_dir, 'tests/', 'background_seqs.fa'))

@pytest.fixture(scope = "module")
def get_names_csv(get_data_dir):
    return str(os.path.join(get_data_dir, 'tests/', 'names.csv'))

# need to keep fixtures that call built-in tmp_path within same scope as tmp_path (function
@pytest.fixture(scope = "function")
def get_renamed_fasta(tmp_path):
    return str(os.path.join(tmp_path, 'pytest_renamed.fa'))

class TestSpora:
    def test_read_test_focal_fasta(self, get_focal_sequences):
        assert len(list(SeqIO.parse(get_focal_sequences, "fasta"))) == 4
    def test_read_test_background_fasta(self, get_background_sequences):
        assert len(list(SeqIO.parse(get_background_sequences, "fasta"))) == 6

    def test_run_outputs(self, tmp_path, get_focal_sequences, get_background_sequences,
                         get_alignment_reference, get_renamed_fasta):

        results = subprocess.run(
            ['spora', '-f', get_focal_sequences, '-b', get_background_sequences, '--rename', '-p', 'pytest',
                '-r', get_alignment_reference, '-o', str(tmp_path)],
            stdout=subprocess.PIPE)

        assert len(list(SeqIO.parse(get_renamed_fasta, "fasta"))) == 10

        new_names = ["pytest_" + str(i) for i in range(1, 11, 1)]
        names_in_fasta = []
        for record in SeqIO.parse(get_renamed_fasta, "fasta"):
            names_in_fasta.append(record.id)
        assert names_in_fasta == new_names


    def test_run_with_missing_names_csv(self, tmp_path, get_focal_sequences, get_background_sequences,
                         get_alignment_reference, get_names_csv, get_renamed_fasta):

        results = subprocess.run(
            ['spora', '-f', get_focal_sequences, '-b', get_background_sequences, '--rename', '-p', 'pytest',
                    '-r', get_alignment_reference, '-o', str(tmp_path), '--names-csv', get_names_csv],
            stdout=subprocess.PIPE)

        names_in_fasta = []
        for record in SeqIO.parse(get_renamed_fasta, "fasta"):
                names_in_fasta.append(record.id)
        names_not_all = ['Renamed_1', 'Renamed_2', 'Renamed_3',
            'Focal_4', 'Renamed_4', 'Renamed_5', 'Background_3',
                             'Renamed_6', 'Renamed_7', 'Renamed_8']
        assert names_in_fasta == names_not_all

        output_snp_dists = os.path.join(tmp_path, "pytest_snp_dists.csv")

        with open(output_snp_dists) as f:
            lines = f.readlines()
        assert str('Renamed_8,Background_3,5\n') in lines

    def test_run_with_console_output(self, tmp_path, get_focal_sequences, get_background_sequences,
                         get_alignment_reference, get_names_csv):

        results = subprocess.run(['spora', '-f', get_focal_sequences, '-b', get_background_sequences, '--rename', '-p', 'pytest',
                '-r', get_alignment_reference, '-o', str(tmp_path), '--names-csv', get_names_csv],
                                 stdout=subprocess.PIPE)
        assert 'WARNING: the following record has no match in samples IDs and will be kept with the original name: Focal_4' \
               in results.stdout.decode('utf-8')
        

# Copyright 2024 Xin Huang
#
# GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, please see
#
#    https://www.gnu.org/licenses/gpl-3.0.en.html


import pytest
from sai.utils.generators import WindowDataGenerator


@pytest.fixture
def test_generator():
    # Initialize the WindowDataGenerator with actual data files
    generator = WindowDataGenerator(
        vcf_file="tests/data/test.data.vcf",
        chr_name="21",
        ref_ind_file="tests/data/test.ref.ind.list",
        tgt_ind_file="tests/data/test.tgt.ind.list",
        src_ind_file="tests/data/test.src.ind.list",
        win_len=1000,  # Set window length as appropriate for testing
        win_step=500,  # Set window step as appropriate for testing
        anc_allele_file=None,
        ploidy=2,
        is_phased=True,
    )
    return generator


def test_initialization(test_generator):
    # Verify initialization parameters
    assert test_generator.win_len == 1000
    assert test_generator.win_step == 500
    assert test_generator.ploidy == 1


def test_window_data_generator(test_generator):
    # Collect data from generator
    data_list = list(test_generator.get())

    # Ensure windows were generated
    assert len(data_list) == 376

    # Inspect first window's contents for expected format and data
    first_window = data_list[0]
    assert "chr_name" in first_window
    assert "start" in first_window
    assert "end" in first_window
    assert "ref_pop" in first_window
    assert first_window["ref_pop"] == "ref1"
    assert "tgt_pop" in first_window
    assert "src_pop_list" in first_window
    assert "ref_gts" in first_window
    assert "tgt_gts" in first_window
    assert "src_gts_list" in first_window
    assert "ploidy" in first_window


def test_len(test_generator):
    # Check if __len__ provides a reasonable window count
    assert len(test_generator) == 376


@pytest.fixture
def test_generator_two_sources():
    # Initialize the WindowDataGenerator with num_src=2 for testing two-source combinations
    generator = WindowDataGenerator(
        vcf_file="tests/data/test.data.vcf",
        chr_name="21",
        ref_ind_file="tests/data/test.ref.ind.list",
        tgt_ind_file="tests/data/test.tgt.ind.list",
        src_ind_file="tests/data/test.src.ind.list",
        win_len=1000,  # Set window length as appropriate for testing
        win_step=500,  # Set window step as appropriate for testing
        num_src=2,  # Set to 2 to test two-source combinations
        anc_allele_file=None,
        ploidy=2,
        is_phased=False,
    )
    return generator


def test_initialization_two_sources(test_generator_two_sources):
    # Verify initialization parameters for two-source generator
    assert test_generator_two_sources.win_len == 1000
    assert test_generator_two_sources.win_step == 500
    assert test_generator_two_sources.ploidy == 2
    assert test_generator_two_sources.num_src == 2


def test_window_data_generator_with_two_sources(test_generator_two_sources):
    # Collect data from generator with two sources
    data_list = list(test_generator_two_sources.get())

    # Ensure windows were generated and have two sources in src_pop_list
    assert len(data_list) > 0  # Ensure data was generated
    first_window = data_list[0]

    # Check keys in the first window
    assert "start" in first_window
    assert "end" in first_window
    assert "ref_pop" in first_window
    assert "tgt_pop" in first_window
    assert "src_pop_list" in first_window
    assert "ref_gts" in first_window
    assert "tgt_gts" in first_window
    assert "src_gts_list" in first_window
    assert "ploidy" in first_window

    # Verify that src_pop_list contains exactly two source populations
    assert len(first_window["src_pop_list"]) == 2
    assert (
        len(first_window["src_gts_list"]) == 2
    )  # Ensure two sets of genotypes in src_gts_list


def test_len_two_sources(test_generator_two_sources):
    # Check if __len__ provides a reasonable window count with two-source combinations
    assert len(test_generator_two_sources) > 0  # Ensure it counts windows correctly
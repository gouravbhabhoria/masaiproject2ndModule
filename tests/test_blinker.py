import sys
import os
# Add the parent directory to sys.path before importing anything from life.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from life import next_gen
def test_blinker_oscillator():
    # Horizontal blinker in a 5x5 board
    width, height = 5, 5
    blinker_initial = {(1, 2), (2, 2), (3, 2)}
    blinker_next_expected = {(2, 1), (2, 2), (2, 3)}
    # After one generation, blinker should be vertical
    assert next_gen(blinker_initial, width, height) == blinker_next_expected
    # After two generations, blinker returns to horizontal
    assert next_gen(blinker_next_expected, width, height) == blinker_initial

def test_glider_movement():
    # Glider pattern in a 5x5 board
    width, height = 5, 5
    glider_initial = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
    glider_next_expected = {(0, 1), (1, 2), (2, 1), (2, 2), (1, 3)}
    # After one generation, glider should transform to expected pattern
    assert next_gen(glider_initial, width, height) == glider_next_expected

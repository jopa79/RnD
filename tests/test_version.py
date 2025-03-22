"""
Test version information
"""

import pytest
from image_harvester import __version__

def test_version():
    """
    Test that the version string is properly formatted.
    """
    assert isinstance(__version__, str)
    assert len(__version__.split('.')) >= 2

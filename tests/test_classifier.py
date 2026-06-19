"""Tests for the ESG classifier module."""
# import pytest  # not available in this env
from unittest.mock import patch, MagicMock
from src.models.esg_classifier import classify, classify_batch


def test_classify_empty_string():
    label, conf = classify("")
    assert label == "None"
    assert conf == 0.0


def test_classify_returns_valid_label():
    mock_result = [[{"label": "Environmental", "score": 0.92}]]
    with patch("src.models.esg_classifier._load_pipeline") as mock_pipe:
        mock_pipe.return_value = MagicMock(return_value=mock_result)
        label, conf = classify("Carbon emissions increased sharply")
    assert label in {"Environmental", "Social", "Governance", "None"}


def test_classify_batch_empty():
    result = classify_batch([])
    assert result == []


def test_classify_batch_length():
    texts = ["pollution fines", "labor dispute", "board fraud"]
    mock_results = [
        [{"label": "Environmental", "score": 0.9}],
        [{"label": "Social", "score": 0.85}],
        [{"label": "Governance", "score": 0.88}],
    ]
    with patch("src.models.esg_classifier._load_pipeline") as mock_pipe:
        mock_pipe.return_value = MagicMock(return_value=mock_results)
        results = classify_batch(texts)
    assert len(results) == 3

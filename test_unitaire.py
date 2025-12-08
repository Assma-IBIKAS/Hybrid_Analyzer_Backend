import pytest
from unittest.mock import patch
from hf_service import classify_with_hf
from gemini_service import call_gemini


@patch("hf_service.requests.post")   
def test_hf(mock_hf):
    mock_hf.return_value.json.return_value = [{"label": "Sport", "score": 0.85}]
    res = classify_with_hf("j'aime le Football",["Colture","Sport","Tourisme"])
    cat = res[0]["label"]
    score = res[0]["score"]
    assert isinstance(res,list)
    assert cat == "Sport"
    assert score > 0.5


@patch("gemini_service.genai.client.Models.generate_content")
def test_gemini(mock_gemini):
    summary_text = "Hello Tamanalt !!"
    tone = "Positive"
    mock_gemini.return_value.text = f'{{"summary": "{summary_text}", "tone": "{tone}"}}'
    res = call_gemini("How are u today Tamanalt !!!","Colture")

    assert summary_text in str(res)
    assert tone in str(res)


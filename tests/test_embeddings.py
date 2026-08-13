# pyrefly: ignore [missing-import]
from embeddings.embedding_model import get_embedding_model


def test_embedding_model():

    model = get_embedding_model()

    vector = model.embed_query(
        "What is artificial intelligence?"
    )

    assert vector is not None
    assert len(vector) > 0
from loaders.text_splitter import split_text


def test_text_is_split():

    text = "This is a test document. " * 200

    chunks = split_text(text)

    assert len(chunks) > 1


def test_empty_text_is_rejected():

    try:

        split_text("")

        assert False

    except ValueError:

        assert True


def test_chunks_are_not_empty():

    text = "This is a test document. " * 100

    chunks = split_text(text)

    assert all(
        chunk.strip()
        for chunk in chunks
    )
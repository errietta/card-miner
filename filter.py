"""Not sure why Tagger is not found by pylint."""

from fugashi import Tagger  # pylint: disable=no-name-in-module
import logging

logger = logging.getLogger(__name__)


def extract_vocab(sentences):
    """
    Extracts a set of vocabulary words from a list of sentences, filtering by
    part of speech. Excludes words that are numbers.

    This function uses a morphological tagger to analyze each sentence and
    extracts words whose part of speech is either noun ("名詞"), verb ("動詞"), or
    adjective ("形容詞").  For each matching word, the lemma (base form) is added
    to the vocabulary set if available; otherwise, the surface form is used.

    Args: sentences (Iterable[str]): A list or iterable of sentences to process.

    Returns: set: A set of unique vocabulary words (lemmas or surface forms)
    matching the allowed parts of speech.
    """
    # Nouns, verbs, and adjectives
    allowed_pos = ("名詞", "動詞", "形容詞")
    # Exclulude numbers and proper nouns
    excluded_pos2 = ("数", "数詞", "固有名詞")
    # Exclude foreign words and symbols
    excluded_goshu = ("外", "記号")
    tagger = Tagger()
    vocab = set()
    for sentence in sentences:
        for word in tagger(sentence):
            pos = word.feature.pos1
            if (
                pos in allowed_pos
               and word.feature.pos2 not in excluded_pos2
               and word.feature.goshu not in excluded_goshu
            ):
                logger.debug(f"Word: {word.surface}, feature {word.feature}")
                # Use lemma if available (for base form comparison)
                vocab.add(word.feature.lemma or word.surface)
    return vocab


def filter_sentences_by_new_words(new_sentence_list, existing_sentence_list):
    """
    Filters sentences from new_sentence_list that contain words not present in
    existing_sentence_list. Also returns the new words found in each sentence.

    Args: new_sentence_list (list of str): List of sentences to filter.
    existing_sentence_list (list of str): List of sentences representing known
    vocabulary.

    Returns: list of tuples: Each tuple contains (sentence, set of new words)
    where the set contains words in the sentence not found in the vocabulary
    extracted from existing_sentence_list.
    """
    known_vocab = extract_vocab(existing_sentence_list)
    results = []
    for sentence in new_sentence_list:
        sentence_vocab = extract_vocab([sentence])
        new_words = sentence_vocab - known_vocab
        if new_words:
            results.append((sentence, new_words))
    return results

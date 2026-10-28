
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Locate the knowledge document
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base" / "troubleshooting.txt"


def load_knowledge():
    """Load and split the knowledge document into topic sections."""
    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {KNOWLEDGE_FILE}"
        )

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    sections = []
    current_section = []

    for line in text.splitlines():
        if line.strip().startswith("TOPIC:"):
            if current_section:
                sections.append("\n".join(current_section))
            current_section = [line]
        elif current_section:
            current_section.append(line)

    if current_section:
        sections.append("\n".join(current_section))

    return [section for section in sections if section.strip()]


def search_knowledge(question, top_k=2):
    """Return the most relevant troubleshooting sections."""
    documents = load_knowledge()

    if not question.strip():
        return []

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    document_vectors = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])

    scores = cosine_similarity(
        question_vector,
        document_vectors
    )[0]

    # Rank documents from most relevant to least relevant
    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_k]:
        if scores[index] > 0:
            results.append({
                "topic": documents[index].splitlines()[0],
                "score": round(float(scores[index]), 3),
                "content": documents[index]
            })

    return results


if __name__ == "__main__":
    print("TraceBack AI - Knowledge Retrieval Test")
    print("--------------------------------------")

    question = input("Enter a troubleshooting question: ")

    results = search_knowledge(question)

    if results:
        for number, result in enumerate(results, start=1):
            print(f"\nResult {number}: {result['topic']}")
            print(f"Relevance score: {result['score']}")
            print(result["content"])
    else:
        print("\nNo relevant information found in the knowledge base.")

# import re
# import numpy as np
# from sentence_transformers import SentenceTransformer


# model = SentenceTransformer("all-MiniLM-L6-v2")


# def split_sentences(text):
#     return re.split(r'(?<=[.!?])\s+', text.strip())


# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# def semantic_chunk(
#     text,
#     percentile=90,
#     min_sentences=2,
#     max_sentences=12
# ):
#     sentences = split_sentences(text)

#     if len(sentences) <= min_sentences:
#         return [text]

#     # 1. Embed every sentence
#     embeddings = model.encode(
#         sentences,
#         normalize_embeddings=True
#     )

#     # 2. Similarity between neighboring sentences
#     similarities = []

#     for i in range(len(embeddings) - 1):
#         similarity = cosine_similarity(
#             embeddings[i],
#             embeddings[i + 1]
#         )
#         similarities.append(similarity)

#     # 3. Find unusually large semantic jumps
#     # Convert similarity -> distance
#     distances = 1 - np.array(similarities)

#     threshold = np.percentile(distances, percentile)

#     # 4. Create chunks
#     chunks = []
#     current = []

#     for i, sentence in enumerate(sentences):
#         current.append(sentence)

#         is_last = i == len(sentences) - 1

#         if is_last:
#             chunks.append(" ".join(current))
#             break

#         semantic_break = distances[i] >= threshold
#         too_large = len(current) >= max_sentences

#         # Don't create tiny chunks
#         enough_sentences = len(current) >= min_sentences

#         if (semantic_break and enough_sentences) or too_large:
#             chunks.append(" ".join(current))
#             current = []

#     return chunks


# text = """
# Python is a programming language widely used for data science.
# It has a large ecosystem of numerical and machine learning libraries.
# NumPy and pandas are particularly popular.

# The Pacific Ocean is the largest ocean on Earth.
# It covers more than one-third of the Earth's surface.
# Its geography includes thousands of islands.
# """

# chunks = semantic_chunk(text)

# for i, chunk in enumerate(chunks):
#     print(f"\n--- CHUNK {i} ---")
#     print(chunk)



from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode([
    "What is subscriber provisioning?",
    "How does subscriber registration work?"
])

print(embeddings.shape)
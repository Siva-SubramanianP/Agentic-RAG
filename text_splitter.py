from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def structure_aware_recursive_chunk(
    markdown_text: str,
    document_name: str,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
):
    # """
    # Split Markdown into structure-aware, recursively sized chunks.

    # Parameters
    # ----------
    # markdown_text : str
    #     Input Markdown document.
    # document_name : str
    #     Name of the source document.
    # chunk_size : int
    #     Maximum chunk size in characters.
    # chunk_overlap : int
    #     Overlap between chunks.

    # Returns
    # -------
    # list[dict]
    #     Chunks with text and metadata.
    # """

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
            ("####", "h4"),
        ],
        strip_headers=False,
    )

    sections = header_splitter.split_text(markdown_text)
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",  # paragraph
            "\n",    # line
            ". ",    # sentence
            " ",     # word
            "",      # character fallback
        ],
        length_function=len,
    )

    chunks = []
    for section in sections:

        section_chunks = recursive_splitter.split_documents(
            [section]
        )

        for chunk in section_chunks:

            metadata = {
                **chunk.metadata,
            }

            chunks.append({
                "text": chunk.page_content,
                "metadata": metadata,
            })
    return chunks


# # -------------------------------------------------------------
# # Example
# # -------------------------------------------------------------

# markdown = """
# # Machine Learning

# Machine learning allows computers to learn patterns from data.

# ## Supervised Learning

# Supervised learning uses labeled training data.

# ### Classification

# Classification predicts discrete categories such as spam or not spam.

# ### Regression

# Regression predicts continuous numerical values such as house prices.

# ## Unsupervised Learning

# Unsupervised learning works with unlabeled data.

# ### Clustering

# Clustering groups similar observations together.
# """

# chunks = structure_aware_recursive_chunk(
#     markdown_text=markdown,
#     document_name="machine_learning.md",
#     chunk_size=500,
#     chunk_overlap=75,
# )

# for chunk in chunks:
#     print("=" * 80)
#     print("ID:", chunk["metadata"]["chunk_id"])
#     print("Metadata:", chunk["metadata"])
#     print(chunk["text"])
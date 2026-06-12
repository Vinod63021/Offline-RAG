from langchain.schema import Document


def hierarchical_chunk_documents(
    documents,
    max_chunk_size=1200
):

    chunks = []

    for doc in documents:

        text = doc.page_content

        metadata = doc.metadata.copy()

        sections = text.split("\n\n")

        current_chunk = ""

        for section in sections:

            section = section.strip()

            if not section:
                continue

            if (
                len(current_chunk)
                + len(section)
                + 2
                <= max_chunk_size
            ):

                current_chunk += (
                    section + "\n\n"
                )

            else:

                if current_chunk.strip():

                    chunks.append(
                        Document(
                            page_content=current_chunk.strip(),
                            metadata=metadata
                        )
                    )

                current_chunk = (
                    section + "\n\n"
                )

        if current_chunk.strip():

            chunks.append(
                Document(
                    page_content=current_chunk.strip(),
                    metadata=metadata
                )
            )

    return chunks
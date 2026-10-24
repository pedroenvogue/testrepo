def WeightedZoneForMoreThanTwoTerms(query_terms, weights, posting_lists):
    # posting_lists: a list of postings lists, one for each query term
    # scores: array to hold scores for documents
    scores = {}

    # Initialize pointers for each posting list
    pointers = [0] * len(posting_lists)
    # Get the first document ID for each list
    current_docs = [posting_lists[i][pointers[i]][0] if pointers[i] < len(posting_lists[i]) else None for i in range(len(posting_lists))]

    while all(doc_id is not None for doc_id in current_docs):
        # Find the maximum document ID among the current ones
        max_doc = max(current_docs)

        # Check if all current documents have the same ID (i.e., max_doc == min_doc)
        min_doc = min(current_docs)
        if max_doc == min_doc:
            # Document contains all terms
            doc_id = max_doc
            # Retrieve and sum zone contributions for this document
            doc_score = 0
            for i in range(len(posting_lists)):
                # Assuming posting is (doc_id, zone_contribution)
                zone_contrib = posting_lists[i][pointers[i]][1]
                doc_score += weights[i] * zone_contrib
            scores[doc_id] = doc_score

            # Advance all pointers
            for i in range(len(posting_lists)):
                pointers[i] += 1
                if pointers[i] < len(posting_lists[i]):
                    current_docs[i] = posting_lists[i][pointers[i]][0]
                else:
                    current_docs[i] = None
        else:
            # Advance pointers for lists with doc_id less than max_doc
            for i in range(len(posting_lists)):
                if current_docs[i] is not None and current_docs[i] < max_doc:
                    pointers[i] += 1
                    if pointers[i] < len(posting_lists[i]):
                        current_docs[i] = posting_lists[i][pointers[i]][0]
                    else:
                        current_docs[i] = None

    return scores
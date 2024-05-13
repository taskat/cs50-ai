import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if len(corpus[page]) == 0:
        return {key: 1 / len(corpus) for key in corpus.keys()}
    next = dict()
    for key in corpus.keys():
        next[key] = (1 - damping_factor) / len(corpus)
    possible = corpus[page]
    for key in possible:
        next[key] += damping_factor / len(possible)
    return next


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = {key: 0 for key in corpus.keys()}
    current = random.choice(list(corpus.keys()))
    counter = 1
    while counter <= n:
        samples[current] += 1
        model = transition_model(corpus, current, damping_factor)
        current = random.choices(list(model.keys()), weights=model.values(), k=1)[0]
        counter += 1
    for key in samples.keys():
        samples[key] /= n
    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {key: 1 / len(corpus) for key in corpus.keys()}
    while True:
        new_ranks = {key: (1 - damping_factor) / len(corpus) for key in corpus.keys()}
        for key in corpus.keys():
            neighbors = corpus[key]
            if len(neighbors) == 0:
                neighbors = corpus.keys()
            for neighbor in neighbors:
                new_ranks[neighbor] += damping_factor * ranks[key] / len(neighbors)
        if max_change(ranks, new_ranks) < 0.001:
            break
        ranks = new_ranks
    return new_ranks


def max_change(old, new):
    changes = []
    for key in old.keys():
        changes.append(abs(old[key] - new[key]))
    return max(changes)


if __name__ == "__main__":
    main()

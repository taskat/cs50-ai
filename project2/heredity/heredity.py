import csv
import itertools
import math
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probabilities = []
    for person in people.keys():
        trait = person in have_trait
        gene_count = number_of_genes(person, one_gene, two_genes)
        if people[person]["father"] is None:
            probabilities.append(PROBS["gene"][gene_count] * PROBS["trait"][gene_count][trait])
            continue
        mother_gene = number_of_genes(people[person]["mother"], one_gene, two_genes)
        father_gene = number_of_genes(people[person]["father"], one_gene, two_genes)
        from_mother_0 = from_parent(mother_gene, 0)
        from_father_0 = from_parent(father_gene, 0)
        from_mother_1 = from_parent(mother_gene, 1)
        from_father_1 = from_parent(father_gene, 1)
        gene_probability = 0
        if gene_count == 0:
            gene_probability = from_mother_0 * from_father_0
        elif gene_count == 1:
            gene_probability = from_father_0 * from_mother_1 + from_father_1 * from_mother_0
        elif gene_count == 2:
            gene_probability = from_father_1 * from_mother_1
        probabilities.append(gene_probability * PROBS["trait"][gene_count][trait])
    return math.prod(probabilities)


def from_parent(parent_genes, passed):
    """
    Returns the probability of getting passed number of genes (from that parent) if the parent has parent_genes
    """
    if passed == 0:
        if parent_genes == 0:
            return 1 - PROBS["mutation"]
        if parent_genes == 1:
            return 0.5
        return PROBS["mutation"]
    if parent_genes == 0:
        return PROBS["mutation"]
    if parent_genes == 1:
        return 0.5
    return 1 - PROBS["mutation"]


def number_of_genes(name, one_gene, two_genes):
    """
    Returns the number of genes the given people have
    """
    if name in one_gene:
        return 1
    elif name in two_genes:
        return 2
    return 0


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        genes = number_of_genes(person, one_gene, two_genes)
        trait = person in have_trait
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        prob_sum = sum(probabilities[person]["gene"].values())
        probabilities[person]["gene"] = {key: value / prob_sum for key,
                                         value in probabilities[person]["gene"].items()}
        trait_sum = sum(probabilities[person]["trait"].values())
        probabilities[person]["trait"] = {key: value / trait_sum for key,
                                          value in probabilities[person]["trait"].items()}


if __name__ == "__main__":
    main()

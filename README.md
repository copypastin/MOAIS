
## Measure of Artificial Intelligence Similarity 🗿 (MOAIS) 

MOAIS is a tool designed to detect the similarity between automated code snippets and human-written code. This project is inspired by Stanford's Measure of Software Similarity (MOSS), which aims to automatically detect software plagiarism.

See the original MOSS paper for more details:

> (https://theory.stanford.edu/~aiken/moss/)
> (https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf)


#### How does it work?

    *In short...*

    1. MOAIS takes a programming assignment and rubric as input.
    2. It uses AI to generate hundreds of variations of solutions to the problem.
    3. These generated solutions are then compared against the student-written code to assess similarity.

    *In detail...*

    - MOAIS leverages the GitHub Copilot CLI to generate code snippets based on the provided programming assignment and rubric.
        - Additionally, prompts are also designed to push for more unique responses.
    - Using these generated snippets, MOAIS creates a comprehensive dataset of potential solutions.
    - MOAIS uses the Winnowing algorithm to break code snippets into hashes.
    - These hashes are then compared using Jaccard Similarity Index to identify similarities and potential plagiarism through similarities in code structure and logic.


#### Theories to be tested

- AI-generated code can be used as a benchmark to evaluate the originality of student submissions as they follow similar patterns and structures.
- Monte Carlo methods can be employed to estimate the distribution of similarities between code snippets.

#### Installation Requirements

- Python 3.8 or higher (and packages listed in requirements.txt)
- Copilot CLI
- GitHub CLI


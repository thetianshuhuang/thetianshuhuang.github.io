---
hide:
- navigation
---

# Tianshu Huang / **Open Source Portfolio**

<div style="width: 100%; display: grid; gap: 5px; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));">
    <img src="/assets/research/red_rover.jpg">
    <img src="/assets/research/abstract_dataloader.png">
    <img src="/assets/research/iq1m.png">
</div>

Since my research interests focus on *nonstandard* problems which are generally difficult for a human to interpret &mdash; and sanity-check, my research philosophy places a strong emphasis on writing modular, auditable code. As domains like radar spectrum and computer systems lie outside of the machine learning mainstream, tackling these problems also requires a substantial engineering investment in novel infrastructure for data collection, processing, and experimentation.

Some particular up-and-coming[^0] technologies for the python-ML ecosystem which I believe in strongly include:

[^0]: Tools like `uv`, `ruff`, `mkdocs`, `mkdocstrings` are already de-facto standards for new projects, and don't need any promoting.

??? success "**Type Annotations & Type Checking**"

    Between the core python language type specification, now-standard static type checking with tools like [pyright](https://github.com/Microsoft/pyright), array annotation with [jaxtyping](https://docs.kidger.site/jaxtyping/), and runtime type checking with [beartype](https://github.com/beartype/beartype), the python [gradual typing](http://scheme2006.cs.uchicago.edu/13-siek.pdf) [playbook](https://peps.python.org/pep-0484/) has just about gotten to the point where it can cover the majority of machine learning use cases.

    - Rigorous adherence to type annotation and type checking best practices eliminates many common classes of bugs[^1], replacing them with `TypeErrors` which are raised at function boundaries.
    - Python's type system also provides a standardized and mechanically-verifiable way of [describing sensor data types](https://wiselabcmu.github.io/abstract-dataloader/types/).

??? success "**Jax**"

    Compared to it's contemporary competitors Pytorch and Tensorflow, [Jax](https://docs.jax.dev/en/latest/index.html) has an (at least in my view) incredibly elegant and powerful programming model which revolves around functional programming. It's also natively built around a powerful compiler stack which pretty much guarantees that your code will be fast &mdash; if you can get it to compile[^2].

    - Other key benefits including full support for all (un)signed integer, float, and complex types ... [unlike](https://github.com/pytorch/pytorch/issues/125718) [pytorch](https://github.com/pytorch/pytorch/issues/58734).
    - This does come overhead in that functional programming can be difficult to get used to for those without training[^3].

    Unfortunately, due to Pytorch's status as the de-facto standard framework for the community, my current work is all pytorch-based.

[^1]: E.g., `ValueError: shape mismatch` or out-of-memory errors induced by unintended shape broadcasting
[^2]: In this way, Jax is very much the Rust of Machine Learning: it takes some effort to convince the compiler your code can run on a GPU, but if you can do it, you're guaranteed to avoid many types of performance issues that you'd otherwise get on an interpreter-first framework like Pytorch.
[^3]: Fortunately, CMU is a [functional programming school](https://www.cs.cmu.edu/~15150/), so it's no problem finding students here who can handle it!

## Active Projects

My current active projects are centered around the RadarML initiative, which seeks to build a software ecosystem for learning on mmWave radar spectrum.

<div class="grid cards" markdown>

- :material-cube-outline: [`abstract_dataloader`](https://radarml.github.io/abstract-dataloader/)

    ---

    abstract interface for composable dataloaders and preprocessing pipelines

- :material-antenna: `xwr` *(coming soon!)*

    ---

    python interface for collecting raw time signal data from TI mmWave radars

- :material-video-wireless-outline: `red-rover` *(coming soon!)*

    ---

    our "third generation[^4]" radar spectrum data collection system

- :octicons-ai-model-16: `nrdk` *(coming soon!)*

    ---

    the neural radar development kit for deep learning on multimodal radar data

</div>

## Paper Artifacts

<div class="grid cards" markdown>

- :material-sprout: [`beanstalk`](https://github.com/arjunr2/beanstalk)

    ---

    instrumentation & data analysis for [Beanstalk (OOPSLA '25)](https://dl.acm.org/doi/10.1145/3720428)

- :dart: [`dart`](https://wiselabcmu.github.io/dart/)

    ---

    jax-based [implementation](https://github.com/wiselabcmu/dart) & [dataset](https://zenodo.org/records/10938617) for [DART (CVPR '24)](https://wiselabcmu.github.io/dart/)

- :material-weather-windy: [`pitot`](https://github.com/WiseLabCMU/pitot)

    ---

    jax-based implementation and dataset for [Pitot (MLSys '25)](https://arxiv.org/abs/2503.06428)

- :material-flask-round-bottom: [`OptimizerAmalgamation`](https://github.com/VITA-Group/OptimizerAmalgamation)

    ---

    implementation artifact for [Optimizer Amalgamation (ICLR '22)](https://openreview.net/pdf?id=VqzXzA9hjaX)

</div>

---

## Deprecated Projects

<div class="grid cards" markdown>

- :material-video-wireless-outline: [`rover`](https://github.com/wiseLabCMU/rover)

    ---

    our "second generation[^4]" radar spectrum data collection system

- :material-clouds: [`cirrus`](https://github.com/SilverLineFramework/runtime-manager)

    ---

    minimum viable [silverline-compatible](https://ieeexplore.ieee.org/document/11018768) stack for distributed benchmarking

- :material-bookshelf: [`l2o`](https://github.com/thetianshuhuang/l2o)

    ---

    optimization meta-learning framework for Tensorflow 2[^5]

- :material-chart-scatter-plot: [`bmcc`](https://github.com/thetianshuhuang/bmcc)

    ---

    C-accelerated Markov-Chain Monte Carlo implementation for Bayesian Clustering[^6]

</div>

[^4]: "First generation": a non-automated solution using only officially supported TI software; "Second generation": a partially automated and somewhat modular system relying on official TI software, with some custom implementations; "Third generation": a fully automated, modular, and tightly-integrated linux-based data collection system without any TI software dependencies on the data collection computer
[^5]: Jax's functional programming ["differentiation is a higher order function"](https://docs.jax.dev/en/latest/key-concepts.html#transformations) approach makes optimization meta-learning vastly simpler to implement, completely eliminating the need for such a complicated framework.
[^6]: This library has been abandoned since it turns out there is not much demand for Bayesian Clustering algorithms. In particular, these methods are only really suitable for low-dimension (<50) moderate-data (>100, <10000) settings where powerful, fully-automated clustering is required, of which there simply aren't that many.

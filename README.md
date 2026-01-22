# Jupyter Notebooks - Inference & Causality (DLMAIIAC)

This repository contains a small set of **Jupyter notebooks** that illustrate topics from probabilistic modelling and causal inference, including:

* **Causal inference with** [`doWhy`](https://github.com/microsoft/dowhy) (confounding, backdoor adjustment, interventions / the *do*-operator)
* **Bayesian networks** with `pgmpy` (Wet Grass / Sprinkler and the classic “Asia” network)
* **Markov chains** (convergence to the equilibrium / stationary distribution)
* **Bayesian linear regression** with `PyMC3`

Pinned Python dependencies are listed in `requirements.txt`.

## Quickstart

### 1) Create an environment

Using `venv`:

```bash
python -m venv .venv
.
.venv\Scripts\activate
pip install -r requirements.txt
```

Using `conda`:

```bash
conda create -n dlmaiiuk01 python=3.8 -y
conda activate dlmaiiuk01
pip install -r requirements.txt
```

### 2) (Optional) Install Graphviz system packages

Some notebooks render graphs. For that, you may need Graphviz installed on your OS.

* Linux (Debian/Ubuntu):

```bash
sudo apt install graphviz libgraphviz-dev graphviz-dev pkg-config
```

On Windows, install Graphviz (e.g. from https://graphviz.org/download/) and make sure `dot` is available on your `PATH`.

### 3) Start JupyterLab

```bash
jupyter lab
```

## Notebooks (what you can do with them)

* **DoWhyFirstSteps.ipynb**
  * Generate synthetic causal data, define a `CausalModel`, identify the estimand and estimate the **ATE** using linear regression and propensity score methods.

* **doWhy_Confounder.ipynb**
  * Demonstrate a classic **confounding** situation (“sweet spot” artifact) and show that the effect disappears after adjustment.

* **doWhy_CausalDo.ipynb**
  * Work with **interventions** using the *do*-operator: compare outcomes under `do(X=1)` vs `do(X=0)` and compute the ATE.

* **Adjusting_for_confounder_binary_variables.ipynb**
  * Binary treatment with a confounder: compare biased estimation (no confounder) vs adjusted estimation (backdoor methods) and discuss refutation.

* **Adjusting_for_confounder_continuous_variables.ipynb**
  * Continuous treatment and multiple outcomes: estimate effects outcome-by-outcome and run a **placebo refuter** to sanity-check results.

* **Sprinkler.ipynb**
  * Build the Wet Grass Bayesian network (C/S/R/W), define CPTs, and compute posterior probabilities using `pgmpy`’s variable elimination.

* **AsiaBayesNet.ipynb**
  * Load and query the well-known **Asia** Bayesian network (from a BIF file) and run inference with evidence.

* **MCEquilibrium.ipynb**
  * Define a Markov chain transition matrix, iterate states, and observe convergence to the equilibrium distribution.

* **LinearRegressionProbabilistic.ipynb**
  * Bayesian linear regression in **PyMC3**: specify priors, sample the posterior, inspect diagnostics, and visualize uncertainty / credible intervals.

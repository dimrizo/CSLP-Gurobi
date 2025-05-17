# CSLP-Gurobi

## Description

This is a Mixed Integer-Linear Problem (MILP) model for the Charging Stations Location Problem (CSLP) when considering an electric bus public transport network, two types of available chargers (slow and fast) as well as their potential charging scheduling to the chargers that will be installed. This model has been initially presented in the publication by Gkiotsalitis et al., available at the link : https://www.sciencedirect.com/science/article/pii/S0306261924026266
  
## Installation

Before installing the project, ensure you have Python installed on your system (Python 3.6 or newer is recommended). Additionally, you will need Gurobi Optimizer, which requires a license. You can obtain a free academic license or evaluate a commercial license from [Gurobi's website](https://www.gurobi.com).

1. **Install Gurobi:** Follow the instructions on the Gurobi website to install Gurobi and obtain a license. This typically involves downloading Gurobi, installing it, and setting up the license file on your machine.

2. **Set Gurobi Environment Variable:** Ensure the `GRB_LICENSE_FILE` environment variable is set to the path of your Gurobi license file and the Gurobi bin directory is added to your system’s PATH.

3. **Install Gurobi Python Interface:** Once Gurobi is installed, you can install the Gurobi Python interface with pip (that is the Gurobi Python library that is imported in our script).

4. **Clone and Setup Your Project:** Now, clone (or just download) this repository and install the project's dependencies (can be done through the requremets file).

## Installation

To use the code you can just run it as a Python script given that all dependencies are installed. Make sure that you comment in/out all necessary/unnecessary code given the model Use Case example that you want to run (as indicated in the article and Python code).

## Contributing

Contributions to this project are welcome! Here's how you can contribute:

1. Fork the Project
2. Commit your Changes
3. Push to the Branch
4. Open a Pull Request

Please ensure your pull request adheres to the project's coding standards.

## License

This repository is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contact

For any queries or further information, please reach out to any of the authors of the article using the contact details provided there.

## Acknowledgements

The present work is partially funded by the metaCCAZE Project (Flexibly adapted MetaInnovations, use cases, collaborative business and governance models to accelerate deployment of smart and shared Zero Emission mobility for passengers and freight). This project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No. 101139678.

<br>

<img src="https://www.metaccaze-project.eu/wp-content/uploads/2024/02/metaCCAZE-Logo.svg" width="750" height="130">

<br><br>

This work has been supported by the Railways and Transport Laboratory at the National Technical University of Athens (NTUA).
Find more information at the link: http://railwaysandtransportlab.civil.ntua.gr/

<br>


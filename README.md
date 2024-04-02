# CSLP-Gurobi

## Description

This is a Mixed Integer-Linear Problem (MILP) model for the Charging Stations Location Problem (CSLP) when considering a public transport network operated by Electric Busses. This model has been initally presented in the publication by Gkiotsalitis et al., available at the link : (LINK TO BE ADDED HERE)
  
## Installation

Before installing the project, ensure you have Python installed on your system (Python 3.6 or newer is recommended). Additionally, you will need Gurobi Optimizer, which requires a license. You can obtain a free academic license or evaluate a commercial license from [Gurobi's website](https://www.gurobi.com).

1. **Install Gurobi:** Follow the instructions on the Gurobi website to install Gurobi and obtain a license. This typically involves downloading Gurobi, installing it, and setting up the license file on your machine.

2. **Set Gurobi Environment Variable:** Ensure the `GRB_LICENSE_FILE` environment variable is set to the path of your Gurobi license file and the Gurobi bin directory is added to your system’s PATH.

3. **Install Gurobi Python Interface:** Once Gurobi is installed, you can install the Gurobi Python interface by running:

4. **Clone and Setup Your Project:** Now, clone this repository and install the project's dependencies.
    bash
    Copy code
    git clone https://github.com/dimrizo/CSLP-Gurobi
    cd CSLP-Gurobi
    pip install -r requirements.txt

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

This work was partially funded by the European Union's Horizon Europe research and innovation programme metaCCAZE (Grant Agreement no ----).
Find more information at the link: https://www.metaccaze-project.eu/

<br>

<img src="https://www.metaccaze-project.eu/wp-content/uploads/2024/02/metaCCAZE-Logo.svg" width="664" height="150">

<br><br>

This work has been suppored by the Railways and Transport Laboratory at the National Technical Univerity of Athens (NTUA).
Find more information at the link: https://railwaysandtransportlab.civil.ntua.gr/

<br>

<img src="https://railwaysandtransportlab.civil.ntua.gr/wp-content/uploads/2023/04/RTLab_logo-1-1024x372.png" width="470" height="170">

<br>


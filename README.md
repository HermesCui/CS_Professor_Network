
# Academic Network Visualization Script

This script allows you to input the URLs of professors from DBLP (https://dblp.org/) and generates a network graph with their 1-depth coauthors from 2020s to current record. The resulting graph visualizes the collaborative relationships between these professors and their coauthors.

## Setup

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- The required Python packages

### Installation

1. Clone the repository or download the script.
2. Navigate to the directory containing the script.
3. Install the required packages using pip:

```bash
pip install requests beautifulsoup4 networkx matplotlib
```

## Usage

1. **Edit the script to include the desired professor URLs:**

   Update the `professor_urls` dictionary in the script to include the URLs of the professors you want to analyze. For example:

   ```python
   professor_urls = {
         "[ProfessorName]": "[dplp_url]",
   }
   ```

2. **Run the script:**

   Execute the script in your terminal:

   ```bash
   python academic_network.py
   ```

3. **View the output:**

   The script will generate a network graph and save it as `full_network.png` in the current directory. 


## License

This project is licensed under the MIT License.



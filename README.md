# scs-dlc-date-predictor
A small Python script that predicts the announcement and release dates of SCS Software DLCs (for American Truck Simulator and Euro Truck Simulator 2) based on when the related Steam achievements are added.

The prediction is calculated from historical data of previous DLCs, using average time intervals between:
- the addition of Steam achievements,
- the reveal date of the release date,
- and the actual release date.



## Example Output

In the console :

=== Estimation for the DLC Nordic Horizons ===\
Achievements added: 23 October 2025\
Estimated reveal date (average): 07 November 2025\
Estimated release date (average): 01 December 2025\
Estimated release date (nearest Thursday): 04 December 2025

Charts generated : 

*partie à adapter* 

## Requirements

- **Python 3.8+**
- Libraries:
  - `matplotlib` (for chart display)
  - `statistics` *(standard library)*
  - `datetime` *(standard library)*

Install dependencies with:

```bash
pip install matplotlib
```

## Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/lucasrecan/scs-dlc-date-predictor.git
    cd scs-dlc-date-predictor
    ```
2. Run the script
    ```bash
    python main.py
    ```
3. The script will print estimated dates in the console and open multiple charts comparing the timing of past DLCs.

*partie à adapter* 

## Notes

This project is **purely for fun** and based on empirical patterns from previous SCS DLC releases.  
It is **not affiliated with or endorsed by SCS Software**.


## License

This project is released under the **MIT License**.  
Feel free to reuse or modify the code.

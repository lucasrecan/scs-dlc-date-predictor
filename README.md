# scs-dlc-date-predictor
A small Python script that predicts the announcement and release dates of SCS Software DLCs (for American Truck Simulator and Euro Truck Simulator 2) based on when the related Steam achievements are added.

The prediction is calculated from historical data of previous DLCs, using average time intervals between:
- the addition of Steam achievements,
- the reveal date of the release date,
- and the actual release date.



## Example Output
```
Type q to quit at any time.
--------------------------------------------------------------------
Select the game you want to analyze.
1. Euro Truck Simulator 2
2. American Truck Simulator
Choose a number > 1
--------------------------------------------------------------------
1. Show average delays between success addition and reveal/release
2. Show historical delays for each released DLC in a timeline graph
3. Show evolution of delays between steps in a different graph
4. Predict dates for the next DLC (if its successes were added)
5. Go back
Choose a number > 4
--------------------------------------------------------------------
Next DLC name: Nordic Horizons
Date of success addition (format DD/MM/YYYY): 23/10/2025

=== Estimate for Nordic Horizons if delays are the same as Greece (last release) ===
Success addition: 23 October 2025
Estimated reveal date: 10 November 2025
Estimated release date: 25 November 2025
Estimated release (closest Thursday): 27 November 2025

=== Estimate for Nordic Horizons based on averages ===
Success addition: 23 October 2025
Average reveal date: 14 November 2025
Average release date: 26 November 2025
Average release (closest Thursday): 27 November 2025
--------------------------------------------------------------------

Press Enter to continue...
--------------------------------------------------------------------
1. Show average delays between success addition and reveal/release
2. Show historical delays for each released DLC in a timeline graph
3. Show evolution of delays between steps in a different graph
4. Predict dates for the next DLC (if its successes were added)
5. Go back
Choose a number > 1
Average delay success → reveal: 22 days
Average delay success → release: 34 days
```
Charts generated : 

![chronologie](chrolonogie_ex.png)
![evolution](evolution_ex.png)

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

## Notes

This project is **purely for fun** and based on empirical patterns from previous SCS DLC releases.  
It is **not affiliated with or endorsed by SCS Software**.


## License

This project is released under the **MIT License**.  
Feel free to reuse or modify the code.

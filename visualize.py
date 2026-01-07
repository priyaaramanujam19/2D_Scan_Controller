import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from config import load_yaml_file
config = load_yaml_file()
def csv_to_heatmap_array(filename, x_steps, y_steps):
    df = pd.read_csv(filename)
    
    # Only keep first x_steps * y_steps rows and ignore summary rows(peak detection details)
    num_scan_points = x_steps * y_steps
    df = df.iloc[:num_scan_points]
    
    # Convert to numeric, keeping NaNs for failed points
    df["filtered_value"] = pd.to_numeric(df["filtered_value"], errors='coerce')
    
    values = df["filtered_value"].values
    heatmap = np.full((y_steps, x_steps), np.nan)
    
    i = 0
    for y in range(y_steps):
        row_indices = range(x_steps) if y % 2 == 0 else reversed(range(x_steps))
        for x in row_indices:
            heatmap[y][x] = values[i] if i < len(values) else np.nan
            i += 1
    
    return heatmap

def plot_and_save_heatmap(data_array, output_file, cmap="Reds", show_plot=False):
    im = plt.imshow(data_array, cmap=cmap, origin="lower", interpolation="none",
                    vmin=np.nanmin(data_array), vmax=np.nanmax(data_array))
    im.cmap.set_bad(color='black')  # Failed points in black
    plt.colorbar(im, label="Filtered Sensor Value")
    plt.title("2D Scan Heatmap")
    plt.xlabel("X Step")
    plt.ylabel("Y Step")
    plt.savefig(output_file)
    if show_plot == True: # Displays the plot in jupyter notebook when the function is called
        plt.show()
    plt.close()

if __name__ == "__main__":
    heatmap_array = csv_to_heatmap_array(
        filename=config["output_csv"],
        x_steps=config["x_range"]["steps"],
        y_steps=config["y_range"]["steps"]
    )
    plot_and_save_heatmap(heatmap_array, config["heatmap_output"], cmap="Reds")

# ----------------------------------------------------------------------------------------------------
# HJC
# IESDMC
# 2024-12-11
# ver1.0
# ----------------------------------------------------------------------------------------------------
import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy import read
from datetime import datetime



def plot_mseeds(DataFile, sync_time=False):
    """
    Plots mseed files dynamically based on their count.
    Each subplot represents one mseed file, and multiple waveforms in the same file are plotted together.
    If sync_time is True, all subplots share the same time axis.
    """
    num_files = len(DataFile)
    if num_files == 0:
        print("Error: No mseed files provided.")
        sys.exit(1)

    elif num_files > 6:
        print("Error: Too many mseed files. Maximum allowed is 6.")
        sys.exit(1)

    # Prepare figure with (n, 1) layout
    fig, axes = plt.subplots(num_files, 1, figsize=(12, num_files * 2), squeeze=False)
    axes = axes.flatten()

    # Determine global start and end times if sync_time is enabled
    global_start, global_end = None, None
    if sync_time:
        global_start = min(tr.stats.starttime for mseed in DataFile for tr in read(mseed))
        global_end = max(tr.stats.endtime for mseed in DataFile for tr in read(mseed))

    for i, mseed_file in enumerate(DataFile):
        try:
            st = read(mseed_file)  # Read the mseed file
            ax = axes[i]

            # Determine local start and end times
            local_start = min(tr.stats.starttime for tr in st)
            local_end = max(tr.stats.endtime for tr in st)

            # Check if the time range exceeds 7 days
            if (local_end - local_start) > 7*24*3600:
                print(f"Error: File {mseed_file} exceeds 7-day length limit.")
                sys.exit(1)

            start_time = global_start if sync_time else local_start
            end_time = global_end if sync_time else local_end

            for tr in st:
                # Generate time data for plotting
                times = tr.times("matplotlib")
                data = tr.data
                ax.plot(times, data, label=f"{tr.stats.station}.{tr.stats.channel}.{tr.stats.network}.{tr.stats.location}", linewidth=0.8)
            
            # Set x-axis limits to remove empty space
            ax.set_xlim(mdates.date2num(local_start.datetime), mdates.date2num(local_end.datetime))

            # Set legends
            ax.legend(loc="upper right", fontsize=8)
            ax.grid()

           # Adjust x-axis ticks: 7 points
            total_time = end_time - start_time
            time_ticks = [start_time + i * total_time / 6 for i in range(7)]
            tick_labels = []
            last_label_time = None

            # Determine the format for the x-axis labels
            for tick in time_ticks:
                tick_datetime = tick.datetime
                if not last_label_time or tick_datetime.date() != last_label_time.date() or (tick_datetime - last_label_time).total_seconds() >= 600:
                    # Full datetime for the first tick or if it's a new day
                    tick_labels.append(tick_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    # Only time for subsequent ticks on the same day
                    tick_labels.append(tick_datetime.strftime("%H:%M:%S"))
                last_label_time = tick_datetime

            ax.set_xticks(mdates.date2num([t.datetime for t in time_ticks]))
            ax.set_xticklabels(tick_labels)

            # Ensure x and y-axis labels are displayed
            ax.set_ylabel("Amplitude", fontsize=8)
            if i == num_files - 1:
                ax.set_xlabel("Time (UTC)", fontsize=10)

            plt.setp(ax.xaxis.get_majorticklabels())
        except Exception as e:
            print(f"Error reading {mseed_file}: {e}")
            sys.exit(1)

    plt.tight_layout()
    plt.show()


def main():
    # Argument parser to handle options
    parser = argparse.ArgumentParser(description="Plot sac or mseed files with optional synchronized time axis.")
    parser.add_argument("-s", "--synch", action="store_true", help="Synchronize time axis for all plots")
    parser.add_argument("DataFile", nargs="+", help="List of seismic data in sac or mseed format to plot (max 6)")

    args = parser.parse_args()

    if len(args.DataFile) == 0 or len(args.DataFile) > 6:
        print("Error: Provide between 1 and 6 mseed files.")
        sys.exit(1)

    plot_mseeds(args.DataFile, sync_time=args.synch)


if __name__ == "__main__":
    main()


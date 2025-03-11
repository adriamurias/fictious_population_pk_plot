import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import odeint

def dydt(y, t):
    # y[0] represents the variable for exponential growth
    # y[1] represents the variable for bi-exponential decline
    ka = 1.5  # Growth rate
    kb = 1  # Decay rate for the first component of bi-exponential decline
    kc = 0.6
    dydt1 = -ka * y[0]  # absorption compartment
    dydt2 = ka * y[0] - kb * y[1] - kc * y[1]  # central compartment
    return [dydt1, dydt2]

F = 1
D0 = 500

# Initial conditions
y0 = [F * D0, 0]  # Initial values for the two variables

# Time points
points_number = 100
t = np.linspace(0, 5, points_number)  # 40 time points

# Solving the ODE
y = odeint(dydt, y0, t)

# Create dataframe
df = pd.DataFrame({'t': t, 'y': y[:, 1]})

# Update rcParams for font
plt.rcParams.update({'font.family': 'Arial'})

fig, ax = plt.subplots(1, 1)

cm = sns.color_palette("PuBu", 4)

# Simulate and add points with different confidence intervals manually
for ix, ci in enumerate(range(20, 100, 20)):
    # Simulate wider confidence interval
    scale = ci / 2  # Adjust the denominator to make the intervals wider or narrower
    y_upper = df['y'] + scale
    y_lower = df['y'] - scale
    ax.fill_between(df['t'], y_lower, y_upper, color=cm[ix], alpha=0.3, label=f'{ci}')


# Base line plot
sns.lineplot(data=df, x="t", y="y", ax=ax, errorbar=None, color="black", label='Median')

# Generate fewer simulated points within the confidence interval
simulated_points_number = 100  # Reduced number of simulated points
t_simulated = np.random.choice(df['t'], size=simulated_points_number, replace=True)
y_simulated_lower = np.interp(t_simulated, df['t'], y_lower)
y_simulated_upper = np.interp(t_simulated, df['t'], y_upper)
simulated_points = np.random.uniform(low=y_simulated_lower, high=y_simulated_upper, size=(simulated_points_number,))

# Scatter plot for the data points without legend entry
ax.scatter(t_simulated, simulated_points, color='purple', s=5, zorder=5)
    
# Remove the top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Increase thickness of axis lines
ax.spines['bottom'].set_linewidth(3)
ax.spines['left'].set_linewidth(3)

# Add axis labels
ax.set_xlabel('Time', fontsize=18, fontstyle='italic')
ax.set_ylabel('Concentration', fontsize=18, fontstyle='italic')

# Only show ticks on the left and bottom spines
ax.yaxis.tick_left()
ax.xaxis.tick_bottom()

# Set the number of ticks on both axes to 5
# ax.set_xticks(np.linspace(t.min(), t.max(), 5))
# # Manually set the limits for the y-axis to ensure even distribution of ticks
# y_min, y_max = df['y'].min() - 20 / 4, df['y'].max() + 80 / 4  # Adjust for maximum CI
# ax.set_ylim(y_min, y_max)


# Remove the numbers from the axes
ax.set_xticklabels([])
ax.set_yticklabels([])

# Make the ticks slightly longer
ax.tick_params(axis='both', length=10)  # Increase the length of ticks

# Create custom legend
handles, labels = ax.get_legend_handles_labels()
handles.append(ax.scatter([], [], color='purple', s=5))
labels.append('Observed data')
ax.legend(handles=handles, labels=labels)

#plt.legend()
plt.savefig("fictious_pop_pk_plot.png", dpi=300)
plt.show()

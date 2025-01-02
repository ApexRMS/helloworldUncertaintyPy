from osgeo import gdal

# Load SyncroSim python package
import pysyncrosim as ps

# Load numpy and pandas
import numpy as np
import pandas as pd

# Get the SyncroSim Scenario that is currently running
myScenario = ps.Scenario()

# Load Run Control Datasheet to set timesteps
run_settings = myScenario.datasheets(name="helloworldUncertaintyPy_RunControl")

# Set timesteps
timesteps = np.array(range(run_settings.MinimumTimestep.item(),
                           run_settings.MaximumTimestep.item() + 1))

# Load Scenario's input Datasheet from SyncroSim Library into DataFrame
my_input_dataframe = myScenario.datasheets(name="helloworldUncertaintyPy_InputDatasheet")

# Extract model inputs from Input DataFrame
m_mean = my_input_dataframe.mMean.item()
m_sd = my_input_dataframe.mSD.item()
b = my_input_dataframe.b.item()

# Set up empty pandas DataFrame to accept output values
my_output_dataframe = myScenario.datasheets(name="helloworldUncertaintyPy_OutputDatasheet")

# For loop through iterations
for i in range(1, run_settings.MaximumIteration.item() + 1):
    
    # Extract a slope value from normal distribution
    m = np.random.normal(loc=m_mean, scale=m_sd)
    
    # Do calculations
    y = m * timesteps + b

    # Store relevant output in temporary data frame
    temp_data_frame = pd.DataFrame({"Timestep": timesteps,
                                    "Iteration": [i] * len(y),
                                    "y": y})

    # Append temporary data frame to output data frame
    my_output_dataframe = pd.concat([my_output_dataframe, temp_data_frame])

# Save the output DataFrame to the Scenario output Datasheet
myScenario.save_datasheet(name="helloworldUncertaintyPy_OutputDatasheet",
                          data=my_output_dataframe)

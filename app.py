import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from processor import calculate_power_spectrum


def main():
    st.title("Time Series to Power Spectrum Analyzer")
    
    # Sidebar for parameters
    st.sidebar.header("Parameters")
    sample_rate = st.sidebar.number_input(
        "Sampling Rate (Hz)",
        min_value=1.0,
        value=100.0,
        help="Number of samples per second in your data"
    )
    
    
    # File upload
    st.header("Upload Time Series Data")
    st.write("Upload a file with your time series data. The file should have a column or array containing the time series values.")
    
    # Define accepted file types
    accepted_types = ["csv", "json", "bin", "txt"]
    uploaded_file = st.file_uploader("Choose a file", type=accepted_types)
    
    if uploaded_file is not None:
        try:
            # Load data based on file type
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if file_type == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_type == 'json':
                df = pd.read_json(uploaded_file)
            elif file_type == 'bin':
                # Read binary file as numpy array
                data = np.frombuffer(uploaded_file.read())
                df = pd.DataFrame({'values': data})
            elif file_type == 'txt':
                df = pd.read_csv(uploaded_file, header=None, names=['values'])
                
            # Column selection
            st.header("Select Data Column")
            data_column = st.selectbox(
                "Choose the column containing your time series data",
                options=df.columns
            )
            
            # Display raw data
            st.subheader("Raw Time Series Data")
            fig_raw = go.Figure()
            fig_raw.add_trace(go.Scatter(
                y=df[data_column],
                mode='lines',
                name='Raw Data'
            ))
            fig_raw.update_layout(
                xaxis_title="Sample Number",
                yaxis_title="Amplitude",
                showlegend=True
            )
            st.plotly_chart(fig_raw)
            
            
            if st.button("Calculate Power Spectrum"):
                # Calculate and display power spectrum
                freqs, power = calculate_power_spectrum(df[data_column].values, sample_rate)
            
                st.subheader("Power Spectrum")
                fig_spectrum = go.Figure()
                fig_spectrum.add_trace(go.Scatter(
                    x=freqs,
                    y=power,
                    mode='lines',
                    name='Power Spectrum'
                ))
                fig_spectrum.update_layout(
                    xaxis_title="Frequency (Hz)",
                    yaxis_title="Power",
                    showlegend=True
                )
                st.plotly_chart(fig_spectrum)
                
                # Add download button for spectrum data
                spectrum_df = pd.DataFrame({
                    'Frequency_Hz': freqs,
                    'Power': power
                })
                csv = spectrum_df.to_csv(index=False)
                st.download_button(
                    label="Download Power Spectrum Data",
                    data=csv,
                    file_name="power_spectrum.csv",
                    mime="text/csv"
                )
            
        except Exception as e:
            import traceback
            st.error(f"Error processing file: {str(e)}\n\nTraceback:\n{traceback.format_exc()}")

if __name__ == "__main__":
    main()
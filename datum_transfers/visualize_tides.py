import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

class TidalVisualizer:
    def __init__(self, excel_file, station1_name, station2_name):
        self.excel_file = excel_file
        self.station1_name = station1_name
        self.station2_name = station2_name
        self.station1 = None
        self.station2 = None
        
    def load_data(self):
        self.station1 = pd.read_excel(self.excel_file, sheet_name=0)
        self.station2 = pd.read_excel(self.excel_file, sheet_name=1)
        
        for df in [self.station1, self.station2]:
            df['DateTime'] = pd.to_datetime(
                df['Date'].astype(str) + ' ' + df['Time'].astype(str),
                format='mixed',
                dayfirst=True,
                errors='coerce'
            )
            df.sort_values('DateTime', inplace=True)
            df.reset_index(drop=True, inplace=True)
        
        return self
    
    def plot(self, save_path=None):
        fig, ax = plt.subplots(figsize=(14, 7))
        
        ax.plot(self.station1['DateTime'], self.station1['Height(m)'], 
                color='#2E86AB', linewidth=1.5, label=self.station1_name, alpha=0.9)
        ax.plot(self.station2['DateTime'], self.station2['Height(m)'], 
                color='#E94F37', linewidth=1.5, label=self.station2_name, alpha=0.9)
        
        msl1 = self.station1['Height(m)'].mean()
        msl2 = self.station2['Height(m)'].mean()
        
        ax.axhline(y=msl1, color='#2E86AB', linestyle='--', linewidth=2, 
                   label=f'{self.station1_name} MSL: {msl1:.3f} m')
        ax.axhline(y=msl2, color='#E94F37', linestyle='--', linewidth=2, 
                   label=f'{self.station2_name} MSL: {msl2:.3f} m')
        
        datum_transfer = msl1 - msl2
        ax.set_xlabel('Date/Time', fontsize=12)
        ax.set_ylabel('Height (m)', fontsize=12)
        ax.set_title(f'Tidal Comparison: {self.station1_name} vs {self.station2_name}\n'
                     f'Datum Transfer: {datum_transfer:+.3f} m', fontsize=14, fontweight='bold')
        
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.close(fig)
        return self


def main():
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = Path(__file__).parent.parent / 'plots'
    output_dir.mkdir(exist_ok=True)
    
    datasets = [
        {
            'file': 'Tide_Data_Lagos_Escravos_May2026.xlsx',
            'station1': 'Escravos Bar',
            'station2': 'Lagos Bar',
            'output': 'lagos_escravos_may2026.png'
        },
        {
            'file': 'Tide_Data_Lagos_Escravos_September2026.xlsx',
            'station1': 'Lagos Bar',
            'station2': 'Escravos Bar',
            'output': 'lagos_escravos_september2026.png'
        },
        {
            'file': 'Tide_Data_Bonny_River_Bar_Escravos_Bar_may2026.xlsx',
            'station1': 'Bonny River Bar',
            'station2': 'Escravos Bar',
            'output': 'bonny_escravos_may2026.png'
        }
    ]
    
    for ds in datasets:
        excel_path = data_dir / ds['file']
        if not excel_path.exists():
            print(f"File not found: {excel_path}")
            continue
            
        print(f"\nProcessing: {ds['file']}")
        viz = TidalVisualizer(excel_path, ds['station1'], ds['station2'])
        viz.load_data()
        viz.plot(save_path=output_dir / ds['output'])


if __name__ == "__main__":
    main()

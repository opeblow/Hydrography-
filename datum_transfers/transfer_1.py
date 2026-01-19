
import pandas as pd
import numpy as np
from datetime import datetime

class DatumTransfer:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.escravos = None
        self.lagos = None
        self.stats = {}
        self.datum_transfer = {}
        
    def load_data(self):
        print("Loading data...")
        
        self.escravos = pd.read_excel(self.excel_file, sheet_name=0)
        self.lagos = pd.read_excel(self.excel_file, sheet_name=1)
        for df in [self.escravos, self.lagos]:
            df['Time'] = df['Time'].astype(str).str.zfill(4)
            df['DateTime'] = pd.to_datetime(
                df['Date'].astype(str) + ' ' + 
                df['Time'].str[:2] + ':' + df['Time'].str[2:],
                errors='coerce'
            )
            df.sort_values('DateTime', inplace=True)
            df.reset_index(drop=True, inplace=True)
        
        print(f" Escravos: {len(self.escravos)} observations")
        print(f"Lagos: {len(self.lagos)} observations")
        
        return self
    
    def calculate_statistics(self):
        print("\nCalculating statistics...")
        
        for name, df in [('Escravos', self.escravos), ('Lagos', self.lagos)]:
            
            msl = df['Height(m)'].mean()
            
          
            hw = df[df['Tide_Type'].str.upper() == 'HW']['Height(m)']
            lw = df[df['Tide_Type'].str.upper() == 'LW']['Height(m)']
            
            mhw = hw.mean()
            mlw = lw.mean()
            tidal_range = mhw - mlw
            
            self.stats[name] = {
                'MSL': msl,
                'MHW': mhw,
                'MLW': mlw,
                'Tidal_Range': tidal_range,
                'Std_Dev': df['Height(m)'].std(),
                'N_Obs': len(df)
            }
            
            print(f"\n{name}:")
            print(f"  MSL: {msl:.3f} m")
            print(f"  MHW: {mhw:.3f} m")
            print(f"  MLW: {mlw:.3f} m")
            print(f"  Range: {tidal_range:.3f} m")
        
        return self
    
    def calculate_datum_transfer(self):
        print("\n" + "="*50)
        print("DATUM TRANSFER CALCULATION")
        print("="*50)
        
        lagos_msl = self.stats['Lagos']['MSL']
        escravos_msl = self.stats['Escravos']['MSL']
        
        
        dt_value = lagos_msl - escravos_msl
        lagos_std = self.stats['Lagos']['Std_Dev']
        escravos_std = self.stats['Escravos']['Std_Dev']
        lagos_n = self.stats['Lagos']['N_Obs']
        escravos_n = self.stats['Escravos']['N_Obs']
        
        se = np.sqrt((lagos_std**2 / lagos_n) + (escravos_std**2 / escravos_n))
        uncertainty = 1.96 * se
        
        self.datum_transfer = {
            'value': dt_value,
            'uncertainty': uncertainty,
            'lagos_msl': lagos_msl,
            'escravos_msl': escravos_msl
        }
        
        print(f"\nLagos MSL:     {lagos_msl:.3f} m")
        print(f"Escravos MSL:  {escravos_msl:.3f} m")
        print(f"\nDATUM TRANSFER: {dt_value:+.3f} m ± {uncertainty:.3f} m")
        
        if dt_value > 0:
            print(f"\n Lagos CD is {dt_value:.3f} m HIGHER than Escravos CD")
            print(f"To convert Lagos to Escravos: SUBTRACT {dt_value:.3f} m")
        else:
            print(f"\n Lagos CD is {abs(dt_value):.3f} m LOWER than Escravos CD")
            print(f" To convert Lagos to Escravos: ADD {abs(dt_value):.3f} m")
        
        print("="*50)
        
        return self
    
    def get_daily_msl(self):
        lagos_daily = self.lagos.groupby(
            self.lagos['DateTime'].dt.date
        )['Height (m)'].mean()
        
        escravos_daily = self.escravos.groupby(
            self.escravos['DateTime'].dt.date
        )['Height (m)'].mean()
        
        return lagos_daily, escravos_daily
    
    def run(self):
        self.load_data()
        self.calculate_statistics()
        self.calculate_datum_transfer()
        return self


if __name__ == "__main__":
    excel_file=r"C:\Users\user\Documents\hydrography\data\Tide_Data_Lagos_Escravos_May2026.xlsx"
    analyzer = DatumTransfer(excel_file)
    analyzer.run()
    print("\nAnalysis complete!")
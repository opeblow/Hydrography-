
import pandas as pd
import numpy as np
from datetime import datetime

class DatumTransfer:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.bonny = None
        self.escravos = None
        self.stats = {}
        self.datum_transfer = {}
        
    def load_data(self):
        print("Loading data...")
        
        self.bonny = pd.read_excel(self.excel_file, sheet_name=0)
        self.escravos = pd.read_excel(self.excel_file, sheet_name=1)
        
        for df, name in [(self.bonny, 'Bonny River Bar'), (self.escravos, 'Escravos Bar')]:
            df['Time'] = df['Time'].astype(str).str.zfill(4)
            
           
            df['DateTime'] = pd.to_datetime(
                df['Date'].astype(str) + ' ' + 
                df['Time'].str[:2] + ':' + df['Time'].str[2:],
                errors='coerce'
            )
            
         
            df.sort_values('DateTime', inplace=True)
            df.reset_index(drop=True, inplace=True)
        
        print(f"Bonny River Bar: {len(self.bonny)} observations")
        print(f" Escravos Bar: {len(self.escravos)} observations")
        
        return self
    
    def calculate_statistics(self):
        print("\nCalculating statistics...")
        
        for name, df in [('Bonny River Bar', self.bonny), ('Escravos Bar', self.escravos)]:
          
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
                'N_Obs': len(df),
                'N_HW': len(hw),
                'N_LW': len(lw)
            }
            
            print(f"\n{name}:")
            print(f"  MSL: {msl:.3f} m")
            print(f"  MHW: {mhw:.3f} m")
            print(f"  MLW: {mlw:.3f} m")
            print(f"  Range: {tidal_range:.3f} m")
            print(f"  Observations: {len(df)} (HW: {len(hw)}, LW: {len(lw)})")
        
        return self
    
    def calculate_datum_transfer(self):
        print("\n" + "="*60)
        print("DATUM TRANSFER CALCULATION")
        print("Bonny River Bar to Escravos Bar")
        print("="*60)
        
        bonny_msl = self.stats['Bonny River Bar']['MSL']
        escravos_msl = self.stats['Escravos Bar']['MSL']
        
        
        dt_value = bonny_msl - escravos_msl
        bonny_std = self.stats['Bonny River Bar']['Std_Dev']
        escravos_std = self.stats['Escravos Bar']['Std_Dev']
        bonny_n = self.stats['Bonny River Bar']['N_Obs']
        escravos_n = self.stats['Escravos Bar']['N_Obs']
        
        se = np.sqrt((bonny_std**2 / bonny_n) + (escravos_std**2 / escravos_n))
        uncertainty = 1.96 * se
        
        self.datum_transfer = {
            'value': dt_value,
            'uncertainty': uncertainty,
            'bonny_msl': bonny_msl,
            'escravos_msl': escravos_msl
        }
        
        print(f"\nBonny River Bar MSL:     {bonny_msl:.3f} m")
        print(f"Escravos Bar MSL:        {escravos_msl:.3f} m")
        print(f"\nDATUM TRANSFER: {dt_value:+.3f} m ± {uncertainty:.3f} m")
        
        if dt_value > 0:
            print(f"\n Bonny River Bar CD is {dt_value:.3f} m HIGHER than Escravos Bar CD")
            print(f"To convert Bonny to Escravos: SUBTRACT {dt_value:.3f} m")
        else:
            print(f"\n Bonny River Bar CD is {abs(dt_value):.3f} m LOWER than Escravos Bar CD")
            print(f" To convert Bonny to Escravos: ADD {abs(dt_value):.3f} m")
        
        print("="*60)
        
        return self
    
    def get_daily_msl(self):
        bonny_daily = self.bonny.groupby(
            self.bonny['DateTime'].dt.date
        )['Height(m)'].mean()
        
        escravos_daily = self.escravos.groupby(
            self.escravos['DateTime'].dt.date
        )['Height(m)'].mean()
        
        return bonny_daily, escravos_daily
    
    def run(self):
        self.load_data()
        self.calculate_statistics()
        self.calculate_datum_transfer()
        return self



if __name__ == "__main__":
    excel_file=r"C:\Users\user\Documents\hydrography\data\Tide_Data_Bonny_River_Bar_Escravos_Bar_may2026.xlsx"
    
   
    analyzer = DatumTransfer(excel_file)
    analyzer.run()
    
    print("\nAnalysis complete!")
    
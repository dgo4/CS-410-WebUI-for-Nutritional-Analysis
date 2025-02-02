import argparse
import pandas as pd
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--react_path", type=str,
                        help="path to all reactions in tsv format",
                        required=False,
			default="./Preprocessed-Human-GEM/all-reactions.tsv")
    parser.add_argument("-o", "--out_dir", type=str,
                        help="path to output dir",
                        required=False,
			default="./Preprocessed-Human-GEM")
    parser.add_argument("-l", "--log_path", type=str,
                        help="path to log file",
                        required=False, 
			default="./preprocess_human-gem-sets.log")
    args = parser.parse_args()
    return args

def react_set_1(react_gem, out_dir):
    react_set_1_dir = out_dir + '/Reaction-Set-1'
    Path(react_set_1_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_gem = react_gem[react_gem['Direction'] == 1]
    one_more_mets_in = react_gem[react_gem['Measured_Metabolite_Count'] > 0]
    print(one_more_mets_in.shape)
    one_more_mets_in.to_csv(react_set_1_dir + '/reaction-set-1.tsv', sep='\t', index=False)
    print(one_more_mets_in.shape)
    
def react_set_2(react_gem, out_dir):
    react_set_2_dir = out_dir + '/Reaction-Set-2'
    Path(react_set_2_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_gem = react_gem[react_gem['Direction'] == 1]
    one_more_mets_in = react_gem[(react_gem['Measured_Substrate_Count'] > 0) & (react_gem['Measured_Product_Count'] > 0)]
    print(one_more_mets_in.shape)
    one_more_mets_in.to_csv(react_set_2_dir + '/reaction-set-2.tsv', sep='\t', index=False)
    print(one_more_mets_in.shape)
    
def reverse_equation(eqn):
    eqn_split = eqn.split(' => ')
    if(len(eqn_split) != 2):
        print('Something wrong!')
    new_eqn = eqn_split[1] + ' => ' + eqn_split[0]
    #print(eqn, eqn_split, new_eqn)
    return new_eqn

def react_set_3(react_gem, out_dir):
    react_set_3_dir = out_dir + '/Reaction-Set-3'
    Path(react_set_3_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_df = react_gem[react_gem['Measured_Metabolite_Count'] > 0]
    print(react_df.shape)
    react_df.to_csv(react_set_3_dir + '/reaction-set-3-basic.tsv', sep='\t', index=False)
    print(react_df.shape)
    react1_df = react_df[react_df.Direction == 1]
    react2_df = react_df[react_df.Direction == 2].copy()
    react3_df = react2_df.copy()
    react2_df['RXN_ID'] = react2_df['RXN_ID'] + 'F'
    react2_df['EQUATION'] = react2_df['EQUATION'].str.replace('<=>','=>')
    #print(react2_df.head())

    react3_df['EQUATION'] = react3_df['EQUATION'].apply(lambda x: reverse_equation(x))
    react3_df['RXN_ID'] = react3_df['RXN_ID'] + 'B'
    #swapping columns
    react3_df[['EQUATION_LHS', 'EQUATION_RHS']] = react3_df[['EQUATION_RHS', 'EQUATION_LHS']]
    react3_df[['Substrate_Set', 'Product_Set']] = react3_df[['Product_Set', 'Substrate_Set']]
    react3_df[['Substrate_Count', 'Product_Count']] = react3_df[['Product_Count', 'Substrate_Count']]
    react3_df[['Measured_Substrate', 'Measured_Product']] = react3_df[['Measured_Product', 'Measured_Substrate']]
    react3_df[['Measured_Substrate_Count', 'Measured_Product_Count']] = react3_df[['Measured_Product_Count', 'Measured_Substrate_Count']]
    #print(react3_df.head())

    react_df = pd.concat([react1_df, react2_df, react3_df], axis=0)
    react_df.to_csv(react_set_3_dir + '/reaction-set-3.tsv', sep='\t', index=False)
    

def react_set_4(react_gem, out_dir):
    react_set_4_dir = out_dir + '/Reaction-Set-4'
    Path(react_set_4_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_df = react_gem[(react_gem['Measured_Substrate_Count'] > 0) & (react_gem['Measured_Product_Count'] > 0)]
    print(react_df.shape)
    react_df.to_csv(react_set_4_dir + '/reaction-set-4-basic.tsv', sep='\t', index=False)
    print(react_df.shape)

    react1_df = react_df[react_df.Direction == 1]
    react2_df = react_df[react_df.Direction == 2].copy()
    react3_df = react2_df.copy()

    react2_df['RXN_ID'] = react2_df['RXN_ID'] + 'F'
    react2_df['EQUATION'] = react2_df['EQUATION'].str.replace('<=>','=>')
    #print(react2_df.head())

    react3_df['EQUATION'] = react3_df['EQUATION'].apply(lambda x: reverse_equation(x))
    react3_df['RXN_ID'] = react3_df['RXN_ID'] + 'B'
    #swapping columns
    react3_df[['EQUATION_LHS', 'EQUATION_RHS']] = react3_df[['EQUATION_RHS', 'EQUATION_LHS']]
    react3_df[['Substrate_Set', 'Product_Set']] = react3_df[['Product_Set', 'Substrate_Set']]
    react3_df[['Substrate_Count', 'Product_Count']] = react3_df[['Product_Count', 'Substrate_Count']]
    react3_df[['Measured_Substrate', 'Measured_Product']] = react3_df[['Measured_Product', 'Measured_Substrate']]
    react3_df[['Measured_Substrate_Count', 'Measured_Product_Count']] = react3_df[['Measured_Product_Count', 'Measured_Substrate_Count']]
    #print(react3_df.head())

    react_df = pd.concat([react1_df, react2_df, react3_df], axis=0)
    react_df.to_csv(react_set_4_dir + '/reaction-set-4.tsv', sep='\t', index=False)
    
def str_to_set(cell):
    print(cell)
    if(type(cell) == 'str'):
      cell = ''.join(c for c in cell if c not in "'{}")
      if(len(cell) == 0):
        return {}
      cell = set(cell.split(', '))
    if('set()' in cell):
      return {}
    return cell
    
def react_set_5(react_gem, out_dir):
    react_set_5_dir = out_dir + '/Reaction-Set-5'
    Path(react_set_5_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_df = react_gem[react_gem['Measured_Metabolite_Count'] > 0].copy()
    print(react_df.shape)
    react_df.to_csv(react_set_5_dir + '/reaction-set-5-basic.tsv', sep='\t', index=False)
    print(react_df.shape)

    react_df['Substrate_Set'] = react_df['Substrate_Set'].apply(lambda x: str_to_set(x))
    react_df['Product_Set'] = react_df['Product_Set'].apply(lambda x: str_to_set(x))
    react_df['Measured_Substrate'] = react_df['Measured_Substrate'].apply(lambda x: str_to_set(x))
    react_df['Measured_Product'] = react_df['Measured_Product'].apply(lambda x: str_to_set(x))

    react1_df = react_df[react_df.Direction == 1]
    react2_df = react_df[react_df.Direction == 2].copy()

    react2_df['Substrate_Set'] = react2_df['Metabolite_Set']
    react2_df['Product_Set'] = react2_df['Metabolite_Set']

    react2_df['Measured_Substrate'] = react2_df['Measured_Metabolite']
    react2_df['Measured_Product'] = react2_df['Measured_Metabolite']

    react_df = pd.concat([react1_df, react2_df], axis=0)

    react_df.to_csv(react_set_5_dir + '/reaction-set-5.tsv', sep='\t', index=False)
    
def react_set_6(react_gem, out_dir):
    react_set_6_dir = out_dir + '/Reaction-Set-6'
    Path(react_set_6_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_df = react_gem[(react_gem['Measured_Substrate_Count'] > 0) & (react_gem['Measured_Product_Count'] > 0)].copy()
    print(react_df.shape)
    react_df.to_csv(react_set_6_dir + '/reaction-set-6-basic.tsv', sep='\t', index=False)
    print(react_df.shape)

    react_df['Substrate_Set'] = react_df['Substrate_Set'].apply(lambda x: str_to_set(x))
    react_df['Product_Set'] = react_gem['Product_Set'].apply(lambda x: str_to_set(x))
    react_df['Measured_Substrate'] = react_gem['Measured_Substrate'].apply(lambda x: str_to_set(x))
    react_df['Measured_Product'] = react_gem['Measured_Product'].apply(lambda x: str_to_set(x))

    react1_df = react_df[react_df.Direction == 1]
    react2_df = react_df[react_df.Direction == 2].copy()

    react2_df['Substrate_Set'] = react2_df['Metabolite_Set']
    react2_df['Product_Set'] = react2_df['Metabolite_Set']

    react2_df['Measured_Substrate'] = react2_df['Measured_Metabolite']
    react2_df['Measured_Product'] = react2_df['Measured_Metabolite']

    react_df = pd.concat([react1_df, react2_df], axis=0)
    react_df.to_csv(react_set_6_dir + '/reaction-set-6.tsv', sep='\t', index=False)

def react_set_7(react_gem, out_dir):
    react_set_7_dir = out_dir + '/Reaction-Set-7'
    Path(react_set_7_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_gem = react_gem[react_gem['Direction'] == 1]
    two_more_mets_in = react_gem[react_gem['Measured_Metabolite_Count'] > 1]
    print(two_more_mets_in.shape)
    two_more_mets_in.to_csv(react_set_7_dir + '/reaction-set-7.tsv', sep='\t', index=False)
    print(two_more_mets_in.shape)
    
def react_set_8(react_gem, out_dir):
    react_set_8_dir = out_dir + '/Reaction-Set-8'
    Path(react_set_8_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_df = react_gem[react_gem['Measured_Metabolite_Count'] > 1]
    print(react_df.shape)
    react_df.to_csv(react_set_8_dir + '/reaction-set-8-basic.tsv', sep='\t', index=False)
    print(react_df.shape)
    react1_df = react_df[react_df.Direction == 1]
    react2_df = react_df[react_df.Direction == 2].copy()
    react3_df = react2_df.copy()
    react2_df['RXN_ID'] = react2_df['RXN_ID'] + 'F'
    react2_df['EQUATION'] = react2_df['EQUATION'].str.replace('<=>','=>')
    print(react2_df.head())

    react3_df['EQUATION'] = react3_df['EQUATION'].apply(lambda x: reverse_equation(x))
    react3_df['RXN_ID'] = react3_df['RXN_ID'] + 'B'
    #swapping columns
    react3_df[['EQUATION_LHS', 'EQUATION_RHS']] = react3_df[['EQUATION_RHS', 'EQUATION_LHS']]
    react3_df[['Substrate_Set', 'Product_Set']] = react3_df[['Product_Set', 'Substrate_Set']]
    react3_df[['Substrate_Count', 'Product_Count']] = react3_df[['Product_Count', 'Substrate_Count']]
    react3_df[['Measured_Substrate', 'Measured_Product']] = react3_df[['Measured_Product', 'Measured_Substrate']]
    react3_df[['Measured_Substrate_Count', 'Measured_Product_Count']] = react3_df[['Measured_Product_Count', 'Measured_Substrate_Count']]

    print(react3_df.head())

    react_df = pd.concat([react1_df, react2_df, react3_df], axis=0)
    react_df.to_csv(react_set_8_dir + '/reaction-set-8.tsv', sep='\t', index=False)
    
def react_set_9(react_gem, out_dir):
    react_set_9_dir = out_dir + '/Reaction-Set-9'
    Path(react_set_9_dir).mkdir(parents=True, exist_ok=True)
    
    react_gem = react_gem[~react_gem['SUBSYSTEM'].isin(['Transport reactions', 'Exchange/demand reactions'])]
    react_df = react_gem[react_gem['Measured_Metabolite_Count'] > 1].copy()
    print(react_df.shape)
    react_df.to_csv(react_set_9_dir + '/reaction-set-9-basic.tsv', sep='\t', index=False)
    print(react_df.shape)

    react_df['Substrate_Set'] = react_df['Substrate_Set'].apply(lambda x: str_to_set(x))
    react_df['Product_Set'] = react_df['Product_Set'].apply(lambda x: str_to_set(x))
    react_df['Measured_Substrate'] = react_df['Measured_Substrate'].apply(lambda x: str_to_set(x))
    react_df['Measured_Product'] = react_df['Measured_Product'].apply(lambda x: str_to_set(x))

    react1_df = react_df[react_df.Direction == 1]
    react2_df = react_df[react_df.Direction == 2].copy()

    react2_df['Substrate_Set'] = react2_df['Metabolite_Set']
    react2_df['Product_Set'] = react2_df['Metabolite_Set']

    react2_df['Measured_Substrate'] = react2_df['Measured_Metabolite']
    react2_df['Measured_Product'] = react2_df['Measured_Metabolite']

    react_df = pd.concat([react1_df, react2_df], axis=0)

    react_df.to_csv(react_set_9_dir + '/reaction-set-9.tsv', sep='\t', index=False)
    
def main(args):
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    orig_stdout = sys.stdout
    log_file = open(args.log_path, 'w') 
    sys.stdout = log_file

    react_gem = pd.read_csv(args.react_path, sep='\t')
    print(react_gem.head())
    print(react_gem.shape)
    print("react_set_1")
    react_set_1(react_gem, args.out_dir)
    print("react_set_2")
    react_set_2(react_gem, args.out_dir)
    print("react_set_3")
    react_set_3(react_gem, args.out_dir)
    print("react_set_4")
    react_set_4(react_gem, args.out_dir)
    print("react_set_5")
    react_set_5(react_gem, args.out_dir)
    print("react_set_6")
    react_set_6(react_gem, args.out_dir)
    print("react_set_7")
    react_set_7(react_gem, args.out_dir)
    print("react_set_8")
    react_set_8(react_gem, args.out_dir)
    print("react_set_9")
    react_set_9(react_gem, args.out_dir)
    
if __name__ == "__main__":
    main(parse_args())

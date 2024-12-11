import argparse
import pandas as pd
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gem_path", type=str,
                        help="path to end metabolomics profile in xlsx format",
                        required=False,
			default="./data/Human-GEM.xlsx")
    parser.add_argument("-m", "--met_75_path", type=str,
                        help="path to list of 75 metabolites in tsv format",
			required=False,
			default="./Preprocessed-Metabolome/gem_overlapped_metabolites.tsv")
    parser.add_argument("-o", "--out_dir", type=str,
                        help="path to output dir",
                        required=False,
			default="./Preprocessed-Human-GEM")
    parser.add_argument("-l", "--log_path", type=str,
                        help="path to log file",
                        required=False, 
			default="./preprocess_human-gem-all.log")
    args = parser.parse_args()
    return args

def extract_metabolites(eqn):
    old = eqn.split(' + ')
    new = set()
    flag = False
    for i_old in old:
        i_old_split = i_old.split(' ')
        if(len(i_old_split)>1):
            if(i_old_split[0].replace(".", "").isnumeric()): # If a metabolite has a coefficient in reaction equation
                i_new = i_old[len(i_old_split[0])+1:]
                #print(i_new, i_old)
                #i_new = i_old.replace(i_old_split[0] + ' ', '')
                #print(i_old, '->', i_new)
                new.add(i_new)
                flag = True
            else:
                new.add(i_old)
        else:
            new.add(i_old)
    #if(flag):
        #print('old', old)
        #print('new', new)
        #print()
    return new
            

def all_reactions(met_75_path, gem_path, out_dir):
    met75 = pd.read_csv(met_75_path, sep='\t')
    met75 = set(met75['MET_ID'])
    print(met75)
    react_gem = pd.read_excel(gem_path, sheet_name='RXNS', usecols=['ID', 'EQUATION', 'SUBSYSTEM'])

    subsystem = react_gem['SUBSYSTEM'].value_counts()
    print(subsystem)

    react_gem = react_gem.rename(columns={'ID': 'RXN_ID'})
    pattern = '|'.join(['\\[e\\]', '\\[x\\]', '\\[m\\]', '\\[c\\]', '\\[l\\]', '\\[r\\]', '\\[g\\]', '\\[n\\]', '\\[i\\]'])
    #react_gem['EQUATION'] = react_gem['EQUATION'].str.replace(pattern, '')
    react_gem['EQUATION'] = react_gem['EQUATION'].str.replace('\\[.\\]', '', regex=True)
    react_gem['Direction'] = react_gem['EQUATION'].apply(lambda x: 2 if '<=>' in x else 1)
    react_gem['EQUATION'] = react_gem['EQUATION'].str.replace('<=>', '=>')
    react_gem[['EQUATION_LHS', 'EQUATION_RHS']] = react_gem['EQUATION'].str.split(' => ', expand=True)
    react_gem['Substrate_Set'] = react_gem['EQUATION_LHS'].apply(lambda x: extract_metabolites(x))
    react_gem['Product_Set'] = react_gem['EQUATION_RHS'].apply(lambda x: extract_metabolites(x))
    react_gem['Metabolite_Set'] = react_gem.apply(lambda x: x['Product_Set'].union(x['Substrate_Set']), axis=1)

    react_gem['Substrate_Count'] = react_gem['Substrate_Set'].apply(lambda x: len(x))
    react_gem['Product_Count'] = react_gem['Product_Set'].apply(lambda x: len(x))
    react_gem['Metabolite_Count'] = react_gem['Metabolite_Set'].apply(lambda x: len(x))
    react_gem['Measured_Substrate'] = react_gem['Substrate_Set'].apply(lambda x: x.intersection(met75))
    react_gem['Measured_Product'] = react_gem['Product_Set'].apply(lambda x: x.intersection(met75))
    react_gem['Measured_Metabolite'] = react_gem['Metabolite_Set'].apply(lambda x: x.intersection(met75))

    react_gem['Measured_Substrate_Count'] = react_gem['Measured_Substrate'].apply(lambda x: len(x))
    react_gem['Measured_Product_Count'] = react_gem['Measured_Product'].apply(lambda x: len(x))
    react_gem['Measured_Metabolite_Count'] = react_gem['Measured_Metabolite'].apply(lambda x: len(x))
    #react_gem.head()
    react_gem.to_csv(out_dir + '/all-reactions.tsv', sep='\t', index=False)
    return react_gem

def main(args):
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    orig_stdout = sys.stdout
    log_file = open(args.log_path, 'w') 
    sys.stdout = log_file

    react_gem = all_reactions(args.met_75_path, args.gem_path, args.out_dir)
    
if __name__ == "__main__":
    main(parse_args())

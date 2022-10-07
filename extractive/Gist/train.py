import argparse
from codes import train_classifier

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--data_path', default = 'data/text/', type = str, help = 'Folder containing textual data')
    parser.add_argument('--features_path', default = 'features/', type = str, help = 'Folder to store features of the textual data')
    parser.add_argument('--model_path', default = 'features/', type = str, help = 'Path where trained summarization model is present')
    parser.add_argument('--lr', default = 0.001, type = float, help = 'learning rate of the model')
    parser.add_argument('--numleaves', default = 1043, type = int, help = 'no. of leaves')
    parser.add_argument('--n_est', default = 1043, type = int, help = 'no. of estimators')


    args = parser.parse_args()

    train_classifier.train_lgbm(args)


if __name__ == '__main__':
    main()
        

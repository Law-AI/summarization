# Scripts and codes

pointer-generator - Repository - https://github.com/abisee/pointer-generator

chunker.ipynb - Script to divide a text file into chunks. Here each chunk will be saved in a text file.

combiner.ipynb - Script to combine the summaries generated for each chunk in a text file into the final summary 

# Usage

1. Change the path variable in the get_root_path function to the path of the dataset in utilities.py
2. Use chunker to chunk the input text files into chunk text files.
3. Use the pointer generator method to summarize each chunk. 
4. Use the combiner to combine the summaries for every chunk to generate the final summaries.

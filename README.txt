ABOUT THE PROJECT:
  The python module contains two main functions:

    The first function creates a bitmap index which takes an input file, output path, and a boolean value that specifies if the output is sorted or not.
      - The input file must contain database schema per line in the file.
      - The output path is a path for which the out put file is stored
      - The "sorted" is the boolean value that specifies if the output should be sorted or not

    The second function creates a bitmap compression file which takes an input file(bitmap index file), output path, compression method, and word size.
      - The input file must be a bitmap index
      - The output path is a path for which the out put file is stored
      - The compression method specifies which type of method to be used such as BBC, WAH, or VAL.
      - The word size determines the size of the word to be used for compressing

METHODS INSIDE THE PYTHON MODULE:
  - create_index(input_file, output_path, sorted)
  - compress_index(input_file, output_path, compression_method, word_size)
  - create_run_string(runType, runCount, word_size)

HOW TO RUN:
  To run the python functions, you have to manually call the function inside the file and provide the required arguments.
    e.g:
      create_index('animals_small.txt','my_bitmaps/', False)
      compress_index('my_bitmaps/animals_small.txt', 'my_compressed/', 'WAH', 8)

  Then run the python module in the terminal (on MAC) like:
    % python3 Bitmap_Index_Compression.py

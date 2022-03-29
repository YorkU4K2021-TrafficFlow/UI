import pandas as pd

# Takes raw csv and cleans it leaving data unchanged
# file - the string path representation of the csv to be looked at
def clean_csv(file: str) -> DataFrame:
    # read in the input CSV
    # TODO: remove hardcoded path, figure out where to look and tell py to look there - confer with team
    df = pd.read_csv(file)

    # the input comes in with the first row being read as labels, so we need to get them as floats
    r0 = [float(n) for n in list(df.columns.values)]
    # perform some simple operations to insert the created row and correct ordering
    # put at front
    df.loc[-1] = r0
    # prepare the width
    df.index += 1
    # slide it down
    df = df.sort_index()
    # rename the columns as an index, i wasn't sure what would be best and felt this safe
    df.rename(columns ={x:y for x,y in zip(df.columns,range(0,len(df.columns)))}, inplace = True)

    # tada
    return(df)

# binary normalization
# data - the data to be normalized
# ref - the reference point to gauge what the output should be by
# inc - whether we should include values equal to ref as 1 or 0
# outputs the finished normalized dataframe 
def bin_nor(data: DataFrame, ref: float, inc: bool) -> DataFrame:
    # start with a new version for the result
    res = data.copy()
    # go through all cells
    for col in data.columns:
        for row in data.rows:
            # behaviour for when reference is hit dead on
            if data[col][row] == ref:
                # based on if this is inclusive with reference
                if inc:
                    res[col][row] = 1
                else:
                    res[col][row] = 0
            # above reference
            elif data[col][row] > ref:
                res[col][row] = 1
            # below reference
            else:
               res[col][row] = 0
    return(res)


# min max style normalization
# data - the data to be normalized
# outputs the finished normalized dataframe
def minmax_nor(data: DataFrame) -> DataFrame:
    # use the max and min from the data to create result
    res = (data-data.min())/(data.max()-data.min())
    return(res)
    

# normalize each column based on the sum of its values
def sum_nor(data:DataFrame) -> DataFrame:
    res = data.copy()
    # for all columns
    for col in res.columns:
        #normalize by dividing with the sum
        res[col] /= res[col].sum()

    return(res)

from geopy.geocoders import Nominatim
import pandas as pd
import re

# used in address validation
geoloc = Nominatim(user_agent='Rec')

# regex token identifying a valid postal code
POSTAL_REG = '/^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d$/i'

# regex token identifying a valid lat or lon
LATLON_REG = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$i'

def is_postal(inp: str):
    return re.search(POSTAL_REG, inp)

# returns true if input is a street address
def is_address(inp: str):
    location = geoloc.geocode(address)
    if (location != None):
        return True
    else:
        return False

# returns true if input is lattitude or longitude
def is_latlon(inp: str):
    
    return True

# utility function creating a list with 1 elements for src, dst respectively
# each element represents a boolean corresponding to whether that input is valid
def which_valid(src: str, dst: str):
    res = [False,False]
    if (is_postal(src) or is_address(src) or is_latlon(src)):
        res[-1]=True
    if (is_postal(dst) or is_address(dst) or is_latlon(dst)):
        res[0]=True
    return res

# utility function for boolean checking of inputs
def is_valid(src: str, dst: str):
    res = which_valid(src, dst)
    # input is only valid when they both are
    if (res[-1] and res[1]):
        return True
    else:
        return False




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




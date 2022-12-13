from flask import Flask, flash, redirect, render_template, request, session, abort,send_from_directory,send_file,jsonify
import pandas as pd

import json


#1. Declare application
application= Flask(__name__)

#2. Declare data stores
class DataStore():
    BoroughName=None
    Year=None
    PropertyName= None
    PropertyType= None
    Occupancy= None
    SourceEUI= None
    NaturalGasUse= None
    ElectricityUse= None
    TotalGHGEmissions= None
    WaterUse= None
    Prod= None
data=DataStore()


@application.route("/main",methods=["GET","POST"])

#3. Define main code
@application.route("/",methods=["GET","POST"])
def homepage():
    BoroughName = request.form.get('borough_field','Manhattan')
    Year = request.form.get('Year_field', 2013)
    PropertyType = request.form.get('Property_Type', 'Office')
    # Occupancy = request.form.get('Occupancy', 'All')
    # SourceEUI = request.form.get('SourceEUI', 'All')
    # NaturalGasUse = request.form.get('NaturalGasUse', 'All')
    # ElectricityUse = request.form.get('ElectricityUse', 'All')
    # TotalGHGEmissions = request.form.get('TotalGHGEmissions', 'All')
    # WaterUse = request.form.get('WaterUse', 'All')

    data.BoroughName=BoroughName
    data.Year=Year
    data.PropertyType= PropertyType
    # data.Occupancy= Occupancy
    # data.SourceEUI= SourceEUI
    # data.NaturalGasUse= NaturalGasUse
    # data.ElectricityUse= ElectricityUse
    # data.TotalGHGEmissions= TotalGHGEmissions
    # data.WaterUse= WaterUse

    # Note: MAC and Windows has different handling when reading this file !!!
    # Windows:  df = pd.read_csv('NewYorkEnergyUsage.csv')
    df = pd.read_csv('../NewYorkEnergyUsage.csv')
    # dfP=dfP
    
    
    #print(CountryName)
    #Year = data.Year
    #data.Year = Year

    # choose columns to keep, in the desired nested json hierarchical order
    df = df[df.Borough == BoroughName]
    df = df[df["Year Built"] == int(Year)]
    df = df[df["Property Type"] == PropertyType]
    # df = df[df["Occupancy"]== Occupancy]
    # df = df[df["Source EUI (kBtu/ft²)"] == SourceEUI]
    # df = df[df["Natural Gas Use (kBtu)"] == NaturalGasUse]
    # df = df[df["Electricity Use - Grid Purchase (kBtu)"] == ElectricityUse]
    # df = df[df["Total GHG Emissions (Metric Tons CO2e)"] == TotalGHGEmissions]
    # df = df[df["Water Use (All Water Sources) (kgal)"] == WaterUse]
    print(df.head())
    # df = df.drop(
    # ['Country', 'Item Code', 'Flag', 'Unit', 'Year Code', 'Element', 'Element Code', 'Code', 'Item'], axis=1)
    df = df[["Property Type", "Property Name", "Electricity Use - Grid Purchase (kBtu)"]]

    # order in the groupby here matters, it determines the json nesting
    # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
    df1 = df.groupby(['Property Type', 'Property Name'])['Electricity Use - Grid Purchase (kBtu)'].sum()
    df1 = df1.reset_index()
    print(df1.head())

    # start a new flare.json document
    flare = dict()
    d = {"name": "flare", "children": []}

    for line in df1.values:
        Category = line[0]
        Cat = line[1]
        value = line[2]

        # make a list of keys
        keys_list = []
        for item in d['children']:
            keys_list.append(item['name'])

        # if 'the_parent' is NOT a key in the flare.json yet, append it
        if not Category in keys_list:
            d['children'].append({"name": Category, "children": [{"name": Cat, "size": value}]})

        # if 'the_parent' IS a key in the flare.json, add a new child to it
        else:
            d['children'][keys_list.index(Category)]['children'].append({"name": Cat, "size": value})

    flare = d
    e = json.dumps(flare)
    data.Prod = json.loads(e)
    Prod=data.Prod
    return render_template("Map_zoom_newyork.html", BoroughName=BoroughName, Year=Year, Prod=Prod)

# Below is the information print out
#    id  ... Average Year
#207    313  ...   177.290244
#750   1089  ...   152.011661
#923   1373  ...   152.011661
#1481  2106  ...   199.964497
#1800  2559  ...   168.784931
#[5 rows x 13 columns]

@application.route("/get-data/",methods=["GET","POST"])
def returnProdData():
    df1 = pd.read_csv('NewYorkEnergyUsage.csv')
    Boroughs = df1["Borough"].values
    sEUI = df1["Source EUI (kBtu/ft²)"].values
    dict_sEUI = {}
    for i in range(len(Boroughs)):
        dict_sEUI[Boroughs[i]] = sEUI[i]
    return json.dumps(dict_sEUI)
# export the final result to a json file
@application.route("/get-data",methods=["GET","POST"])
def returnData():
    df = pd.read_csv('NewYorkEnergyUsage.csv', index_col=0)
    dfa = df.values
    list_item = []
    cols = df.columns.values.tolist()
    for l in dfa:
        item = {}
        for i in range(len(cols)):
            item[cols[i]] = l[i]
        list_item.append(item)
    return json.dumps(list_item)
# Below for automatically populate in the dropdown list

# Below for automatically populate in the dropdown list
@application.route("/get-date",methods=["GET","POST"])
def returnYearList():

    df = pd.read_csv('../NewYorkEnergyUsage.csv')
    yeardf = df["Year Built"].unique()

    print(yeardf)
    # Array to json, should be transfer to list firstly
    yearJsonString = json.dumps({'Year': yeardf.tolist()})

    return yearJsonString

if __name__ == "__main__":
    application.run(debug=True)



# Function for LTV_1 predict
def predict_ltv_1(agg_data):
  ARPU = agg_data['Revenue_month']/agg_data['MAU_month'].mean()
  ARPU_mean = ARPU.mean()
  Lifetime_mean = agg_data['Lifetime_month'].mean()
  #print('ARPU Mean:     ', ARPU_mean)
  #print('Lifetime Mean: ', Lifetime_mean)
  LTV_1 = ARPU_mean * Lifetime_mean
  return print('LTV_1: ', round(LTV_1, 2))


# Function for LTV_2 predict
def predict_ltv_2(agg_data):
    # Retention function
    def retention_func(days):
      return 1/(0.2*days+2)

    ARPU_mean = (agg_data['Revenue_month']/agg_data['MAU_month']).mean()
    #
    select = ['1_day_Retention', '7_day_Retention', '30_day_Retention']
    RETENTION = agg_data[select].mean().to_list()
    #
    DAYS = [1, 7, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360,
            390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720]

    DF = pd.DataFrame(DAYS)
    DF.columns = ['DAYS']
    DF['RETENTION'] = 0
    DF['RETENTION'].iloc[:3] = RETENTION
    DF['RETENTION'].iloc[3:] = DF['DAYS'].iloc[3:].apply(lambda x: retention_func(x))

    # DF.plot(x="DAYS", y="RETENTION", alpha=0.5)
    # DF.plot.scatter(x="DAYS", y="RETENTION", alpha=0.5)
    LTV_2 = (ARPU_mean * DF['RETENTION']).sum()
    return print('LTV_2 with integral of Retention: ', round(LTV_2, 2))


# Function for LTV_2 predict
def predict_ltv_3(agg_data):
    # Retention function
    def comulative_ARPU_func(days):
      return 0.23404*np.log(days)

    ARPU_mean = (agg_data['Revenue_month']/agg_data['MAU_month']).mean()
    #
    select = ['CARPU_7_days', 'CARPU_14_days',
              'CARPU_30_days', 'CARPU_60_days']
    CARPU = agg_data[select].mean().to_list()
    #
    DAYS = [1, 7, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360,
            390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720]

    DF = pd.DataFrame(DAYS)
    DF.columns = ['DAYS']
    DF['CARPU'] = 0
    DF['CARPU'].iloc[:4] = CARPU
    DF['CARPU'].iloc[4:] = DF['DAYS'].iloc[3:].apply(lambda x: comulative_ARPU_func(x))

    # DF.plot(x="DAYS", y="RETENTION", alpha=0.5)
    # DF.plot.scatter(x="DAYS", y="RETENTION", alpha=0.5)
    LTV_3 = DF['CARPU'].max()
    return print('LTV_3 with max of CARPU: ', round(LTV_3, 2))
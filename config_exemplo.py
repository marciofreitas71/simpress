wsdl_url = 'https://api-counters.nddprint.com/CountersWS/CountersData.asmx?WSDL'
service_method = 'GetReferenceCountersData' #'GetPlainCountersData'
output_csv = 'output-reference-2023-10-27.csv' #'output-plain-2023-10-15.csv'
payload = {
    'dealerName': 'XXXXX',
    'dealerUserEmail': 'xxxxx@xxx.com.br',
    'dealerUserPassword': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    #'dateTimeStart': '2023-10-17 00:00:00',
    'dateTimeEnd': '2023-11-30 02:00:00',
    'maxLimitDaysEarlier': 1,
    'enterpriseName': '9853_TRE_BA',
    'serialNumber': '',
    'siteName': '',
    'siteDivisionName': '',
    'engaged': False,
    'fieldsList': 'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #'EnterpriseName;PrinterDeviceID;SerialNumber;AddressName;siteName;EnabledCounters;CounterTypeName;FirstCounterTotal;LatestCounterTotal;FirstCounterMono;LatestCounterMono;FirstCounterColor;LatestCounterColor' #'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #
}
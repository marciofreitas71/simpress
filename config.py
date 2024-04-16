from datetime import datetime
import simpress_print

dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"

wsdl_url = 'https://api-counters.nddprint.com/CountersWS/CountersData.asmx?WSDL'
service_method = 'GetReferenceCountersData' #'GetPlainCountersData'
output_csv = 'output-reference-2023-10-27.csv' #'output-plain-2023-10-15.csv'
payload = {
    'dealerName': 'SIMPRESS',
    'dealerUserEmail': 'ruguedes@tre-ba.jus.br',
    'dealerUserPassword': '8lYKAfLbl2FKqAJgWWRA5Q==',
    # 'dateTimeStart': '2023-01-01 00:00:00',
    # 'dateTimeEnd': '2024-04-11 02:00:00',
    'dateTimeEnd': dateTimeEnd ,
    'maxLimitDaysEarlier': 1,
    'enterpriseName': '9853_TRE_BA',
    'serialNumber': '',
    'siteName': '',
    'siteDivisionName': '',
    'engaged': False,
    'fieldsList': 'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #'EnterpriseName;PrinterDeviceID;SerialNumber;AddressName;siteName;EnabledCounters;CounterTypeName;FirstCounterTotal;LatestCounterTotal;FirstCounterMono;LatestCounterMono;FirstCounterColor;LatestCounterColor' #'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #
}
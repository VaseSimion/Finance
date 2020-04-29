import random


list_of_technology = ["AAPL", "ACIW", "ACN", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "AMD", "AMAT",
                      "ANET", "ANSS", "ARW", "ATVI", "AVGO", "AVT", "AZPN", "BA", "BB", "BLL",
                      "BLKB", "BR", "CDK", "CDNS", "CERN", "CHKP", "CIEN", "COMM", "COUP",
                      "CREE", "CRM", "CRUS", "CRWD", "CSCO", "CVLT",
                      "CY", "CYBR", "DBX", "DDD", "DDOG", "DLB", "DOCU", "DOX", "DXC", "EA", "EFX", "EQT",
                      "FCEL", "FDS", "FEYE", "FIT", "FTNT", "FVRR", "G", "GE", "GLW", "GPRO",
                      "GRMN", "GRPN", "HIMX", "HPE", "HPQ", "IAC", "IBM",
                      "INFO", "INTC", "IPGP", "IT", "JBL", "JCOM", "KEX", "LOGI",
                      "MCHP", "MSFT", "MCO", "MDB", "MDRX", "MOMO", "MSCI", "MSI", "MU", "NCR",
                      "NLOK", "NLSN", "NOW", "NUAN",
                      "NVDA", "NTAP", "NTGR",  "NXPI", "OKTA", "ON", "PANW", "PAYX", "PBI",
                      "PCG", "PFPT", "PING", "PTC", "PINS", "QCOM", "ORCL", "QRVO", "OTEX", "SABR",
                      "SHOP", "SNAP", "SPCE", "SPGI", "SPLK", "SQ", "SSNC",
                      "STM", "STX", "SYY", "SWKS", "TEAM", "TER", "TEVA", "TLND",
                      "TSM", "TTWO", "TWLO", "VEEV", "VLO", "VMW", "VRSK", "VSAT",
                      "WDC", "WIX", "WORK", "ZM", "XRX", "ZBRA", "ZEN", "ZNGA", "ZS"]

list_of_materials = ["AA", "ATI", "BLL", "CCJ", "CENX", "CCK", "UFS", "EXP", "EGO", "FCX", "GPK",
                     "IP", "KGC", "LPX", "MLM", "NEM", "NUE", "OC", "OI", "PKG", "PAAS", "RS", "RGLD", "SON", "SCCO",
                     "TRQ", "X", "VALE", "VMC", "WPM", "AUY", "MMM", "AIV", "ALB", "APD", "ASH", "AVY", "CE", "CX",
                     "CF", "CTVA", "DOW", "DD", "EXP", "EMN", "ECL", "IFF", "FMC", "HUN", "ICL", "LYB", "MEOH", "MOS",
                     "NEU", "POL", "PPG", "RPM", "SHW", "SLGN", "SQM", "GRA", "WLK"]

list_of_communication_services = ["ACIA", "GOOG", "AMCX", "T", "BIDU", "CTL", "CHTR", "CHL", "CHU", "CHT",
                                  "CMCSA", "DISCA", "DISH", "DIS", "EXPE", "FFIV", "FB", "FOXA", "FTR", "GDDY",
                                  "GRUB", "IPG", "LBTYA", "LN", "LYFT", "MTCH", "NFLX", "OMC",
                                  "PINS", "RCI", "ROKU", "SBAC", "SNAP", "SPOT", "S", "TMUS", "TU", "TTD", "TRIP",
                                  "TWTR", "UBER", "VEON", "VZ", "VIAB", "VIAC", "WB", "YNDX", "Z"]

list_of_utilities_and_real_estate = ["AES", "AEE", "AEP", "AWK", "WTR", "ATO", "CMS", "ED", "DUK", "EIX", "EVRG",
                                     "EXC", "FE", "MDU", "NFG", "NEE", "NI", "NRG", "OGE", "PPL", "PEG", "SRE", "SO",
                                     "UGI", "XEL", "AGNC", "ARE", "AMH", "AVB", "BXP", "CPT", "CBL", "CBRE", "CB",
                                     "CLNY", "CXP", "ESS", "FRT", "GLPI", "JLL", "PB", "SVC", "SITC"]

list_of_energy = ["LNT", "AR", "APA", "BKR", "COG", "CNP", "CHK", "CVX", "SNP", "CNX", "CXO", "COP",
                  "CLB", "DCP", "DVN", "DO", "D", "DRQ", "DTE", "ENS", "EPD", "EOG", "EQT", "XOM", "FSLR", "GPOR",
                  "HAL", "HP", "HES", "HFC", "KMI", "LPI", "MMP", "MRO", "MPC", "MUR", "NBR", "NOV", "NBL",
                  "NS", "OAS", "OXY", "OII", "OKE", "PBR", "PSX", "PXD", "QEP", "RRC", "RES", "SSL", "SLB", "SM",
                  "SWN", "SPWR", "TRGP", "FTI", "VAL", "VLO", "VSLR", "WLL", "WMB", "WEC", "INT"]

list_of_industrials = ["AOS", "AYI", "AEIS", "ACM", "AER", "AGCO", "ALLE", "ALSN", "AME", "APH", "AXE", "BA", "CAT",
                       "CLH", "CGNX", "CFX", "CR", "CSX", "CMI", "DE", "DCI", "DOV", "ETN", "EMR", "FAST", "FDX",
                       "FLEX", "FLS", "FLR", "GD", "GE", "GWR", "GLNG", "GGG", "HXL", "HON", "HII", "IEX", "ITW",
                       "IR", "ITRI", "JEC", "JCI", "KSU", "KBR", "KMT", "KEYS", "KEX", "KNX", "LII", "LECO", "LFUS",
                       "LMT", "MIC", "MIDD", "MSM", "NDSN", "NOC", "NSC", "ODFL", "PH", "PNR", "PWR", "RTN", "RBC",
                       "RSG", "ROK", "ROP", "R", "SPR", "SPXC", "TDY", "TEX", "TXT", "TTC", "TDG", "TRMB", "TRN", "UAL",
                       "URI", "UTX", "UNP", "UPS", "VMI", "WAB", "WM", "WCC", "XPO", "XYL"]

list_of_consumer_discretionary = ["ANF", "ADNT", "ALK", "BABA", "AMZN", "AAL", "AEO", "APTV", "ASNA", "AN", "AZO",
                                  "CAR",
                                  "BBBY", "BBY", "BJ", "BLMN", "BWA", "BV", "EAT", "BC", "BURL", "CAL", "GOOS", "CPRI",
                                  "KMX", "CRI", "CVNA", "CHWY", "CMG", "CHRW", "CNK", "CTAS", "COLM", "CPA", "CPRT",
                                  "DHI", "DAN", "DLPH", "DAL", "DKS", "DDS", "DOL", "DNKN", "EBAY", "ELF", "ETSY",
                                  "RACE", "FCAU", "FL", "F", "FBHS", "FOSL", "GME", "GPS", "GTX", "GPC", "GIL", "GM",
                                  "GNC", "GT", "HRB", "HBI", "HOG", "HAS", "HTZ", "HD", "H", "IGT", "IRBT", "ITT",
                                  "JPC", "SJM", "JD", "JBLU", "JMIA", "KAR", "KSS", "KTB", "LB", "LVS", "LEA", "LEG",
                                  "LEN", "LEVI", "LYV", "LKQ", "LOW", "LULU", "M", "MANU", "MAN", "MAR", "MAS", "MAT",
                                  "MCD", "MLCO", "MELI", "MGM", "MHK", "NWL", "NKE", "NIO", "JWN", "NVEE", "OSK",
                                  "PTON", "PDD", "PII", "POOL", "PHM", "PVH", "RL", "RVLV", "RHI", "RCL", "SBH",
                                  "SGMS", "SMG", "SEE", "SIX", "SNA", "LUV", "SAVE", "SWK", "SBUX", "TPR",
                                  "TEN", "TSLA", "MSG", "REAL", "TJX", "THO", "TIF", "TOL", "TSCO", "TUP",
                                  "ULTA", "UAA",
                                  "URBN", "VFC", "VC", "W", "WEN", "WHR", "WSM", "WW", "WYND", "WYNN"]

list_of_consumer_staples = ["MO", "ADM", "BYND", "BRFS", "BG", "CPB", "CHD", "CLX", "KO", "CL", "CAG", "STZ", "COTY",
                            "DG", "ENR", "EL", "FLO", "GIS", "HLF", "HLT", "HRL", "INGR", "K", "KDP", "KMB", "KHC",
                            "KR", "LK", "MKC", "TAP", "MDLZ", "PEP", "PM", "RAD", "SPB", "SFM", "SYY", "TGT",
                            "HAIN", "TSN", "UNFI", "VFF", "WBA", "WMT", "YUM"]

list_of_healthcare = ["ABT", "ABBV", "ACAD", "ALC", "ALXN", "ALGN", "ALKS", "AGN", "ALNY", "ABC", "AMGN", "ANTM",
                      "ARNA", "AVTR", "BHC", "BAX", "BDX", "BIO", "BIIB", "BMRN", "BSX", "BMY", "BKD", "BRKR", "CARA",
                      "CAH", "CNC", "CI", "COO", "CRBP", "CRSP", "CVS", "DHR", "DVA", "EW", "LLY", "EHC", "ENDP",
                      "EXAS", "GILD", "GWPH", "HCA", "HUM", "IDXX", "ILMN", "INCY", "INVA", "ISRG", "NVTA", "IQV",
                      "JAZZ", "JNJ", "LH", "LVGO", "MCK", "MD", "MDT", "MRK", "MTD", "MYL", "NGM", "OPK", "PKI",
                      "PFE", "QGEN", "REGN", "SGEN", "SYK", "TDOC", "TFX", "THC", "TEVA", "TMO", "TLRY", "UNH",
                      "UHS", "VAR", "VRTX", "WAT", "ZBH", "ZTS"]

list_of_financials = ["AFC", "AIG", "ACC", "AXP", "AMT", "AMP", "NLY", "AON", "ACGL", "ARCC", "AJG", "AIZ", "AGO",
                      "AXS", "BAC", "BK", "BKU", "BLK", "BOKF", "BRO", "COF", "CBOE", "CBRE", "SCHW",
                      "CIM", "CINF", "CIT", "C", "CME", "CNO", "CMA", "CBSH", "CXW", "BAP", "CCI", "CWK", "DLR", "DFS",
                      "DEI", "DRE", "ETFC", "EWBC", "EQIX", "EQR", "RE", "EXR", "FII", "FIS", "FNF", "FITB", "FHN",
                      "FRC", "BEN", "CFR", "GNW", "GPN", "GS", "HBAN", "PEAK", "HIG", "HST", "HHC", "IEP", "ICE",
                      "IBN", "IVZ", "IRM", "ITUB", "JKHY", "JHG", "JEF", "JPM", "KEY", "KRC", "KIM", "KKR", "LAZ",
                      "LM", "LC", "TREE", "LNC", "L", "LPLA", "MTB", "MKL", "MMC", "MA", "MET", "MTG", "MS", "NDAQ",
                      "NTRS", "NYCB", "ORI", "PYPL", "PBCT", "PNC", "BPOP", "PFG", "PSEC", "PRU", "RDN", "RJF",
                      "RLGY", "REG", "RF", "RGA", "RNR", "SEIC", "SBNY", "SLM", "SQ", "STT", "SF", "STI", "SIVB",
                      "SNV", "TROW", "AMTD", "ALL", "BX", "PGR", "TD", "TRV", "TFC", "TWO", "USB", "UBS",
                      "UMPQ", "UNM", "V", "WRB", "WBS", "WFC", "WELL", "WU", "WEX", "WLTW", "WETF", "ZION"]


european_stocks = ["ADS.DE", "ALO.PA", "BAYN.DE", "BMW.DE", "IFX.DE", "LHA.DE", "MAERSK-B.CO", "NOVO-B.CO",
                   "NZYM-B.CO", "SU.PA", "VWS.CO"]


def get_lists():
    print(len(list_of_industrials + list_of_technology + list_of_communication_services + list_of_energy +
              list_of_utilities_and_real_estate + list_of_materials + list_of_consumer_discretionary +
              list_of_consumer_staples + list_of_healthcare + list_of_financials))
    return list_of_industrials + list_of_technology + list_of_communication_services + list_of_energy + \
        list_of_utilities_and_real_estate + list_of_materials + list_of_consumer_discretionary + \
        list_of_consumer_staples + list_of_healthcare + list_of_financials


# investing side of Trading212

investing_list_of_energy = ["AES", "APA", "BKR", "BLDP", "BSM", "COG", "CHK", "CVX", "XEC", "CMS", "COP", "CEIX",
                            "CZZ", "DVN", "DO", "FANG", "DTE", "ENB", "ENPH", "ETR", "EOG", "EQT", "ES", "EXC", "EXTN",
                            "XOM", "FSLR", "FCEL", "HAL", "HP", "HES", "KMI", "KOS", "MRO", "MPC", "MDR", "MUR",
                            "MUSA", "NOV", "NEE", "NBL", "DNOW", "OXY", "OKE", "BTU", "PSX", "PXD", "PLUG", "RRC",
                            "SLB", "SEDG", "SO", "SWN", "SPWR", "TRP", "FTI", "RIG", "VAL", "VLO", "VNOM", "VSLR",
                            "WMB"]

investing_list_of_materials = ["MMM", "AEM", "AIV", "ADP", "AA", "AU", "AVY", "BCPC", "BLL", "GOLD", "CCJ", "CF", "DOW",
                               "DD", "EMN", "ESI", "FMC", "FCX", "GCP", "ICL", "IP", "IFF", "LYB", "MLM", "NEM", "NUE",
                               "OI", "PPG", "SSL", "SEE", "SHW", "STLD", "MOS", "VMC", "WRK", "AUY"]

investing_list_of_industrials = ["ATU", "AME", "APH", "ATRO", "BDC", "BHE", "BA", "BGG", "CAT", "CFX", "CMI", "CW",
                                 "DE", "DOV", "ETN", "EMR", "WATT", "EXPO", "FAST", "FLS", "FLR", "GD", "GE", "GHM",
                                 "HON", "HWM", "ICHR", "ITW", "IR", "IVAC", "ITRI", "J", "JBT", "JCI", "KAI", "KEYS",
                                 "KE", "LECO", "LMT", "MNTX", "MIDD", "NATI", "NOC", "OSIS", "PCAR", "PH", "PNR", "PWR",
                                 "RXN", "ROK", "ROP", "SNA", "SPXC", "FLOW", "SXI", "TEL", "TNC", "TTEC", "TXT", "TKR",
                                 "BLD", "TWIN", "WWD",  "AEIS", "ACM", "ALRM", "ALLE", "BMI", "CAI", "ERII", "FTDR",
                                 "EAF", "LFUS", "RBC", "RSG", "R", "SITE", "SRCL", "TRMB", "UPS", "URI", "GWW", "WM",
                                 "WTS", "XYL", "CHRW", "CSX", "DAL", "EXPD", "FDX", "JBHT", "KSU", "LSTR", "NSC",
                                 "ODFL", "LUV", "UNP"]

investing_list_of_consumer_discretionary = ["TWOU", "AAN", "ADNT", "AAP", "BABA", "AMZN", "AAL", "APTV", "ASGN", "AN",
                                            "AZO", "CAR", "BBSI", "BECN", "BBBY", "BBY", "BGSF", "BLMN", "APRN", "BWA",
                                            "BYD", "BRC", "BV", "BLDR", "BURL", "CAL", "GOOS", "CPRI", "KMX", "CCL",
                                            "CVNA", "CHWY", "CMG", "CNK", "CTAS", "CPRT", "CTVA", "CRVL", "DHI", "DRI",
                                            "DLPH", "DKS", "EBAY", "ECL", "ERI", "ETSY", "FCFS", "FVRR", "F", "FOSL",
                                            "GME", "GPS", "GTX", "GM", "GPC", "GT", "GRWG", "HRB", "HBI", "HOG", "HAS",
                                            "HSII", "HMSY", "HD", "NSP", "JD", "JMIA", "KELYA", "KFRC", "KSS", "KTB",
                                            "KFY", "LB", "LAUR", "LEG", "LEN", "LEVI", "LAD", "LK", "LULU", "M", "MANU",
                                            "MAN", "MAR", "MAS", "MAT", "MCD", "MELI", "MHK", "NRC", "NWL", "NKE",
                                            "NIO", "JWN", "ORLY", "PTON", "PDD", "PLNT", "RL", "PHM", "PVH", "QRTEA",
                                            "RCII", "RVLV", "RHI", "ROST", "RCL", "SGMS", "SHAK", "SSTI", "SIG", "SIX",
                                            "SKYW", "SLM", "SWK", "SBUX", "STRA", "TLRD", "TPR", "TSLA", "TXRH", "REAL",
                                            "TIF", "TJX", "TSCO", "TBI", "ULTA", "UA", "UAL", "URBN", "VFC", "SPCE",
                                            "W", "WHR", "WING", "WW", "WYND", "WYNN", "YUM"]

investing_list_of_consumer_staples = ["MO", "ADM", "BGS", "BYND", "BJ", "CVGW", "CPB", "CLX", "KO", "CCEP", "CL", "CAG",
                                      "STZ", "COST", "CRON", "DAR", "DG", "DLTR", "ELF", "EL", "GIS", "GO", "HLF",
                                      "HRL", "SJM", "K", "KDP", "KMB", "KHC", "KR", "MKC", "TAP", "MDLZ", "MNST", "PEP",
                                      "PM", "PG", "SAFM", "SYY", "TGT", "HSY", "TSN", "VFF", "WBA", "WMT"]

investing_list_of_healthcare = ["ABT", "ABBV", "ABMD", "ACHC", "ACAD", "ADPT", "ADUS", "AERI", "A", "AGIO", "AKCA",
                                "ALC", "ALLK", "AGN", "ALLO", "AMRN", "AMED", "ABC", "AMGN", "AMN", "ANTM", "APHA",
                                "ARNA", "ACB", "AVNS", "AVTR", "AXGT", "BHC", "BAX", "BDX", "BIIB", "BLFS", "BMRN",
                                "BEAT", "BLUE", "BSX", "BBIO", "BMY", "CTST", "CGC", "CAH", "CI", "CRBP", "CRSP",
                                "CCRN", "CVS", "DHR", "DVA", "XRAY", "DXCM", "EW", "LLY", "ENDP", "EXAS", "FGEN",
                                "FREQ", "GILD", "GH", "GWPH", "HCA", "HSIC", "HEPA", "HSKA", "HEXO", "HUM", "IDXX",
                                "ILMN", "IMMU", "INCY", "INMD", "NTLA", "ISRG", "NVTA", "JNJ", "LH", "LVGO", "MNK",
                                "MCK", "MDT", "MRK", "MRNA", "MYL", "MYGN", "NH", "NEOG", "NBIX", "NGM", "NUVA", "PDCO",
                                "PKI", "PRGO", "PFE", "DGX", "REGN", "SAGE", "SDC", "SYK", "TARO", "THC", "TMO", "TLRY",
                                "TCDA", "UNH", "UHS", "VAR", "VRTX", "WAT", "ZBH", "ZTS", "ZGNX"]

investing_list_of_financials = ["QFIN", "AER", "AMG", "AFL", "AGNC", "AIG", "AL", "ADS", "ALL", "AXP", "AMP", "ABCB",
                                "AON", "ACGL", "ASB", "AIZ", "AXS", "BANF", "BAC", "BMO", "BK", "BKU", "BANR", "BRKB",
                                "BLK", "BCOR", "BRO", "COF", "CATM", "SCHW", "CB", "CINF", "C", "CME", "CMA", "CBU",
                                "CODI", "BAP", "CACC", "CRT", "DFS", "ETFC", "EPR", "ERIE", "EVR", "FIS", "FITB",
                                "FISV", "BEN", "GFN", "GNW", "GL", "GS", "GSHD", "HIG", "HRZN", "HBAN", "ICE", "IVZ",
                                "JKHY", "JEF", "JPM", "KW", "KEY", "KKR", "LAZ", "LM", "TREE", "LNC", "L", "MTB", "MMC",
                                "MA", "MCY", "MET", "MS", "NDAQ", "NAVI", "NTRS", "JMF", "ORI", "PYPL", "PBCT", "PNC",
                                "BPOP", "PGR", "PRU", "QD", "RF", "SUNS", "SQ", "STT", "STNE", "SIVB", "SYF", "TROW",
                                "AMTD", "BX", "TRV", "TFC", "USB", "UBSI", "UNM", "VLY", "VIRT", "V", "WFC", "WU",
                                "WLTW", "WTFC", "ZION"]

investing_list_of_technology = ["DDD", "ACN", "ACIW", "ATVI", "ADBE", "AMD", "AGYS", "AIRG", "AKAM", "MDRX", "AYX",
                                "AMBA", "AMSWA", "AMKR", "ASYS", "ADI", "ANSS", "APPF", "APPN", "AAPL", "AMAT", "AAOI",
                                "AZPN", "ASUR", "TEAM", "ADSK", "ADP", "AVID", "AVT", "AWRE", "ACLS", "AXTI", "BAND",
                                "BNFT", "BLKB", "BB", "EPAY", "BOX", "BCOV", "AVGO", "BRKS", "CCMP", "CACI", "CDNS",
                                "CAMP", "CDW", "CERN", "CEVA", "ECOM", "CHKP", "CRUS", "CSCO", "CTXS", "NET", "CTSH",
                                "COHR", "COMM", "CPSI", "CLGX", "CSOD", "GLW", "CSGP", "COUP", "CREE", "CRWD", "CSGS",
                                "CTS", "CYBR", "DDOG", "DGII", "DMRC", "APPS", "DIOD", "DVX", "DSPG", "EBIX", "EA",
                                "EMKR", "EIGI", "ENV", "EPAM", "PLUS", "EFX", "EVBG", "MRAM",  "EXTR", "FFIV", "FDS",
                                "FSLY", "FEYE", "FIT", "FIVN", "FLIR", "FSCT", "FORM", "FTNT", "GRMN", "GSB", "GLOB",
                                "GLUU", "GPRO", "GSIT", "GWRE", "HLIT", "HPE", "HPQ", "HUBS", "IBM", "INFO", "IMMR",
                                "INOV", "IPHI", "INSE", "INTC", "IDCC", "INTU", "IPGP", "JBL", "JCOM", "JNPR", "KLAC",
                                "KOPN", "LRCX", "LSCC", "LDOS", "LPSN", "RAMP", "LOGI", "LITE", "MTSI", "MANH", "MKTX",
                                "MRVL", "MXIM", "MXL", "MLNX", "MCHP", "MU", "MSFT", "MSTR", "MIME", "MITK", "MOBL",
                                "MODN", "MDB", "MPWR", "MCO", "MSI", "NPTN", "NTAP", "NTES", "NCR", "NTGR", "NTCT",
                                "NEWR", "NLSN", "NOK", "NLOK", "NUAN", "NTNX", "NVEC", "NVDA", "NXPI", "OKTA", "OMCL",
                                "ON", "ORCL", "PANW", "PCYG", "PKE", "PAYX", "PCTY", "PCTI", "PDFS", "PEGA", "PRFT",
                                "PLAB", "PING", "PBI", "PXLW", "PLXS", "POWI", "PRGS", "PFPT", "PRO", "PTC", "QADA",
                                "QADB", "QRVO", "QCOM", "QLYS", "QMCO", "RMBS", "RPD", "RTX", "RNWK", "RP", "RST",
                                "SABR", "CRM", "SANM", "SCSC", "STX", "SCWX", "SMTC", "NOW", "SSTI", "SIGM", "SLAB",
                                "SLP", "SWKS", "WORK", "SGH", "SNE", "SPLK", "SPOT", "SPSC", "SSNC", "SRT", "SSYS",
                                "SMCI", "SYKE", "SYNC", "SYNA", "SNCR", "SNX", "SNPS", "TTWO", "TLND", "TECD", "TDC",
                                "TER", "TXN", "TRU", "TTEC", "TTMI", "TWLO", "TYL", "UI", "UCTT", "UIS", "UMC", "UPLD",
                                "VRNS", "VECO", "VRNT", "VRSK", "VERI", "VSAT", "VIAV", "VRTU", "VMW", "VUZI", "WDC",
                                "WDAY", "WL", "XRX", "XLNX", "XPER", "YEXT", "ZBRA", "ZEN", "ZNGA", "ZS"]

investing_list_of_communication_services = ["EGHT", "ACIA", "GOOGL", "GOOG", "T", "BIDU", "BKNG", "CABO", "CARG", "CTL",
                                            "CHTR", "CMCSA", "CVLT", "CMTL", "DISCA", "DISCK", "DISH", "SATS", "EB",
                                            "EXPE", "FB", "FOXA", "FTR", "GDDY",  "GRPN", "HSTM", "IAC", "INAP", "IPG",
                                            "IRDM", "KVHI", "LILA", "LILAK", "LBTYK", "LTRPB", "LTRPA", "LGF-B", "LORL",
                                            "LYFT", "MTCH", "NFLX", "NWSA", "NWS", "OMC", "PINS", "QRTEA", "ROKU",
                                            "SHOP", "SSTK", "SBGI", "SIRI", "SNAP", "SOGO", "TMUS", "TGNA", "TTD",
                                            "TZOO", "TRIP", "TRUE", "TWTR", "UBER", "USM", "VEON", "VZ", "VIAB", "VIAC",
                                            "VOD", "DIS", "WIX", "YNDX", "Z", "ZIXI", "ZM"]

investing_list_of_utilities_and_real_estate = ["ALE", "LNT", "AEE", "AEP", "AWR", "AVA", "BKH", "BIT", "CNP", "ED",
                                               "DUK", "EIX", "EVRG", "FE", "GWRS", "MGEE", "NI", "NRG", "PCG", "PNW",
                                               "PPL", "PEG", "SRE", "WEC", "XEL", "ADC", "AMT", "AVB", "BXP", "BRX",
                                               "BPY", "CBRE", "CLNY", "CXW", "CCI", "CONE", "EQIX", "EQR", "ESS",
                                               "FPIBP", "FRT", "PEAK", "HST", "HPP", "IIPR", "IRM", "KIM", "LTC", "MAC",
                                               "MGRC", "MPW", "MNR", "NMRK", "PK", "PLYM", "PLD", "PSA", "O", "BFS",
                                               "SBAC", "SPG", "SLG", "SRC", "STOR", "SHO", "SKT", "VTR", "VICI", "VNO",
                                               "WELL", "WY", "WSR"]


def get_investing_lists():
    investment_list = investing_list_of_industrials + investing_list_of_technology + \
                      investing_list_of_communication_services + investing_list_of_energy + \
                      investing_list_of_utilities_and_real_estate + investing_list_of_materials + \
                      investing_list_of_consumer_discretionary + investing_list_of_consumer_staples + \
                      investing_list_of_healthcare + investing_list_of_financials

    random.shuffle(investment_list)
    print(len(investment_list))
    return investment_list

#print(get_investing_lists())
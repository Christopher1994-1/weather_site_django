def countries(country_code):
    codes ={ 
            
    # all european countries
    'AL': 'Europe',
    'AD': 'Europe',
    'AT': 'Europe',
    'BY': 'Europe',
    'BE': 'Europe',
    'BA': 'Europe',
    'BG': 'Europe',
    'HR': 'Europe',
    'CY': 'Europe',
    'CZ': 'Europe',
    'DK': 'Europe',
    'EE': 'Europe',
    'FO': 'Europe',
    'FI': 'Europe',
    'FR': 'Europe',
    'DE': 'Europe',
    'GR': 'Europe',
    'HU': 'Europe',
    'IS': 'Europe',
    'IE': 'Europe',
    'IT': 'Europe',
    'LV': 'Europe',
    'LI': 'Europe',
    'LT': 'Europe',
    'LU': 'Europe',
    'MK': 'Europe',
    'MT': 'Europe',
    'MD': 'Europe',
    'MC': 'Europe',
    'ME': 'Europe',
    'NL': 'Europe',
    'NO': 'Europe',
    'PL': 'Europe',
    'PT': 'Europe',
    'RO': 'Europe',
    'RU': 'Europe',
    'SM': 'Europe',
    'RS': 'Europe',
    'SK': 'Europe',
    'SI': 'Europe',
    'ES': 'Europe',
    'SE': 'Europe',
    'CH': 'Europe',
    'UA': 'Europe',
    'GB': 'Europe',
    'VA': 'Europe',
    
    
    'BM': 'North America',  # Bermuda
    'CA': 'North America',  # Canada
    'GL': 'North America',  # Greenland
    'MX': 'North America',  # Mexico
    'PM': 'North America',  # Saint Pierre and Miquelon
    'US': 'North America',  # United States
    'VG': 'North America',   # British Virgin Islands
    
    
    'AR': 'South America',  # Argentina
    'BO': 'South America',  # Bolivia
    'BR': 'South America',  # Brazil
    'CL': 'South America',  # Chile
    'CO': 'South America',  # Colombia
    'EC': 'South America',  # Ecuador
    'FK': 'South America',  # Falkland Islands
    'GF': 'South America',  # French Guiana
    'GY': 'South America',  # Guyana
    'PE': 'South America',  # Peru
    'PY': 'South America',  # Paraguay
    'SR': 'South America',  # Suriname
    'UY': 'South America',  # Uruguay
    'VE': 'South America',   # Venezuela
    }
    
    new_region = codes[country_code]
        
        
    return new_region
        

import requests
import os
#from addressmap import popover
from addressmapmodal import  popover, blank_popover


#GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
#GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
 

def extract_lat_long_via_address(address_or_zipcode, GOOGLE_API_KEY):
    print("in extract")

    lat, lng = None, None
    if len(address_or_zipcode) < 1:
        return "Please enter an address", None, blank_popover(), None
    
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    
    if r.status_code not in range(200, 299):
        
        return "address not found", None, blank_popover(), None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''    
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        return "address not found.", None, blank_popover(), None
        pass

    #districts = get_district(lat, lng)
    #county = get_county(lat, lon)
    #return get_district(lat, lng)
    return "address found at: (" + str(lat)+","+str(lng)+").  " ,None, popover(lat,lng, address_or_zipcode), get_district(lat,lng)


def get_district(lat,lon):
    
    if lat is None or lon is None:
        return None
    base_url = "https://zfa9qwmegs.us-west-2.awsapprunner.com/district"
    endpoint = f"{base_url}?lat={lat}&lon={lon}"
    r = requests.get(endpoint)
    print(r.status_code)
    
    if r.status_code not in range(200, 299):
        
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''    
        results = r.json()
        print(results)
    except:
        pass

    district_list = results['district']
    # if no districts returned - either bad lat/lon or point not in polygons
    #if not district_list:
    #    msg = results['msg']

    if len(results['district']) > 0:
        print("districts found")
        print(results['district'])
        
        return "Your address is in Colorado Congressional " + results['district'][0] + ".  " 
    else:
        return "Colorado district not found, please verify your address.  "    

def get_county(lat,lon):
    print("lat/lon")
    print(lat)
    print(lon)
    if lat is None or lon is None:
        return None
    base_url = "https://zfa9qwmegs.us-west-2.awsapprunner.com/county"
    endpoint = f"{base_url}?lat={lat}&lon={lon}"
    r = requests.get(endpoint)
    print(r.status_code)
    
    if r.status_code not in range(200, 299):
        
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''    
        results = r.json()
        print(results)
    except:
        pass

    
    # if no districts returned - either bad lat/lon or point not in polygons
    #if not district_list:
    #    msg = results['msg']

    if len(results['county']) > 0:

        return ".  You can register to vote in  " + results['county'][0] 
    else:
        return "County not found.  Please verify address."    

       


if __name__ == "__main__":
    #lat, lng = extract_lat_long_via_address("17301 W Colfax Ave Suite 110, Golden, CO 80401")

    #lat, lng = extract_lat_long_via_address("281 Silver Queen, Durango, CO, 81301")
    lat = 37.209 
    lon=-107.788
    district = get_county(lat,lon)
    print(district)


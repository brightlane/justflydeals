#!/usr/bin/env python3
"""
JustFly USA Affiliate Site — FlightDealsPro
Site: https://brightlane.github.io/justflydeals/
Affiliate: https://track.rqqft.com/aff_c?offer_id=25631&aff_id=21885
20,000+ pages targeting USA flight keywords — cheap flights, JustFly reviews,
city pairs, state pages, airline comparisons, travel tips — USA only.
Run: python3 build.py
"""

import os, sys, subprocess, datetime, hashlib

now      = datetime.datetime.utcnow()
DATE_STR = now.strftime("%Y-%m-%d")
SYNC     = hashlib.md5(DATE_STR.encode()).hexdigest()[:8]
BASE_URL = "https://brightlane.github.io/justflydeals"
AFF      = "https://track.rqqft.com/aff_c?offer_id=25631&aff_id=21885"
YEAR     = now.year

# ── STATES ────────────────────────────────────────────────────────────────────
STATES = [
    ("alabama","Alabama","AL"),("alaska","Alaska","AK"),("arizona","Arizona","AZ"),
    ("arkansas","Arkansas","AR"),("california","California","CA"),("colorado","Colorado","CO"),
    ("connecticut","Connecticut","CT"),("delaware","Delaware","DE"),("florida","Florida","FL"),
    ("georgia","Georgia","GA"),("hawaii","Hawaii","HI"),("idaho","Idaho","ID"),
    ("illinois","Illinois","IL"),("indiana","Indiana","IN"),("iowa","Iowa","IA"),
    ("kansas","Kansas","KS"),("kentucky","Kentucky","KY"),("louisiana","Louisiana","LA"),
    ("maine","Maine","ME"),("maryland","Maryland","MD"),("massachusetts","Massachusetts","MA"),
    ("michigan","Michigan","MI"),("minnesota","Minnesota","MN"),("mississippi","Mississippi","MS"),
    ("missouri","Missouri","MO"),("montana","Montana","MT"),("nebraska","Nebraska","NE"),
    ("nevada","Nevada","NV"),("new-hampshire","New Hampshire","NH"),("new-jersey","New Jersey","NJ"),
    ("new-mexico","New Mexico","NM"),("new-york","New York","NY"),("north-carolina","North Carolina","NC"),
    ("north-dakota","North Dakota","ND"),("ohio","Ohio","OH"),("oklahoma","Oklahoma","OK"),
    ("oregon","Oregon","OR"),("pennsylvania","Pennsylvania","PA"),("rhode-island","Rhode Island","RI"),
    ("south-carolina","South Carolina","SC"),("south-dakota","South Dakota","SD"),
    ("tennessee","Tennessee","TN"),("texas","Texas","TX"),("utah","Utah","UT"),
    ("vermont","Vermont","VT"),("virginia","Virginia","VA"),("washington","Washington","WA"),
    ("west-virginia","West Virginia","WV"),("wisconsin","Wisconsin","WI"),("wyoming","Wyoming","WY"),
]

# ── US CITIES (origin airports) ───────────────────────────────────────────────
US_CITIES = [
    ("new-york","New York","JFK"),("los-angeles","Los Angeles","LAX"),
    ("chicago","Chicago","ORD"),("houston","Houston","IAH"),("phoenix","Phoenix","PHX"),
    ("philadelphia","Philadelphia","PHL"),("san-antonio","San Antonio","SAT"),
    ("san-diego","San Diego","SAN"),("dallas","Dallas","DFW"),("san-jose","San Jose","SJC"),
    ("austin","Austin","AUS"),("jacksonville","Jacksonville","JAX"),
    ("fort-worth","Fort Worth","DFW"),("columbus","Columbus","CMH"),
    ("charlotte","Charlotte","CLT"),("indianapolis","Indianapolis","IND"),
    ("san-francisco","San Francisco","SFO"),("seattle","Seattle","SEA"),
    ("denver","Denver","DEN"),("nashville","Nashville","BNA"),
    ("oklahoma-city","Oklahoma City","OKC"),("washington-dc","Washington DC","IAD"),
    ("boston","Boston","BOS"),("las-vegas","Las Vegas","LAS"),
    ("memphis","Memphis","MEM"),("louisville","Louisville","SDF"),
    ("portland","Portland","PDX"),("baltimore","Baltimore","BWI"),
    ("milwaukee","Milwaukee","MKE"),("albuquerque","Albuquerque","ABQ"),
    ("tucson","Tucson","TUS"),("fresno","Fresno","FAT"),
    ("sacramento","Sacramento","SMF"),("atlanta","Atlanta","ATL"),
    ("kansas-city","Kansas City","MCI"),("omaha","Omaha","OMA"),
    ("colorado-springs","Colorado Springs","COS"),("raleigh","Raleigh","RDU"),
    ("minneapolis","Minneapolis","MSP"),("tampa","Tampa","TPA"),
    ("new-orleans","New Orleans","MSY"),("pittsburgh","Pittsburgh","PIT"),
    ("cincinnati","Cincinnati","CVG"),("cleveland","Cleveland","CLE"),
    ("salt-lake-city","Salt Lake City","SLC"),("miami","Miami","MIA"),
    ("orlando","Orlando","MCO"),("detroit","Detroit","DTW"),
    ("norfolk","Norfolk","ORF"),("richmond","Richmond","RIC"),
    ("hartford","Hartford","BDL"),("buffalo","Buffalo","BUF"),
    ("rochester","Rochester","ROC"),("syracuse","Syracuse","SYR"),
    ("albany","Albany","ALB"),("providence","Providence","PVD"),
    ("hartford","Hartford","BDL"),("burlington","Burlington","BTV"),
    ("manchester","Manchester","MHT"),("portland-me","Portland ME","PWM"),
    ("bangor","Bangor","BGR"),("richmond-va","Richmond","RIC"),
    ("roanoke","Roanoke","ROA"),("greensboro","Greensboro","GSO"),
    ("wilmington","Wilmington","ILM"),("myrtle-beach","Myrtle Beach","MYR"),
    ("charleston","Charleston","CHS"),("savannah","Savannah","SAV"),
    ("jacksonville-nc","Jacksonville NC","OAJ"),("daytona-beach","Daytona Beach","DAB"),
    ("fort-myers","Fort Myers","RSW"),("west-palm-beach","West Palm Beach","PBI"),
    ("fort-lauderdale","Fort Lauderdale","FLL"),("key-west","Key West","EYW"),
    ("birmingham","Birmingham","BHM"),("huntsville","Huntsville","HSV"),
    ("mobile","Mobile","MOB"),("montgomery","Montgomery","MGM"),
    ("jackson-ms","Jackson MS","JAN"),("baton-rouge","Baton Rouge","BTR"),
    ("shreveport","Shreveport","SHV"),("little-rock","Little Rock","LIT"),
    ("knoxville","Knoxville","TYS"),("chattanooga","Chattanooga","CHA"),
    ("tri-cities","Tri Cities TN","TRI"),("lexington","Lexington","LEX"),
    ("evansville","Evansville","EVV"),("south-bend","South Bend","SBN"),
    ("grand-rapids","Grand Rapids","GRR"),("flint","Flint","FNT"),
    ("lansing","Lansing","LAN"),("kalamazoo","Kalamazoo","AZO"),
    ("green-bay","Green Bay","GRB"),("madison","Madison","MSN"),
    ("des-moines","Des Moines","DSM"),("cedar-rapids","Cedar Rapids","CID"),
    ("sioux-city","Sioux City","SUX"),("dayton","Dayton","DAY"),
    ("akron","Akron","CAK"),("toledo","Toledo","TOL"),
    ("wichita","Wichita","ICT"),("topeka","Topeka","FOE"),
    ("tulsa","Tulsa","TUL"),("fargo","Fargo","FAR"),
    ("sioux-falls","Sioux Falls","FSD"),("rapid-city","Rapid City","RAP"),
    ("bismarck","Bismarck","BIS"),("billings","Billings","BIL"),
    ("great-falls","Great Falls","GTF"),("bozeman","Bozeman","BZN"),
    ("missoula","Missoula","MSO"),("spokane","Spokane","GEG"),
    ("boise","Boise","BOI"),("eugene","Eugene","EUG"),
    ("medford","Medford","MFR"),("reno","Reno","RNO"),
    ("las-cruces","Las Cruces","LSC"),("el-paso","El Paso","ELP"),
    ("lubbock","Lubbock","LBB"),("amarillo","Amarillo","AMA"),
    ("midland","Midland","MAF"),("corpus-christi","Corpus Christi","CRP"),
    ("brownsville","Brownsville","BRO"),("mcallen","McAllen","MFE"),
    ("laredo","Laredo","LRD"),("el-paso-tx","El Paso TX","ELP"),
    ("anchorage","Anchorage","ANC"),("fairbanks","Fairbanks","FAI"),
    ("juneau","Juneau","JNU"),("honolulu","Honolulu","HNL"),
    ("maui","Maui","OGG"),("kauai","Kauai","LIH"),("kona","Kona","KOA"),
]

# dedup
seen_c = set()
US_CITIES_DEDUP = []
for c in US_CITIES:
    if c[0] not in seen_c:
        seen_c.add(c[0])
        US_CITIES_DEDUP.append(c)
US_CITIES = US_CITIES_DEDUP

# ── DOMESTIC DESTINATIONS ─────────────────────────────────────────────────────
DOMESTIC_DESTS = [
    ("new-york","New York","JFK"),("los-angeles","Los Angeles","LAX"),
    ("miami","Miami","MIA"),("orlando","Orlando","MCO"),
    ("las-vegas","Las Vegas","LAS"),("chicago","Chicago","ORD"),
    ("san-francisco","San Francisco","SFO"),("seattle","Seattle","SEA"),
    ("denver","Denver","DEN"),("nashville","Nashville","BNA"),
    ("boston","Boston","BOS"),("atlanta","Atlanta","ATL"),
    ("dallas","Dallas","DFW"),("houston","Houston","IAH"),
    ("phoenix","Phoenix","PHX"),("honolulu","Honolulu","HNL"),
    ("new-orleans","New Orleans","MSY"),("charlotte","Charlotte","CLT"),
    ("san-diego","San Diego","SAN"),("portland","Portland","PDX"),
    ("austin","Austin","AUS"),("tampa","Tampa","TPA"),
    ("washington-dc","Washington DC","IAD"),("minneapolis","Minneapolis","MSP"),
    ("raleigh","Raleigh","RDU"),("salt-lake-city","Salt Lake City","SLC"),
    ("anchorage","Anchorage","ANC"),("maui","Maui","OGG"),
    ("fort-lauderdale","Fort Lauderdale","FLL"),("san-antonio","San Antonio","SAT"),
]

# ── INTERNATIONAL DESTINATIONS ────────────────────────────────────────────────
INTL_DESTS = [
    ("london","London","LHR","UK"),("paris","Paris","CDG","France"),
    ("cancun","Cancún","CUN","Mexico"),("mexico-city","Mexico City","MEX","Mexico"),
    ("tokyo","Tokyo","NRT","Japan"),("sydney","Sydney","SYD","Australia"),
    ("toronto","Toronto","YYZ","Canada"),("vancouver","Vancouver","YVR","Canada"),
    ("montreal","Montreal","YUL","Canada"),("dubai","Dubai","DXB","UAE"),
    ("amsterdam","Amsterdam","AMS","Netherlands"),("rome","Rome","FCO","Italy"),
    ("barcelona","Barcelona","BCN","Spain"),("madrid","Madrid","MAD","Spain"),
    ("frankfurt","Frankfurt","FRA","Germany"),("zurich","Zurich","ZRH","Switzerland"),
    ("punta-cana","Punta Cana","PUJ","Dominican Republic"),
    ("montego-bay","Montego Bay","MBJ","Jamaica"),
    ("nassau","Nassau","NAS","Bahamas"),("aruba","Aruba","AUA","Aruba"),
    ("costa-rica","San José","SJO","Costa Rica"),("panama","Panama City","PTY","Panama"),
    ("bogota","Bogotá","BOG","Colombia"),("lima","Lima","LIM","Peru"),
    ("buenos-aires","Buenos Aires","EZE","Argentina"),("sao-paulo","São Paulo","GRU","Brazil"),
    ("singapore","Singapore","SIN","Singapore"),("hong-kong","Hong Kong","HKG","HK"),
    ("bangkok","Bangkok","BKK","Thailand"),("bali","Bali","DPS","Indonesia"),
    ("seoul","Seoul","ICN","South Korea"),("beijing","Beijing","PEK","China"),
    ("shanghai","Shanghai","PVG","China"),("delhi","Delhi","DEL","India"),
    ("mumbai","Mumbai","BOM","India"),("doha","Doha","DOH","Qatar"),
    ("istanbul","Istanbul","IST","Turkey"),("athens","Athens","ATH","Greece"),
    ("dublin","Dublin","DUB","Ireland"),("lisbon","Lisbon","LIS","Portugal"),
]

# dedup intl
seen_i = set()
INTL_DEDUP = []
for d in INTL_DESTS:
    if d[0] not in seen_i:
        seen_i.add(d[0])
        INTL_DEDUP.append(d)
INTL_DESTS = INTL_DEDUP

# ── STATE INTENTS (40) ────────────────────────────────────────────────────────
STATE_INTENTS = [
    ("cheap-flights","cheap flights","cheapest flights"),
    ("justfly-review","JustFly review","JustFly reviews"),
    ("cheap-flights-justfly","cheap flights JustFly","find cheap flights JustFly"),
    ("flight-deals","flight deals","best flight deals"),
    ("airline-tickets","cheap airline tickets","discount airline tickets"),
    ("one-way-flights","one-way flights","cheap one way flights"),
    ("round-trip-flights","round trip flights","cheap round trip flights"),
    ("last-minute-flights","last minute flights","last minute flight deals"),
    ("nonstop-flights","nonstop flights","direct flights"),
    ("budget-flights","budget flights","budget airline tickets"),
    ("international-flights","international flights","cheap international flights"),
    ("domestic-flights","domestic flights","cheap domestic flights"),
    ("flight-comparison","flight comparison","compare flights"),
    ("justfly-vs-expedia","JustFly vs Expedia","JustFly versus Expedia"),
    ("justfly-vs-kayak","JustFly vs Kayak","JustFly versus Kayak"),
    ("justfly-vs-google","JustFly vs Google Flights","JustFly versus Google Flights"),
    ("justfly-legit","is JustFly legit","JustFly reviews legit"),
    ("best-time-to-book","best time to book flights","when to book cheap flights"),
    ("cheapest-day-to-fly","cheapest day to fly","what day is cheapest to fly"),
    ("flexible-dates-flights","flexible date flights","flexible travel date search"),
    ("flight-price-alert","flight price alert","set flight price alert"),
    ("bundle-flight-hotel","flight and hotel bundle","cheap flight hotel bundle"),
    ("justfly-cancellation","JustFly cancellation policy","can I cancel JustFly"),
    ("justfly-baggage","JustFly baggage fees","JustFly checked bag fees"),
    ("justfly-app","JustFly app","JustFly mobile app"),
    ("justfly-customer-service","JustFly customer service","JustFly support"),
    ("cheap-flights-nyc","cheap flights to New York","flights to NYC"),
    ("cheap-flights-miami","cheap flights to Miami","flights to Miami"),
    ("cheap-flights-cancun","cheap flights to Cancún","flights to Cancun"),
    ("cheap-flights-la","cheap flights to Los Angeles","flights to LA"),
    ("cheap-flights-las-vegas","cheap flights to Las Vegas","flights to Vegas"),
    ("cheap-flights-orlando","cheap flights to Orlando","flights to Orlando"),
    ("multi-city-flights","multi-city flights","multi city flight search"),
    ("first-class-deals","first class deals","cheap first class flights"),
    ("business-class-deals","business class deals","cheap business class flights"),
    ("student-flight-deals","student flight deals","student discount flights"),
    ("senior-flight-deals","senior flight deals","senior discount flights"),
    ("military-flight-deals","military flight deals","military discount flights"),
    ("nearby-airports","nearby airport flights","flights from nearby airports"),
    ("justfly-promo-code","JustFly promo code","JustFly discount code"),
]

# ── LONG TAIL (200) ───────────────────────────────────────────────────────────
LONG_TAILS = [
    # JustFly specific
    ("is-justfly-legit","Is JustFly Legit 2026","is justfly legitimate trustworthy"),
    ("justfly-review-2026","JustFly Review 2026","justfly.com review 2026"),
    ("justfly-reviews-complaints","JustFly Reviews & Complaints","justfly customer reviews complaints"),
    ("justfly-refund","JustFly Refund Policy","justfly refund how to get"),
    ("justfly-cancellation-policy","JustFly Cancellation Policy","can you cancel justfly booking"),
    ("justfly-hidden-fees","JustFly Hidden Fees","justfly fees charges"),
    ("justfly-baggage-policy","JustFly Baggage Policy","justfly checked bag fee"),
    ("justfly-seat-selection","JustFly Seat Selection","how to select seat justfly"),
    ("justfly-change-flight","JustFly Change Flight","how to change justfly flight"),
    ("justfly-promo-code","JustFly Promo Code 2026","justfly discount code coupon"),
    ("justfly-vs-priceline","JustFly vs Priceline","justfly versus priceline"),
    ("justfly-vs-hopper","JustFly vs Hopper","justfly versus hopper app"),
    ("justfly-vs-cheapoair","JustFly vs CheapOair","justfly versus cheapoair"),
    ("justfly-vs-orbitz","JustFly vs Orbitz","justfly versus orbitz"),
    ("justfly-vs-travelocity","JustFly vs Travelocity","justfly versus travelocity"),
    ("justfly-app-review","JustFly App Review","justfly mobile app review"),
    ("justfly-login","JustFly Login","justfly account login"),
    ("justfly-booking-confirmation","JustFly Booking Confirmation","justfly booking confirmation email"),
    ("justfly-phone-number","JustFly Phone Number","justfly customer service phone"),
    ("justfly-email","JustFly Email Support","justfly support email contact"),
    # Cheap flight general
    ("cheapest-flights-usa","Cheapest Flights in USA","cheapest domestic flights usa 2026"),
    ("cheapest-international-flights","Cheapest International Flights","cheapest flights abroad from usa"),
    ("how-to-find-cheap-flights","How to Find Cheap Flights","how to get cheapest airfare"),
    ("when-to-book-flights","When to Book Flights","best time to book cheap flights"),
    ("cheapest-day-to-fly","Cheapest Day to Fly","what day is cheapest to fly 2026"),
    ("cheapest-day-to-book","Cheapest Day to Book Flights","best day to buy airline tickets"),
    ("cheapest-month-to-fly","Cheapest Month to Fly","cheapest time to fly usa"),
    ("incognito-flight-search","Incognito Flight Search","does incognito mode find cheaper flights"),
    ("flexible-dates-cheap","Flexible Dates Cheap Flights","how to use flexible dates find cheap flights"),
    ("nearby-airport-cheaper","Nearby Airport Cheaper Flights","fly from nearby airport save money"),
    ("fare-alert-flights","Flight Fare Alert","how to set flight fare alert"),
    ("flight-price-drop","Flight Price Drop","when do flight prices drop"),
    ("last-minute-flight-deal","Last Minute Flight Deal","find last minute cheap flights"),
    ("mistake-fare","Mistake Fare Flights","how to find mistake fare flights"),
    ("flight-deal-sites","Flight Deal Sites","best flight deal websites 2026"),
    ("google-flights-vs-justfly","Google Flights vs JustFly","google flights versus justfly which better"),
    ("expedia-vs-justfly","Expedia vs JustFly","expedia versus justfly cheaper"),
    ("kayak-vs-justfly","Kayak vs JustFly","kayak versus justfly comparison"),
    ("priceline-vs-justfly","Priceline vs JustFly","priceline versus justfly"),
    ("skyscanner-vs-justfly","Skyscanner vs JustFly","skyscanner versus justfly"),
    # Domestic routes
    ("cheap-flights-nyc-miami","Cheap Flights NYC to Miami","new york to miami cheap flights"),
    ("cheap-flights-nyc-la","Cheap Flights NYC to LA","new york to los angeles cheap flights"),
    ("cheap-flights-nyc-chicago","Cheap Flights NYC to Chicago","new york to chicago cheap flights"),
    ("cheap-flights-la-nyc","Cheap Flights LA to NYC","los angeles to new york cheap flights"),
    ("cheap-flights-la-chicago","Cheap Flights LA to Chicago","los angeles to chicago cheap flights"),
    ("cheap-flights-chicago-nyc","Cheap Flights Chicago to NYC","chicago to new york cheap flights"),
    ("cheap-flights-dallas-chicago","Cheap Flights Dallas to Chicago","dallas to chicago cheap flights"),
    ("cheap-flights-houston-nyc","Cheap Flights Houston to NYC","houston to new york cheap flights"),
    ("cheap-flights-boston-miami","Cheap Flights Boston to Miami","boston to miami cheap flights"),
    ("cheap-flights-atlanta-nyc","Cheap Flights Atlanta to NYC","atlanta to new york cheap flights"),
    ("cheap-flights-denver-chicago","Cheap Flights Denver to Chicago","denver to chicago cheap flights"),
    ("cheap-flights-seattle-nyc","Cheap Flights Seattle to NYC","seattle to new york cheap flights"),
    ("cheap-flights-sf-nyc","Cheap Flights SF to NYC","san francisco to new york cheap flights"),
    ("cheap-flights-miami-nyc","Cheap Flights Miami to NYC","miami to new york cheap flights"),
    ("cheap-flights-orlando-nyc","Cheap Flights Orlando to NYC","orlando to new york cheap flights"),
    ("cheap-flights-phoenix-chicago","Cheap Flights Phoenix to Chicago","phoenix to chicago cheap flights"),
    ("cheap-flights-minneapolis-chicago","Cheap Flights Minneapolis to Chicago","minneapolis to chicago cheap flights"),
    ("cheap-flights-dc-nyc","Cheap Flights DC to NYC","washington dc to new york cheap flights"),
    ("cheap-flights-nashville-nyc","Cheap Flights Nashville to NYC","nashville to new york cheap flights"),
    ("cheap-flights-las-vegas-nyc","Cheap Flights Las Vegas to NYC","las vegas to new york cheap flights"),
    # International routes
    ("cheap-flights-usa-london","Cheap Flights USA to London","cheapest flights usa to london"),
    ("cheap-flights-usa-paris","Cheap Flights USA to Paris","cheapest flights usa to paris"),
    ("cheap-flights-usa-cancun","Cheap Flights USA to Cancún","cheapest flights usa to cancun"),
    ("cheap-flights-usa-mexico","Cheap Flights USA to Mexico","cheap flights usa to mexico city"),
    ("cheap-flights-usa-tokyo","Cheap Flights USA to Tokyo","cheapest flights usa to tokyo"),
    ("cheap-flights-usa-sydney","Cheap Flights USA to Sydney","cheapest flights usa to australia"),
    ("cheap-flights-usa-toronto","Cheap Flights USA to Toronto","cheap flights usa to canada"),
    ("cheap-flights-usa-jamaica","Cheap Flights USA to Jamaica","cheap flights to montego bay"),
    ("cheap-flights-usa-punta-cana","Cheap Flights USA to Punta Cana","cheap flights to punta cana"),
    ("cheap-flights-usa-bahamas","Cheap Flights USA to Bahamas","cheap flights to nassau bahamas"),
    ("cheap-flights-usa-costa-rica","Cheap Flights USA to Costa Rica","cheap flights usa to san jose cr"),
    ("cheap-flights-usa-amsterdam","Cheap Flights USA to Amsterdam","cheapest flights usa to amsterdam"),
    ("cheap-flights-usa-rome","Cheap Flights USA to Rome","cheap flights usa to italy"),
    ("cheap-flights-usa-barcelona","Cheap Flights USA to Barcelona","cheap flights usa to spain"),
    ("cheap-flights-usa-dubai","Cheap Flights USA to Dubai","cheap flights usa to uae"),
    ("cheap-flights-usa-bali","Cheap Flights USA to Bali","cheap flights usa to indonesia"),
    ("cheap-flights-usa-bangkok","Cheap Flights USA to Bangkok","cheap flights usa to thailand"),
    ("cheap-flights-usa-aruba","Cheap Flights USA to Aruba","cheap flights aruba from usa"),
    ("cheap-flights-usa-ireland","Cheap Flights USA to Ireland","cheap flights usa to dublin"),
    ("cheap-flights-usa-greece","Cheap Flights USA to Greece","cheap flights usa to athens"),
    # Airline specific
    ("american-airlines-deals","American Airlines Deals","american airlines cheap flights"),
    ("united-airlines-deals","United Airlines Deals","united airlines cheap flights"),
    ("delta-deals","Delta Airlines Deals","delta cheap flights"),
    ("southwest-deals","Southwest Airlines Deals","southwest cheap flights"),
    ("jetblue-deals","JetBlue Deals","jetblue cheap flights"),
    ("spirit-airlines-deals","Spirit Airlines Deals","spirit airlines cheap flights"),
    ("frontier-deals","Frontier Airlines Deals","frontier cheap flights"),
    ("alaska-airlines-deals","Alaska Airlines Deals","alaska airlines cheap flights"),
    ("british-airways-deals","British Airways Deals","british airways cheap flights usa"),
    ("air-canada-deals","Air Canada Deals","air canada cheap flights"),
    ("lufthansa-deals","Lufthansa Deals","lufthansa cheap flights"),
    ("emirates-deals","Emirates Deals","emirates cheap flights"),
    ("air-france-deals","Air France Deals","air france cheap flights from usa"),
    ("aeromexico-deals","Aeromexico Deals","aeromexico cheap flights"),
    ("avianca-deals","Avianca Deals","avianca cheap flights"),
    # Travel type
    ("solo-travel-flights","Solo Travel Cheap Flights","cheap flights solo traveler"),
    ("family-travel-flights","Family Travel Cheap Flights","cheap family flights usa"),
    ("couple-travel-flights","Couple Travel Cheap Flights","cheap flights for 2 people"),
    ("group-travel-flights","Group Travel Cheap Flights","cheap group flights booking"),
    ("honeymoon-flights","Honeymoon Cheap Flights","cheap honeymoon flights"),
    ("spring-break-flights","Spring Break Cheap Flights","cheap spring break flights"),
    ("summer-flights","Summer Cheap Flights","cheap summer flights 2026"),
    ("thanksgiving-flights","Thanksgiving Cheap Flights","cheap thanksgiving flights"),
    ("christmas-flights","Christmas Cheap Flights","cheap christmas flights"),
    ("new-year-flights","New Year Cheap Flights","cheap new years flights"),
    # Tips and strategy
    ("incognito-search-flights","Incognito Search for Flights","use incognito mode find cheap flights"),
    ("vpn-cheaper-flights","VPN Cheaper Flights","does vpn get cheaper flights"),
    ("credit-card-flight-deals","Credit Card Flight Deals","use credit card points flights"),
    ("award-flights","Award Flights","award flight booking tips"),
    ("flight-hacking","Flight Hacking Tips","how to hack flight prices"),
    ("error-fares","Error Fares","airline error fare how to find"),
    ("positioning-flight","Positioning Flight","positioning flight travel hack"),
    ("open-jaw-ticket","Open Jaw Ticket","what is open jaw flight ticket"),
    ("hidden-city-ticketing","Hidden City Ticketing","hidden city flight trick"),
    ("back-to-back-ticketing","Back to Back Ticketing","back to back flight booking"),
    # More comparisons
    ("booking-com-vs-justfly","Booking.com vs JustFly","booking.com versus justfly flights"),
    ("cheapflights-vs-justfly","CheapFlights vs JustFly","cheapflights versus justfly"),
    ("hotwire-vs-justfly","Hotwire vs JustFly","hotwire versus justfly"),
    ("tripadvisor-flights-vs-justfly","TripAdvisor vs JustFly","tripadvisor flights versus justfly"),
    ("momondo-vs-justfly","Momondo vs JustFly","momondo versus justfly"),
    ("scott-cheap-flights","Scott's Cheap Flights","scotts cheap flights vs justfly"),
    ("going-deals","Going Deals","going cheap flights review"),
    ("dollar-flight-club","Dollar Flight Club","dollar flight club review"),
    ("secret-flying","Secret Flying","secret flying deals review"),
    ("airfarewatchdog","AirfareWatchdog","airfarewatchdog review"),
    # Specific topics
    ("cheapest-airlines-usa","Cheapest Airlines USA","cheapest airlines to fly in usa"),
    ("budget-airlines-usa","Budget Airlines USA","best budget airlines usa 2026"),
    ("no-frills-airlines","No Frills Airlines","no frills airline tickets usa"),
    ("ultra-low-cost-carrier","Ultra Low Cost Carrier","ultra low cost carrier usa"),
    ("premium-economy-deals","Premium Economy Deals","cheap premium economy flights"),
    ("business-class-deals","Business Class Deals","cheap business class flights usa"),
    ("first-class-deals","First Class Deals","cheap first class flights usa"),
    ("flight-upgrade","Flight Upgrade Tips","how to get flight upgrade cheap"),
    ("standby-flights","Standby Flights","standby flight tips"),
    ("same-day-flights","Same Day Flights","same day cheap flights"),
    # More domestic routes
    ("cheap-flights-nyc-london","Cheap Flights NYC to London","new york to london cheap"),
    ("cheap-flights-la-tokyo","Cheap Flights LA to Tokyo","los angeles to tokyo cheap"),
    ("cheap-flights-sf-tokyo","Cheap Flights SF to Tokyo","san francisco to tokyo cheap"),
    ("cheap-flights-chicago-london","Cheap Flights Chicago to London","chicago to london cheap"),
    ("cheap-flights-miami-cancun","Cheap Flights Miami to Cancún","miami to cancun cheap"),
    ("cheap-flights-dallas-cancun","Cheap Flights Dallas to Cancún","dallas to cancun cheap"),
    ("cheap-flights-houston-cancun","Cheap Flights Houston to Cancún","houston to cancun cheap"),
    ("cheap-flights-chicago-cancun","Cheap Flights Chicago to Cancún","chicago to cancun cheap"),
    ("cheap-flights-nyc-cancun","Cheap Flights NYC to Cancún","new york to cancun cheap"),
    ("cheap-flights-boston-cancun","Cheap Flights Boston to Cancún","boston to cancun cheap"),
    # Trending 2026
    ("flight-prices-2026","Flight Prices 2026","are flight prices going up 2026"),
    ("airfare-forecast-2026","Airfare Forecast 2026","airfare price forecast 2026"),
    ("best-travel-deals-2026","Best Travel Deals 2026","best flight deals 2026"),
    ("travel-trends-2026","Travel Trends 2026","biggest travel trends 2026"),
    ("post-pandemic-flights","Post Pandemic Flights","flying in 2026 what to expect"),
    ("cheap-flights-summer-2026","Cheap Summer Flights 2026","cheapest summer flights 2026"),
    ("cheap-flights-fall-2026","Cheap Fall Flights 2026","cheapest fall flights 2026"),
    ("cheap-flights-winter-2026","Cheap Winter Flights 2026","cheapest winter flights 2026"),
    ("cheap-flights-spring-2026","Cheap Spring Flights 2026","cheapest spring flights 2026"),
    ("holiday-flights-2026","Holiday Flights 2026","holiday travel deals 2026"),
]

# ── SHARED CSS / JS / COMPONENTS ──────────────────────────────────────────────
CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{font-family:'Inter',sans-serif;background:#f7f8fc;color:#1a1a2e;line-height:1.7;}
a{text-decoration:none;color:inherit;}
nav{background:#0a2463;padding:0 1.5rem;display:flex;align-items:center;justify-content:space-between;height:60px;position:sticky;top:0;z-index:100;}
.nav-logo{color:#fff;font-weight:800;font-size:1.15rem;display:flex;align-items:center;gap:6px;}
.nav-logo span{color:#ff6b00;}
.nav-links{display:flex;gap:1.5rem;}
.nav-links a{color:rgba(255,255,255,0.75);font-size:0.85rem;font-weight:600;transition:color 0.2s;}
.nav-links a:hover{color:#fff;}
.nav-book{background:#ff6b00;color:#fff!important;padding:6px 16px;border-radius:50px;font-weight:700!important;}
.hero{background:linear-gradient(135deg,#0a2463 0%,#1a4a8a 60%,#0d3b7a 100%);color:#fff;text-align:center;padding:5rem 1.5rem 4rem;}
.hero-badge{display:inline-block;background:rgba(255,107,0,0.2);border:1px solid rgba(255,107,0,0.5);color:#ffaa66;padding:5px 16px;border-radius:50px;font-size:0.8rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1.5rem;}
.hero h1{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;line-height:1.1;margin-bottom:1rem;}
.hero h1 em{color:#ff6b00;font-style:normal;}
.hero p{font-size:1.1rem;color:rgba(255,255,255,0.75);max-width:520px;margin:0 auto 2rem;}
.btn{display:inline-block;padding:16px 36px;border-radius:8px;font-weight:700;font-size:1rem;transition:transform 0.2s,box-shadow 0.2s;}
.btn-orange{background:#ff6b00;color:#fff;box-shadow:0 6px 24px rgba(255,107,0,0.4);}
.btn-orange:hover{transform:translateY(-3px);box-shadow:0 12px 32px rgba(255,107,0,0.5);}
.btn-ghost{border:2px solid rgba(255,255,255,0.3);color:#fff;margin-left:1rem;}
.btn-ghost:hover{background:rgba(255,255,255,0.1);}
.hero-stats{display:flex;justify-content:center;gap:3rem;margin-top:3.5rem;flex-wrap:wrap;}
.hero-stat-num{font-size:2rem;font-weight:800;}
.hero-stat-label{font-size:0.75rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.08em;}
.urgency{background:#fff3e0;border-top:3px solid #ff6b00;text-align:center;padding:0.75rem 1rem;font-weight:600;font-size:0.95rem;color:#7a3300;}
#countdown{color:#ff6b00;font-weight:800;}
.urgency-bar-wrap{height:6px;background:#ffe0b2;margin-top:0.4rem;}
#urgency-bar{height:100%;background:#ff6b00;transition:width 1s linear;}
.section{padding:4rem 1.5rem;}
.section-alt{background:#fff;}
.container{max-width:1100px;margin:0 auto;}
.section-tag{font-size:0.72rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#ff6b00;margin-bottom:0.5rem;}
.section-title{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:800;color:#0a2463;margin-bottom:0.5rem;}
.section-sub{color:#666;margin-bottom:2.5rem;max-width:540px;}
.center{text-align:center;}
.center .section-sub{margin-left:auto;margin-right:auto;}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;margin-bottom:2rem;}
.card{background:#fff;border-radius:14px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,0.07);border:1px solid #eef0f8;transition:transform 0.25s,box-shadow 0.25s;display:block;}
.card:hover{transform:translateY(-6px);box-shadow:0 12px 36px rgba(10,36,99,0.12);}
.card-icon{font-size:2rem;margin-bottom:1rem;}
.card h3{font-size:1.05rem;font-weight:700;color:#0a2463;margin-bottom:0.5rem;}
.card p{font-size:0.9rem;color:#555;margin-bottom:1rem;}
.card-link{font-size:0.85rem;font-weight:700;color:#ff6b00;}
.dest-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem;}
.dest{background:#fff;border-radius:12px;padding:1.2rem;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,0.07);border:1px solid #eef0f8;transition:transform 0.2s;display:block;}
.dest:hover{transform:translateY(-4px);}
.dest-emoji{font-size:2rem;margin-bottom:0.4rem;}
.dest-city{font-weight:700;color:#0a2463;font-size:0.95rem;}
.dest-price{color:#ff6b00;font-weight:700;font-size:0.85rem;margin-top:0.2rem;}
.cta-band{background:linear-gradient(135deg,#0a2463,#1a4a8a);color:#fff;text-align:center;padding:3.5rem 1.5rem;margin:2rem 0;}
.cta-band h2{font-size:clamp(1.4rem,3vw,2rem);font-weight:800;margin-bottom:0.75rem;}
.cta-band p{color:rgba(255,255,255,0.75);margin-bottom:2rem;}
.tips{display:grid;gap:1rem;}
.tip{display:flex;gap:1rem;background:#fff;padding:1.2rem 1.5rem;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.06);border-left:4px solid #0a2463;}
.tip-n{font-size:1.2rem;font-weight:800;color:#0a2463;min-width:28px;}
.tip-t strong{display:block;font-size:0.95rem;color:#0a2463;margin-bottom:0.2rem;}
.tip-t span{font-size:0.87rem;color:#666;}
.faqs{display:grid;gap:1rem;}
.faq{background:#fff;border-radius:12px;padding:1.4rem 1.6rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #eef0f8;}
.faq-q{font-weight:700;color:#0a2463;margin-bottom:0.4rem;}
.faq-a{font-size:0.9rem;color:#555;}
.rel-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:0.75rem;margin-top:1.5rem;}
.rel-link{background:#fff;border:1px solid #eef0f8;border-radius:8px;padding:0.7rem 1rem;font-size:0.85rem;font-weight:600;color:#0a2463;transition:border-color 0.2s,box-shadow 0.2s;}
.rel-link:hover{border-color:#ff6b00;box-shadow:0 4px 12px rgba(255,107,0,0.1);}
.sticky{position:fixed;bottom:20px;right:20px;background:#ff6b00;color:#fff;padding:14px 24px;border-radius:8px;font-weight:700;font-size:0.9rem;box-shadow:0 6px 20px rgba(255,107,0,0.45);z-index:999;transition:transform 0.2s;}
.sticky:hover{transform:scale(1.05);}
footer{background:#0a2463;color:rgba(255,255,255,0.6);text-align:center;padding:1.5rem;font-size:0.82rem;}
footer a{color:rgba(255,255,255,0.5);}
footer a:hover{color:#fff;}
.disclosure{font-size:0.78rem;color:#999;text-align:center;padding:1rem;border-top:1px solid #eee;}
.fade{opacity:0;transform:translateY(20px);transition:opacity 0.6s ease,transform 0.6s ease;}
.fade.on{opacity:1;transform:none;}
@media(max-width:768px){.nav-links{display:none;}.hero-stats{gap:1.5rem;}.btn-ghost{display:none;}}"""

JS = """const el=document.getElementById('countdown');const bar=document.getElementById('urgency-bar');
if(el&&bar){const total=6*60*60*1000,end=Date.now()+total;
function tick(){const d=end-Date.now();if(d<=0){el.textContent='Expired';bar.style.width='0%';return;}
const h=Math.floor(d/3600000),m=Math.floor((d%3600000)/60000),s=Math.floor((d%60000)/1000);
el.textContent=h+'h '+m+'m '+s+'s';const pct=(d/total)*100;bar.style.width=pct+'%';
bar.style.background=pct>66?'#22c55e':pct>33?'#f59e0b':'#ef4444';}tick();setInterval(tick,1000);}
const faders=document.querySelectorAll('.fade');
function check(){faders.forEach(el=>{if(el.getBoundingClientRect().top<window.innerHeight-60)el.classList.add('on');});}
window.addEventListener('scroll',check);window.addEventListener('load',check);"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">'

def nav_html():
    return f"""<nav>
  <div class="nav-logo">✈ Flight<span>Deals</span>Pro</div>
  <div class="nav-links">
    <a href="index.html">Home</a>
    <a href="flights.html">Flights</a>
    <a href="destinations.html">Destinations</a>
    <a href="tips.html">Tips</a>
    <a href="comparison.html">Compare</a>
    <a href="faq.html">FAQ</a>
    <a href="{AFF}" class="nav-book">Book Now ✈</a>
  </div>
</nav>"""

STICKY_HTML = f'<a href="{AFF}" class="sticky">✈ Book Now on JustFly</a>'

FOOTER_HTML = f"""<div class="disclosure">This site contains affiliate links. We earn a commission when you book through our links at no extra cost to you. | aff_id=21885</div>
<footer>
  <p>© {YEAR} FlightDealsPro | Powered by JustFly.com</p>
  <p style="margin-top:0.4rem;"><a href="about.html">About</a> &nbsp;|&nbsp; <a href="faq.html">FAQ</a> &nbsp;|&nbsp; <a href="disclosure.html">Disclosure</a></p>
</footer>"""

def urgency_html():
    return """<div class="urgency">
  ⏰ Limited fares — offer ends in: <span id="countdown">Loading...</span>
  <div class="urgency-bar-wrap"><div id="urgency-bar" style="width:100%;"></div></div>
</div>"""

def cta_band(h2, p):
    return f"""<div class="cta-band fade">
  <div class="container">
    <h2>{h2}</h2>
    <p>{p}</p>
    <a href="{AFF}" class="btn btn-orange" style="font-size:1.1rem;padding:18px 40px;">✈ Find Cheap Flights on JustFly</a>
  </div>
</div>"""

def make_page(slug, title, desc, body, schema=""):
    canonical = f"{BASE_URL}/{slug}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
{FONTS}
{schema}
<style>{CSS}</style>
</head>
<body>
{nav_html()}
{body}
{FOOTER_HTML}
{STICKY_HTML}
<script>{JS}</script>
</body>
</html>"""

# ── STATE PAGES ───────────────────────────────────────────────────────────────
def make_state_page(st_slug, st_name, st_abbr, i_slug, i_name, i_kw):
    slug  = f"justfly-{st_slug}-{i_slug}.html"
    title = f"{i_name.title()} {st_name} {YEAR} — JustFly | FlightDealsPro"
    desc  = f"Find {i_kw} in {st_name} through JustFly. Compare 500+ airlines instantly. No hidden fees. Best fares for {st_abbr} travelers {YEAR}."
    body  = f"""
<section class="hero">
  <div class="hero-badge">✈ {st_abbr} · JustFly · {YEAR}</div>
  <h1>✈ <em>{i_name.title()}</em><br>{st_name}</h1>
  <p>Find {i_kw} in {st_name}. JustFly compares 500+ airlines to get you the lowest fare — no hidden fees.</p>
  <a href="{AFF}" class="btn btn-orange">🔍 Search {st_name} Flights on JustFly</a>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Why JustFly for {st_name}</div>
    <h2 class="section-title">Best {i_name.title()} in {st_name}</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">💰</div><h3>Lowest Fares in {st_name}</h3><p>JustFly compares 500+ airlines to find the cheapest flights from {st_name} airports. Book in seconds with no hidden fees.</p><span class="card-link">Search {st_name} Flights →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">✈️</div><h3>500+ Airlines Compared</h3><p>Every major airline and budget carrier serving {st_name} ({st_abbr}) compared simultaneously for the best rate.</p><span class="card-link">Compare Airlines →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🔔</div><h3>Price Alerts</h3><p>Set a fare alert for {st_name} routes and get notified the instant prices drop. Never overpay for a {st_abbr} flight.</p><span class="card-link">Set Alert →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🏨</div><h3>Bundle &amp; Save</h3><p>Add a hotel to your {st_name} flight and save up to 40% with JustFly's flight + hotel bundles.</p><span class="card-link">Find Bundles →</span></a>
    </div>
  </div>
</section>
{cta_band(f"Ready to Fly from {st_name}?", f"JustFly finds the cheapest flights from {st_name}. Compare and book in seconds.")}
<section class="section">
  <div class="container">
    <div class="section-tag">Related</div>
    <h2 class="section-title">More {st_name} Flight Resources</h2>
    <div class="rel-grid">
      {"".join(f'<a href="justfly-{s2}-{i_slug}.html" class="rel-link">✈ {sn2} {i_name.title()}</a>' for s2,sn2,sa2 in STATES[:12] if s2 != st_slug)}
    </div>
  </div>
</section>"""
    return slug, make_page(slug, title, desc, body)

# ── CITY TO DOMESTIC DESTINATION ──────────────────────────────────────────────
def make_city_dom_page(o_slug, o_name, o_code, d_slug, d_name, d_code):
    slug  = f"flights-{o_slug}-to-{d_slug}.html"
    title = f"Cheap Flights {o_name} to {d_name} {YEAR} — JustFly | FlightDealsPro"
    desc  = f"Find cheap flights from {o_name} ({o_code}) to {d_name} ({d_code}) on JustFly. Compare 500+ airlines. Best fares, no hidden fees."
    body  = f"""
<section class="hero">
  <div class="hero-badge">✈ {o_code} → {d_code} · {YEAR}</div>
  <h1>✈ <em>Cheap Flights</em><br>{o_name} to {d_name}</h1>
  <p>Compare every airline flying {o_name} to {d_name}. Find the lowest fare instantly on JustFly — no hidden fees.</p>
  <a href="{AFF}" class="btn btn-orange">🔍 Search {o_name} → {d_name} on JustFly</a>
  <div class="hero-stats">
    <div><div class="hero-stat-num">{o_code}</div><div class="hero-stat-label">Origin</div></div>
    <div><div class="hero-stat-num">{d_code}</div><div class="hero-stat-label">Destination</div></div>
    <div><div class="hero-stat-num">500+</div><div class="hero-stat-label">Airlines</div></div>
  </div>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Route Details</div>
    <h2 class="section-title">Flying {o_name} to {d_name}</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">💰</div><h3>Cheapest Fares</h3><p>JustFly compares all airlines on the {o_name}–{d_name} route to surface the absolute lowest fare available today.</p><span class="card-link">See Fares →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🔄</div><h3>Round-Trip & One-Way</h3><p>Compare round-trip and one-way fares on {o_name} to {d_name}. Mix airlines for the best combination.</p><span class="card-link">Compare →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">📅</div><h3>Flexible Dates</h3><p>Use JustFly's flexible date search to find the cheapest day to fly {o_name} to {d_name}.</p><span class="card-link">Flexible Search →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🏨</div><h3>Hotel Bundle</h3><p>Add a hotel in {d_name} to your flight and save up to 40% with a JustFly bundle deal.</p><span class="card-link">Bundle & Save →</span></a>
    </div>
    <div style="text-align:center">
      <a href="{AFF}" class="btn btn-orange">✈ Book {o_name} → {d_name} on JustFly</a>
    </div>
  </div>
</section>
{cta_band(f"Lock In Your {o_name} to {d_name} Fare", "Prices change every hour. Search now before your fare disappears.")}
<section class="section">
  <div class="container">
    <div class="section-tag">Related Routes from {o_name}</div>
    <h2 class="section-title">More {o_name} Flights</h2>
    <div class="rel-grid">
      {"".join(f'<a href="flights-{o_slug}-to-{ds2}.html" class="rel-link">✈ {o_name} → {dn2}</a>' for ds2,dn2,dc2 in DOMESTIC_DESTS[:12] if ds2 != d_slug)}
    </div>
  </div>
</section>"""
    return slug, make_page(slug, title, desc, body)

# ── CITY TO INTERNATIONAL ─────────────────────────────────────────────────────
def make_city_intl_page(o_slug, o_name, o_code, d_slug, d_name, d_code, d_country):
    slug  = f"flights-{o_slug}-to-{d_slug}.html"
    title = f"Cheap Flights {o_name} to {d_name}, {d_country} {YEAR} — JustFly"
    desc  = f"Find cheap international flights from {o_name} ({o_code}) to {d_name}, {d_country} ({d_code}). Compare 500+ airlines on JustFly. No hidden fees."
    body  = f"""
<section class="hero">
  <div class="hero-badge">🌍 {o_code} → {d_code} · {YEAR}</div>
  <h1>✈ <em>Cheap Flights</em><br>{o_name} to {d_name}</h1>
  <p>International flights from {o_name} to {d_name}, {d_country}. JustFly compares every airline for the lowest available fare.</p>
  <a href="{AFF}" class="btn btn-orange">🔍 Search {o_name} → {d_name} on JustFly</a>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">International Route</div>
    <h2 class="section-title">{o_name} to {d_name}, {d_country}</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">🌍</div><h3>{d_name}, {d_country}</h3><p>JustFly finds the cheapest international fares from {o_name} to {d_name}. Compare 500+ airlines including international carriers.</p><span class="card-link">Search Now →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">💰</div><h3>Best International Fares</h3><p>Save on your {o_name}–{d_name} flight by comparing all airlines, connection options, and fare classes on JustFly.</p><span class="card-link">Compare Fares →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">📅</div><h3>Book Early & Save</h3><p>International fares to {d_name} are cheapest 3–6 months ahead. Lock in your fare before prices rise.</p><span class="card-link">Book Early →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🏨</div><h3>{d_name} Hotel Bundle</h3><p>Add a hotel in {d_name} to your international flight and save up to 40% with JustFly's bundle deals.</p><span class="card-link">Bundle & Save →</span></a>
    </div>
  </div>
</section>
{cta_band(f"Ready to Fly to {d_name}?", f"Book your {o_name} to {d_name} international flight on JustFly. Lowest fares guaranteed.")}"""
    return slug, make_page(slug, title, desc, body)

# ── LONG TAIL PAGES ───────────────────────────────────────────────────────────
def make_longtail_page(lt_slug, lt_name, lt_kw):
    slug  = f"{lt_slug}.html"
    title = f"{lt_name} | JustFly Guide — FlightDealsPro"
    desc  = f"Complete guide to {lt_kw}. JustFly compares 500+ airlines for the lowest fares. Expert tips and strategies for cheap flights {YEAR}."
    body  = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">✈ FlightDealsPro Expert Guide</div>
  <h1><em>{lt_name}</em></h1>
  <p>Everything you need to know about {lt_kw} — expert analysis and tips to save on your next flight.</p>
  <a href="{AFF}" class="btn btn-orange">✈ Search Cheap Flights on JustFly</a>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Expert Guide</div>
    <h2 class="section-title">{lt_name}</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">🔍</div><h3>Search on JustFly</h3><p>JustFly is one of the best tools for {lt_kw}. It compares 500+ airlines instantly for the lowest available fare.</p><span class="card-link">Search JustFly →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">💰</div><h3>Save More</h3><p>Use flexible dates, compare one-way vs round-trip, and bundle with a hotel to maximize savings on {lt_kw}.</p><span class="card-link">Find Best Deals →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">📅</div><h3>Book at the Right Time</h3><p>Domestic: book 6–8 weeks ahead. International: 3–6 months ahead. Use fare alerts to catch price drops.</p><span class="card-link">Set Fare Alert →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🏨</div><h3>Bundle & Save More</h3><p>Add a hotel to your flight and save up to 40%. JustFly's bundles often beat booking separately.</p><span class="card-link">View Bundles →</span></a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="faqs fade">
      <div class="faq"><div class="faq-q">What is the best way to find {lt_kw}?</div><div class="faq-a">JustFly is one of the top platforms for {lt_kw}. It compares 500+ airlines simultaneously and often surfaces fares not available elsewhere.</div></div>
      <div class="faq"><div class="faq-q">Is JustFly the best option for {lt_kw}?</div><div class="faq-a">JustFly consistently ranks among the top flight search tools, particularly for bundle deals and flexible date searches related to {lt_kw}.</div></div>
      <div class="faq"><div class="faq-q">How do I get the lowest price for {lt_kw}?</div><div class="faq-a">Use flexible dates, search in incognito mode, set fare alerts, and consider nearby airports. JustFly makes all of these easy.</div></div>
    </div>
    <div style="text-align:center;margin-top:2rem;">
      <a href="{AFF}" class="btn btn-orange">✈ Book on JustFly Now →</a>
    </div>
  </div>
</section>
{cta_band("Ready to Find Cheap Flights?", "JustFly compares 500+ airlines. Lowest fares, no hidden fees.")}
<section class="section">
  <div class="container">
    <div class="section-tag">Related Topics</div>
    <h2 class="section-title">More Flight Resources</h2>
    <div class="rel-grid">
      {"".join(f'<a href="{ls2}.html" class="rel-link">✈ {ln2}</a>' for ls2,ln2,lk2 in LONG_TAILS[:12] if ls2 != lt_slug)}
    </div>
  </div>
</section>"""
    return slug, make_page(slug, title, desc, body)

# ── STATIC PAGES (keep originals) ─────────────────────────────────────────────
def make_flights_page():
    slug = "flights.html"
    title = f"Cheap Flights 2026 — JustFly Flight Search | FlightDealsPro"
    desc  = "Find the cheapest flights with JustFly. Compare one-way, round-trip, and multi-city fares from 500+ airlines instantly."
    body  = f"""
<section class="hero">
  <div class="hero-badge">✈ 500+ Airlines Compared</div>
  <h1>Find <em>Cheap Flights</em><br>on JustFly</h1>
  <p>Real-time fares from every major airline. One-way, round-trip, or multi-city.</p>
  <a href="{AFF}" class="btn btn-orange">🔍 Search Flights Now</a>
  <div class="hero-stats">
    <div><div class="hero-stat-num">500+</div><div class="hero-stat-label">Airlines</div></div>
    <div><div class="hero-stat-num">$73</div><div class="hero-stat-label">Avg. Savings</div></div>
    <div><div class="hero-stat-num">4.9★</div><div class="hero-stat-label">Rating</div></div>
  </div>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Flight Types</div>
    <h2 class="section-title">Every Type of Flight, One Platform</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">🔄</div><h3>Round-Trip</h3><p>Book outbound and return in one search. JustFly finds the cheapest combination across all airlines.</p><span class="card-link">Search Round-Trip →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">➡️</div><h3>One-Way</h3><p>Mix and match airlines for the cheapest one-way fares on any route.</p><span class="card-link">Search One-Way →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🌐</div><h3>Multi-City</h3><p>Build a custom itinerary visiting multiple cities, optimized for the lowest total fare.</p><span class="card-link">Search Multi-City →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🏨</div><h3>Flight + Hotel</h3><p>Bundle your flight with a hotel and save up to 40%. Exclusive rates on every destination.</p><span class="card-link">Bundle & Save →</span></a>
    </div>
  </div>
</section>
{cta_band("Prices Drop Daily — Don't Miss Out", "Fares on top routes change every hour. Lock in the lowest price now.")}"""
    return slug, make_page(slug, title, desc, body)

def make_destinations_page():
    slug = "destinations.html"
    title = f"Top Flight Destinations 2026 — Cheap Fares | FlightDealsPro"
    desc  = "Browse top travel destinations and find cheap flights via JustFly. Live fares to New York, London, Paris, Tokyo, Cancún, and more."
    dests = [
        ("🗽","New York","From $89"),("🏰","London","From $299"),("🗼","Paris","From $319"),
        ("🌸","Tokyo","From $549"),("🏖️","Cancún","From $149"),("🌴","Miami","From $99"),
        ("🎰","Las Vegas","From $79"),("🌉","San Francisco","From $119"),
        ("🏙️","Chicago","From $89"),("☀️","Orlando","From $99"),
        ("🎵","Nashville","From $109"),("🌊","Honolulu","From $299"),
    ]
    dest_cards = "".join(f'<a href="{AFF}" class="dest"><div class="dest-emoji">{e}</div><div class="dest-city">{c}</div><div class="dest-price">{p}</div></a>' for e,c,p in dests)
    body = f"""
<section class="hero">
  <div class="hero-badge">🌍 Top Destinations 2026</div>
  <h1>Where Will You <em>Fly</em><br>This Year?</h1>
  <p>Hot routes with the best fares. Book now before prices rise.</p>
  <a href="{AFF}" class="btn btn-orange">✈ Search All Destinations</a>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container center">
    <div class="section-tag">Popular Routes</div>
    <h2 class="section-title">Top Destinations Right Now</h2>
    <p class="section-sub">Fares updated daily. Click any destination to see live prices.</p>
    <div class="dest-grid fade">{dest_cards}</div>
    <a href="{AFF}" class="btn btn-orange">✈ Search All Destinations on JustFly</a>
  </div>
</section>
{cta_band("Ready to Book Your Trip?", "JustFly compares 500+ airlines for every destination. Find your lowest fare now.")}"""
    return slug, make_page(slug, title, desc, body)

def make_tips_page():
    slug = "tips.html"
    title = f"10 Tips for Finding Cheap Flights 2026 | FlightDealsPro"
    desc  = "Expert tips to find cheap flights every time. Cut airfare by 30–60% using JustFly and flexible booking strategies."
    tips = [
        ("Book on Tuesday or Wednesday","Airfare is cheapest mid-week. Avoid Friday–Sunday when prices spike 15–25%."),
        ("Fly early morning or late night","Off-peak departures are 20–30% cheaper with lower cancellation rates."),
        ("Be flexible with dates","Shifting your trip by 1–3 days can save $100–$400, especially around holidays."),
        ("Book domestic 6–8 weeks out","The sweet spot for US flights. Too early or too late costs more."),
        ("Book international 3–6 months out","For transatlantic and transpacific routes, book well in advance."),
        ("Try nearby airports","A secondary airport 60–90 minutes away can cut your fare by up to 40%."),
        ("Set fare alerts on JustFly","Get notified the instant prices drop on your route. Never miss a deal."),
        ("Search in incognito mode","Airlines track repeat searches and raise prices. Always use a private window."),
        ("Bundle flight + hotel","Booking together saves 15–40% over booking separately."),
        ("Consider a one-stop flight","A connecting flight often costs 30–50% less than nonstop."),
    ]
    tip_html = "".join(f'<div class="tip"><div class="tip-n">{str(i+1).zfill(2)}</div><div class="tip-t"><strong>{t}</strong><span>{d}</span></div></div>' for i,(t,d) in enumerate(tips))
    body = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">💡 Expert Travel Tips</div>
  <h1>How to Find <em>Cheap Flights</em><br>Every Time</h1>
  <p>Proven strategies to cut your airfare by 30–60%.</p>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Airfare Strategy</div>
    <h2 class="section-title">10 Rules for Cheap Flights</h2>
    <div class="tips fade">{tip_html}</div>
    <div style="text-align:center;margin-top:2rem;">
      <a href="{AFF}" class="btn btn-orange">✈ Apply These Tips — Search JustFly Now</a>
    </div>
  </div>
</section>
{cta_band("Put These Tips to Work", "Use JustFly's flexible search to find the cheapest fares with all these strategies.")}"""
    return slug, make_page(slug, title, desc, body)

def make_comparison_page():
    slug = "comparison.html"
    title = f"JustFly vs Expedia vs Kayak vs Google Flights 2026 | FlightDealsPro"
    desc  = "Unbiased comparison of JustFly vs Expedia, Kayak, and Google Flights. Features, pricing, and which platform wins."
    body = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">⚖️ Unbiased Comparison</div>
  <h1>JustFly vs <em>The Competition</em></h1>
  <p>How does JustFly stack up against Expedia, Kayak, and Google Flights?</p>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Platform Comparison</div>
    <h2 class="section-title">JustFly vs Expedia vs Kayak vs Google Flights</h2>
    <div style="overflow-x:auto" class="fade">
      <table>
        <tr><th>Feature</th><th>JustFly <span style="background:#ff6b00;color:#fff;font-size:0.65rem;font-weight:700;padding:2px 7px;border-radius:50px;margin-left:5px;">BEST</span></th><th>Expedia</th><th>Kayak</th><th>Google Flights</th></tr>
        <tr><td>Flight + Hotel Bundles</td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#ccc;">—</span></td><td><span style="color:#ccc;">—</span></td></tr>
        <tr><td>Car Rental Bundling</td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#ccc;">—</span></td><td><span style="color:#ccc;">—</span></td></tr>
        <tr><td>500+ Airlines</td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#ccc;">—</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td></tr>
        <tr><td>Price Alerts</td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td></tr>
        <tr><td>Flexible Date Search</td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td>Partial</td><td><span style="color:#16a34a;font-weight:700;">✔</span></td><td><span style="color:#16a34a;font-weight:700;">✔</span></td></tr>
        <tr><td>Starting Price</td><td><strong style="color:#ff6b00;">Lowest</strong></td><td>Mid</td><td>Mid</td><td>Variable</td></tr>
      </table>
    </div>
    <div style="text-align:center;">
      <a href="{AFF}" class="btn btn-orange">✈ Book on JustFly — Best Value</a>
    </div>
  </div>
</section>
{cta_band("JustFly Wins on Price", "Compare yourself and see why millions choose JustFly for cheap flights.")}"""
    return slug, make_page(slug, title, desc, body)

def make_faq_page():
    slug = "faq.html"
    title = f"JustFly FAQ 2026 — Is It Legit? | FlightDealsPro"
    desc  = "Answers to common JustFly questions. Is JustFly legit? Cancellation, fees, and booking tips."
    schema = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"Is JustFly legit?","acceptedAnswer":{"@type":"Answer","text":"Yes. JustFly is a fully accredited, IATA-certified travel booking platform."}},
{"@type":"Question","name":"Is JustFly cheaper than Expedia?","acceptedAnswer":{"@type":"Answer","text":"JustFly frequently offers lower fares, especially on flight and hotel bundles."}},
{"@type":"Question","name":"What is the cheapest day to book flights?","acceptedAnswer":{"@type":"Answer","text":"Tuesday and Wednesday are historically cheapest. Avoid weekends when prices spike 15-25%."}}
]}</script>"""
    faqs = [
        ("Is JustFly legit?","Yes. JustFly is a fully accredited, IATA-certified booking platform used by millions of travelers. It partners with 500+ airlines worldwide."),
        ("Is JustFly cheaper than Expedia?","JustFly frequently offers lower fares, especially on flight + hotel bundles. It compares hundreds of airlines simultaneously."),
        ("What is the cheapest day to book flights?","Tuesday and Wednesday are historically cheapest. Avoid weekends when prices are typically 15–25% higher."),
        ("Can I cancel a JustFly booking?","Policies vary by airline and fare type. Many fares include a 24-hour free cancellation window. Always check fare rules."),
        ("Does JustFly compare all airlines?","JustFly compares fares from 500+ airlines including all major carriers and many budget airlines."),
        ("How far ahead should I book?","Domestic: 6–8 weeks ahead. International: 3–6 months ahead. Use price alerts to catch fare drops."),
        ("Does JustFly have hidden fees?","JustFly shows all fees upfront. Always review the fare breakdown before confirming your booking."),
        ("Can I change my JustFly flight?","Flight changes are subject to airline policies and may incur fees. Check your fare rules at booking."),
    ]
    faq_html = "".join(f'<div class="faq"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    body = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">❓ FAQ</div>
  <h1>JustFly — Your Questions <em>Answered</em></h1>
  <p>Everything you need to know before booking your flight.</p>
</section>
{urgency_html()}
<section class="section section-alt">
  <div class="container">
    <div class="faqs fade">{faq_html}</div>
    <div style="text-align:center;margin-top:2rem;">
      <a href="{AFF}" class="btn btn-orange">✈ Book on JustFly Now →</a>
    </div>
  </div>
</section>
{cta_band("Still Have Questions?", "The best way to understand JustFly is to try it. Search flights now — it's free.")}"""
    return slug, make_page(slug, title, desc, body, schema)

# ── SITEMAP / ROBOTS ──────────────────────────────────────────────────────────
def make_sitemap(slugs):
    iso = now.strftime("%Y-%m-%d")
    sm  = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += f'  <url><loc>{BASE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority><lastmod>{iso}</lastmod></url>\n'
    for s in slugs:
        sm += f'  <url><loc>{BASE_URL}/{s}</loc><changefreq>weekly</changefreq><priority>0.7</priority><lastmod>{iso}</lastmod></url>\n'
    sm += '</urlset>\n'
    return sm

def make_robots():
    return f"User-agent: *\nAllow: /\nDisallow: /build.py\nDisallow: /.github/\nSitemap: {BASE_URL}/sitemap.xml\n"

def make_llms():
    return f"# FlightDealsPro — JustFly USA Affiliate\n> Updated: {DATE_STR}\n> Affiliate links present\n\n## About\n20,000+ page USA affiliate site for JustFly.com flight booking.\nCovers all 50 states, 120 US city pairs, international routes, and 200 long-tail flight keywords.\n\n## Site: {BASE_URL}/\n"

# ── MAIN ──────────────────────────────────────────────────────────────────────
def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.stdout.strip(): print(r.stdout.strip())
    return r.returncode

if __name__ == "__main__":
    # Count estimate
    state_p = len(STATES) * len(STATE_INTENTS)
    dom_p   = len(US_CITIES) * len(DOMESTIC_DESTS)
    intl_p  = len(US_CITIES) * len(INTL_DESTS)
    lt_p    = len(LONG_TAILS)
    static_p = 6
    total   = state_p + dom_p + intl_p + lt_p + static_p

    print(f"✈  JustFly Build — {DATE_STR}  sync={SYNC}")
    print(f"   State pages:       {state_p:,}")
    print(f"   City→Domestic:     {dom_p:,}")
    print(f"   City→Intl:         {intl_p:,}")
    print(f"   Long-tail pages:   {lt_p:,}")
    print(f"   Static pages:      {static_p:,}")
    print(f"   Total: {total:,} pages")

    # Static files
    with open("robots.txt","w",encoding="utf-8") as f: f.write(make_robots())
    with open("llms.txt","w",encoding="utf-8") as f: f.write(make_llms())
    with open(".nojekyll","w") as f: f.write("")
    print("✅ robots.txt  llms.txt  .nojekyll")

    slugs = []
    count = 0

    # Static pages
    for slug, html in [make_flights_page(), make_destinations_page(), make_tips_page(),
                       make_comparison_page(), make_faq_page()]:
        if slug not in ("flights.html","destinations.html","tips.html","comparison.html","faq.html"):
            continue
        with open(slug,"w",encoding="utf-8") as f: f.write(html)
        slugs.append(slug)
        count += 1
    # Write all static
    for fn, html in [make_flights_page(), make_destinations_page(), make_tips_page(),
                     make_comparison_page(), make_faq_page()]:
        with open(fn,"w",encoding="utf-8") as f: f.write(html)
        if fn not in slugs: slugs.append(fn)

    print("   Generating state pages...")
    for st_slug, st_name, st_abbr in STATES:
        for i_slug, i_name, i_kw in STATE_INTENTS:
            slug, html = make_state_page(st_slug, st_name, st_abbr, i_slug, i_name, i_kw)
            with open(slug,"w",encoding="utf-8") as f: f.write(html)
            slugs.append(slug)
            count += 1

    print("   Generating city → domestic pages...")
    for o_slug, o_name, o_code in US_CITIES:
        for d_slug, d_name, d_code in DOMESTIC_DESTS:
            if o_slug == d_slug: continue
            slug, html = make_city_dom_page(o_slug, o_name, o_code, d_slug, d_name, d_code)
            with open(slug,"w",encoding="utf-8") as f: f.write(html)
            slugs.append(slug)
            count += 1
            if count % 5000 == 0: print(f"   {count:,}/{total:,}...")

    print("   Generating city → international pages...")
    for o_slug, o_name, o_code in US_CITIES:
        for d_slug, d_name, d_code, d_country in INTL_DESTS:
            slug, html = make_city_intl_page(o_slug, o_name, o_code, d_slug, d_name, d_code, d_country)
            with open(slug,"w",encoding="utf-8") as f: f.write(html)
            slugs.append(slug)
            count += 1
            if count % 5000 == 0: print(f"   {count:,}/{total:,}...")

    print("   Generating long-tail pages...")
    for lt in LONG_TAILS:
        slug, html = make_longtail_page(*lt)
        with open(slug,"w",encoding="utf-8") as f: f.write(html)
        slugs.append(slug)
        count += 1

    print(f"✅ {count:,} pages written")

    with open("sitemap.xml","w",encoding="utf-8") as f: f.write(make_sitemap(slugs))
    print(f"✅ sitemap.xml — {len(slugs)+1:,} URLs")

    print("\n── Git ──")
    run("git add -A")
    n = int(subprocess.run("git diff --cached --name-only | wc -l",
        shell=True,capture_output=True,text=True).stdout.strip())
    print(f"Staged: {n:,} files")
    if n == 0:
        print("Nothing to commit"); sys.exit(0)
    run(f'git commit -m "justfly sync {SYNC}"')
    import time
    for i in range(1,6):
        print(f"Push attempt {i}...")
        run("git fetch origin main")
        if run("git rebase origin/main") != 0:
            run("git rebase --abort"); time.sleep(5); continue
        if run("git push origin HEAD:main") == 0:
            print("✅ Pushed"); break
        time.sleep(5)
    else:
        print("❌ Push failed"); sys.exit(1)

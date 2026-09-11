from django.shortcuts import render
from django.http import JsonResponse

CPSE_DATA = [
    {
        "id": "ongc",
        "name": "ONGC",
        "fullName": "Oil and Natural Gas Corporation",
        "category": "Maharatna CPSE",
        "sector": "Oil & Gas",
        "shortDescription": "India's premier exploration and production company, contributing over 70% of crude oil and natural gas production to fuel the nation's energy security.",
        "overview": "Oil and Natural Gas Corporation (ONGC) is a Maharatna Central Public Sector Enterprise under the Ministry of Petroleum and Natural Gas. Established in 1956, ONGC is India's largest crude oil and natural gas company, operating across India and international basins through its overseas arm, ONGC Videsh.",
        "keyAreas": [
            "Deepwater & Ultra-Deepwater Offshore Exploration",
            "Onshore Hydrocarbon Basin Production",
            "Subsea Pipeline Operations & Field Development",
            "Renewable Energy & Offshore Wind Initiatives"
        ],
        "contributions": [
            "Produces ~71% of India's domestic crude oil requirement.",
            "Operates over 11,000 km of subsea and onshore pipeline networks.",
            "Pioneered deepwater drilling in the Krishna Godavari Basin (KG-DWN-98/2).",
            "Targeting 10 GW of renewable energy capacity by 2030."
        ],
        "stats": {
            "founded": "1956",
            "headquarters": "Dehradun / New Delhi",
            "domesticProduction": "70%+",
            "workforce": "26,000+"
        },
        "officialWebsite": "https://ongcindia.com",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1574689231351-85e742749490?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Deepwater KG-DWN-98/2 Development Project",
            "Mumbai High North Field Redevelopment Phase-IV",
            "Deen Dayal West Field Gas Production"
        ]
    },
    {
        "id": "iocl",
        "name": "IOCL",
        "fullName": "Indian Oil Corporation Limited",
        "category": "Maharatna CPSE",
        "sector": "Oil & Gas / Downstream Energy",
        "shortDescription": "India's largest integrated energy corporation with operations spanning refining, pipeline transportation, fuel marketing, and green hydrogen ventures.",
        "overview": "Indian Oil Corporation Limited (IOCL) is India's highest-ranked energy CPSE on the Fortune Global 500. With a massive network of refineries, cross-country pipelines, and over 35,000 fuel stations across India, IndianOil guarantees fuel security to every corner of the nation.",
        "keyAreas": [
            "Petroleum Refining & Quality Petrochemicals",
            "Cross-Country Crude & Product Pipeline Transport",
            "Retail Fuel Marketing, Auto-LPG & EV Charging",
            "Sustainable Green Hydrogen & Compressed Bio-Gas (CBG)"
        ],
        "contributions": [
            "Refining capacity of 70.05 MMTPA across 9 major refineries.",
            "Network of over 17,500 km of pipelines across India.",
            "Pioneered Indane LPG cylinder distribution serving 140+ million households.",
            "Establishing 10,000 EV charging stations nationwide."
        ],
        "stats": {
            "founded": "1959",
            "headquarters": "New Delhi",
            "refiningShare": "32%",
            "fuelStations": "35,000+"
        },
        "officialWebsite": "https://iocl.com",
        "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1527018601619-a508a2be00cd?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Paradip Refinery Petrochemical Complex Expansion",
            "Mathura Refinery Green Hydrogen Plant",
            "Ennore LNG Import & Regasification Terminal"
        ]
    },
    {
        "id": "ntpc",
        "name": "NTPC",
        "fullName": "NTPC Limited",
        "category": "Maharatna CPSE",
        "sector": "Power & Energy",
        "shortDescription": "India's largest power utility, powering one-fourth of the nation's electricity needs while rapidly expanding into solar, wind, and green hydrogen energy.",
        "overview": "NTPC Limited is India's largest power generation conglomerate under the Ministry of Power. With a total installed capacity exceeding 75 GW, NTPC is committed to providing reliable, affordable power while leading India's clean energy transition toward net-zero carbon emissions.",
        "keyAreas": [
            "Thermal Power Generation & Ultra-Supercritical Plants",
            "Large-Scale Utility Solar Photovoltaic & Wind Farms",
            "Hydro Electric Power Generation",
            "Green Hydrogen Production & Battery Energy Storage (BESS)"
        ],
        "contributions": [
            "Generates 25%+ of India's total electricity output.",
            "Targeting 60 GW of renewable energy capacity by 2032.",
            "Building India's largest floating solar plant at Ramagundam.",
            "Pioneering Carbon Capture and Utilization (CCU) projects."
        ],
        "stats": {
            "founded": "1975",
            "headquarters": "New Delhi",
            "installedCapacity": "75+ GW",
            "powerShare": "25%+"
        },
        "officialWebsite": "https://ntpc.co.in",
        "image": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Khavda 4.75 GW Ultra-Mega Renewable Park",
            "Ramagundam 100 MW Floating Solar Project",
            "Vindhyachal 4760 MW Thermal Power Station"
        ]
    },
    {
        "id": "sail",
        "name": "SAIL",
        "fullName": "Steel Authority of India Limited",
        "category": "Maharatna CPSE",
        "sector": "Steel & Manufacturing",
        "shortDescription": "One of India's premier steelmakers, producing high-grade steel for railways, defence, space exploration, bridges, and infrastructure development.",
        "overview": "Steel Authority of India Limited (SAIL) is a Maharatna public sector enterprise under the Ministry of Steel. Operating 5 integrated steel plants and 3 special steel units across India, SAIL supplies high-quality steel for national infrastructure projects including Chandrayaan launchpads, naval warships, and railway networks.",
        "keyAreas": [
            "Integrated Steel Manufacturing & Blast Furnace Operations",
            "Special Alloy Steel for Defence & Space Applications",
            "Long Rails for Indian Railways Infrastructure",
            "Eco-Friendly Green Steel & Energy Optimization"
        ],
        "contributions": [
            "Annual crude steel production capacity of over 20 Million Tonnes.",
            "Supplied steel for iconic national projects like Chenab Bridge & Atal Tunnel.",
            "Primary supplier of long rails to Indian Railways.",
            "Special alloy steel supplier for INS Vikrant aircraft carrier."
        ],
        "stats": {
            "founded": "1954",
            "headquarters": "New Delhi",
            "crudeSteelCapacity": "20+ MTPA",
            "steelPlants": "5 Integrated"
        },
        "officialWebsite": "https://sail.co.in",
        "image": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Bhilai Steel Plant 7 MTPA Modernization",
            "Rourkela Hot Strip Mill 2 Project",
            "Special Steel Production for Strategic Indian Navy Warships"
        ]
    },
    {
        "id": "bhel",
        "name": "BHEL",
        "fullName": "Bharat Heavy Electricals Limited",
        "category": "Maharatna CPSE",
        "sector": "Heavy Engineering & Power Equipment",
        "shortDescription": "India's premier engineering and manufacturing enterprise, manufacturing heavy electrical transformers, power turbines, locomotives, and defence systems.",
        "overview": "Bharat Heavy Electricals Limited (BHEL) is a Maharatna CPSE under the Ministry of Heavy Industries. Established in 1964, BHEL is India's largest power equipment manufacturer with a vast product portfolio spanning energy, industry, transport, transmission, renewables, and defence engineering.",
        "keyAreas": [
            "Steam & Gas Turbines, Thermal Power Equipment",
            "Hydro Power Turbines & Substation Transformers",
            "Electric Railway Locomotives & Vande Bharat Propulsion Systems",
            "Defence Naval Guns, Space Solar Panels & Industry Motors"
        ],
        "contributions": [
            "Installed over 190+ GW of power equipment globally.",
            "Supplying propulsion equipment for Vande Bharat semi-high-speed trains.",
            "Manufactures 76/62 Super Rapid Gun Mounts for Indian Navy.",
            "Pioneering indigenous 800 MW Advanced Ultra-Supercritical power technology."
        ],
        "stats": {
            "founded": "1964",
            "headquarters": "New Delhi",
            "installedPowerBase": "190+ GW",
            "manufacturingPlants": "16 Units"
        },
        "officialWebsite": "https://bhel.com",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1581092335397-9583fe92d232?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Vande Bharat 80 Sleeper Trainset Manufacturing",
            "800 MW AUSC Thermal Power Plant Technology",
            "76/62 Naval Gun Mount Systems for Indian Navy"
        ]
    },
    {
        "id": "bpcl",
        "name": "BPCL",
        "fullName": "Bharat Petroleum Corporation Limited",
        "category": "Maharatna CPSE",
        "sector": "Oil & Gas / Fuel Marketing",
        "shortDescription": "A Fortune 500 energy giant driving innovation in refining, fuel retailing, aviation turbine fuel, and electric mobility solutions.",
        "overview": "Bharat Petroleum Corporation Limited (BPCL) is a Maharatna energy enterprise under the Ministry of Petroleum and Natural Gas. BPCL operates world-class refineries at Mumbai, Kochi, and Bina, along with over 21,000 retail fuel stations providing 'Pure for Sure' fuel quality.",
        "keyAreas": [
            "Petroleum Refining & High-Quality Fuel Products",
            "Retail Fuel Distribution & MAK Lubricants",
            "Aviation Fuelling Infrastructure at Major Airports",
            "E-Drive Electric Vehicle Charging & Green Energy Networks"
        ],
        "contributions": [
            "Refining capacity of 35.3 MMTPA across 3 modern refineries.",
            "Over 21,000 retail fuel outlets equipped with automated purity checks.",
            "Kochi Refinery is India's largest public sector refinery unit.",
            "Expanding 7,000 EV fast-charging corridors along major national highways."
        ],
        "stats": {
            "founded": "1952",
            "headquarters": "Mumbai",
            "refineries": "3 Major Units",
            "outlets": "21,000+"
        },
        "officialWebsite": "https://bharatpetroleum.in",
        "image": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1527018601619-a508a2be00cd?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Kochi Refinery Propylene Derivative Petrochemical Project",
            "Bina Refinery Polypropylene Unit Expansion",
            "Electric Vehicle Highway Fast-Charging Corridors"
        ]
    },
    {
        "id": "iosl",
        "name": "IOSL",
        "fullName": "IndianOil Skytanking Limited",
        "category": "CPSE Joint Venture Affiliate",
        "sector": "Aviation Fuel Logistics & Infrastructure",
        "shortDescription": "India's premier aviation fuelling service provider, managing state-of-the-art Jet Fuel (ATF) hydrant systems and refueling at major international airports.",
        "overview": "IndianOil Skytanking Limited (IOSL) is a specialized joint venture enterprise formed to design, build, and operate automated Aviation Turbine Fuel (ATF) into-plane fuelling services and fuel hydrant systems at premier international airports across India.",
        "keyAreas": [
            "Airport Fuel Hydrant System Design & Operations",
            "Into-Plane Aviation Turbine Fuel (ATF) Refuelling",
            "Aviation Fuel Quality Control & Safety Testing",
            "Green Airport Fuel Management & Sustainable Aviation Fuel (SAF)"
        ],
        "contributions": [
            "Manages airport fuel hydrant networks at Bengaluru, Delhi, and Mumbai airports.",
            "Refuels thousands of domestic and international flights daily with 99.999% precision.",
            "Implements zero-spill automated refuelling safety technologies.",
            "Pioneering Sustainable Aviation Fuel (SAF) blending infrastructure in India."
        ],
        "stats": {
            "founded": "2006",
            "headquarters": "Bengaluru / New Delhi",
            "airportsServed": "20+ Major Airports",
            "flightsRefuelled": "500,000+ Annually"
        },
        "officialWebsite": "https://www.skytanking.com",
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1508873696983-2df515122519?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": [
            "Kempegowda International Airport Fuel Hydrant Expansion",
            "Delhi International Airport T3 Into-Plane Refuelling",
            "Noida International Airport (Jewar) ATF Pipeline & Storage Facility"
        ]
    }
]

SECTORS_DATA = [
    {
        "id": "oil-gas",
        "title": "Oil & Gas Exploration",
        "icon": "flame",
        "description": "Securing national energy independence through upstream exploration, offshore drilling, cross-country pipelines, and modern refining capacity.",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "cpseCount": 3
    },
    {
        "id": "power-energy",
        "title": "Power & Clean Energy",
        "icon": "zap",
        "description": "Driving 24x7 electricity supply with ultra-supercritical thermal power, hydro generation, utility solar parks, and green hydrogen projects.",
        "image": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=800&q=80",
        "cpseCount": 2
    },
    {
        "id": "steel-manufacturing",
        "title": "Steel & Metallurgy",
        "icon": "anvil",
        "description": "Forging high-strength steel for railway long rails, defence naval warships, space rocket launchpads, and national highway bridges.",
        "image": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=800&q=80",
        "cpseCount": 1
    },
    {
        "id": "heavy-engineering",
        "title": "Heavy Machinery & Engineering",
        "icon": "cog",
        "description": "Manufacturing world-class heavy electrical turbines, locomotives, defence gun mounts, and sub-station transformers.",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
        "cpseCount": 1
    },
    {
        "id": "aviation-logistics",
        "title": "Aviation Fuel & Infrastructure",
        "icon": "plane",
        "description": "Operating automated jet fuel hydrant infrastructure and into-plane refuelling for domestic and international aviation.",
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=800&q=80",
        "cpseCount": 1
    },
    {
        "id": "renewable-energy",
        "title": "Renewable Energy & Green Mobility",
        "icon": "sun",
        "description": "Building ultra-mega solar parks, floating solar projects, highway EV fast-charging corridors, and bio-fuel blending units.",
        "image": "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80",
        "cpseCount": 4
    }
]

PROJECTS_DATA = [
    {
        "id": "proj-1",
        "title": "Khavda Ultra-Mega Renewable Energy Park",
        "cpse": "NTPC Limited",
        "sector": "Renewable Energy",
        "description": "Developing India's largest 4.75 GW solar and wind renewable park in the Rann of Kutch, Gujarat to accelerate carbon reduction goals.",
        "image": "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "proj-2",
        "title": "KG-DWN-98/2 Ultra-Deepwater Gas Development",
        "cpse": "ONGC",
        "sector": "Oil & Gas",
        "description": "Pioneering deepwater oil and natural gas production in the Krishna Godavari Basin, boosting domestic energy supply by 15%.",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "proj-3",
        "title": "Paradip Integrated Refinery & Petrochemical Complex",
        "cpse": "IOCL",
        "sector": "Refining & Petrochemicals",
        "description": "Expanding the 15 MMTPA refinery into a world-class petrochemical hub supplying polypropylene and ethylene to Indian industries.",
        "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "proj-4",
        "title": "Bhilai Steel Plant 7 MTPA Modernization",
        "cpse": "SAIL",
        "sector": "Steel & Metallurgy",
        "description": "Modernizing blast furnaces and continuous casting lines to manufacture 260-meter long rails for high-speed Indian Railways tracks.",
        "image": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "proj-5",
        "title": "Vande Bharat Propulsion & Power Assemblies",
        "cpse": "BHEL",
        "sector": "Heavy Engineering",
        "description": "Manufacturing indigenous traction motors, transformers, and electrical propulsion equipment for India's high-speed Vande Bharat trains.",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "proj-6",
        "title": "Noida International Airport Jet Fuel Pipeline",
        "cpse": "IOSL",
        "sector": "Aviation Logistics",
        "description": "Designing and operating the automated ATF hydrant system and direct pipeline connectivity for Jewar International Airport.",
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=800&q=80"
    }
]

NEWS_DATA = [
    {
        "id": "news-1",
        "date": "September 10, 2026",
        "category": "National Milestone",
        "headline": "Indian CPSEs Record Highest Ever Capital Expenditure of ₹4.5 Lakh Crore",
        "excerpt": "Department of Public Enterprises reports record CAPEX execution across oil, power, steel, and heavy engineering CPSEs supporting National Infrastructure Pipeline."
    },
    {
        "id": "news-2",
        "date": "September 04, 2026",
        "category": "Green Energy",
        "headline": "NTPC & IOCL Partner to Establish Joint Venture for 10 GW Green Hydrogen Capacity",
        "excerpt": "Maharatna giants NTPC and IndianOil sign strategic agreement to accelerate green hydrogen production for refinery decarbonization."
    },
    {
        "id": "news-3",
        "date": "August 28, 2026",
        "category": "Defence & Manufacturing",
        "headline": "SAIL & BHEL Complete Supply of Special Alloys for Next-Gen Naval Warships",
        "excerpt": "Indigenously developed steel plates and rapid naval gun mounts delivered to Indian Navy under Atmanirbhar Bharat initiative."
    },
    {
        "id": "news-4",
        "date": "August 15, 2026",
        "category": "Energy Infrastructure",
        "headline": "ONGC Begins Oil Production From Ultra-Deepwater Block in Krishna Godavari Basin",
        "excerpt": "Offshore production milestone achieved at Floating Production Storage and Offloading (FPSO) unit, strengthening domestic crude supply."
    }
]

MEDIA_DATA = [
    {
        "id": "m-1",
        "title": "Offshore Hydrocarbon Rig Operation",
        "cpse": "ONGC",
        "category": "Refineries & Rigs",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1000&q=80"
    },
    {
        "id": "m-2",
        "title": "Petroleum Refinery at Night",
        "cpse": "IOCL",
        "category": "Refineries & Rigs",
        "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1000&q=80"
    },
    {
        "id": "m-3",
        "title": "Floating Solar Power Plant",
        "cpse": "NTPC",
        "category": "Power Plants",
        "image": "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=1000&q=80"
    },
    {
        "id": "m-4",
        "title": "Blast Furnace Steel Pouring",
        "cpse": "SAIL",
        "category": "Steel Mills",
        "image": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=1000&q=80"
    },
    {
        "id": "m-5",
        "title": "Heavy Electric Power Turbine Assembly",
        "cpse": "BHEL",
        "category": "Renewable Infrastructure",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1000&q=80"
    },
    {
        "id": "m-6",
        "title": "Airport Jet Refuelling Hydrant System",
        "cpse": "IOSL",
        "category": "Refineries & Rigs",
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1000&q=80"
    }
]


def home(request):
    context = {
        'cpses': CPSE_DATA,
        'sectors': SECTORS_DATA,
        'projects': PROJECTS_DATA,
        'news': NEWS_DATA,
        'media': MEDIA_DATA,
    }
    return render(request, 'index.html', context)


def api_cpses(request):
    return JsonResponse({'cpses': CPSE_DATA})


def api_cpse_detail(request, cpse_id):
    cpse = next((c for c in CPSE_DATA if c['id'].lower() == cpse_id.lower()), None)
    if cpse:
        return JsonResponse(cpse)
    return JsonResponse({'error': 'CPSE not found'}, status=404)

"""
Feature 1.4: Financial Savings Simulator & Inter-Plant Transfer Service

Surfaces cost-saving actions ("transfer duplicate/equivalent parts instead of buy new")
by cross-referencing duplicate/equivalent parts against warehouse locations across CPSEs
using GPS Haversine distance and transit freight estimation.
"""

import math
from typing import Any, Dict, List, Optional


CPSE_PLANT_HUBS = [
    {
        "hub_id": "HUB_ONGC_HAZIRA",
        "plant_name": "ONGC Hazira Gas Complex",
        "company": "ONGC",
        "city": "Hazira (Surat)",
        "state": "Gujarat",
        "latitude": 21.1166,
        "longitude": 72.6517,
        "stock_inventory": 450,
        "available_unit_price": 18500.0,
    },
    {
        "hub_id": "HUB_IOCL_MATHURA",
        "plant_name": "IOCL Mathura Refinery",
        "company": "IOCL",
        "city": "Mathura",
        "state": "Uttar Pradesh",
        "latitude": 27.4924,
        "longitude": 77.6737,
        "stock_inventory": 280,
        "available_unit_price": 19200.0,
    },
    {
        "hub_id": "HUB_IOCL_BARAUNI",
        "plant_name": "IOCL Barauni Refinery",
        "company": "IOCL",
        "city": "Barauni",
        "state": "Bihar",
        "latitude": 25.4419,
        "longitude": 86.0245,
        "stock_inventory": 190,
        "available_unit_price": 21000.0,
    },
    {
        "hub_id": "HUB_IOCL_PANIPAT",
        "plant_name": "IOCL Panipat Refinery",
        "company": "IOCL",
        "city": "Panipat",
        "state": "Haryana",
        "latitude": 29.3909,
        "longitude": 76.9635,
        "stock_inventory": 520,
        "available_unit_price": 18900.0,
    },
    {
        "hub_id": "HUB_CPCL_CHENNAI",
        "plant_name": "CPCL Chennai Refinery",
        "company": "CPCL",
        "city": "Manali (Chennai)",
        "state": "Tamil Nadu",
        "latitude": 13.1672,
        "longitude": 80.2889,
        "stock_inventory": 310,
        "available_unit_price": 22500.0,
    },
    {
        "hub_id": "HUB_HPCL_VIZAG",
        "plant_name": "HPCL Vizag Refinery",
        "company": "HPCL",
        "city": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "latitude": 17.6868,
        "longitude": 83.2185,
        "stock_inventory": 380,
        "available_unit_price": 20500.0,
    },
    {
        "hub_id": "HUB_NTPC_RAMAGUNDAM",
        "plant_name": "NTPC Ramagundam Power Station",
        "company": "NTPC",
        "city": "Ramagundam",
        "state": "Telangana",
        "latitude": 18.7562,
        "longitude": 79.5186,
        "stock_inventory": 150,
        "available_unit_price": 21800.0,
    },
    {
        "hub_id": "HUB_SAIL_BHILAI",
        "plant_name": "SAIL Bhilai Steel Plant",
        "company": "SAIL",
        "city": "Bhilai",
        "state": "Chhattisgarh",
        "latitude": 21.1938,
        "longitude": 81.3509,
        "stock_inventory": 640,
        "available_unit_price": 17800.0,
    },
    {
        "hub_id": "HUB_BHEL_HARIDWAR",
        "plant_name": "BHEL Haridwar Plant",
        "company": "BHEL",
        "city": "Haridwar",
        "state": "Uttarakhand",
        "latitude": 29.9457,
        "longitude": 78.1642,
        "stock_inventory": 210,
        "available_unit_price": 23000.0,
    },
    {
        "hub_id": "HUB_BPCL_MUMBAI",
        "plant_name": "BPCL Mumbai Refinery",
        "company": "BPCL",
        "city": "Mahul (Mumbai)",
        "state": "Maharashtra",
        "latitude": 19.0144,
        "longitude": 72.8479,
        "stock_inventory": 400,
        "available_unit_price": 19800.0,
    },
]


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance between two GPS coordinates using Haversine formula.
    """
    r = 6371.0  # Earth's mean radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 1)


def calculate_transport_cost(distance_km: float, units: int = 10, unit_weight_kg: float = 5.0) -> float:
    """
    Calculate estimated freight transit logistics cost.
    Formula: Base Freight + (Distance * Rate per KM * Total Weight Factor)
    """
    base_freight = 2500.0  # Minimum handling fee
    per_km_rate = 14.5  # Heavy freight rate per km
    total_weight_kg = units * unit_weight_kg
    weight_factor = max(1.0, total_weight_kg / 50.0)

    cost = base_freight + (distance_km * per_km_rate * weight_factor * 0.35)
    return round(cost, 2)


def simulate_financial_savings(
    destination_plant: str = "NTPC Ramagundam Power Station",
    required_units: int = 50,
    new_procurement_price: float = 24000.0,
    preferred_source_hub_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Primary Financial Savings Simulation API.
    Cross-references warehouse locations across CPSEs, calculates Haversine route distance,
    logistics freight cost, and surface transfer recommendations.
    """
    # Robust destination plant matching
    dest_lower = (destination_plant or "").lower()
    dest_hub = None
    for h in CPSE_PLANT_HUBS:
        if (
            h["plant_name"].lower() in dest_lower
            or dest_lower in h["plant_name"].lower()
            or h["company"].lower() in dest_lower
            or h["city"].lower() in dest_lower
        ):
            dest_hub = h
            break
    if not dest_hub:
        dest_hub = CPSE_PLANT_HUBS[6]  # Fallback to NTPC Ramagundam Power Station

    # Find best source hub with available stock
    available_sources = []
    for hub in CPSE_PLANT_HUBS:
        if hub["hub_id"] != dest_hub["hub_id"] and hub["stock_inventory"] >= 10:
            dist = haversine_distance_km(
                hub["latitude"], hub["longitude"], dest_hub["latitude"], dest_hub["longitude"]
            )
            freight = calculate_transport_cost(dist, units=required_units)
            purchase_cost = required_units * new_procurement_price
            transfer_unit_cost = hub["available_unit_price"]
            total_transfer_cost = (required_units * transfer_unit_cost) + freight
            savings = max(0.0, purchase_cost - total_transfer_cost)

            available_sources.append({
                "source_hub": hub,
                "distance_km": dist,
                "freight_cost": freight,
                "purchase_cost": purchase_cost,
                "total_transfer_cost": total_transfer_cost,
                "net_savings": round(savings, 2),
                "savings_pct": round((savings / purchase_cost) * 100.0, 1) if purchase_cost > 0 else 0.0,
            })

    # Sort sources by maximum net financial savings
    available_sources.sort(key=lambda x: x["net_savings"], reverse=True)
    best_option = available_sources[0] if available_sources else None

    if not best_option:
        return {
            "has_transfer": False,
            "transfer_available": False,
            "recommendation": "PROCURE_NEW",
            "recommendation_pill": "Procure New (No Surplus Stock Found)",
            "recommendation_label": "Procure New",
            "destination_plant": dest_hub["plant_name"],
            "source_plant": "No Surplus Source",
            "nearest_source_plant": "No Surplus Source",
            "distance_km": 0.0,
            "required_units": required_units,
            "unit_price": new_procurement_price,
            "total_purchase_cost": required_units * new_procurement_price,
            "freight_cost": 0.0,
            "net_savings": 0.0,
            "saved_cr": "₹0",
            "savings_fmt": "₹0",
        }

    src = best_option["source_hub"]
    savings_num = best_option["net_savings"]
    purchase_num = best_option["purchase_cost"]
    freight_num = best_option["freight_cost"]

    savings_fmt = f"₹{int(savings_num):,}"
    purchase_fmt = f"₹{int(purchase_num):,}"
    freight_fmt = f"₹{int(freight_num):,}"

    if savings_num >= 10000000:
        saved_cr_str = f"₹{savings_num / 10000000:.2f} Cr"
    elif savings_num >= 100000:
        saved_cr_str = f"₹{savings_num / 100000:.2f} Lakhs"
    else:
        saved_cr_str = savings_fmt

    return {
        "has_transfer": True,
        "transfer_available": True,
        "recommendation": "TRANSFER_AVAILABLE",
        "recommendation_pill": f"Transfer Available (Save {saved_cr_str}) vs Procure New",
        "recommendation_label": f"Transfer Available (Save {saved_cr_str})",
        "source_plant": src["plant_name"],
        "nearest_source_plant": src["plant_name"],
        "source_company": src["company"],
        "source_location": f"{src['city']}, {src['state']}",
        "destination_plant": dest_hub["plant_name"],
        "destination_company": dest_hub["company"],
        "destination_location": f"{dest_hub['city']}, {dest_hub['state']}",
        "distance_km": best_option["distance_km"],
        "required_units": required_units,
        "surplus_available": src["stock_inventory"],
        "unit_price": new_procurement_price,
        "new_unit_price": new_procurement_price,
        "transfer_unit_price": src["available_unit_price"],
        "total_purchase_cost": purchase_num,
        "new_purchase_total": purchase_num,
        "purchase_cost_fmt": purchase_fmt,
        "freight_cost": freight_num,
        "estimated_freight": freight_num,
        "freight_cost_fmt": freight_fmt,
        "total_transfer_cost": best_option["total_transfer_cost"],
        "total_transfer_total": best_option["total_transfer_cost"],
        "net_savings": savings_num,
        "saved_cr": saved_cr_str,
        "savings_fmt": savings_fmt,
        "savings_percentage": best_option["savings_pct"],
        "route_summary": {
            "from": f"{src['plant_name']} ({src['city']})",
            "to": f"{dest_hub['plant_name']} ({dest_hub['city']})",
            "distance_str": f"{best_option['distance_km']} KM",
            "freight_vs_purchase": f"{freight_fmt} Freight vs {purchase_fmt} Purchase",
        },
        "cta_label": f"Request Inter-CPSE Transfer ({saved_cr_str} Savings)",
        "cta_action": "REQUEST_STOCK_TRANSFER",
    }


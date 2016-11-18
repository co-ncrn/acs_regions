# Regionalization script
# July 29, 2016
# Becky Davies

# Support Functions for full_script for regionalization

import pysal as ps
import pandas as pd
from shutil import copyfile
import copy
import numpy as np
import geopandas as gp  
import shapely
import zipfile
import os.path
import json
import random


def set_scenario(scenario):                                                
    count = ['B01003_001']
    all_types = ['count','prop','ratio']
    
    if scenario == "housing":
        scenario2 = 'hous'
    elif scenario == "general":
        scenario2 = 'gen'
    elif scenario == "transportation":
        scenario2 = 'trans'
    elif scenario == "poverty":
        scenario2 = 'pov'
    elif scenario == 'sovi':
        scenario2 = 'sovi'

    return count, all_types, scenario2

#function to correct for islands    
def isIsland(msa, w):    
    if msa=='13380':
        # Bellingham, WA
        neighbors = w.neighbors
        weights = w.weights
        #Lummi Island, connected via ferry 
        neighbors['53073010900'].append('53073940000')
        neighbors['53073940000'].append('53073010900')
        weights['53073010900'].append(1.0)
        weights['53073940000'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa == '14740':
        # Bremerton-Silverdale, WA
        neighbors = w.neighbors
        weights = w.weights
        # Bainbridge Island, connected to mainland by bridge
        neighbors['53035090700'].extend(['53035090800', '53035940100'])
        neighbors['53035090800'].extend(['53035090700', '53035940100'])
        neighbors['53035940100'].extend(['53035090700', '53035090800'])
        weights['53035090700'].extend([1.0,1.0])
        weights['53035090800'].extend([1.0,1.0])
        weights['53035940100'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa == '15260':
        # Brunswick, GA
        neighbors = w.neighbors
        weights = w.weights
        # Saint Simons Island, connected to mainland via Torras Causeway
        neighbors['13127000403'].extend(['13127000200', '13127000102'])
        neighbors['13127000200'].extend(['13127000403', '13127000102'])
        neighbors['13127000102'].extend(['13127000403', '13127000200'])
        weights['13127000200'].extend([1.0,1.0])
        weights['13127000403'].extend([1.0,1.0])
        weights['13127000102'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa == '15380':
        # Buffalo-Cheektowaga-Niagara Falls, NY
        neighbors = w.neighbors
        weights = w.weights
        # Grand Island connects to mainland on south via roadway
        neighbors['36029007304'].extend(['36029007302', '36029008300','36029008400'])
        neighbors['36029007302'].extend(['36029007304', '36029008300','36029008400'])
        neighbors['36029008300'].extend(['36029007304', '36029007302','36029008400'])
        neighbors['36029008400'].extend(['36029007304', '36029007302','36029008300'])
        weights['36029007304'].extend([1.0,1.0,1.0])
        weights['36029007302'].extend([1.0,1.0,1.0])
        weights['36029008300'].extend([1.0,1.0,1.0])
        weights['36029008400'].extend([1.0,1.0,1.0])
        # Grand Island connects to mainland on north via roadway
        neighbors['36029007303'].extend(['36029007302', '36063022000','36063021700'])
        neighbors['36029007302'].extend(['36029007303', '36063022000','36063021700'])
        neighbors['36063022000'].extend(['36029007303', '36029007302','36063021700'])
        neighbors['36063021700'].extend(['36029007303', '36029007302','36063022000'])
        weights['36029007303'].extend([1.0,1.0,1.0])
        weights['36029007302'].extend([1.0,1.0,1.0])
        weights['36063022000'].extend([1.0,1.0,1.0])
        weights['36063021700'].extend([1.0,1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='15980':
        #Cape Coral - Fort Myers, FL
        neighbors = w.neighbors
        weights = w.weights
        #Captiva Island connected to Sanibel Island via roadway
        neighbors['12071080100'].append('12071080204')
        neighbors['12071080204'].append('12071080100')
        weights['12071080100'].append(1.0)
        weights['12071080204'].append(1.0)
        # Sanibel Island connects to mainland
        neighbors['12071080204'].extend(['12071080202', '12071001915','12071001911'])
        neighbors['12071080202'].extend(['12071080204', '12071001915','12071001911'])
        neighbors['12071001915'].extend(['12071080204', '12071080202','12071001911'])
        neighbors['12071001911'].extend(['12071080204', '12071001915','12071080202'])
        weights['12071080204'].extend([1.0,1.0,1.0])
        weights['12071080202'].extend([1.0,1.0,1.0])
        weights['12071001915'].extend([1.0,1.0,1.0])
        weights['12071001911'].extend([1.0,1.0,1.0])
        # Fort Myers Beach connects to mainland via San Carlos Island
        neighbors['12071060102'].append('12071060101')
        neighbors['12071060101'].append('12071060102')
        weights['12071060102'].append(1.0)
        weights['12071060101'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='16700':
        # Charleston-North Charleston, NC
        neighbors = w.neighbors
        weights = w.weights
        #Folly Island, bridge
        neighbors['45019002004'].append('45019002003')
        neighbors['45019002003'].append('45019002004')
        weights['45019002003'].append(1.0)
        weights['45019002004'].append(1.0)
        # Kiawah Island, bridge divides two tracts
        neighbors['45019002104'].extend(['45019002105', '45019002103'])
        neighbors['45019002105'].extend(['45019002104', '45019002103'])
        neighbors['45019002103'].extend(['45019002104', '45019002105'])
        weights['45019002104'].extend([1.0,1.0])
        weights['45019002105'].extend([1.0,1.0])
        weights['45019002103'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='18880':
        #Crestview-Fort Walton Beach-Destin, FL
        neighbors = w.neighbors
        weights = w.weights
        # Santa Rosa Island, connected to neighbors by two separate bridges
        neighbors['12091023200'].extend(['12091023303', '12091022600'])
        neighbors['12091023303'].extend(['12091023200'])
        neighbors['12091022600'].extend(['12091023200'])
        weights['12091023200'].extend([1.0,1.0])
        weights['12091023303'].extend([1.0])
        weights['12091022600'].extend([1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='19820':
        #Detroit-Warren-Dearborn, MI
        neighbors = w.neighbors
        weights = w.weights
        #Belle Isle, connected via one bridge that divides two mainland tracts
        neighbors['26163985500'].extend(['26163516500', '26163515700'])
        neighbors['26163516500'].extend(['26163985500', '26163515700'])
        neighbors['26163515700'].extend(['26163985500', '26163516500'])
        weights['26163985500'].extend([1.0,1.0])
        weights['26163516500'].extend([1.0,1.0])
        weights['26163515700'].extend([1.0,1.0])
        #Harsens Island, connected via ferry on dividing line of two mainland tracts
        neighbors['26147648000'].extend(['26147646000', '26147647000'])
        neighbors['26147646000'].extend(['26147648000', '26147647000'])
        neighbors['26147647000'].extend(['26147648000', '26147646000'])
        weights['26147648000'].extend([1.0,1.0])
        weights['26147646000'].extend([1.0,1.0])
        weights['26147647000'].extend([1.0,1.0])
        #Gross Ille
        neighbors['26163594000'].extend(['26163596300', '26163595000'])
        neighbors['26163596300'].extend(['26163594000', '26163595000'])
        neighbors['26163595000'].extend(['26163594000', '26163596300'])
        weights['26163594000'].extend([1.0,1.0])
        weights['26163596300'].extend([1.0,1.0])
        weights['26163595000'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='20260':
        # Duluth, MN-WI
        neighbors = w.neighbors
        weights = w.weights
        # Park Point, connected via bridge
        neighbors['27137002200'].append('27137001900')
        neighbors['27137001900'].append('27137002200')
        weights['27137002200'].append(1.0)
        weights['27137001900'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='25940':
        # Hilton Head Island - Bluffton - Beaufort, SC
        neighbors = w.neighbors
        weights = w.weights
        # Parris Island, connected via road/low bridge through wetland area
        neighbors['45013000503'].append('45013001000')
        neighbors['45013001000'].append('45013000503')
        weights['45013001000'].append(1.0)
        weights['45013000503'].append(1.0)
        #Hunting Island, connected via road bridge
        neighbors['45013001200'].extend(['45013001102', '45013001101'])
        neighbors['45013001102'].extend(['45013001200', '45013001101'])
        neighbors['45013001101'].extend(['45013001102', '45013001200'])
        weights['45013001200'].extend([1.0,1.0])
        weights['45013001102'].extend([1.0,1.0])
        weights['45013001101'].extend([1.0,1.0])
        #Daufuski Island, connected via ferry to Hilton Head Island
        neighbors['45013002101'].append('45013010400')
        neighbors['45013010400'].append('45013002101')
        weights['45013002101'].append(1.0)
        weights['45013010400'].append(1.0)
        #Gibbs Island, connected via road bridge
        neighbors['45013000903'].extend(['45013000700', '45013000800'])
        neighbors['45013000700'].extend(['45013000800', '45013000903'])
        neighbors['45013000800'].extend(['45013000700', '45013000903'])
        weights['45013000903'].extend([1.0,1.0])
        weights['45013000700'].extend([1.0,1.0])
        weights['45013000800'].extend([1.0,1.0])
        # Ladys Island
        neighbors['45013000902'].extend(['45013000600', '45013000700'])
        neighbors['45013000600'].extend(['45013000700', '45013000902'])
        neighbors['45013000700'].extend(['45013000600', '45013000902'])
        weights['45013000902'].extend([1.0,1.0])
        weights['45013000600'].extend([1.0,1.0])
        weights['45013000700'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='27340':
        # Jacksonville, NC
        neighbors = w.neighbors
        weights = w.weights
        # North Topsail Beach
        neighbors['37133000403'].extend(['37133000401', '37133000402'])
        neighbors['37133000402'].extend(['37133000403', '37133000401'])
        neighbors['37133000401'].extend(['37133000403', '37133000402'])
        weights['37133000403'].extend([1.0,1.0])
        weights['37133000401'].extend([1.0,1.0])
        weights['37133000402'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='28140':
        # Kansas City, KS-MO
        neighbors = w.neighbors
        weights = w.weights
        # Armourdale neighborhood, connected via roadway to populated tracts
        neighbors['20209042600'].extend(['20209042300', '20209042400'])
        neighbors['20209042300'].extend(['20209042600', '20209042400'])
        neighbors['20209042400'].extend(['20209042600', '20209042300'])
        weights['20209042600'].extend([1.0,1.0])
        weights['20209042300'].extend([1.0,1.0])
        weights['20209042400'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='31080':
        # Los Angeles - Long Beach - Anaheim, CA
        # join two small islands (Lido Isle and Balboa Island) to the mainland in
        # Los Angeles (note: the huge islands off the coast of LA were clipped
        # from the shapefile)
        neighbors = w.neighbors
        weights = w.weights
        # lido isle, connected via bridge
        neighbors['06059062900'].append('06059063500')
        neighbors['06059063500'].append('06059062900')
        weights['06059062900'].append(1.0)
        weights['06059063500'].append(1.0)
        # balboa island, connected via bridge
        neighbors['06059062701'].extend(['06059063005', '06059063006'])
        neighbors['06059063005'].extend(['06059062701', '06059063006'])
        neighbors['06059063006'].extend(['06059062701', '06059063005'])
        weights['06059062701'].extend([1.0,1.0])
        weights['06059063005'].extend([1.0,1.0])
        weights['06059063006'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='33100':
        # Miami - Fort Lauderdale - West Palm Beach, FL
        neighbors = w.neighbors
        weights = w.weights
        #North Bay Village, connected via bridges on either side to 
        #mainland other islands
        neighbors['12086003917'].extend(['12086003916', '12086003918'])
        neighbors['12086003916'].extend(['12086003917'])
        neighbors['12086003918'].extend(['12086003917'])
        weights['12086003917'].extend([1.0,1.0])
        weights['12086003916'].extend([1.0])
        weights['12086003918'].extend([1.0])
        # North Bay Island, connected via bridges on either side to other 
        # islands attached to mainland
        neighbors['12086003918'].extend(['12086001301', '12086003917'])
        neighbors['12086001301'].extend(['12086003918'])
        neighbors['12086003917'].extend(['12086003918'])
        weights['12086003918'].extend([1.0,1.0])
        weights['12086001301'].extend([1.0])
        weights['12086003917'].extend([1.0])
        # Brickell Key, connected via bridge
        neighbors['12086006707'].append('12086006709')
        neighbors['12086006709'].append('12086006707')
        weights['12086006707'].append(1.0)
        weights['12086006709'].append(1.0)
        # Jupiter Inlet Colony
        neighbors['12099000101'].extend(['12099000102','12099000202','12099000301'])
        neighbors['12099000102'].extend(['12099000101','12099000202','12099000301','12099000407'])
        neighbors['12099000202'].extend(['12099000101','12099000102','12099000301'])
        neighbors['12099000301'].extend(['12099000101','12099000102','12099000202','12099000407'])
        neighbors['12099000407'].extend(['12099000301','12099000102'])
        weights['12099000101'].extend([1.0,1.0,1.0])
        weights['12099000102'].extend([1.0,1.0,1.0,1.0])
        weights['12099000202'].extend([1.0,1.0,1.0])
        weights['12099000301'].extend([1.0,1.0,1.0,1.0])
        weights['12099000407'].extend([1.0,1.0])
        # Dodge Island area. Dodge Island is empty but it is connected to a collection of small islands 
        # that have roads connecting to the mainland and Miami Beach
        neighbors['12086004102'].extend(['12086002703', '12086004106','12086004203','12086004406','12086004500','12086003702'])
        neighbors['12086002703'].extend(['12086004102'])
        neighbors['12086004106'].extend(['12086004102','12086004203'])
        neighbors['12086004203'].extend(['12086004102','12086004106'])
        neighbors['12086004406'].extend(['12086004102','12086004500'])
        neighbors['12086004500'].extend(['12086004102','12086004406'])
        neighbors['12086003702'].extend(['12086004102'])
        weights['12086004102'].extend([1.0,1.0,1.0,1.0,1.0,1.0])
        weights['12086002703'].extend([1.0])
        weights['12086004106'].extend([1.0,1.0])
        weights['12086004203'].extend([1.0,1.0])
        weights['12086004406'].extend([1.0,1.0])
        weights['12086004500'].extend([1.0,1.0])
        weights['12086003702'].extend([1.0])
        # Key Biscayne connected to mainland because intermediary tract is excluded (Virginia Key is a park)
        neighbors['12086004602'].extend(['12086004605', '12086006706'])
        neighbors['12086004605'].extend(['12086004602','12086006706'])
        neighbors['12086006706'].extend(['12086004605','12086004602'])
        weights['12086004602'].extend([1.0,1.0])
        weights['12086004605'].extend([1.0,1.0])
        weights['12086006706'].extend([1.0,1.0])
        # West Palm Beach connects to mainland via a series of bridges
        # 98 bridge
        neighbors['12099003504'].append('12099003400')
        neighbors['12099003400'].append('12099003504')
        weights['12099003504'].append(1.0)
        weights['12099003400'].append(1.0)
        # 704 bridge
        neighbors['12099003509'].append('12099002700')
        neighbors['12099002700'].append('12099003509')
        weights['12099003509'].append(1.0)
        weights['12099002700'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='34820':
        #Myrtle Beach, SC
        neighbors = w.neighbors
        weights = w.weights
        #Bald Head Island, connected via ferry to mainland
        neighbors['37019020307'].append('37019020306')
        neighbors['37019020306'].append('37019020307')
        weights['37019020307'].append(1.0)
        weights['37019020306'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='34940':
        # Naples, FL
        neighbors = w.neighbors
        weights = w.weights
        #Big Key, connected to mainland via bridge 
        neighbors['12021010902'].extend(['12021011106', '12021011102'])
        neighbors['12021011106'].extend(['12021010902', '12021011102'])
        neighbors['12021011102'].extend(['12021010902', '12021011106'])
        weights['12021010902'].extend([1.0,1.0])
        weights['12021011106'].extend([1.0,1.0])
        weights['12021011102'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='35840':
        # North Port - Sarasota - Bradenton, FL
        neighbors = w.neighbors
        weights = w.weights
        # Lido Key, connected via bridges
        neighbors['12115000700'].extend(['12115000101', '12115000801'])
        neighbors['12115000101'].extend(['12115000700'])
        neighbors['12115000801'].extend(['12115000700'])
        weights['12115000700'].extend([1.0,1.0])
        weights['12115000101'].extend([1.0])
        weights['12115000801'].extend([1.0])
        # Ana Maria Island, connected via bridge to mainland
        neighbors['12081001800'].extend(['12081001701','12081001204'])
        neighbors['12081001701'].extend(['12081001204','12081001800'])
        neighbors['12081001204'].extend(['12081001800','12081001701'])
        weights['12081001800'].extend([1.0,1.0])
        weights['12081001701'].extend([1.0,1.0])
        weights['12081001204'].extend([1.0,1.0])
        #Stickney Point Rd. bridge to mainland
        neighbors['12115001908'].extend(['12115001801','12115002005'])
        neighbors['12115001801'].extend(['12115001908','12115002005'])
        neighbors['12115002005'].extend(['12115001908','12115001801'])
        weights['12115001908'].extend([1.0,1.0])
        weights['12115001801'].extend([1.0,1.0])
        weights['12115002005'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='35620':
        # New York - Newark - Jersey City, NY-NJ-PA
        neighbors = w.neighbors
        weights = w.weights
        #Shelter Island, ferry connections on either side of island
        neighbors['36103180300'].extend(['36103170101', '36103190708'])
        neighbors['36103170101'].extend(['36103180300'])
        neighbors['36103190708'].extend(['36103180300'])
        weights['36103180300'].extend([1.0,1.0])
        weights['36103170101'].extend([1.0])
        weights['36103190708'].extend([1.0])
        #City Island
        neighbors['36005051600'].append('36005050400')
        neighbors['36005050400'].append('36005051600')
        weights['36005051600'].append(1.0)
        weights['36005050400'].append(1.0)
        #Broad Channel Island to Rockaway Beach connected by highway
        neighbors['36081107201'].extend(['36081094201', '36081094202'])
        neighbors['36081094201'].extend(['36081107201', '36081094202'])
        neighbors['36081094202'].extend(['36081107201', '36081094201'])
        weights['36081107201'].extend([1.0, 1.0])
        weights['36081094201'].extend([1.0, 1.0])
        weights['36081094202'].extend([1.0, 1.0])
        #Long Beach Island to Manahawkin connected by highway
        neighbors['34029739000'].extend(['34029735103', '34029735104'])
        neighbors['34029735103'].extend(['34029739000', '34029735104'])
        neighbors['34029735104'].extend(['34029739000', '34029735103'])
        weights['34029735103'].extend([1.0, 1.0])
        weights['34029739000'].extend([1.0, 1.0])
        weights['34029735104'].extend([1.0, 1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='36140':
        # Ocean City, NJ
        neighbors = w.neighbors
        weights = w.weights
        # Corson's Inlet State Park,connected to adjacent tract by highway
        neighbors['34009020205'].append('34009020302')
        neighbors['34009020302'].append('34009020205')
        weights['34009020205'].append(1.0)
        weights['34009020302'].append(1.0)
        # Cape May
        neighbors['34009021900'].append('34009021702')
        neighbors['34009021702'].append('34009021900')
        weights['34009021900'].append(1.0)
        weights['34009021702'].append(1.0)
        # Wildwood Crest
        neighbors['34009021500'].append('34009021702')
        neighbors['34009021702'].append('34009021500')
        weights['34009021500'].append(1.0)
        weights['34009021702'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='38940':
        # Port St. Lucie, FL
        neighbors = w.neighbors
        weights = w.weights
        # Fort Pierce area, connected via bridge to rest of census tracts
        # Also connected to neighboring land mass outside of MSA
        neighbors['12111380901'].append('12111381204')
        neighbors['12111381204'].append('12111380901')
        weights['12111380901'].append(1.0)
        weights['12111381204'].append(1.0)
        # Causeway Island connected to mainland by bridge
        neighbors['12111381300'].append('12111380100')
        neighbors['12111380100'].append('12111381300')
        weights['12111381300'].append(1.0)
        weights['12111380100'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)  
    if msa=='39300':
        # Providence-Warwick, RI-MA
        neighbors = w.neighbors
        weights = w.weights
        # Block Island, connected via ferry
        neighbors['44009041500'].append('44009051504')
        neighbors['44009051504'].append('44009041500')
        weights['44009041500'].append(1.0)
        weights['44009051504'].append(1.0)
        # Jamestown connected via bridge on either side
        neighbors['44005041300'].extend(['44005041100', '44009050402'])
        neighbors['44005041100'].extend(['44005041300'])
        neighbors['44009050402'].extend(['44005041300'])
        weights['44005041300'].extend([1.0, 1.0])
        weights['44005041100'].extend([1.0])
        weights['44009050402'].extend([1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='39460':
        # Punta Gorda, FL
        neighbors = w.neighbors
        weights = w.weights
        # Peninsula connected to mainland by highway at El Jobean
        neighbors['12015020400'].extend(['12015030502', '12015030100'])
        neighbors['12015030100'].extend(['12015020400', '12015030502'])
        neighbors['12015030502'].extend(['12015020400', '12015030100'])
        weights['12015020400'].extend([1.0, 1.0])
        weights['12015030100'].extend([1.0])
        weights['12015030502'].extend([1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='41980': 
        #San Juan, PR 
        neighbors = w.neighbors
        weights = w.weights
        # City/Island of San Juan Connected to mainland by two highways
        neighbors['72127000700'].extend(['72127000900', '72127004200'])
        neighbors['72127000900'].extend(['72127000700', '72127000900'])
        neighbors['72127004200'].extend(['72127000700', '72127004200'])
        weights['72127000700'].extend([1.0, 1.0])
        weights['72127000900'].extend([1.0, 1.0])
        weights['72127004200'].extend([1.0, 1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='42660':
        # Seattle - Tacoma - Bellevue, WA
        neighbors = w.neighbors
        weights = w.weights
        # Fox Island, connected via bridge
        neighbors['53053072410'].extend(['53053072409', '53053072405'])
        neighbors['53053072405'].extend(['53053072410', '53053072409'])
        neighbors['53053072409'].extend(['53053072410', '53053072405'])
        weights['53053072410'].extend([1.0,1.0])
        weights['53053072405'].extend([1.0,1.0])
        weights['53053072409'].extend([1.0,1.0])
        # Northern Vashon Island, connected via ferry to mainland
        neighbors['53033027701'].append('53033011600')
        neighbors['53033011600'].append('53033027701')
        weights['53033027701'].append(1.0)
        weights['53033011600'].append(1.0)
        # Southern Vashon Island, connected via ferry to mainland
        neighbors['53033027702'].append('53053060300')
        neighbors['53053060300'].append('53033027702')
        weights['53033027702'].append(1.0)
        weights['53053060300'].append(1.0)
        # Roadway crossing bay between Wauna and Purdy
        neighbors['53053072503'].append('53053072504')
        neighbors['53053072504'].append('53053072503')
        weights['53053072503'].append(1.0)
        weights['53053072504'].append(1.0)
        # Mercer Island connected via bridge on east bank
        neighbors['53033009500'].extend(['53033008900', '53033024300'])
        neighbors['53033008900'].extend(['53033009500', '53033024300'])
        neighbors['53033024300'].extend(['53033008900', '53033009500'])
        weights['53033009500'].extend([1.0,1.0])
        weights['53033008900'].extend([1.0,1.0])
        weights['53033024300'].extend([1.0,1.0])        
        # Mercer Island connected via bridge on west bank
        neighbors['53033024400'].extend(['53033024500', '53033023900'])
        neighbors['53033024500'].extend(['53033024400', '53033023900'])
        neighbors['53033023900'].extend(['53033024400', '53033024500'])
        weights['53033024400'].extend([1.0,1.0])
        weights['53033024500'].extend([1.0,1.0])
        weights['53033023900'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='45300':
        # Tampa - St. Petersburg - Clearwater, FL
        neighbors = w.neighbors
        weights = w.weights
        #Harbour Island, connected via two bridges to mainland
        neighbors['12057005102'].extend(['12057005101', '12057005301'])
        neighbors['12057005101'].extend(['12057005102', '12057005301'])
        neighbors['12057005301'].extend(['12057005102', '12057005101'])
        weights['12057005102'].extend([1.0,1.0])
        weights['12057005101'].extend([1.0,1.0])
        weights['12057005301'].extend([1.0,1.0])
        #Diamond Isle, connected via elevated highway/bridge on either side 
        neighbors['12103026001'].extend(['12103026002', '12103025900'])
        neighbors['12103026002'].extend(['12103026001'])
        neighbors['12103025900'].extend(['12103026001'])
        weights['12103026001'].extend([1.0,1.0])
        weights['12103026002'].extend([1.0])
        weights['12103025900'].extend([1.0])
        #Isla Del Sol, connected via elevated highway/bridge on three sides
        neighbors['12103020108'].extend(['12103020106', '12103020107', '12103028002'])
        neighbors['12103020106'].extend(['12103020108'])
        neighbors['12103020107'].extend(['12103020108'])
        neighbors['12103028002'].extend(['12103020108'])
        weights['12103020108'].extend([1.0,1.0,1.0])
        weights['12103020106'].extend([1.0])
        weights['12103020107'].extend([1.0])
        weights['12103028002'].extend([1.0])
        #Bayway Isles, connected via elevated highway/bridge on two sides
        neighbors['12103020107'].extend(['12103020105', '12103020108'])
        neighbors['12103020105'].extend(['12103020107'])
        neighbors['12103020108'].extend(['12103020107'])
        weights['12103020107'].extend([1.0, 1.0])
        weights['12103020105'].extend([1.0])
        weights['12103020108'].extend([1.0])
        #Davis Islands, connected via two bridges to one mainland tract
        neighbors['12057005401'].append('12057005500')
        neighbors['12057005500'].append('12057005401')
        weights['12057005401'].append(1.0)
        weights['12057005500'].append(1.0)
        #Paradise Island, connected via two bridges to other islands/mainland
        neighbors['12103027903'].extend(['12103022401', '12103027901'])
        neighbors['12103022401'].extend(['12103027903'])
        neighbors['12103027901'].extend(['12103027903'])
        weights['12103027903'].extend([1.0, 1.0])
        weights['12103022401'].extend([1.0])
        weights['12103027901'].extend([1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='47260':
        # Virginia Beach-Norfolk-Newport News, VA-NC
        neighbors = w.neighbors
        weights = w.weights
        # Gloucester Point connects to Yorktown via highway
        neighbors['51073100301'].append('51199050500')
        neighbors['51199050500'].append('51073100301')
        weights['51199050500'].append(1.0)
        weights['51073100301'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='48900':
        # Wilmington, NC
        neighbors = w.neighbors
        weights = w.weights
        # Wrightsville Beach, connected via bridge that divides two tracts
        neighbors['37129011800'].extend(['37129012001', '37129011703'])
        neighbors['37129012001'].extend(['37129011800', '37129011703'])
        neighbors['37129011703'].extend(['37129011800', '37129011703'])
        weights['37129011800'].extend([1.0,1.0])
        weights['37129012001'].extend([1.0,1.0])
        weights['37129011703'].extend([1.0,1.0])
        w = ps.W(neighbors, weights, w.id_order)
    if msa=='sandyCO':
        #Hurricane Sandy region
        neighbors = w.neighbors
        weights = w.weights
        #Shelter Island, ferry connections on either side of island
        neighbors['36103180300'].extend(['36103170101', '36103190708'])
        neighbors['36103170101'].extend(['36103180300'])
        neighbors['36103190708'].extend(['36103180300'])
        weights['36103180300'].extend([1.0,1.0])
        weights['36103170101'].extend([1.0])
        weights['36103190708'].extend([1.0])
        #City Island
        neighbors['36005051600'].append('36005050400')
        neighbors['36005050400'].append('36005051600')
        weights['36005051600'].append(1.0)
        weights['36005050400'].append(1.0)
        #Broad Channel Island to Rockaway Beach connected by highway
        neighbors['36081107201'].extend(['36081094201', '36081094202'])
        neighbors['36081094201'].extend(['36081107201', '36081094202'])
        neighbors['36081094202'].extend(['36081107201', '36081094201'])
        weights['36081107201'].extend([1.0, 1.0])
        weights['36081094201'].extend([1.0, 1.0])
        weights['36081094202'].extend([1.0, 1.0])
        #Long Beach Island to Manahawkin connected by highway
        neighbors['34029739000'].extend(['34029735103', '34029735104'])
        neighbors['34029735103'].extend(['34029739000', '34029735104'])
        neighbors['34029735104'].extend(['34029739000', '34029735103'])
        weights['34029735103'].extend([1.0, 1.0])
        weights['34029739000'].extend([1.0, 1.0])
        weights['34029735104'].extend([1.0, 1.0])
        # Corson's Inlet State Park,connected to adjacent tract by highway
        neighbors['34009020205'].append('34009020302')
        neighbors['34009020302'].append('34009020205')
        weights['34009020205'].append(1.0)
        weights['34009020302'].append(1.0)
        # Cape May
        neighbors['34009021900'].append('34009021702')
        neighbors['34009021702'].append('34009021900')
        weights['34009021900'].append(1.0)
        weights['34009021702'].append(1.0)
        w = ps.W(neighbors, weights, w.id_order)
    return w
        
def moe(values):
    adds = 0
    for value in values:
        moex = (value)**2
        adds = adds + moex
    return adds 

def rename_vars(results, scenario):
    output_data = [results.ests_area, results.moes_area, results.cvs_area, results.ests_region, results.moes_region, results.cvs_region]
    for x in output_data:
        if scenario == "general":
            x.rename(columns={'prop_var0':'occupied', 'prop_var1':'married', 
                'prop_var2':'bachdeg', 'prop_var3':'samehous', 'prop_var4':'white',  
                'prop_var5':'black', 'prop_var6':'hisp', 'prop_var7':'under18', 'prop_var8':'65over',
                'ratio_var0':'avgrooms', 'ratio_var1':'avghhinc', 'ratio_var2':'pphh'},inplace=True)
        elif scenario == "poverty":
            x.rename(columns={'prop_var0':'chabvpov', 'prop_var1':'abvpov', 
                'prop_var2':'employed','ratio_var0':'hsincown', 'ratio_var1':'hsincrent'}, inplace=True)
        elif scenario == "transportation":
            x.rename(columns={'prop_var0':'drvlone', 'prop_var1':'transit', 
                'ratio_var0':'vehiclpp', 'ratio_var1':'avgcmmte',},inplace=True)
        elif scenario == "housing":
            x.rename(columns={'prop_var0':'occupied', 'prop_var1':'pctown',  
                'prop_var2':'pctrent', 'prop_var3':'snglfmly', 'ratio_var0':'avgrooms', 
                'ratio_var1':'avghmval', 'ratio_var2': 'avgrent'},inplace=True)
        elif scenario == "sovi":
            x.rename(columns={'prop_var0':'BLACK', 'prop_var1':'QNATAM', 
                'prop_var2':'QASIAN', 'prop_var3':'QHISP', 'prop_var4':'PRENTER', 'prop_var5':'QNRRES', 'prop_var6':'QFEMALE',
                'prop_var7':'QFHH', 'prop_var8':'QUNOCCHU', 'prop_var9':'QED12LES', 'prop_var10':'QEXTRCT', 'prop_var11':'QSERV', 
                'prop_var12':'QNOAUTO', 'prop_var13':'QPOVTY', 'prop_var14':'QMOHO', 'prop_var15':'QFEMLBR', 'prop_var16':'QSSBEN', 'prop_var17':'QFAM',
                'prop_var18':'QAGEDEP', 'prop_var19':'QESL', 'prop_var20':'QCVLUN', 'ratio_var0':'QPUNIT', 
                'ratio_var1':'PERCAP', 'ratio_var2': 'QRICH200K', 
                'ratio_var3': 'AVGHSEVAL', 'ratio_var4': 'AVGGRENT', 'ratio_var5': 'POPDENS'},inplace=True)
                #'ratio_var3': 'POPDENS'},inplace=True)
    results.ests_area.columns = results.ests_area.columns + 'E'
    results.moes_area.columns = results.moes_area.columns + 'M'
    results.cvs_area.columns = results.cvs_area.columns + 'CV'
    results.ests_region.columns = results.ests_region.columns + 'E'
    results.moes_region.columns = results.moes_region.columns + 'M'
    results.cvs_region.columns = results.cvs_region.columns + 'CV' 
    return results
    
def create_tractcsv(output_path, results, input_files, columns, scenario, prefix):    
    
    #Create csv containing all original input data for tracts (TID)
    # flatten list of lists
    columns = [item for sublist in columns for item in sublist]      
    # create set from variables to remove duplicates with same names
    all_vars = set(columns)
    #remove variables with '.' because they are duplicates
    leave_out = [s for s in all_vars if '.' in s]
    all_vars = [x for x in all_vars if x not in leave_out]
    all_vars.remove('B01003_001E')
    all_vars.remove('B01003_001M')
    all_vars.append('B01003_001E')
    all_vars.append('B01003_001M')
    # concatenate all input files into one file
    inputs = pd.concat(input_files, axis=1)
    # create new data frame and progressively add columns to ensure no duplicates
    inputs_v2 = pd.DataFrame()
    for x in all_vars:
        # if calling column variable creates series, copy series
        if isinstance(inputs[x], pd.Series):
            inputs_v2[x] = inputs[x]
        # if calling column variable creates data frame, then there are two
        # columns with same name so only one should be copied into the new DF
        elif isinstance(inputs[x], pd.DataFrame): 
            inputs_v2[x] = inputs[x].ix[:,0:1]  
    # rename tract GEOID column to TID
    inputs_v2.index.rename('TID',inplace=True)
    # add calculated values from regionalization to csv
    area_results = [results.ests_area, results.moes_area, results.cvs_area]
    for x in area_results:
        x.index = inputs_v2.index
    # combine inputs from census and calculated input variables
    all_inputs = pd.concat([inputs_v2, results.ests_area, results.moes_area, results.cvs_area], axis=1)
    all_inputs.to_csv(output_path + prefix + 'input_tracts.csv')
    return all_inputs

def create_crosswalk(output_path, prefix, shp_map, results):
    #IV.C. Region to tract crosswalk
    # get list of tracts from input shapefile
    tracts = shp_map.GEOID
    # create data frame from region ids
    s = pd.DataFrame(results.region_ids)
    # rename column to regionID
    s.rename(columns={0:'RID'},inplace=True)
    # convert to int from float
    s.RID = s.RID.astype(int)
    # create data frame from tract list
    s2 = pd.DataFrame(map(tracts.get, s.index))
    # rename column to TID
    s2.rename(columns={0:'TID'},inplace=True)
    #add 'g' before tract names
    s2['TID'] = 'g' + s2['TID'].astype(str)
    # concantenate data frames to create crosswalk
    crosswalk = pd.concat([s, s2], axis=1)
    # write to file
    crosswalk.to_csv(output_path + prefix + 'crosswalk.csv', index=False)
    return crosswalk
    
def create_regioncsv(output_path, prefix, results, input_files, all_inputs, crosswalk):
    #IV.D. Region variable values
    #Calculate the input variables for the regions
    #input variables
    input_ests = [input_files[2], input_files[4]]
    input_moes = [input_files[3], input_files[5]]
    columns_ests = [input_files[2].columns, input_files[4].columns]
    columns_moes = [input_files[3].columns, input_files[5].columns]
    # flatten list of lists
    columns_ests = [item for sublist in columns_ests for item in sublist]      
    columns_moes = [item for sublist in columns_moes for item in sublist]  
    # create set from variables to remove duplicates with same names
    all_vars_ests = set(columns_ests)
    all_vars_moes = set(columns_moes)
    #remove variables with '.' because they are duplicates
    leave_out_ests = [s for s in all_vars_ests if '.' in s]
    leave_out_moes = [s for s in all_vars_moes if '.' in s]
    all_vars_ests = [x for x in all_vars_ests if x not in leave_out_ests]
    all_vars_moes = [x for x in all_vars_moes if x not in leave_out_moes]
    # concatenate all input files into one file
    inputsE = pd.concat(input_ests, axis=1)
    inputsM = pd.concat(input_moes, axis=1)
    
    # create new data frame and progressively add columns to ensure no duplicates
    inputs_M2 = pd.DataFrame()
    all_vars_moes.sort()
    for x in all_vars_moes:
        # if calling column variable creates series, copy series
        if isinstance(inputsM[x], pd.Series):
            inputs_M2[x] = inputsM[x]
        # if calling column variable creates data frame, then there are two
        # columns with same name so only one should be copied into the new DF
        elif isinstance(inputsM[x], pd.DataFrame): 
            inputs_M2[x] = inputsM[x].ix[:,0:1] 
    inputs_E2 = pd.DataFrame()
    all_vars_ests.sort()
    for o in all_vars_ests:
        # if calling column variable creates series, copy series
        if isinstance(inputsE[o], pd.Series):
            inputs_E2[o] = inputsE[o]
        # if calling column variable creates data frame, then there are two
        # columns with same name so only one should be copied into the new DF
        elif isinstance(inputsE[o], pd.DataFrame): 
            inputs_E2[o] = inputsE[o].ix[:,0:1]  
    inputs_E2.index.rename('TID',inplace=True)
    inputs_M2.index.rename('TID',inplace=True)
    
    #input_vars = list(input_data.columns[1:])
    outputE = pd.DataFrame(pd.DataFrame(columns=inputs_E2.columns))
    outputM = pd.DataFrame(pd.DataFrame(columns=inputs_M2.columns))
    regions = list(set(crosswalk['RID']))
    regions.sort()
    regions = pd.Series(regions)
    for x in regions:
        #identify rows for region
        region = crosswalk.loc[crosswalk['RID'] == x]
        #identify TID for rows
        tracts = list(region.TID.values)    
        for a in range(len(inputs_E2.columns)):
            region_data = inputs_E2[inputs_E2.index.isin(tracts)]        
            region_value = sum(region_data[inputs_E2.columns[a]].values)
            outputE.set_value(x, inputs_E2.columns[a], region_value)
            outputE.index.rename('RID')
        for a in range(len(inputs_M2.columns)):
            region_data = inputs_M2[inputs_M2.index.isin(tracts)]
            region_value = np.sqrt(moe(region_data[inputs_M2.columns[a]].values))
            outputM.set_value(x, inputs_M2.columns[a], region_value)
            outputM.index.rename('RID')       

    # Write output regions calculated values to file, append region input vars
    #join 
    df = pd.concat([results.ests_region, results.moes_region, results.cvs_region], axis=1)
    df.insert(0, 'RID', df.index)
    # write to file
    df = pd.merge(outputM, df, left_index=True, right_on='RID')
    df = pd.merge(outputE, df, left_index=True, right_on='RID') 
    df.drop('RID', axis=1, inplace=True)
    df.index.rename('RID', inplace=True)
    df.to_csv(output_path + prefix + 'output_regions.csv', index=True)     
    return df
    
def create_shapes(output_path, prefix, results, shp_map, all_inputs, df, prj, json_path, value):
    #Shapefiles for new regions and input tracts
    #copy region IDs from results
    rids = copy.copy(results.region_ids)
    #add rids column to the 
    shp_map['rids'] = rids
    # dissolve the tracts into regions
    region_groups = shp_map.groupby('rids')
    region_map = gp.GeoDataFrame(index=region_groups.indices.keys())
    region_map['rids'] = region_groups.indices.keys()
    region_map['geometry'] = region_groups.geometry.apply(shapely.ops.unary_union)
    region_map.rename(columns={'rids':'RID'},inplace=True)
    shp_map.rename(columns={'rids':'RID'},inplace=True)
    # convert to int from float
    region_map.RID = region_map.RID.astype(int)
    shp_map.RID = shp_map.RID.astype(int)
    #write shapefiles to file
    region_map.to_file(output_path + prefix + 'regions.shp')
    shp_map.to_file(output_path + prefix + 'tracts.shp')
    # Copy projection file
    new_prj2 = output_path + prefix + 'tracts.prj'
    copyfile(prj, new_prj2)
    # Copy projection file
    new_prj3 = output_path + prefix + 'regions.prj'
    copyfile(prj, new_prj3)
    
    #join tract data to tract shapefile to create geojson
    shp_map.GEOID = 'g' + shp_map.GEOID
    shp_map.rename(columns = {'GEOID': 'TID'}, inplace=True)
    all_inputs.columns = all_inputs.columns.str.replace("_", "")
    all_inputs = all_inputs.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    newmap = pd.merge(shp_map, all_inputs, left_on='TID', right_index = True)
    newmap = newmap.round(3)
    newmap = newmap.replace([np.inf, -np.inf], np.nan)
    newmap = newmap.replace(np.nan,' ', regex=True)
    newmap = gp.GeoDataFrame(newmap)
    # Convert Geopandas DF to JSON file
    with open(json_path + value + '_tract.geojson', 'w') as f:
        f.write(newmap.to_json())
    
    #join region data to region shapefile
    df.columns = df.columns.str.replace("_", "")
    df = df.astype('float')
    dmap = pd.merge(region_map, df, left_on='RID', right_index=True)
    dmap = dmap.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    dmap = dmap.round(3)
    dmap = dmap.replace(np.nan,' ', regex=True)
    dmap.RID = dmap.RID.astype('str')
    dmap = gp.GeoDataFrame(dmap)
    # Convert Geopandas DF to JSON file
    with open(json_path + prefix + 'region.geojson', 'w') as f:
        f.write(dmap.to_json())

def style_geojson(outputpath, typeID, geo):
    
    #Open JSON file as Python object
    with open(outputpath) as f:
        data = json.load(f)

    x = len(data['features'])
    
    # Iterate through all features (regions)
    for i in range(x): 
    
        # Add styling to polygon
        # Randomly color regions
        r = lambda: random.randint(0,255)
        color = ('#%02X%02X%02X' % (r(),r(),r()))
        r = color
        data['features'][i]['properties']['stroke'] = '#000066'
        data['features'][i]['properties']["fill"] = r
        data['features'][i]['properties']["stroke-width"] = 2 
        data['features'][i]['properties']["fill-opacity"] = .6
        data['features'][i]['properties']["stroke-opacity"] = 10

    # Write back to file          
    with open(outputpath,"w") as f:
        json.dump(data, f, sort_keys=True)
        
def create_weights(output_path, prefix, w):
    # Spatial weights matrix file
    gal = ps.open(output_path + prefix + 'weights_matrix.gal','w')
    gal.write(w)
    gal.close()
    
def meta(output_path, meta, dict1):
    # Copy metdata file & data dictionary to output
    metadata = output_path + 'metadata.txt'
    dataDict = output_path + 'dataDict.csv'
    copyfile(meta, metadata)
    copyfile(dict1, dataDict)
    return metadata, dataDict   
    
def makeArchive(fileList, archive, root, path):
    """
    'fileList' is a list of file names - full path each name
    'archive' is the file name for the archive with a full path
    """
    if not os.path.exists(path):
        os.makedirs(path)
    a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)

    for f in fileList:
        print "archiving file %s" % (f)
        a.write(f, os.path.relpath(f, root))
    a.close()
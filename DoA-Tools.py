import http.client
import json
import os
from binascii import b2a_hex
from hashlib import sha1
from time import time, sleep

__author__ = 'AlphaQ2 (Suresh Kumar)'
__credits__ = 'Lucifa & Temprid'
__version__ = '1.3.0'
__maintainer__ = 'https://www.facebook.com/groups/thesanctuary.doa/'

########################################################################################################################
#                                             SCRIPT SECTION - Do Not Edit!                                            #
########################################################################################################################
# -------------------------------------------------------------------------------------------------------------------- #
#                                                   GAME DICTIONARIES                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
troop_dict = {'AbyssalRavager': 'Abyssal Ravager', 'AquaTroop': 'Fangtooth', 'ArcticLeviathan': 'Arctic Leviathan',
              'ArmoredTransport': 'Armored Transport', 'BattleDragon': 'Battle Dragon', 'ChargeTroop': 'Storm Drake',
              'ColossalMite': 'Colossal Mite', 'Conscript': 'Conscript', 'DarkSlayer': 'Dark Slayer',
              'Defendo': 'Thunder Golem', 'DesertTroop': 'Sand Strider', 'DimensionalRuiner': 'Dimensional Ruiner',
              'DragonRider': 'Dragon Rider', 'FireMirror': 'Fire Mirror', 'FireTroop': 'Lava Jaw',
              'ForestTroop': 'Petrified Titan', 'FrostGiant': 'Frost Giant', 'Giant': 'Giant',
              'Halberdsman': 'Halberdsman', 'Harrier': 'Steelshard Harrier', 'IceTroop': 'Soul Reaper',
              'LightningCannon': 'Lightning Cannon', 'Longbowman': 'Longbowman', 'Minotaur': 'Minotaur',
              'PackDragon': 'Pack Dragon', 'Porter': 'Porter', 'SeaSiren': 'Sea Siren',
              'ShadowStalker': 'Shadow Stalker', 'Shaman': 'Shaman', 'Spy': 'Spy', 'StoneTroop': 'Granite Ogre',
              'SwampTroop': 'Venom Dweller', 'SwiftStrikeDragon': 'Swift Strike Dragon', 'VengeWyrm': 'Venge Wyrm',
              'VoltRanger': 'Volt Ranger', 'WarScarab': 'War Scarab', 'WindTroop': 'Banshee'}

game_dict = {'Silo': 'Silo', 'Farm': 'Farm', 'Lumbermill': 'Lumbermill', 'Mine': 'Mine', 'Quarry': 'Quarry',
             'EnergyCollector': 'Reaping Stones', 'Factory': 'Factory', 'DragonKeep': 'Dragon Keep', 'Wall': 'Wall',
             'Fortress': 'Fortress', 'Garrison': 'Garrison', 'Home': 'Home', 'OfficerQuarter': 'Officer Quarter',
             'Rookery': 'Rookery', 'Metalsmith': 'Metalsmith', 'MusterPoint': 'Muster Point', 'Cathedral': 'Cathedral',
             'ScienceCenter': 'Science Center', 'Sentinel': 'Sentinel', 'StorageVault': 'Storage Vault',
             'Theater': 'Theater', 'TrainingCamp': 'Training Camp', 'SpectralDragonKeep': 'Dragon Keep',
             'DarkPortal': 'Dark Portal', 'Mausoleum': 'Mausoleum', 'KaiserDragonKeep': 'Dragon Keep', 'Forge': 'Forge',
             'Greenhouse': 'Greenhouse', 'Library': 'Library', 'Workshop': 'Academy', 'CaveDragonKeep': 'Dragon Keep',
             'CaveCathedral': 'Cathedral', 'CaveDepot': 'Depot', 'CaveForge': 'Forge', 'CaveGreenhouse': 'Greenhouse',
             'CaveLibrary': 'Library', 'CaveTrainingCamp': 'Training Camp', 'CaveWorkshop': 'Academy',
             'LunaShrine': 'Shrine', 'LunaDepot': 'Depot', 'LunaCathedral': 'Cathedral', 'LunaForge': 'Forge',
             'LunaGreenhouse': 'Greenhouse', 'LunaLibrary': 'Library', 'LunaWorkshop': 'Academy',
             'ColossusDragonKeep': 'Dragon Keep', 'ColossusWall': 'Wall', 'Warehouse': 'Warehouse',
             'TroopQuarters': 'Troop Quarters', 'WarpGate': 'Warp Gate', 'WarpPortal': 'Warp Portal',
             'LeviathanDragonKeep': 'Dragon Keep', 'LeviathanWall': 'Wall', 'LeviathanWarehouse': 'Warehouse',
             'LeviathanTroopQuarters': 'Troop Quarters', 'LeviathanMarketplace': 'Marketplace', 'capital': 'Capital',
             'cave': 'Steelshard Caverns', 'chrono': 'Cliffs of Chronos', 'colossus': 'The Lost City',
             'desert': 'Solarian Highlands', 'fire': 'Fire Outpost', 'forest': 'Gaea Spring', 'ice': 'Ice Outpost',
             'leviathan': 'The Abyssal Palace', 'luna': 'Luna Plains', 'skythrone': 'Skythrone',
             'spectral': 'Spectral Ruins', 'stone': 'Stone Outpost', 'swamp': 'Sunken Temple', 'water': 'Water Outpost',
             'wind': 'Wind Outpost'}

forge_dict = {'AbyssalRavagerAmuletOfRenewal': 'Amulet Of Renewal', 'AbyssalRavagerChameleonPotion': 'Chameleon Potion',
              'AbyssalRavagerEagleEyePotion': 'Eagle Eye Potion', 'AbyssalRavagerFarShotPotion': 'Far Shot Potion',
              'AbyssalRavagerFuryPotion': 'Fury Potion', 'AbyssalRavagerIronskinPotion': 'Ironskin Potion',
              'AbyssalRavagerQuicksilverPotion': 'Quicksilver Potion', 'AbyssalRavagerStasisPotion': 'Stasis Potion',
              'AbyssalRavagerSunFireBreath': 'Sun Fire Breath', 'AbyssalRavagerVitalityPotion': 'Vitality Potion',
              'ArcticLeviathanAmulet': 'Amulet', 'ArcticLeviathanChameleonPotion': 'Chameleon Potion',
              'ArcticLeviathanEagleEyePotion': 'Eagle Eye Potion', 'ArcticLeviathanFarShotPotion': 'Far Shot Potion',
              'ArcticLeviathanFuryPotion': 'Fury Potion', 'ArcticLeviathanGrimArrows': 'Grim Arrows',
              'ArcticLeviathanIronskinPotion': 'Ironskin Potion', 'ArcticLeviathanPlating': 'Plating',
              'ArcticLeviathanQuicksilverPotion': 'Quicksilver Potion', 'ArcticLeviathanShadowHelm': 'Shadow Helm',
              'ArcticLeviathanStasisPotion': 'Stasis Potion', 'ArcticLeviathanVitalityPotion': 'Vitality Potion',
              'ArmoredTransportChameleonPotion': 'Chameleon Potion', 'ArmoredTransportClaws': 'Claws',
              'ArmoredTransportFuryPotion': 'Fury Potion', 'ArmoredTransportIronskinPotion': 'Ironskin Potion',
              'ArmoredTransportPlating': 'Plating', 'ArmoredTransportQuicksilverPotion': 'Quicksilver Potion',
              'ArmoredTransportStasisPotion': 'Stasis Potion', 'ArmoredTransportVitalityPotion': 'Vitality Potion',
              'BansheeChameleonPotion': 'Chameleon Potion', 'BansheeClaws': 'Claws', 'BansheeCloak': 'Cloak',
              'BansheeFuryPotion': 'Fury Potion', 'BansheeGrimScythe': 'Grim Scythe',
              'BansheeIronskinPotion': 'Ironskin Potion', 'BansheeQuicksilverPotion': 'Quicksilver Potion',
              'BansheeShadowHelm': 'Shadow Helm', 'BansheeStasisPotion': 'Stasis Potion',
              'BansheeVitalityPotion': 'Vitality Potion', 'BattleDragonChameleonPotion': 'Chameleon Potion',
              'BattleDragonClaws': 'Claws', 'BattleDragonFuryPotion': 'Fury Potion',
              'BattleDragonGrimScythe': 'Grim Scythe', 'BattleDragonIronskinPotion': 'Ironskin Potion',
              'BattleDragonPlating': 'Plating', 'BattleDragonQuicksilverPotion': 'Quicksilver Potion',
              'BattleDragonShadowHelm': 'Shadow Helm', 'BattleDragonStasisPotion': 'Stasis Potion',
              'BattleDragonVitalityPotion': 'Vitality Potion', 'BlackPowder': 'Black Powder',
              'BluePowder': 'Blue Powder', 'ColossalMiteChameleonPotion': 'Chameleon Potion',
              'ColossalMiteClaws': 'Claws', 'ColossalMiteEagleEyePotion': 'Eagle Eye Potion',
              'ColossalMiteFarShotPotion': 'Far Shot Potion', 'ColossalMiteFuryPotion': 'Fury Potion',
              'ColossalMiteGrimArrows': 'Grim Arrows', 'ColossalMiteIronskinPotion': 'Ironskin Potion',
              'ColossalMitePlating': 'Plating', 'ColossalMiteQuicksilverPotion': 'Quicksilver Potion',
              'ColossalMiteShadowHelm': 'Shadow Helm', 'ColossalMiteStasisPotion': 'Stasis Potion',
              'ColossalMiteVitalityPotion': 'Vitality Potion', 'ConscriptAmulet': 'Amulet',
              'ConscriptChameleonPotion': 'Chameleon Potion', 'ConscriptFuryPotion': 'Fury Potion',
              'ConscriptHammer': 'Hammer', 'ConscriptIronskinPotion': 'Ironskin Potion',
              'ConscriptQuicksilverPotion': 'Quicksilver Potion', 'ConscriptSolarMace': 'Solar Mace',
              'ConscriptStarCirclet': 'Star Circlet', 'ConscriptStasisPotion': 'Stasis Potion',
              'ConscriptVitalityPotion': 'Vitality Potion', 'CrackedCog': 'Cracked Cog',
              'DarkSlayerChameleonPotion': 'Chameleon Potion', 'DarkSlayerFuryPotion': 'Fury Potion',
              'DarkSlayerIronskinPotion': 'Ironskin Potion', 'DarkSlayerQuicksilverPotion': 'Quicksilver Potion',
              'DarkSlayerRobes': 'Robes', 'DarkSlayerSolarMace': 'Solar Mace', 'DarkSlayerStaff': 'Staff',
              'DarkSlayerStarCirclet': 'Star Circlet', 'DarkSlayerStasisPotion': 'Stasis Potion',
              'DarkSlayerVitalityPotion': 'Vitality Potion', 'DimensionalRuinerChameleonPotion': 'Chameleon Potion',
              'DimensionalRuinerFuryPotion': 'Fury Potion', 'DimensionalRuinerHammer': 'Hammer',
              'DimensionalRuinerHelm': 'Helm', 'DimensionalRuinerIronskinPotion': 'Ironskin Potion',
              'DimensionalRuinerQuicksilverPotion': 'Quicksilver Potion', 'DimensionalRuinerSolarMace': 'Solar Mace',
              'DimensionalRuinerStarCirclet': 'Star Circlet', 'DimensionalRuinerStasisPotion': 'Stasis Potion',
              'DimensionalRuinerVitalityPotion': 'Vitality Potion', 'DragonRiderBow': 'Bow',
              'DragonRiderChameleonPotion': 'Chameleon Potion', 'DragonRiderEagleEyePotion': 'Eagle Eye Potion',
              'DragonRiderFarShotPotion': 'Far Shot Potion', 'DragonRiderFuryPotion': 'Fury Potion',
              'DragonRiderHelm': 'Helm', 'DragonRiderHelmOfAdoration': 'Helm Of Adoration',
              'DragonRiderIronskinPotion': 'Ironskin Potion', 'DragonRiderQuicksilverPotion': 'Quicksilver Potion',
              'DragonRiderScythe': 'Scythe', 'DragonRiderSeekingArrow': 'Seeking Arrow',
              'DragonRiderStasisPotion': 'Stasis Potion', 'DragonRiderVitalityPotion': 'Vitality Potion',
              'DullScale': 'Dull Scale', 'ElementalAir': 'Elemental Air', 'ElementalEarth': 'Elemental Earth',
              'ElementalFire': 'Elemental Fire', 'ElementalSpirit': 'Elemental Spirit',
              'ElementalWater': 'Elemental Water', 'EliteAbyssalRavagerAmuletOfRenewal': 'Elite Amulet Of Renewal',
              'EliteAbyssalRavagerSunFireBreath': 'Elite Sun Fire Breath', 'EliteArcticLeviathanAmulet': 'Elite Amulet',
              'EliteArcticLeviathanPlating': 'Elite Plating', 'EliteColossalMiteClaws': 'Elite Claws',
              'EliteColossalMitePlating': 'Elite Plating', 'EliteDimensionalRuinerHammer': 'Elite Hammer',
              'EliteDimensionalRuinerHelm': 'Elite Helm', 'EliteDragonRiderBow': 'Elite Bow',
              'EliteDragonRiderHelm': 'Elite Helm', 'EliteLightningCannonPlating': 'Elite Plating',
              'EliteLightningCannonRune': 'Elite Rune', 'EliteSeaSirenScales': 'Elite Scales',
              'EliteSeaSirenTalons': 'Elite Talons', 'EliteShadowStalkerClaws': 'Elite Claws',
              'EliteShadowStalkerPlating': 'Elite Plating', 'EliteShamanHelm': 'Elite Helm',
              'EliteShamanStaff': 'Elite Staff', 'EliteSteelshardHarrierClaws': 'Elite Claws',
              'EliteSteelshardHarrierPlating': 'Elite Plating', 'EliteStormDrakeHelm': 'Elite Helm',
              'EliteStormDrakeSpear': 'Elite Spear', 'EliteThunderGolemHammer': 'Elite Hammer',
              'EliteThunderGolemPlating': 'Elite Plating', 'EliteVengeWyrmPlating': 'Elite Plating',
              'EliteVengeWyrmStaff': 'Elite Staff', 'EliteVoltRangerCloak': 'Elite Cloak',
              'EliteVoltRangerRune': 'Elite Rune', 'EliteWarScarabAmulet': 'Elite Amulet',
              'EliteWarScarabPlating': 'Elite Plating', 'EmeraldTablet': 'Emerald Tablet',
              'EnameledCog': 'Enameled Cog', 'EnchantedIronBar': 'Enchanted Iron Bar',
              'FangtoothChameleonPotion': 'Chameleon Potion', 'FangtoothEagleEyePotion': 'Eagle Eye Potion',
              'FangtoothFarShotPotion': 'Far Shot Potion', 'FangtoothFuryPotion': 'Fury Potion',
              'FangtoothHelm': 'Helm', 'FangtoothIronskinPotion': 'Ironskin Potion',
              'FangtoothQuicksilverPotion': 'Quicksilver Potion', 'FangtoothSpear': 'Spear',
              'FangtoothStasisPotion': 'Stasis Potion', 'FangtoothVitalityPotion': 'Vitality Potion',
              'FineToothedCog': 'Fine Toothed Cog', 'FireMirrorAmuletOfRenewal': 'Amulet Of Renewal',
              'FireMirrorChameleonPotion': 'Chameleon Potion', 'FireMirrorClaws': 'Claws',
              'FireMirrorEagleEyePotion': 'Eagle Eye Potion', 'FireMirrorFarShotPotion': 'Far Shot Potion',
              'FireMirrorFuryPotion': 'Fury Potion', 'FireMirrorHelm': 'Helm',
              'FireMirrorIronskinPotion': 'Ironskin Potion', 'FireMirrorQuicksilverPotion': 'Quicksilver Potion',
              'FireMirrorStasisPotion': 'Stasis Potion', 'FireMirrorSunFireBreath': 'Sun Fire Breath',
              'FireMirrorVitalityPotion': 'Vitality Potion', 'FragileScale': 'Fragile Scale',
              'FrostGiantAmulet': 'Amulet', 'FrostGiantChameleonPotion': 'Chameleon Potion',
              'FrostGiantFuryPotion': 'Fury Potion', 'FrostGiantHammer': 'Hammer',
              'FrostGiantIronskinPotion': 'Ironskin Potion', 'FrostGiantQuicksilverPotion': 'Quicksilver Potion',
              'FrostGiantSolarMace': 'Solar Mace', 'FrostGiantStarCirclet': 'Star Circlet',
              'FrostGiantStasisPotion': 'Stasis Potion', 'FrostGiantVitalityPotion': 'Vitality Potion',
              'GiantAmulet': 'Amulet', 'GiantChameleonPotion': 'Chameleon Potion',
              'GiantCircleOfThorns': 'Circle Of Thorns', 'GiantDawnHammer': 'Dawn Hammer',
              'GiantFuryPotion': 'Fury Potion', 'GiantIronskinPotion': 'Ironskin Potion',
              'GiantQuicksilverPotion': 'Quicksilver Potion', 'GiantStaff': 'Staff',
              'GiantStasisPotion': 'Stasis Potion', 'GiantVitalityPotion': 'Vitality Potion',
              'GraniteOgreChameleonPotion': 'Chameleon Potion', 'GraniteOgreCircleOfThorns': 'Circle Of Thorns',
              'GraniteOgreDawnHammer': 'Dawn Hammer', 'GraniteOgreFuryPotion': 'Fury Potion',
              'GraniteOgreIronskinPotion': 'Ironskin Potion', 'GraniteOgrePlating': 'Plating',
              'GraniteOgreQuicksilverPotion': 'Quicksilver Potion', 'GraniteOgreStaff': 'Staff',
              'GraniteOgreStasisPotion': 'Stasis Potion', 'GraniteOgreVitalityPotion': 'Vitality Potion',
              'GrayPowder': 'Gray Powder', 'GreenPowder': 'Green Powder',
              'HalberdsmanChameleonPotion': 'Chameleon Potion', 'HalberdsmanFuryPotion': 'Fury Potion',
              'HalberdsmanHelmOfAdoration': 'Helm Of Adoration', 'HalberdsmanIronskinPotion': 'Ironskin Potion',
              'HalberdsmanQuicksilverPotion': 'Quicksilver Potion', 'HalberdsmanScythe': 'Scythe',
              'HalberdsmanSeekingArrow': 'Seeking Arrow', 'HalberdsmanShield': 'Shield', 'HalberdsmanSpear': 'Spear',
              'HalberdsmanStasisPotion': 'Stasis Potion', 'HalberdsmanVitalityPotion': 'Vitality Potion',
              'HardenedScale': 'Hardened Scale', 'IdolOfTheNorthWind:': 'Idol Of The North Wind:',
              'IronDust': 'Iron Dust', 'LavaJawAmulet': 'Amulet',
              'LavaJawAmuletOfRenewal': 'Amulet Of Renewal', 'LavaJawChameleonPotion': 'Chameleon Potion',
              'LavaJawClaws': 'Claws', 'LavaJawEagleEyePotion': 'Eagle Eye Potion',
              'LavaJawFarShotPotion': 'Far Shot Potion', 'LavaJawFuryPotion': 'Fury Potion',
              'LavaJawIronskinPotion': 'Ironskin Potion', 'LavaJawQuicksilverPotion': 'Quicksilver Potion',
              'LavaJawStasisPotion': 'Stasis Potion', 'LavaJawSunFireBreath': 'Sun Fire Breath',
              'LavaJawVitalityPotion': 'Vitality Potion', 'LightningCannonChameleonPotion': 'Chameleon Potion',
              'LightningCannonEagleEyePotion': 'Eagle Eye Potion', 'LightningCannonFarShotPotion': 'Far Shot Potion',
              'LightningCannonFuryPotion': 'Fury Potion', 'LightningCannonIronskinPotion': 'Ironskin Potion',
              'LightningCannonPlating': 'Plating', 'LightningCannonQuicksilverPotion': 'Quicksilver Potion',
              'LightningCannonRune': 'Rune', 'LightningCannonSolarMace': 'Solar Mace',
              'LightningCannonStarCirclet': 'Star Circlet', 'LightningCannonStasisPotion': 'Stasis Potion',
              'LightningCannonVitalityPotion': 'Vitality Potion', 'LongbowmanBow': 'Bow',
              'LongbowmanChameleonPotion': 'Chameleon Potion', 'LongbowmanCloak': 'Cloak',
              'LongbowmanEagleEyePotion': 'Eagle Eye Potion', 'LongbowmanFarShotPotion': 'Far Shot Potion',
              'LongbowmanFuryPotion': 'Fury Potion', 'LongbowmanHelmOfAdoration': 'Helm Of Adoration',
              'LongbowmanIronskinPotion': 'Ironskin Potion', 'LongbowmanQuicksilverPotion': 'Quicksilver Potion',
              'LongbowmanSeekingArrows': 'Seeking Arrows', 'LongbowmanStasisPotion': 'Stasis Potion',
              'LongbowmanVitalityPotion': 'Vitality Potion', 'MagicInfusedScale': 'Magic Infused Scale',
              'MetamorphicStone': 'Metamorphic Stone', 'MillenniumSeed': 'Millennium Seed', 'MinotaurAmulet': 'Amulet',
              'MinotaurChameleonPotion': 'Chameleon Potion', 'MinotaurFuryPotion': 'Fury Potion',
              'MinotaurGrimScythe': 'Grim Scythe', 'MinotaurHammer': 'Hammer',
              'MinotaurIronskinPotion': 'Ironskin Potion', 'MinotaurQuicksilverPotion': 'Quicksilver Potion',
              'MinotaurShadowHelm': 'Shadow Helm', 'MinotaurStasisPotion': 'Stasis Potion',
              'MinotaurVitalityPotion': 'Vitality Potion', 'PackDragonChameleonPotion': 'Chameleon Potion',
              'PackDragonClaws': 'Claws', 'PackDragonFuryPotion': 'Fury Potion', 'PackDragonGrimScythe': 'Grim Scythe',
              'PackDragonIronskinPotion': 'Ironskin Potion', 'PackDragonPlating': 'Plating',
              'PackDragonQuicksilverPotion': 'Quicksilver Potion', 'PackDragonShadowHelm': 'Shadow Helm',
              'PackDragonStasisPotion': 'Stasis Potion', 'PackDragonVitalityPotion': 'Vitality Potion',
              'PetrifiedTitanChameleonPotion': 'Chameleon Potion', 'PetrifiedTitanFuryPotion': 'Fury Potion',
              'PetrifiedTitanHammer': 'Hammer', 'PetrifiedTitanHelmOfAdoration': 'Helm Of Adoration',
              'PetrifiedTitanIronskinPotion': 'Ironskin Potion', 'PetrifiedTitanPlating': 'Plating',
              'PetrifiedTitanQuicksilverPotion': 'Quicksilver Potion', 'PetrifiedTitanSeekingArrows': 'Seeking Arrows',
              'PetrifiedTitanStasisPotion': 'Stasis Potion', 'PetrifiedTitanVitalityPotion': 'Vitality Potion',
              'PhilosophersStone': 'Philosophers Stone', 'PorterChameleonPotion': 'Chameleon Potion',
              'PorterFuryPotion': 'Fury Potion', 'PorterIronskinPotion': 'Ironskin Potion',
              'PorterQuicksilverPotion': 'Quicksilver Potion', 'PorterRobes': 'Robes', 'PorterStaff': 'Staff',
              'PorterStasisPotion': 'Stasis Potion', 'PorterVitalityPotion': 'Vitality Potion',
              'PrimalFrost': 'Primal Frost', 'PrimalMagma': 'Primal Magma', 'PrimalOoze': 'Primal Ooze',
              'PrimalSand': 'Primal Sand', 'PrimalSmoke': 'Primal Smoke', 'PrimalStorm': 'Primal Storm',
              'PristineHide': 'Pristine Hide', 'PurplePowder': 'Purple Powder', 'RawIronOre': 'Raw Iron Ore',
              'RefinedIronBar': 'Refined Iron Bar', 'RubyRelic': 'Ruby Relic',
              'SandStriderChameleonPotion': 'Chameleon Potion', 'SandStriderEagleEyePotion': 'Eagle Eye Potion',
              'SandStriderFarShotPotion': 'Far Shot Potion', 'SandStriderFuryPotion': 'Fury Potion',
              'SandStriderHelm': 'Helm', 'SandStriderIronskinPotion': 'Ironskin Potion',
              'SandStriderQuicksilverPotion': 'Quicksilver Potion', 'SandStriderScythe': 'Scythe',
              'SandStriderSpear': 'Spear', 'SandStriderStasisPotion': 'Stasis Potion',
              'SandStriderVitalityPotion': 'Vitality Potion', 'SandstriderHelmOfAdoration': 'Helm Of Adoration',
              'SandstriderSeekingArrow': 'Seeking Arrow', 'SeaSirenChameleonPotion': 'Chameleon Potion',
              'SeaSirenFuryPotion': 'Fury Potion', 'SeaSirenIronskinPotion': 'Ironskin Potion',
              'SeaSirenQuicksilverPotion': 'Quicksilver Potion', 'SeaSirenScales': 'Scales',
              'SeaSirenSolarMace': 'Solar Mace', 'SeaSirenStarCirclet': 'Star Circlet',
              'SeaSirenStasisPotion': 'Stasis Potion', 'SeaSirenTalons': 'Talons',
              'SeaSirenVitalityPotion': 'Vitality Potion', 'ShadowOrb': 'Shadow Orb',
              'ShadowStalkerChameleonPotion': 'Chameleon Potion', 'ShadowStalkerClaws': 'Claws',
              'ShadowStalkerFuryPotion': 'Fury Potion', 'ShadowStalkerGrimScythe': 'Grim Scythe',
              'ShadowStalkerIronskinPotion': 'Ironskin Potion', 'ShadowStalkerPlating': 'Plating',
              'ShadowStalkerQuicksilverPotion': 'Quicksilver Potion', 'ShadowStalkerShadowHelm': 'Shadow Helm',
              'ShadowStalkerStasisPotion': 'Stasis Potion', 'ShadowStalkerVitalityPotion': 'Vitality Potion',
              'ShamanChameleonPotion': 'Chameleon Potion', 'ShamanFuryPotion': 'Fury Potion', 'ShamanHelm': 'Helm',
              'ShamanIronskinPotion': 'Ironskin Potion', 'ShamanQuicksilverPotion': 'Quicksilver Potion',
              'ShamanStaff': 'Staff', 'ShamanStasisPotion': 'Stasis Potion', 'ShamanVitalityPotion': 'Vitality Potion',
              'SilverPowder': 'Silver Powder', 'SolarNectar': 'Solar Nectar', 'SoulReaperAmulet': 'Amulet',
              'SoulReaperChameleonPotion': 'Chameleon Potion', 'SoulReaperClaws': 'Claws',
              'SoulReaperFuryPotion': 'Fury Potion', 'SoulReaperGrimScythe': 'Grim Scythe',
              'SoulReaperIronskinPotion': 'Ironskin Potion', 'SoulReaperQuicksilverPotion': 'Quicksilver Potion',
              'SoulReaperShadowHelm': 'Shadow Helm', 'SoulReaperStasisPotion': 'Stasis Potion',
              'SoulReaperVitalityPotion': 'Vitality Potion', 'SpyChameleonPotion': 'Chameleon Potion',
              'SpyDagger': 'Dagger', 'SpyFuryPotion': 'Fury Potion', 'SpyIronskinPotion': 'Ironskin Potion',
              'SpyQuicksilverPotion': 'Quicksilver Potion', 'SpyRobes': 'Robes', 'SpySolarMace': 'Solar Mace',
              'SpyStarCirclet': 'Star Circlet', 'SpyStasisPotion': 'Stasis Potion',
              'SpyVitalityPotion': 'Vitality Potion', 'SteelshardHarrierChameleonPotion': 'Chameleon Potion',
              'SteelshardHarrierClaws': 'Claws', 'SteelshardHarrierFuryPotion': 'Fury Potion',
              'SteelshardHarrierIronskinPotion': 'Ironskin Potion', 'SteelshardHarrierPlating': 'Plating',
              'SteelshardHarrierQuicksilverPotion': 'Quicksilver Potion', 'SteelshardHarrierSolarMace': 'Solar Mace',
              'SteelshardHarrierStarCirclet': 'Star Circlet', 'SteelshardHarrierStasisPotion': 'Stasis Potion',
              'SteelshardHarrierVitalityPotion': 'Vitality Potion', 'StitchedHide': 'Stitched Hide',
              'StormDrakeChameleonPotion': 'Chameleon Potion', 'StormDrakeFuryPotion': 'Fury Potion',
              'StormDrakeHelm': 'Helm', 'StormDrakeIronskinPotion': 'Ironskin Potion',
              'StormDrakeQuicksilverPotion': 'Quicksilver Potion', 'StormDrakeSpear': 'Spear',
              'StormDrakeStasisPotion': 'Stasis Potion', 'StormDrakeVitalityPotion': 'Vitality Potion',
              'SturdyCog': 'Sturdy Cog', 'SwiftStrikeDragonChameleonPotion': 'Chameleon Potion',
              'SwiftStrikeDragonClaws': 'Claws', 'SwiftStrikeDragonFuryPotion': 'Fury Potion',
              'SwiftStrikeDragonGrimScythe': 'Grim Scythe', 'SwiftStrikeDragonIronskinPotion': 'Ironskin Potion',
              'SwiftStrikeDragonPlating': 'Plating', 'SwiftStrikeDragonQuicksilverPotion': 'Quicksilver Potion',
              'SwiftStrikeDragonShadowHelm': 'Shadow Helm', 'SwiftStrikeDragonStasisPotion': 'Stasis Potion',
              'SwiftStrikeDragonVitalityPotion': 'Vitality Potion', 'TannedHide': 'Tanned Hide',
              'TatteredHide': 'Tattered Hide', 'ThunderGolemChameleonPotion': 'Chameleon Potion',
              'ThunderGolemEagleEyePotion': 'Eagle Eye Potion', 'ThunderGolemFarShotPotion': 'Far Shot Potion',
              'ThunderGolemFuryPotion': 'Fury Potion', 'ThunderGolemHammer': 'Hammer',
              'ThunderGolemIronskinPotion': 'Ironskin Potion', 'ThunderGolemPlating': 'Plating',
              'ThunderGolemQuicksilverPotion': 'Quicksilver Potion', 'ThunderGolemSolarMace': 'Solar Mace',
              'ThunderGolemStarCirclet': 'Star Circlet', 'ThunderGolemStasisPotion': 'Stasis Potion',
              'ThunderGolemVitalityPotion': 'Vitality Potion', 'TransmutationStone': 'Transmutation Stone',
              'TrueChaos': 'True Chaos', 'TrueDarkness': 'True Darkness', 'TrueLife': 'True Life',
              'TrueTime': 'True Time', 'VengeWyrmChameleonPotion': 'Chameleon Potion',
              'VengeWyrmFuryPotion': 'Fury Potion', 'VengeWyrmIronskinPotion': 'Ironskin Potion',
              'VengeWyrmPlating': 'Plating', 'VengeWyrmQuicksilverPotion': 'Quicksilver Potion',
              'VengeWyrmStaff': 'Staff', 'VengeWyrmStasisPotion': 'Stasis Potion',
              'VengeWyrmVitalityPotion': 'Vitality Potion', 'VenomDwellerChameleonPotion': 'Chameleon Potion',
              'VenomDwellerEagleEyePotion': 'Eagle Eye Potion', 'VenomDwellerFarShotPotion': 'Far Shot Potion',
              'VenomDwellerFuryPotion': 'Fury Potion', 'VenomDwellerIronskinPotion': 'Ironskin Potion',
              'VenomDwellerQuicksilverPotion': 'Quicksilver Potion', 'VenomDwellerShield': 'Shield',
              'VenomDwellerStaff': 'Staff', 'VenomDwellerStasisPotion': 'Stasis Potion',
              'VenomDwellerVitalityPotion': 'Vitality Potion', 'VoltRangerChameleonPotion': 'Chameleon Potion',
              'VoltRangerCloak': 'Cloak', 'VoltRangerEagleEyePotion': 'Eagle Eye Potion',
              'VoltRangerFarShotPotion': 'Far Shot Potion', 'VoltRangerFuryPotion': 'Fury Potion',
              'VoltRangerHelmOfAdoration': 'Helm Of Adoration', 'VoltRangerIronskinPotion': 'Ironskin Potion',
              'VoltRangerQuicksilverPotion': 'Quicksilver Potion', 'VoltRangerRune': 'Rune',
              'VoltRangerSeekingArrows': 'Seeking Arrows', 'VoltRangerStasisPotion': 'Stasis Potion',
              'VoltRangerVitalityPotion': 'Vitality Potion', 'WarScarabAmulet': 'Amulet',
              'WarScarabChameleonPotion': 'Chameleon Potion', 'WarScarabCircleOfThorns': 'Circle Of Thorns',
              'WarScarabDawnHammer': 'Dawn Hammer', 'WarScarabFuryPotion': 'Fury Potion',
              'WarScarabIronskinPotion': 'Ironskin Potion', 'WarScarabPlating': 'Plating',
              'WarScarabQuicksilverPotion': 'Quicksilver Potion', 'WarScarabStasisPotion': 'Stasis Potion',
              'WarScarabVitalityPotion': 'Vitality Potion', 'Wheat': 'Wheat', 'YellowPowder': 'Yellow Powder',
              'collect_information_on_the_waste': 'Collect Information on the Waste',
              'consult_the_ancients': 'Consult the Ancients', 'defeat_a_challenger': 'Defeat a Challenger',
              'defeat_the_boss': 'Defeat Thanatos', 'defend_the_villagers': 'Defend the Villagers',
              'escort_cassandra_into_the_waste': 'Escort Cassandra into the Waste', 'find_cassandra': 'Find Cassandra',
              'harvest_in_atlantis': 'Reap What Has Been Sown',
              'house_of_the_rising_sun': 'Discover the House of the Rising Sun',
              'investigate_the_sky_temples': 'Investigate the Sky Temples', 'keeping_the_peace': 'Keeping the Peace',
              'mountain_of_treasures': 'Mountain of Treasures', 'protect_dragon_eggs': 'Protect Dragon Eggs',
              'purple_powder': 'Venture into the Moral Mire', 'scouting_the_anthropus': 'Scouting the Anthropus',
              'seek_the_millennium_seed': 'Seek the Millennium Seed', 'searchtheshadows': 'Search the Shadows',
              'the_lost_cult_of_aphrodite': 'Find the Lost Cult of Aphrodite',
              'train_newly_hatched_dragons': 'Train Newly Hatched Dragons',
              'CapitalAdventurer': 'Tyche', 'WaterOutpostAdventurer': 'Nereus', 'WindAdventurer': 'Galia'}

speed_items_dict = [{'item': 'Blitz', 'exceed': 216000, 'time': 345600},
                    {'item': 'Blast', 'exceed': 86400, 'time': 216000},
                    {'item': 'Bolt', 'exceed': 54000, 'time': 86400},
                    {'item': 'Bore', 'exceed': 28800, 'time': 54000},
                    {'item': 'Bounce', 'exceed': 9000, 'time': 28800},
                    {'item': 'Leap', 'exceed': 3600, 'time': 9000},
                    {'item': 'Jump', 'exceed': 900, 'time': 3600},
                    {'item': 'Skip', 'exceed': 300, 'time': 900},
                    {'item': 'Hop', 'exceed': 60, 'time': 300},
                    {'item': 'Blink', 'exceed': 0, 'time': 60}]

building_dict = {'capital': {'buildings': {'Farm', 'Lumbermill', 'Mine', 'Quarry', 'ScienceCenter', 'Home', 'Rookery',
                                           'DragonKeep', 'Fortress', 'Garrison', 'OfficerQuarter', 'StorageVault',
                                           'Metalsmith', 'MusterPoint', 'Wall', 'Sentinel', 'Theater', 'Factory'},
                             'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 32, 9: 35, 10: 38, 11: 39},
                             'c_slots': {1: 28, 2: 28, 3: 28, 4: 28, 5: 28, 6: 28, 7: 28, 8: 28, 9: 28, 10: 28,
                                         11: 29}},
                 'cave': {'buildings': {'CaveDragonKeep', 'CaveCathedral', 'CaveDepot', 'CaveForge', 'CaveGreenhouse',
                                        'CaveLibrary', 'CaveTrainingCamp', 'CaveWorkshop'},
                          'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                          'c_slots': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8}},
                 'chrono': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                          'Farm', 'Mine', 'Home', 'Silo'},
                            'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                        12: 30},
                            'c_slots': {1: 29, 2: 29, 3: 29, 4: 29, 5: 29, 6: 29, 7: 29, 8: 29, 9: 29, 10: 29, 11: 29,
                                        12: 29}},
                 'colossus': {'buildings': {'ColossusDragonKeep', 'ColossusWall', 'Warehouse', 'TroopQuarters',
                                            'WarpGate', 'WarpPortal'},
                              'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                              'c_slots': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10,
                                          12: 10}},
                 'desert': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                          'Farm', 'Mine', 'Home', 'Silo'},
                            'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                        12: 30},
                            'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                        12: 31}},
                 'fire': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                        'Farm', 'Mine', 'Home', 'Silo'},
                          'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                      12: 30},
                          'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                      12: 31}},
                 'forest': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                          'Farm', 'Mine', 'Home', 'Silo'},
                            'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                        12: 30},
                            'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                        12: 31}},
                 'ice': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                       'Farm', 'Mine', 'Home', 'Silo'},
                         'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                     12: 30},
                         'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                     12: 31}},
                 'leviathan': {'buildings': {'LeviathanDragonKeep', 'LeviathanWall', 'LeviathanWarehouse',
                                             'LeviathanMarketplace', 'LeviathanTroopQuarters'},
                               'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                               'c_slots': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10,
                                           11: 10, 12: 10}},
                 'luna': {'buildings': {'DragonKeep', 'LunaShrine', 'LunaDepot', 'LunaCathedral', 'LunaForge',
                                        'LunaGreenhouse', 'LunaLibrary', 'LunaWorkshop'},
                          'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                          'c_slots': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8}},
                 'skythrone': {
                     'buildings': {'Forge', 'Workshop', 'Cathedral', 'Greenhouse', 'Library', 'KaiserDragonKeep'},
                     'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                     'c_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}},
                 'spectral': {'buildings': {'SpectralDragonKeep', 'DarkPortal', 'Mausoleum', 'EnergyCollector'},
                              'f_slots': {1: 2, 2: 2, 3: 2, 4: 4, 5: 6, 6: 8, 7: 11, 8: 14, 9: 17, 10: 20, 11: 20,
                                          12: 20},
                              'c_slots': {1: 2, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 14, 8: 18, 9: 22, 10: 26, 11: 26,
                                          12: 26}},
                 'stone': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                         'Farm', 'Mine', 'Home', 'Silo'},
                           'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                       12: 30},
                           'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                       12: 31}},
                 'swamp': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                         'Farm', 'Mine', 'Home', 'Silo'},
                           'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                       12: 30},
                           'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                       12: 31}},
                 'water': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                         'Farm', 'Mine', 'Home', 'Silo'},
                           'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                       12: 30},
                           'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                       12: 31}},
                 'wind': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                        'Farm', 'Mine', 'Home', 'Silo'},
                          'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                      12: 30},
                          'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                      12: 31}}}


# -------------------------------------------------------------------------------------------------------------------- #
#                                              FUNCTIONAL CLASSES/MODULES                                              #
# -------------------------------------------------------------------------------------------------------------------- #
def div_line(default='_', suffix=True):
    print(' ' + (default * 78))
    if suffix:
        print(' ')


def screen_update(title, subtitle):
    os.system('cls' if os.name == 'nt' else 'clear')
    v_len = len(__version__)
    try:
        a = '{0}({1})'.format(pData['name'], d_rn) if d_rn != 0 else ''
    except (KeyError, NameError):
        a = ''
    print('\n {0:<55}  {1:>21}\n     {2:<{3}}{4}'.format(title, a, subtitle, 74 - v_len, __version__))
    div_line()


def web_ops(conn, operation, param_add_on, method='POST', post=True):
    global realm, std_param, cookie
    url = 'http://{0}/api/{1}.json'.format(realm, operation)
    params = param_add_on + '{0}&timestamp={1}'.format(std_param, int(time()))
    if not post:
        conn.request(method, url + params)
    else:
        cmd = 'Draoumculiasis' + params + 'LandCrocodile' + url + 'Bevar-Asp'
        # cmd_str = sha1(cmd.encode('utf-8')).hexdigest()
        headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive', 'Content-Length': len(params), 'Origin': 'http://' + realm,
                   'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie, 'DNT': 1, 'Host': realm,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like'
                                 ' Gecko Chrome/45.0.2454.101 Safari/537.36)',
                   'X-Requested-With': 'ShockwaveFlash/19.0.0.226', 'X-S3-AWS': sha1(cmd.encode('utf-8')).hexdigest()}
        conn.request(method, url, params, headers)
    try:
        conn_resp = conn.getresponse()
        if conn_resp.status == 200:
            conn_json = conn_resp.read().decode('utf-8')
            return json.loads(conn_json)
        elif conn_resp.status == 429:
            conn.close()
            for ban_countdown in range(3660):
                screen_update('TOO MANY REQUESTS ERROR', 'Your Recent Activities Has Triggered A Temporary Ban')
                progress(ban_countdown, 3660, 'Ban duration left {0}'.format(cvt_time(3660 - ban_countdown)))
                sleep(1)
            conn.connect()
        elif conn_resp.status == 509:
            conn.close()
            for ban_countdown in range(60):
                screen_update('TOO MANY REQUESTS ERROR', 'Your Recent Activities Has Triggered A Warning')
                progress(ban_countdown, 60, 'Script paused for {0}'.format(cvt_time(60 - ban_countdown)))
                sleep(1)
            conn.connect()
        elif conn_resp.status == 502:
            sleep(5)
        else:
            div_line('#')
            ctr_it('SERVER ERROR: Error Code {0} Returned By The Server'.format(conn_resp.status))
            ctr_it('Please try again later...')
            os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
            quit()
    except http.client.HTTPException:
        sleep(2)
    except http.client.CannotSendRequest:
        div_line('#')
        ctr_it('SERVER ERROR: HTTP Connection Failed!')
        ctr_it('Please reload script and try again...')
        os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
        quit()


def progress(p_count, p_total, prefix, suffix=None):
    filled_len = int(round(50 * p_count / float(p_total)))
    bar = ('▓' * filled_len) + ('░' * (50 - filled_len))
    print(prefix.center(78))
    print(bar.center(78))
    if suffix:
        print(suffix.center(78))


def get_data(title, data1=False, data2=False, data3=False, data4=False, data5=False, data6=False, unmute=True):
    global pData, mData, fData, pfData, cData, tData
    title_text = 'Refreshing' if pData or mData or fData or pfData or cData or tData else 'Retrieving'
    sub_header = '{0} Game Files. Please Wait...'.format(title_text)
    tw_data = None
    max_count, count = [0, 0]
    for check in (data1, data2, data3, data4, data6):
        if check:
            max_count += 1
    if unmute:
        screen_update(title, sub_header)
        progress(count, max_count, 'Initializing...')

    # Get Manifest and Translation
    d_conn = http.client.HTTPConnection('wackoscripts.com', 80)
    req = [{'0': data1, '1': 'Game Manifest', '2': 'manifest'},
           {'0': data6, '1': 'Chests Matrix', '2': 'chest'}]
    for x in range(len(req)):
        if req[x]['0']:
            name = req[x]['1']
            if unmute:
                screen_update(title, sub_header)
                progress(count, max_count, 'Retrieving {0}'.format(name))
            url = 'http://wackoscripts.com/sanctuary/{0}.json'.format(req[x]['2'])
            for web_retry in range(2):
                try:
                    d_conn.request('GET', url)
                    conn_resp = d_conn.getresponse()
                    conn_data = json.loads(conn_resp.read().decode('utf-8'))
                    if req[x]['2'] == 'manifest':
                        mData = conn_data
                    elif req[x]['2'] == 'chest':
                        tw_data = conn_data
                    break
                except (KeyError, TypeError):
                    if unmute:
                        screen_update(title, sub_header)
                        progress(count, max_count, 'Retrieving {0}'.format(name),
                                 'Retrying {0} of 5'.format(web_retry + 1))
                    sleep(1)
                    continue
            if mData or tw_data:
                count += 1
                if unmute:
                    screen_update(title, sub_header)
                    progress(count, max_count, 'Retrieving {0}'.format(name))
            else:
                div_line('#')
                ctr_it('SERVER ERROR: Failed To Retrieve The {0}'.format(name))
                ctr_it('Please Try Again Later...')
                div_line('#')
                sleep(5)
                quit()
            if req[x]['2'] == 'chest':
                translate = (troop_dict, game_dict, forge_dict, tw_data)
                for lookup in translate:
                    for key, value in lookup.items():
                        if key not in tData and value != '':
                            tData[key] = value
                        if key not in tData and value == '':
                            tData[key] = key
    d_conn.close()

    # Get Forge and Player
    d_conn = http.client.HTTPConnection(realm, 80)
    req = [{'0': data2, '1': 'Forge Manifest', '2': 'forge/forge', '3': '', '4': 'GET', '5': True},
           {'0': data3, '1': 'Player Data', '2': 'player', '3': '?', '4': 'GET', '5': False},
           {'0': data4, '1': 'Forge Data', '2': 'forge/player_forge_info', '3': '', '4': 'GET', '5': True}]
    for x in range(len(req)):
        if req[x]['0']:
            name = req[x]['1']
            if unmute:
                screen_update(title, sub_header)
                progress(count, max_count, 'Retrieving {0}'.format(name))
            for web_retry in range(2):
                try:
                    conn_data = web_ops(d_conn, req[x]['2'], req[x]['3'], req[x]['4'], req[x]['5'])
                    if req[x]['2'] == 'forge/forge':
                        fData = conn_data
                    elif req[x]['2'] == 'player':
                        pData = conn_data
                    elif req[x]['2'] == 'forge/player_forge_info':
                        pfData = conn_data
                    break
                except (KeyError, TypeError):
                    if unmute:
                        screen_update(title, sub_header)
                        progress(count, max_count, 'Retrieving {0}'.format(name),
                                 'Retrying {0} of 5'.format(web_retry + 1))
                    sleep(1)
                    continue
            if mData or tw_data:
                count += 1
                if unmute:
                    screen_update(title, sub_header)
                    progress(count, max_count, 'Retrieving {0}'.format(name))
            else:
                div_line('#')
                ctr_it('SERVER ERROR: Failed To Retrieve The {0}'.format(name))
                ctr_it('Please Try Again Later...')
                div_line('#')
                sleep(5)
                quit()

    # Process City Data
    if data5:
        if unmute:
            screen_update(title, sub_header)
            progress(1, 1, 'Retrieving City/Outpost Data')
        cData = {}
        for loc_key in sorted(pData['cities']):
            current_location = None
            if unmute:
                screen_update(title, sub_header)
                progress(1, 1, 'Processing {0}'.format(t(loc_key)))
            for web_retry in range(5):
                try:
                    current_location = web_ops(d_conn, 'cities/{0}'.format(pData['cities'][loc_key]['id']), '')
                    break
                except (KeyError, TypeError):
                    if unmute:
                        screen_update(title, sub_header)
                        progress(1, 1, 'Processing {0}'.format(t(loc_key)), 'Retrying {0} of 5'.format(web_retry + 1))
                    sleep(1)
                    continue
            if current_location:
                cData[loc_key] = current_location
        if not cData:
            div_line('#')
            ctr_it('SERVER ERROR: Failed To Process City/Outpost Data')
            ctr_it('Please Try Again Later...')
            div_line('#')
            quit()

    # Save Entry If Loading Went Well...
    acct = list()
    verify_record = list()
    unique_id = '{0}-{1}'.format(d_ui, d_rn)
    try:
        with open('DoA-Tools.txt', 'r') as read_file:
            r_file = json.load(read_file)
            for x in range(len(r_file)):
                acct.append(r_file[x])
                if r_file[x]['id'] not in verify_record:
                    verify_record.append(r_file[x]['id'])
            if unique_id not in verify_record:
                my_dict = {'id': unique_id, 'ac': pData['name'], 'ui': d_ui, 'dh': d_dh,
                           'rn': d_rn, 'cn': d_cn}
                acct.append(my_dict)
    except FileNotFoundError:
        my_dict = {'id': unique_id, 'ac': pData['name'], 'ui': d_ui, 'dh': d_dh,
                   'rn': d_rn, 'cn': d_cn}
        acct.append(my_dict)
    finally:
        with open('DoA-Tools.txt', 'w') as create_file:
            json.dump(acct, create_file)


def cvt_time(time_value=0, show_seconds=True):
    m, s = divmod(time_value, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if show_seconds:
        if d > 0:
            return '{0:,}d {1:0>2}h {2:0>2}m {3:0>2}s'.format(int(d), int(h), int(m), int(s))
        elif h > 0:
            return '{0}h {1:0>2}m {2:0>2}s'.format(int(h), int(m), int(s))
        elif m > 0:
            return '{0}m {1:0>2}s'.format(int(m), int(s))
        else:
            return '{0}s'.format(int(s))
    else:
        if d > 0:
            return '{0:,}d {1:0>2}h {2:0>2}m'.format(int(d), int(h), int(m))
        elif h > 0:
            return '{0}h {1:0>2}m'.format(int(h), int(m))
        else:
            return '{0}m'.format(int(m))


def ctr_it(string, prefix=False, suffix=False):
    if prefix:
        print('')
    print(string.center(78))
    if suffix:
        print('')


def t(string):
    if string in tData.keys():
        return tData[string]
    else:
        return string


def display_it(my_list, single=True):
    if single:
        max_len = len(max(my_list.values(), key=len))
        max_items = int(76 / (max_len + 2)) if max_len <= 34 else 1
        if len(my_list) < max_items:
            max_items = len(my_list)
        x = ''
        y = 0
        for value in sorted(my_list.values()):
            x += ' {0:{1}} '.format(value, max_len)
            if y == max_items - 1:
                ctr_it(x)
                y = 0
                x = ''
            else:
                y += 1
        if y != 0:
            z = ' ' * ((max_len + 2) * (max_items - y))
            x += z
            ctr_it(x)
    else:
        max_len_key = max_len_value = 0
        for key, value in my_list.items():
            if len(key) > max_len_key:
                max_len_key = len(key)
            if len(str(value)) > max_len_value:
                max_len_value = len(str(value))
        max_len = max_len_key + max_len_value
        max_items = int(76 / (max_len + 4)) if max_len <= 32 else 1
        if len(my_list) < max_items:
            max_items = len(my_list)
        x = ''
        y = 0
        for key, value in sorted(my_list.items()):
            txt = '{0:>{1}}: {2:<{3}}'.format(key, max_len_key, value, max_len_value)
            x += ' {0:<{1}} '.format(txt, max_len)
            if y == max_items - 1:
                ctr_it(x)
                y = 0
                x = ''
            else:
                y += 1
        if y != 0:
            z = ' ' * ((max_len + 4) * (max_items - y))
            x += z
            ctr_it(x)


def set_batch(max_value=0, exec_string=''):
    div_line('-')
    ctr_it('~~~ Available Options ~~~')
    ctr_it('1 to {0}'.format(max_value - 1), suffix=True)
    ctr_it('How many {0}?'.format(exec_string))
    div_line()
    i = input(' Enter selection : ')
    if len(i) >= 1:
        if i.lower() == 'exit':
            return 'exit'
        if i.isnumeric():
            if int(i) in range(1, max_value):
                return int(i)


def set_delay():
    div_line('-')
    ctr_it('~~~ Available Options ~~~')
    ctr_it('0 to 5', suffix=True)
    ctr_it('Each request made to the server increases your chances of a 1 hour')
    ctr_it('ban. The delay feature minimizes your chances of triggering it.\n')
    ctr_it('What delay would you like to set for this run?')
    div_line()
    i = input(' Enter selection : ')
    if len(i) >= 1:
        if i.lower() == 'exit':
            return 'exit'
        if i.isnumeric():
            if int(i) in range(6):
                return int(i)


def proceed_run(exec_string):
    div_line('-')
    ctr_it('~~~ Available Options ~~~')
    ctr_it('Yes   No', suffix=True)
    ctr_it('Proceed with {0}?'.format(exec_string))
    div_line()
    i = input(' Enter selection : ')
    if len(i) >= 1:
        if i.isalpha():
            if i.lower() in 'yes':
                return True
            elif i.lower() in 'no':
                return 'exit'


def nothing_to_do(title, subtitle, text):
    screen_update(title, subtitle)
    div_line('*')
    ctr_it('There Are No {0} Available For Now'.format(text), suffix=True)
    div_line('*')
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')


def result_error(text):
    div_line('#')
    ctr_it('SERVER ERROR')
    ctr_it(text)
    div_line('#')
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    quit()


def smart_truncate(content, length=100, suffix='..'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix


def exit_script():
    os.system('cls' if os.name == 'nt' else 'clear')
    ctr_it('Thank you for using DoA Tools ({0})'.format(__version__), prefix=True, suffix=True)
    ctr_it('Brought to you by')
    ctr_it(__author__)
    ctr_it('With thanks to {0}'.format(__credits__), suffix=True)
    ctr_it('Join us at the sanctuary')
    ctr_it(__maintainer__)
    sleep(3)
    quit()


def enter_script(title):
    global d_ui, d_dh, d_rn, d_cn, pData, mData, fData, pfData, cData, tData
    pData = mData = fData = pfData = cData = tData = {}
    d_ui = d_dh = d_rn = d_cn = 0
    selection = {}
    r_file = None
    try:
        with open('DoA-Tools.txt', 'r') as read_file:
            r_file = json.load(read_file)
            for x in range(len(r_file)):
                selection[r_file[x]['id']] = '{0}({1})'.format(r_file[x]['ac'], r_file[x]['rn'])
    except FileNotFoundError:
        pass
    if selection:
        selected = False
        while not selected:
            screen_update(title, 'Select Game Account')
            ctr_it('~~~ Saved Accounts ~~~', suffix=True)
            display_it(selection)
            print('\n\n NOTE: Enter NEW for a new account entry')
            div_line()
            i = input(' Enter selection : ')
            if len(i) >= 1:
                if i.lower() in 'new':
                    break
                for key, value in selection.items():
                    if i.lower() in value.lower() or i.lower() == value.lower():
                        for x in range(len(r_file)):
                            if r_file[x]['id'] == key:
                                d_ui = r_file[x]['ui']
                                d_dh = r_file[x]['dh']
                                d_rn = r_file[x]['rn']
                                d_cn = r_file[x]['cn']
                                selected = True
                                break
                        break
    get_account_info(title)
    get_realm_info(title)
    switch_realm(title, d_rn, d_cn)


# -------------------------------------------------------------------------------------------------------------------- #
#                                             INTERACTIVE CLASSES/MODULES                                              #
# -------------------------------------------------------------------------------------------------------------------- #
def get_account_info(title):
    global d_ui, d_dh, d_si
    while not d_ui:
        screen_update(title, 'Fill In The Relevant Account Information To Proceed')
        d_select = input(' Enter your USER ID number : ')
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_ui = int(d_select)

    while not d_dh:
        screen_update(title, 'Fill In The Relevant Account Information To Proceed')
        ctr_it('User ID: {0}'.format(d_ui))
        div_line()
        d_select = input(' Enter your DRAGON HEART code : ')
        if len(d_select) >= 3:
            if d_select.isalnum():
                d_dh = d_select


def get_realm_info(title):
    global d_rn, d_cn
    while not d_rn:
        screen_update(title, 'Fill In The Relevant Realm Information To Proceed')
        ctr_it('User ID: {0}   Dragon Heart: {1}'.format(d_ui, d_dh))
        ctr_it(' ')
        div_line()
        d_select = input(' Enter the REALM number : ')
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_rn = int(d_select)

    while not d_cn:
        screen_update(title, 'Fill In The Relevant Realm Information To Proceed')
        ctr_it('User ID: {0}   Dragon Heart: {1}'.format(d_ui, d_dh))
        ctr_it('Realm Number: {0}'.format(d_rn))
        div_line()
        d_select = input(' Enter the Cluster Server number (known as C number) : ')
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_cn = int(d_select)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      FORGE CLASS                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def create_equipment(title):
    # Initialize Craftable Equipment
    screen_update(title, 'Create Troop Equipment')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    x = 0
    d_blacksmith = pfData['result']['blacksmith']['level']
    for key in fData['forge']['items'].keys():
        if fData['forge']['items'][key]['troop_slot_number'] in (1, 2):
            try:
                bs_level = fData['forge']['recipes'][key]['requirements']['blacksmith_level']
            except KeyError:
                continue
            if d_blacksmith >= bs_level:
                try:
                    ingredients = pData['forge']['items']['ingredients']
                    recipe = fData['forge']['recipes'][key]['requirements']
                except KeyError:
                    continue
                d_max_queue = 9999
                y = (len(recipe['items']))
                for r_key, r_value in recipe['items'].items():
                    for r_item in range(len(ingredients)):
                        if r_key == ingredients[r_item]['name']:
                            if r_value < ingredients[r_item]['quantity']:
                                y -= 1
                                if d_max_queue > int(ingredients[r_item]['quantity'] / r_value):
                                    d_max_queue = int(ingredients[r_item]['quantity'] / r_value)
                            else:
                                break
                if y == 0:
                    my_dict = {'troop': fData['forge']['items'][key]['troop_type'],
                               'item': key, 'craftable': d_max_queue,
                               'tier': fData['forge']['items'][key]['tier_value']}
                    d_list.insert(x, my_dict)
    if not d_list:
        nothing_to_do(title, 'Create Troop Equipment', 'Craftable Troop Items')
        return
    else:
        for x in range(len(d_list)):
            if d_list[x]['troop'] not in selection.keys():
                selection[d_list[x]['troop']] = t(d_list[x]['troop'])

    # Select Troop For Equipment Crafting
    d_troop = None
    while d_troop is None:
        screen_update(title, 'Create Troop Equipment')
        ctr_it('~~~ Available Troops ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            d_troop = key
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    selection.clear()
    for x in range(len(d_list)):
        if d_list[x]['item'] not in selection.keys():
            selection[d_list[x]['item']] = '{0}: {1:,}'.format(t(d_list[x]['item']), d_list[x]['craftable'])

    # Select Equipment To Craft
    d_item = None
    while d_item is None:
        screen_update(title, 'Select Troop Equipment')
        ctr_it('Troop: {0}'.format(t(d_troop)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Equipment ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            d_item = key
    d_list[:] = [d for d in d_list if d.get('item') == d_item]

    # Set Minimum Equipment Stat
    d_attrib = None
    selection = {'defense': 'Defense', 'life': 'Life', 'melee': 'Melee', 'range': 'Range', 'ranged': 'Ranged',
                 'speed': 'Speed'}
    while d_attrib is None:
        screen_update(title, 'Select Troop Attribute')
        ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Attributes ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() == value.lower():
                            d_attrib = key

    d_stat = None
    while d_stat is None:
        screen_update(title, 'Set Minimum Value')
        ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
        ctr_it('Requirement: {0}'.format(d_attrib.title()))
        div_line('-')
        ctr_it('Items crafted by the script will be auto crushed')
        ctr_it('if it does not meet the minimum requirement set.\n')
        ctr_it('What would you like to set it to?')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 1:
            if d_select.lower() == 'exit':
                return
            if d_select.isnumeric():
                if int(d_select) in range(1, 10000):
                    d_stat = int(d_select)

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, 'Number Of Equipment To Forge')
        ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
        ctr_it('Requirement: {0:,} {1}'.format(d_stat, d_attrib.title()))
        d_batch = set_batch(d_list[0]['craftable'] + 1, 'equipment would you like to craft')
        if d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Equipment Crafting')
        ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
        ctr_it('Requirement: {0:,} {1}   Crafting: {2:,}'.format(
                d_stat, d_attrib.title(), d_batch))
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed Forging
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Ready To Begin Crafting')
        ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
        ctr_it('Requirement: {0:,} {1}   Crafting: {2:,}   Delay: {3}s'.format(
                d_stat, d_attrib.title(), d_batch, d_delay))
        d_proceed = proceed_run('equipment crafting')
        if d_proceed == 'exit':
            return

    # Forge Equipment
    d_start = time()
    forge_succ = 0
    forge_fail = 0
    len_item = 0
    kept_items = list()
    crushed_items = {}
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(1, d_batch + 1):
        screen_update(title, 'Progress Report...')
        ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
        ctr_it('Requirement: {0:,} {1}   Crafting: {2:,}   Delay: {3}s   Elapsed Time: {4}'.format(
                d_stat, d_attrib.title(), d_batch, d_delay, cvt_time(time() - d_start)))
        div_line('-')
        progress(x, d_batch, 'Crafting {0} Of {1}'.format(x, d_batch),
                 'Success: {0:,}  Failed: {1:,}  Kept: {2:,}  Crushed: {3:,}\n'.format(
                         forge_succ, forge_fail, len(kept_items), forge_succ - len(kept_items)))
        if kept_items:
            ctr_it('~~~ Kept Items ~~~')
            for y in range(len(kept_items)):
                k_item = 'Item {0}: '.format(y + 1) + ', '.join('{0} {1}'.format(
                        k_i.title(), v_i) for k_i, v_i in kept_items[y].items())
                if len(k_item) > len_item:
                    len_item = len(k_item)
                ctr_it('{0:<{1}}'.format(k_item, len_item))
            print(' ')
        if crushed_items:
            ctr_it('~~~ Crushed Items Received ~~~')
            display_it(crushed_items, single=False)
        crush_it = False
        x_param = 'output%5Fname={0}&'.format(d_item)
        for web_retry in range(5):
            sleep(d_delay)
            try:
                main_json = web_ops(d_conn, 'forge/forge_item', x_param)
                result = main_json['result']['success']
                if result:
                    forge_equip = main_json['result']['forge_result']
                    if forge_equip != 'failure':
                        forge_succ += 1
                        if d_attrib in forge_equip['stats'].keys() and d_stat <= forge_equip['stats'][d_attrib]:
                            kept_items.append(forge_equip['stats'])
                        else:
                            x_param = 'player%5Fforge%5Fequipment%5Fid={0}&'.format(forge_equip['id'])
                            crush_it = True
                    else:
                        forge_fail += 1
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
        if crush_it:
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    crush_json = web_ops(d_conn, 'forge/disenchant_equipment', x_param)
                    result = crush_json['result']['success']
                    if result:
                        for y in range(len(crush_json['result']['disenchanted_ingredients'])):
                            if t(crush_json['result']['disenchanted_ingredients'][y]) in crushed_items:
                                crushed_items[t(crush_json['result']['disenchanted_ingredients'][y])] += 1
                            else:
                                crushed_items[t(crush_json['result']['disenchanted_ingredients'][y])] = 1
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
    screen_update(title, 'Summary Report')
    ctr_it('Troop: {0}   Type: {1}'.format(t(d_troop), t(d_item)))
    ctr_it('Requirement: {0:,} {1}   Crafted: {2:,}   Delay: {3}s'.format(d_stat, d_attrib.title(), d_batch, d_delay))
    div_line('-')
    progress(1, 1, 'Process Completed In {0}'.format(cvt_time(time() - d_start)),
             'Success: {0:,}  Failed: {1:,}  Kept: {2:,}  Crushed: {3:,}'.format(
                     forge_succ, forge_fail, len(kept_items), forge_succ - len(kept_items)))
    if kept_items:
        ctr_it('~~~ Kept Items ~~~', prefix=True)
        for y in range(len(kept_items)):
            k_item = 'Item {0}: '.format(y + 1) + ', '.join('{0} {1}'.format(
                    k_i.title(), v_i) for k_i, v_i in kept_items[y].items())
            ctr_it('{0:<{1}}'.format(k_item, len_item))
    if crushed_items:
        ctr_it('~~~ Crushed Items Received ~~~', prefix=True)
        display_it(crushed_items, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, data4=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def forge_ingredient(title):
    # Initialize Craftable Ingredient
    screen_update(title, 'Create Forge Ingredient')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    d_blacksmith = pfData['result']['blacksmith']['level']
    x = 0
    for forge_key in reversed(sorted(fData['forge']['items'].keys())):
        if fData['forge']['items'][forge_key]['type'] == 'ingredient':
            try:
                bs_level = fData['forge']['recipes'][forge_key]['requirements']['blacksmith_level']
            except KeyError:
                continue
            if d_blacksmith >= bs_level:
                try:
                    ingredients = pData['forge']['items']['ingredients']
                    recipe = fData['forge']['recipes'][forge_key]['requirements']
                except KeyError:
                    continue
                d_max_queue = 1024
                for r_item in range(len(ingredients)):
                    if forge_key == ingredients[r_item]['name']:
                        d_max_queue = 1024 - ingredients[r_item]['quantity']
                if d_max_queue != 0:
                    count = (len(recipe['items']))
                    for r_key, r_qty in recipe['items'].items():
                        for r_item in range(len(ingredients)):
                            if r_key == ingredients[r_item]['name']:
                                if r_qty < ingredients[r_item]['quantity']:
                                    count -= 1
                                    if d_max_queue > int(ingredients[r_item]['quantity'] / r_qty):
                                        d_max_queue = int(ingredients[r_item]['quantity'] / r_qty)
                                else:
                                    break
                    if count == 0:
                        my_dict = {'item': forge_key,
                                   'craftable': d_max_queue}
                        d_list.insert(x, my_dict)

    if not d_list:
        nothing_to_do(title, 'Create Forge Ingredient', 'Forgeable Ingrediants')
        return
    else:
        for x in range(len(d_list)):
            if t(d_list[x]['item']) not in selection.keys():
                selection[t(d_list[x]['item'])] = d_list[x]['craftable']

    # Select Ingredient for Crafting
    d_item = None
    while d_item is None:
        screen_update(title, 'Create Forge Ingredient')
        ctr_it('~~~ Available Ingredients ~~~')
        display_it(selection, single=False)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() in t(d_list[x]['item']).lower() or \
                                        d_select.lower() == t(d_list[x]['item']).lower():
                            d_item = d_list[x]['item']
    d_list[:] = [d for d in d_list if d.get('item') == d_item]

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, 'Number Of Ingredient To Forge')
        ctr_it('Ingredient: {0}'.format(t(d_item)))
        ctr_it(' ')
        d_batch = set_batch(d_list[0]['craftable'] + 1, 'ingredients would you like to forge')
        if d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Ingredient Crafting')
        ctr_it('Ingredient: {0}   Crafting: {1:,}'.format(t(d_item), d_batch))
        ctr_it(' ')
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed Forging
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Proceed With Ingredient Forging?')
        ctr_it('Ingredient: {0}   Crafting: {1:,}'.format(t(d_item), d_batch))
        ctr_it('Delay: {0}s'.format(d_delay))
        d_proceed = proceed_run('ingredient forging')
        if d_proceed == 'exit':
            return

    # Forge Ingredients
    selection.clear()
    base_list = {}
    d_start = time()
    for x in range(len(pData['forge']['items']['ingredients'])):
        if t(pData['forge']['items']['ingredients'][x]['name']) not in base_list:
            base_list[t(pData['forge']['items']['ingredients'][x]['name'])] = pData[
                'forge']['items']['ingredients'][x]['quantity']
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(1, d_batch + 1):
        screen_update(title, 'Progress Report...')
        ctr_it('Ingredient: {0}   Crafting: {1:,}'.format(t(d_item), d_batch))
        ctr_it('Delay: {0}s   Elapsed Time: {1}'.format(
                d_delay, cvt_time(time() - d_start)))
        div_line('-')
        progress(x, d_batch, 'Forging {0} of {1}'.format(x, d_batch), ' ')
        if selection:
            ctr_it('~~~ Items Used ~~~')
            display_it(selection, single=False)
        for web_retry in range(5):
            sleep(d_delay)
            try:
                x_param = 'output%5Fname={0}&'.format(d_item)
                main_json = web_ops(d_conn, 'forge/forge_item', x_param)
                result = main_json['result']['success']
                if result:
                    check_use = main_json['result']['forge_items']['ingredients']
                    for y in range(len(check_use)):
                        item_name = t(check_use[y]['name'])
                        if item_name in base_list.keys() and check_use[y]['quantity'] < base_list[item_name]:
                            selection[item_name] = base_list[item_name] - check_use[y]['quantity']
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
    screen_update(title, 'Summary Report')
    ctr_it('Ingredient: {0}   Crafted: {1:,}'.format(t(d_item), d_batch))
    ctr_it('Delay: {0}s'.format(d_delay))
    div_line('-')
    progress(1, 1, 'Forging Ingredients Completed!', 'Process completed in {0}'.format(
            cvt_time(time() - d_start)))
    if selection:
        ctr_it('~~~ Items Used ~~~', prefix=True)
        display_it(selection, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, data4=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def farm_mission(title):
    # Initialize Player Missions
    screen_update(title, 'Select Adventurer For Mission')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    adventurers = pData['forge']['adventurers']
    missions = fData['forge']['missions']
    claimed = False
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(len(adventurers)):
        if adventurers[x]['current_mission'] is not None:
            x_param = 'adventurer_id={0}&mission_type={1}&'.format(
                    adventurers[x]['adventurer_id'], adventurers[x]['current_mission'])
            item_json = web_ops(d_conn, 'player_missions/claim_mission', x_param)
            if item_json['result']['success']:
                claimed = True
            else:
                selection[adventurers[x]['current_mission']] = adventurers[x]['current_mission']
    d_conn.close()
    if claimed:
        get_data(title, data3=True, unmute=False)
        adventurers = pData['forge']['adventurers']
    ingredients = {}
    for x in range(len(pData['forge']['items']['ingredients'])):
        ingredients[pData['forge']['items']['ingredients'][x]['name']] = pData['forge']['items']['ingredients'][x][
            'quantity']
    for x in range(len(adventurers)):
        if adventurers[x]['current_mission'] is None:
            d_level = 0
            for key, value in reversed(
                    sorted(fData['forge']['adventurers'][adventurers[x]['type']]['level_exp'].items())):
                if adventurers[x]['experience'] >= value:
                    d_level = int(key) + 1
                    break
            for mission in sorted(missions.keys()):
                checked = False
                d_max_queue = 9999999
                if mission in selection.keys():
                    continue
                if d_level < missions[mission]['requirements']['adventurer_level']:
                    continue
                if missions[mission]['ends_at'] != 0 and missions[mission]['ends_at'] < time():
                    continue
                if 'any' not in missions[mission]['adventurers'][0] and adventurers[x]['type'] not in \
                        missions[mission]['adventurers'][0]:
                    continue
                if len(missions[mission]['requirements']['items']) > 0:
                    for r_key, r_value in (missions[mission]['requirements']['items']).items():
                        if r_key not in ingredients.keys():
                            break
                        else:
                            if r_value > ingredients[r_key]:
                                break
                            else:
                                checked = True
                                if int(ingredients[r_key] / r_value) < d_max_queue:
                                    d_max_queue = int(ingredients[r_key] / r_value)
                else:
                    checked = True
                if checked:
                    my_dict = {'adventurer': adventurers[x]['type'],
                               'id': adventurers[x]['adventurer_id'],
                               'mission': mission,
                               'time': missions[mission]['cooldown'],
                               'batch': d_max_queue}
                    d_list.append(my_dict)

    if not d_list:
        nothing_to_do(title, 'Select Adventurer For Mission', 'Adventurers')
        return
    else:
        selection.clear()
        for x in range(len(d_list)):
            if t(d_list[x]['mission']) not in selection.keys():
                if d_list[x]['batch'] == 9999999:
                    selection[t(d_list[x]['mission'])] = '*'
                else:
                    selection[t(d_list[x]['mission'])] = d_list[x]['batch']

    # Select Mission
    d_mission = None
    while d_mission is None:
        screen_update(title, 'Select A Mission To Farm')
        ctr_it('~~~ Available Missions ~~~')
        display_it(selection, single=False)
        print('\n * - No limit')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() in t(d_list[x]['mission']).lower() or \
                                        d_select.lower() == t(d_list[x]['mission']).lower():
                            d_mission = d_list[x]['mission']
    d_list[:] = [d for d in d_list if d.get('mission') == d_mission]
    selection.clear()
    for x in range(len(d_list)):
        if d_list[x]['adventurer'] not in selection.keys():
            selection[d_list[x]['adventurer']] = t(d_list[x]['adventurer'])

    # Select Adventurer
    d_adventurer = None
    while d_adventurer is None:
        screen_update(title, 'Select An Adventurer To Farm The Mission')
        ctr_it('Mission: {0} ({1})'.format(t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Adventurers ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            d_adventurer = key
    d_list[:] = [d for d in d_list if d.get('adventurer') == d_adventurer]

    # Select Speed Items
    selection = list()
    a, b, c, d, len_a, len_b, len_c, len_d = ['Item', 'Description', 'Available', 'Exceeding', 4, 11, 9, 9]
    for key in range(len(speed_items_dict)):
        look_up = speed_items_dict[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['item']) > len_a:
                len_a = len(look_up['item'])
            if len(cvt_time(look_up['time'], show_seconds=False)) > len_b:
                len_b = len(cvt_time(look_up['time'], show_seconds=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > len_c:
                len_c = len('{0:,}'.format(pData['items'][look_up['item']]))
            if len(cvt_time(look_up['exceed'], show_seconds=False)) > len_d:
                len_d = len(cvt_time(look_up['exceed'], show_seconds=False))
            my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                       'quantity': pData['items'][look_up['item']], 'use': False}
            selection.append(my_dict)
    if selection:
        while True:
            screen_update('FILL SLOTS', 'Select Speed Items To Use')
            ctr_it('Mission: {0} ({1})   Adventurer: {2}'.format(t(d_mission), cvt_time(
                    d_list[0]['time'], show_seconds=False), t(d_adventurer)))
            ctr_it(' ')
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  Use'.format(a, len_a, b, len_b, c, len_c, d, len_d))
            ctr_it('{0}  {1}  {2}  {3}  ~~~'.format('~' * len_a, '~' * len_b, '~' * len_c, '~' * len_d))
            for key in range(len(selection)):
                use_item = 'Yes' if selection[key]['use'] is True else 'No'
                ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>3}'.format(
                        selection[key]['item'], len_a, cvt_time(selection[key]['time'], show_seconds=False), len_b,
                        selection[key]['quantity'], len_c, cvt_time(selection[key]['exceed'], show_seconds=False),
                        len_d, use_item))
            print('\n Exceeding - Item used when duration exceeds the displayed time')
            div_line('-')
            print(' Selection options available:')
            print(' ALL = Enable all, NONE = Disable all, Item Name = Enable/Disable selected')
            print(' NEXT = Accept list and proceed to the next screen, EXIT = Return to main menu')
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 2:
                if d_select.lower() == 'exit':
                    return
                elif d_select.lower() == 'next':
                    break
                elif d_select.lower() == 'all':
                    for key in range(len(selection)):
                        selection[key]['use'] = True
                elif d_select.lower() == 'none':
                    for key in range(len(selection)):
                        selection[key]['use'] = False
                else:
                    for key in range(len(selection)):
                        if d_select.lower() in selection[key]['item'].lower():
                            selection[key]['use'] = True if selection[key]['use'] is False else False
    d_speed = list()
    speeds_selected = ''
    count = 0
    for x in range(len(selection)):
        if selection[x]['use'] is True:
            d_speed.append(selection[x])
            speeds_selected += ' {0}'.format(selection[x]['item'])
            if selection[x]['time'] >= d_list[0]['time']:
                if d_list[0]['batch'] > selection[x]['quantity']:
                    count += selection[x]['quantity']
                else:
                    count = d_list[0]['batch']
            else:
                count += int((selection[x]['time'] * selection[x]['quantity']) / d_list[0]['time'])
                if count > d_list[0]['batch']:
                    count = d_list[0]['batch']
    if not d_speed:
        count = d_list[0]['batch']

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, 'Number Of Times To Farm Mission')
        ctr_it('Mission: {0} ({1})   Adventurer: {2}'.format(t(d_mission), cvt_time(
                d_list[0]['time'], show_seconds=False), t(d_adventurer)))
        ctr_it(' ')
        if d_speed:
            div_line('-')
            ctr_it('~~~ Speed Items Selected ~~~')
            ctr_it(speeds_selected)
        d_batch = set_batch(count + 1, 'times would you like to farm the mission')
        if d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Farming Missions')
        ctr_it('Mission: {0} ({1})   Adventurer: {2}'.format(t(d_mission), cvt_time(
                d_list[0]['time'], show_seconds=False), t(d_adventurer)))
        ctr_it('Batches: {0:,}'.format(d_batch))
        if d_speed:
            div_line('-')
            ctr_it('~~~ Speed Items Selected ~~~')
            ctr_it(speeds_selected)
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed With Farming
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Proceed With Farming Mission?')
        ctr_it('Mission: {0}   Adventurer: {1}'.format(t(d_mission), t(d_adventurer)))
        ctr_it('Batches: {0:,}   Delay: {1}s'.format(d_batch, d_delay))
        if d_speed:
            div_line('-')
            ctr_it('~~~ Speed Items Selected ~~~')
            ctr_it(speeds_selected)
        d_proceed = proceed_run('farming mission')
        if d_proceed == 'exit':
            return

    # Farm Mission
    d_start = time()
    speeds_used = {}
    items_gained = {}
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(1, d_batch + 1):
        job_id = 0
        duration = -1
        restart_http = False
        while duration != 0:
            screen_update(title, 'Progress Report...')
            ctr_it('Mission: {0}   Adventurer: {1}'.format(t(d_mission), t(d_adventurer)))
            ctr_it('Batches: {0:,}   Delay: {1}s   Elapsed Time: {2}'.format(
                    d_batch, d_delay, cvt_time(time() - d_start)))
            div_line('-')
            if speeds_used:
                progress(x, d_batch, 'Farming {0} of {1}'.format(x, d_batch), ' ')
                ctr_it('~~~ Speed Items Used ~~~')
                display_it(speeds_used, single=False)
                print(' ')
            elif duration == -1:
                progress(x, d_batch, 'Farming {0} of {1}'.format(x, d_batch), 'Initializing...\n')
            else:
                restart_http = True
                progress(x, d_batch, 'Farming {0} of {1}'.format(x, d_batch),
                         'Waiting {0} for job to finish...\n'.format(cvt_time(duration)))
            if items_gained:
                ctr_it('~~~ Items Gained ~~~')
                display_it(items_gained, single=False)
            if duration == -1:
                for web_retry in range(5):
                    sleep(d_delay)
                    x_param = 'adventurer_id={0}&mission_type={1}&'.format(d_list[0]['id'], d_mission)
                    try:
                        main_json = web_ops(d_conn, 'player_missions', x_param)
                        result = main_json['result']['success']
                        if result:
                            duration = d_list[0]['time']
                            job_id = main_json['result']['job']['id']
                            break
                    except (KeyError, TypeError):
                        sleep(1)
                        continue
                    else:
                        sleep(1)
                        continue
            elif duration != 0 and len(d_speed) > 0:
                speed_item = None
                for z in range(len(d_speed)):
                    if duration > d_speed[z]['exceed'] and d_speed[z]['quantity'] != 0:
                        speed_item = d_speed[z]['item']
                        break
                if speed_item is None:
                    if len(d_speed) == 1 and d_speed[0]['quantity'] != 0:
                        speed_item = d_speed[0]['item']
                    else:
                        for z in range(len(d_speed) - 1, -1, -1):
                            if duration <= d_speed[z]['time'] and d_speed[z]['quantity'] != 0:
                                speed_item = d_speed[z]['item']
                                break
                for web_retry in range(5):
                    sleep(d_delay)
                    x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(job_id)
                    try:
                        item_json = web_ops(d_conn, 'player_items/{0}'.format(speed_item), x_param)
                        result = item_json['result']['success']
                        if result:
                            for z in range(len(d_speed)):
                                if speed_item == d_speed[z]['item']:
                                    d_speed[z]['quantity'] -= 1
                            if speed_item in speeds_used:
                                speeds_used[speed_item] += 1
                            else:
                                speeds_used[speed_item] = 1
                            duration = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                            if duration < 1:
                                duration = 0
                            break
                    except (KeyError, TypeError):
                        sleep(1)
                        continue
                    else:
                        sleep(1)
                        continue
            else:
                duration -= 1
                if duration < 1:
                    duration = 0
                sleep(1)
        if restart_http:
            d_conn = http.client.HTTPConnection(realm, 80)
        for web_retry in range(5):
            sleep(d_delay)
            x_param = 'adventurer_id={0}&mission_type={1}&'.format(d_list[0]['id'], d_mission)
            try:
                claim_json = web_ops(d_conn, 'player_missions/claim_mission', x_param)
                result = claim_json['result']['success']
                if result:
                    for y in range(len(claim_json['result']['items'])):
                        if t(claim_json['result']['items'][y]) in items_gained:
                            items_gained[t(claim_json['result']['items'][y])] += 1
                        else:
                            items_gained[t(claim_json['result']['items'][y])] = 1
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
            else:
                sleep(1)
                continue
    screen_update(title, 'Summary Report')
    ctr_it('Mission: {0}   Adventurer: {1}'.format(t(d_mission), t(d_adventurer)))
    ctr_it('Batches: {0:,}   Delay: {1}s'.format(d_batch, d_delay))
    div_line('-')
    progress(1, 1, 'Farming Mission Completed!', 'Process completed in {0}'.format(
            cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ Speed Items Used ~~~', prefix=True)
        display_it(speeds_used, single=False)
    if items_gained:
        ctr_it('~~~ Items Gained ~~~', prefix=True)
        display_it(items_gained, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue . . ."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      CHEST CLASS                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def open_chest(title):
    # Initialize Chest Opener
    screen_update(title, 'Select Chests To Open')
    ctr_it(' Initializing...')
    d_chest = list()
    d_list = list()
    selection = {}
    max_len = 0
    for key, value in pData['items'].items():
        if 'ConfigurableChest' in key and value != 0:
            max_use_quantity = 0
            for manifest in range(len(mData['store']['chest'])):
                if key in mData['store']['chest'][manifest]['type']:
                    max_use_quantity = mData['store']['chest'][manifest]['max_use_quantity']
                    break
            max_len = len(str(value)) if max_len < len(str(value)) else max_len
            my_dict = {'chest': key, 'quantity': value, 'max_use': max_use_quantity}
            d_chest.append(my_dict)

    if not d_chest:
        nothing_to_do(title, 'Open Chests', 'Chests')
        return
    elif len(d_chest) == 1:
        my_dict = {'chest': d_chest[0]['chest'], 'quantity': d_chest[0]['quantity'], 'max_use': d_chest[0]['max_use']}
        d_list.append(my_dict)
    else:
        max_qty_len = 0
        for x in range(len(d_chest)):
            if len(str(d_chest[x]['quantity'])) > max_qty_len:
                max_qty_len = len(str(d_chest[x]['quantity']))
        for x in range(len(d_chest)):
            if d_chest[x]['chest'] not in selection:
                if len(d_chest) > 5 and (max_qty_len + len(t(d_chest[x]['chest']))) > 30:
                    truncate_size = 28 - max_qty_len
                    chest_name = smart_truncate(t(d_chest[x]['chest']), length=truncate_size)
                else:
                    chest_name = t(d_chest[x]['chest'])
                selection[chest_name] = d_chest[x]['quantity']

    # Select Chests
    while len(d_list) == 0:
        screen_update(title, 'Select Chests To Open')
        ctr_it('~~~ Available Chests ~~~')
        display_it(selection, single=False)
        print('\n Note: ALL = Opens all chests listed above')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i.isnumeric() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                elif d_select.lower() == 'all':
                    for x in range(len(d_chest)):
                        my_dict = {'chest': d_chest[x]['chest'], 'quantity': d_chest[x]['quantity'],
                                   'max_use': d_chest[x]['max_use']}
                        d_list.append(my_dict)
                else:
                    for x in range(len(d_chest)):
                        if d_select.lower() in t(d_chest[x]['chest']).lower() or \
                                        d_select.lower() == t(d_chest[x]['chest']).lower():
                            my_dict = {'chest': d_chest[x]['chest'], 'quantity': d_chest[x]['quantity'],
                                       'max_use': d_chest[x]['max_use']}
                            d_list.append(my_dict)

    d_chest = 'Chest: {0}'.format(t(d_list[0]['chest'])) if len(d_list) == 1 else 'Types Of Chest: {0}'.format(
            len(d_list))
    d_quantity = 0
    max_chest = 0
    for x in range(len(d_list)):
        d_quantity += d_list[x]['quantity']
        if max_chest < d_list[x]['quantity']:
            max_chest = d_list[x]['quantity']
        if max_chest > d_list[x]['max_use']:
            max_chest = d_list[x]['max_use']

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, 'Set Batches Of Chests To Open')
        ctr_it('{0}   Total Chests: {1:,}'.format(d_chest, d_quantity))
        ctr_it(' ')
        d_batch = set_batch(max_chest + 1, 'chests would you like to open in batches')
        if d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Batches Of Chests To Open')
        ctr_it('{0}   Total Chests: {1:,}'.format(d_chest, d_quantity))
        ctr_it('Open in Batches: {0}'.format(d_batch))
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Set Batches Of Chests To Open')
        ctr_it('{0}   Total Chests: {1:,}'.format(d_chest, d_quantity))
        ctr_it('Open in Batches: {0}   Delay: {1}s'.format(d_batch, d_delay))
        d_proceed = proceed_run('Opening of Chests')
        if d_proceed == 'exit':
            return

    # Open Chests
    global realm
    screen_update(title, 'Progress Report...')
    ctr_it('{0}   Total Chests: {1:,}'.format(d_chest, d_quantity))
    ctr_it('Open in Batches: {0}   Delay: {1}s'.format(d_batch, d_delay))
    div_line('-')
    progress(0, 1, 'Initializing...')
    selection.clear()
    d_start = time()
    look_up = pData['items']
    overall_received = {'Chests': {}, 'Arsenal': {}, 'Speeds': {}, 'Grants & Seals': {}, 'Others': {}}
    speed_items = ('DarkTestroniusInfusion', 'DarkTestroniusPowder', 'DarkTestroniusDeluxe', 'Hop', 'TranceMarchDrops',
                   'TestroniusInfusion', 'ForcedMarchDrops', 'TranceMarchElixir', 'Godspeed', 'Bounce', 'Skip', 'Jump',
                   'TestroniusPowder', 'TestroniusDeluxe', 'Leap', 'Bore', 'Bolt', 'Blast', 'Blitz', 'Blink')
    total_opened = 0
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(len(d_list)):
        received_items = {'Chests': {}, 'Arsenal': {}, 'Speeds': {}, 'Grants & Seals': {}, 'Others': {}}
        opened = d_list[x]['quantity']
        curr_count = 0
        open_quantity = d_batch
        while opened != 0:
            screen_update(title, 'Progress Report...')
            ctr_it('{0}   Total Chests: {1:,}'.format(d_chest, d_quantity))
            ctr_it('Open in Batches: {0}   Delay: {1}s   Elapsed Time: {2}'.format(
                    d_batch, d_delay, cvt_time(time() - d_start)))
            div_line('-')
            if len(d_list) > 1:
                progress(total_opened, d_quantity, 'Overall Opened: {0:,} of {1:,}'.format(total_opened, d_quantity))
                progress(curr_count, d_list[x]['quantity'], 'Current chest: {0}'.format(t(d_list[x]['chest'])),
                         'Opened {0:,} of {1:,}\n'.format(curr_count, d_list[x]['quantity']))
            else:
                progress(curr_count, d_list[x]['quantity'], 'Opened {0:,} of {1:,}'.format(
                        curr_count, d_list[x]['quantity']), '\n')
            for category in ('Chests', 'Arsenal', 'Speeds', 'Grants & Seals', 'Others'):
                if len(received_items[category]) > 0:
                    selection = received_items[category]
                    ctr_it('~~~ {0} Received ~~~'.format(category))
                    display_it(selection, single=False)
                    print(' ')
            if opened < open_quantity:
                open_quantity = opened
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    x_param = '%5Fmethod=delete&quantity={0}&'.format(open_quantity)
                    main_data = web_ops(d_conn, 'player_items/{0}'.format(d_list[x]['chest']), x_param)
                    result = main_data['result']['success']
                    if result:
                        opened -= open_quantity
                        curr_count += open_quantity
                        total_opened += open_quantity
                        for r_key, r_value in main_data['result']['items'].items():
                            if 'Chest' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    received_items['Chests'][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    received_items['Chests'][t(r_key)] = r_value
                            elif 'TroopPrize' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    received_items['Arsenal'][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    received_items['Arsenal'][t(r_key)] = r_value
                            elif 'Seal' in r_key or 'Grant' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    received_items['Grants & Seals'][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    received_items['Grants & Seals'][t(r_key)] = r_value
                            elif r_key in speed_items:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    received_items['Speeds'][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    received_items['Speeds'][t(r_key)] = r_value
                            else:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    received_items['Others'][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    received_items['Others'][t(r_key)] = r_value
                        if curr_count == d_list[x]['quantity']:
                            look_up = main_data['result']['items']
                        break
                    else:
                        open_quantity /= 2
                except (KeyError, TypeError):
                    sleep(1)
                    continue
        for category in ('Chests', 'Arsenal', 'Speeds', 'Grants & Seals', 'Others'):
            for r_key, r_value in received_items[category].items():
                if r_key in overall_received[category].keys():
                    overall_received[category][r_key] += r_value
                else:
                    overall_received[category][r_key] = r_value
    screen_update(title, 'Summary Report')
    ctr_it('{0}   Total Chests: {1:,}'.format(d_chest, d_quantity))
    ctr_it('Open in Batches: {0}   Delay: {1}s'.format(d_batch, d_delay))
    div_line('-')
    progress(1, 1, 'Chest Opening Completed!', 'Process completed in {0}'.format(
            cvt_time(time() - d_start)))
    for category in ('Chests', 'Arsenal', 'Speeds', 'Grants & Seals', 'Others'):
        if len(overall_received[category]) > 0:
            selection = overall_received[category]
            ctr_it('~~~ {0} Received ~~~'.format(category), prefix=True)
            display_it(selection, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue . . ."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def unpack_arsenal(title):
    # Initialize Open Arsenal
    screen_update(title, 'Select Troop Type')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    max_use_quantity = 0
    for key, value in sorted(pData['items'].items()):
        for manifest in range(len(mData['store']['arsenal'])):
            if key in mData['store']['arsenal'][manifest]['type']:
                max_use_quantity = mData['store']['arsenal'][manifest]['max_use_quantity']
                break
        if 'TroopPrizeItem' in key and value > 0:
            for x in range(len(mData['units'])):
                if mData['units'][x]['type'] in key:
                    if '50TroopPrizeItem' in key:
                        bin_desc, bin_type = ['Fifty', 50]
                    elif '500TroopPrizeItem' in key:
                        bin_desc, bin_type = ['Five Hundred', 500]
                    elif '1000TroopPrizeItem' in key:
                        bin_desc, bin_type = ['One Thousand', 1000]
                    elif '10kTroopPrizeItem' in key:
                        bin_desc, bin_type = ['Ten Thousand', 10000]
                    elif '50kTroopPrizeItem' in key:
                        bin_desc, bin_type = ['Fifty Thousand', 50000]
                    else:
                        continue
                    my_dict = {'troop': mData['units'][x]['type'], 'bin': key, 'quantity': value,
                               'power': mData['units'][x]['stats']['power'], 'bin_desc': bin_desc,
                               'bin_type': bin_type, 'max_use': max_use_quantity, 'use': False}
                    d_list.append(my_dict)
    if not d_list:
        nothing_to_do(title, 'Select Troop Type', 'no bins')
        return
    if len(d_list) == 1:
        d_troop = d_list[0]['troop']
    else:
        d_troop = None
        for x in range(len(d_list)):
            if d_list[x]['troop'] not in selection.keys():
                selection[d_list[x]['troop']] = t(d_list[x]['troop'])
        # Select Troop Type
        while not d_troop:
            screen_update(title, 'Select Troop Type')
            ctr_it('~~~ Available Troop Bins ~~~')
            display_it(selection)
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 3:
                if all(i.isalpha() or i == ' ' for i in d_select):
                    if d_select.lower() == 'exit':
                        return
                    else:
                        for key, value in selection.items():
                            if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                                d_troop = key
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    d_bin_type = None
    if len(d_list) == 1:
        d_list[0]['use'] = True
        d_bin_type = 'selected'
    else:
        selection.clear()
        len_a = 5
        len_b = 8
        len_c = 10
        for x in range(len(d_list)):
            a = '{0}'.format(d_list[x]['bin_desc'])
            if len_a < len(a):
                len_a = len(a)
            b = '{0:,}'.format(d_list[x]['quantity'])
            if len_b < len(b):
                len_b = len(b)
            c = '{0:,}'.format(d_list[x]['bin_type'] * d_list[x]['quantity'] * d_list[x]['power'])
            if len_c < len(c):
                len_c = len(c)

    # Select Bins To Open
    while d_bin_type is None:
        screen_update(title, 'Select Arsenal Type')
        ctr_it('Selected Troop: {0}'.format(t(d_troop)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Bin Types ~~~')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^4}'.format(
                'Type', len_a, 'Quantity', len_b, 'Power Gain', len_c, 'Open'))
        ctr_it('{0}  {1}  {2}  {3}'.format('-' * len_a, '-' * len_b, '-' * len_c, '-' * 4))
        for x in range(len(d_list)):
            a = '{0}'.format(d_list[x]['bin_desc'])
            b = '{0:,}'.format(d_list[x]['quantity'])
            c = '{0:,}'.format(d_list[x]['bin_type'] * d_list[x]['quantity'] * d_list[x]['power'])
            use_item = 'Yes' if d_list[x]['use'] == True else 'No'
            ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5}}  {6:^4}'.format(
                    a, len_a, b, len_b, c, len_c, use_item))
        print('\n Note: ALL = Unpacks all troop bins listed above')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                elif d_select.lower() == 'all':
                    for x in range(len(d_list)):
                        d_list[x]['use'] = True
                        d_bin_type = 'selected'
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() in d_list[x]['bin_desc'].lower() or \
                                        d_select.lower() == d_list[x]['bin_desc'].lower():
                            d_list[x]['use'] = True
                            d_bin_type = 'selected'
    d_list[:] = [d for d in d_list if d.get('use') == True]
    d_batch = None
    if len(d_list) > 1:
        d_bin_type = '{0} Bin Types'.format(len(d_list))
        d_batch = 0
        for x in range(len(d_list)):
            d_batch += d_list[x]['quantity']
    else:
        d_bin_type = '{0:,} Bin Type'.format(d_list[0]['bin_type'])

    # Set Number Of Batches
    while d_batch is None:
        screen_update(title, 'Set Maximum Troop Bins To Unpack')
        ctr_it('Selected Troop: {0}   Unpack: {1}'.format(t(d_troop), d_bin_type))
        ctr_it(' ')
        d_batch = set_batch(d_list[0]['quantity'] + 1, 'troop bins would you like to unpack')
        if d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Instructions')
        ctr_it('Selected Troop: {0}   Unpack: {1}'.format(t(d_troop), d_bin_type))
        ctr_it('Bins Selected: {0:,}'.format(d_batch))
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Proceed With Unpacking Troop Bins?')
        ctr_it('Selected Troop: {0}   Unpack: {1}'.format(t(d_troop), d_bin_type))
        ctr_it('Bins Selected: {0:,}   Delay: {1}s'.format(d_batch, d_delay))
        d_proceed = proceed_run('Unpacking of Troop Bins')
        if d_proceed == 'exit':
            return

    # Unpack Troop Bins
    global realm
    screen_update(title, 'Progress Report...')
    ctr_it('Selected Troop: {0}   Unpack: {1}'.format(t(d_troop), d_bin_type))
    ctr_it('Bins Selected: {0:,}   Delay: {1}s'.format(d_batch, d_delay))
    div_line('-')
    progress(0, 1, 'Initializing...')
    d_start = time()
    total_opened = 0
    d_power = 0
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(len(d_list)):
        current_opened = 0
        if len(d_list) > 1:
            d_quantity = d_list[x]['quantity']
        else:
            d_quantity = d_batch
        open_quantity = d_list[x]['max_use']
        while d_quantity != 0:
            screen_update(title, 'Progress Report...')
            ctr_it('Selected Troop: {0}   Unpack: {1}'.format(t(d_troop), d_bin_type))
            ctr_it('Bins Selected: {0:,}   Delay: {1}s   Elapsed Time: {2}'.format(
                    d_batch, d_delay, cvt_time(time() - d_start)))
            div_line('-')
            progress(total_opened, d_batch, 'Unpacking {0:,} of {1:,}'.format(total_opened, d_batch))
            if len(d_list) > 1:
                progress(current_opened, d_list[x]['quantity'], 'Unpacking {0}'.format(t(d_list[x]['bin'])))
            ctr_it('~~~ Power Gained ~~~', prefix=True)
            ctr_it('{0:,}'.format(d_power))
            if d_quantity < open_quantity:
                open_quantity = d_quantity
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    x_param = '%5Fmethod=delete&quantity={0}&'.format(open_quantity)
                    json_data = web_ops(d_conn, 'player_items/{0}'.format(d_list[x]['bin']), x_param)
                    result = json_data['result']['success']
                    if result:
                        total_opened += open_quantity
                        current_opened += open_quantity
                        d_quantity -= open_quantity
                        d_power += (open_quantity * d_list[x]['bin_type']) * d_list[x]['power']
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
    screen_update(title, 'Summary Report')
    ctr_it('Selected Troop: {0}   Unpack: {1}'.format(t(d_troop), d_bin_type))
    ctr_it('Bins Selected: {0:,}   Delay: {1}s'.format(
            d_batch, d_delay))
    div_line('-')
    progress(total_opened, d_batch, 'Unpacking Troop Bins Completed!'.format(total_opened, d_batch),
             'Process completed in {0}'.format(cvt_time(time() - d_start)))
    ctr_it('~~~ Power Gained ~~~', prefix=True)
    ctr_it('{0:,}'.format(d_power))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue . . ."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def fill_building(title):
    # Initialize
    screen_update(title, 'Fills Slots With Buildings')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    built = list()
    capital_buildings = {}
    for x in range(len(cData['capital']['city']['buildings'])):
        if cData['capital']['city']['buildings'][x]['type'] not in capital_buildings:
            capital_buildings[cData['capital']['city']['buildings'][x]['type']] = \
                cData['capital']['city']['buildings'][x]['level']
    for key in cData.keys():
        city_busy = False
        built.clear()
        if len(cData[key]['city']['jobs']) != 0:
            for check_jobs in range(len(cData[key]['city']['jobs'])):
                if cData[key]['city']['jobs'][check_jobs]['queue'] == 'building':
                    city_busy = True
                    break
        city_slot = list()
        field_slot = list()
        c_slot = f_slot = 0
        for c_key in range(len(cData[key]['city']['buildings'])):
            city = cData[key]['city']['buildings'][c_key]
            built.append(city['type'])
            if city['location'] in 'city':
                city_slot.append(city['slot'])
            if city['location'] in 'field':
                field_slot.append(city['slot'])
            if key == 'capital' and city['type'] == 'Fortress':
                c_slot = building_dict[key]['c_slots'][city['level']]
                f_slot = building_dict[key]['f_slots'][city['level']]
            if key != 'capital' and 'DragonKeep' in city['type']:
                c_slot = building_dict[key]['c_slots'][city['level']]
                f_slot = building_dict[key]['f_slots'][city['level']]
        if not city_busy:
            for x in range(len(mData['buildings'])):
                manifest = mData['buildings'][x]
                if (manifest['location'] in 'city' and len(city_slot) < c_slot) or (
                                manifest['location'] in 'field' and len(field_slot) < f_slot):
                    if manifest['buildable'] is True and manifest['city_max'][key] != 0:
                        if manifest['per_city'] == 0 or (manifest['per_city'] == 1 and manifest['type'] not in built):
                            for z in range(len(manifest['levels'])):
                                if manifest['levels'][z]['level'] == 1:
                                    level = manifest['levels'][z]
                                    my_dict = {'city': key, 'location': manifest['location'], 'type': manifest['type'],
                                               'per_city': manifest['per_city'], 'levels': level, 'c_slot': city_slot,
                                               'c_slot_max': c_slot, 'f_slot': field_slot, 'f_slot_max': f_slot,
                                               'location_id': cData[key]['city']['id']}
                                    d_list.append(my_dict)
                                    if key not in selection:
                                        selection[key] = t(key)
                                    break
    d_location = None
    if not d_list:
        nothing_to_do(title, 'Fills Slots With Buildings', 'no buildings')
        return
    else:
        if len(selection) == 1:
            d_location = selection[0]

    # Select Location
    while d_location is None:
        screen_update(title, 'Select Location')
        ctr_it('~~~ Available Locations ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 2:
            if not d_select.isalpha():
                sleep(1)
            else:
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower():
                            d_location = key
    d_list[:] = [d for d in d_list if d.get('city') == d_location]
    selection.clear()
    d_building = None
    if len(d_list) == 1:
        d_building = d_list[0]['type']
    else:
        for x in range(len(d_list)):
            if d_list[x]['type'] not in selection:
                selection[d_list[x]['type']] = t(d_list[x]['type'])

    # Select Building
    while d_building is None:
        screen_update(title, 'Choose Building For Location')
        ctr_it('Location: {0}'.format(t(d_location)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Buildings ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            d_building = key
                            break
    d_list[:] = [d for d in d_list if d.get('type') == d_building]
    if d_list[0]['location'] == 'city':
        max_slot = d_list[0]['c_slot_max'] - len(d_list[0]['c_slot'])
    else:
        max_slot = d_list[0]['f_slot_max'] - len(d_list[0]['f_slot'])

    # Set Slots If Applicable
    gtg = False
    requirements = {}
    if d_list[0]['per_city'] == 1:
        d_slots = 1
    else:
        d_slots = 0
        while d_slots is 0:
            screen_update(title, 'How Many Slot To Fill?')
            ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
            ctr_it(' ')
            div_line('-')
            ctr_it('~~~ Available Options ~~~')
            ctr_it('1 to {0}'.format(max_slot))
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 1:
                if d_select.lower() == 'exit':
                    return
                if not d_select.isnumeric():
                    sleep(1)
                else:
                    if int(d_select) in range(max_slot + 1):
                        d_slots = int(d_select)
        while gtg is False:
            requirements = {'items': {}, 'buildings': {}, 'resources': {}}
            req_check = list()
            req = d_list[0]['levels']['requirements']
            for key in req.keys():
                for c_key, c_value in req[key].items():
                    if c_key in requirements[key]:
                        if key == 'buildings':
                            if requirements[key][c_key] < c_value:
                                requirements[key][c_key] = c_value
                        else:
                            requirements[key][c_key] += c_value * d_slots
                    else:
                        requirements[key][c_key] = c_value * d_slots
            if len(requirements['items']) + len(requirements['buildings']) + len(requirements['resources']) > 0:
                for key in requirements:
                    if key == 'buildings':
                        for c_key, c_value in requirements[key].items():
                            if c_key in capital_buildings.keys():
                                if c_value > capital_buildings[c_key]:
                                    req = '{0} Level {1} Required. Yours is level {2}'.format(
                                            c_key, c_value, capital_buildings[c_key])
                                    req_check.append(req)
                            else:
                                req = '{0} Level {1} Required. Yours is not built'.format(c_key, c_value)
                                req_check.append(req)
                    if key == 'items':
                        for c_key, c_value in requirements[key].items():
                            if c_key in pData['items']:
                                if pData['items'][c_key] < c_value:
                                    req = '{0:,} {1} Required. You have {2:,}'.format(
                                            c_value, c_key, pData['items'][c_key])
                                    req_check.append(req)
                            else:
                                req = '{0:,} {1} Required. You have none'.format(c_value, c_key)
                                req_check.append(req)
                    if key == 'resources':
                        for c_key, c_value in requirements[key].items():
                            if c_key in cData['capital']['city']['resources']:
                                if cData['capital']['city']['resources'][c_key] < c_value:
                                    req = '{0:,} {1} Required. You have {2:,}'.format(
                                            c_value, c_key, cData['capital']['city']['resources'][c_key])
                                    req_check.append(req)
                            else:
                                req = '{0:,} {1} Required. You have none'.format(c_value, c_key)
                                req_check.append(req)
            screen_update(title, 'How Many Slot To Fill?')
            ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
            ctr_it(' ')
            div_line('-')
            if len(req_check) != 0:
                for x in range(len(req_check)):
                    ctr_it(req_check[x])
                ctr_it('')
                ctr_it('Requirements Not Met. Try Lowering Slots To Fill')
                ctr_it('')
                div_line('-')
                print(' Selection options available:')
                print(' 1-{1} = Slots to fill, EXIT = Return to main menu'.format(max_slot))
                div_line()
            if len(req_check) == 0 and d_slots != 0:
                gtg = True
            else:
                d_select = input('Enter selection : ')
                if len(d_select) >= 1:
                    if d_select.lower() == 'exit':
                        return
                    if not d_select.isnumeric():
                        sleep(1)
                    else:
                        if int(d_select) in range(max_slot + 1):
                            d_slots = int(d_select)
                            req_check.clear()

    # Select Speed Items
    selection = list()
    a, b, c, d, len_a, len_b, len_c, len_d = ['Item', 'Description', 'Available', 'Exceeding', 4, 11, 9, 9]
    for key in range(len(speed_items_dict)):
        look_up = speed_items_dict[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['item']) > len_a:
                len_a = len(look_up['item'])
            if len(cvt_time(look_up['time'], show_seconds=False)) > len_b:
                len_b = len(cvt_time(look_up['time'], show_seconds=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > len_c:
                len_c = len('{0:,}'.format(pData['items'][look_up['item']]))
            if len(cvt_time(look_up['exceed'], show_seconds=False)) > len_d:
                len_d = len(cvt_time(look_up['exceed'], show_seconds=False))
            my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                       'quantity': pData['items'][look_up['item']], 'use': False}
            selection.append(my_dict)
    if selection:
        while True:
            screen_update(title, 'Select Speed Items To Use')
            ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
            ctr_it('Slots To Fill: {0}'.format(d_slots))
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  Use'.format(a, len_a, b, len_b, c, len_c, d, len_d))
            ctr_it('{0}  {1}  {2}  {3}  ~~~'.format('~' * len_a, '~' * len_b, '~' * len_c, '~' * len_d))
            for key in range(len(selection)):
                use_item = 'Yes' if selection[key]['use'] is True else 'No'
                ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>3}'.format(
                        selection[key]['item'], len_a, cvt_time(selection[key]['time'], show_seconds=False), len_b,
                        selection[key]['quantity'], len_c, cvt_time(selection[key]['exceed'], show_seconds=False),
                        len_d, use_item))
            print('\n Exceeding - Item used when duration exceeds the displayed time')
            div_line('-')
            print(' Selection options available:')
            print(' ALL = Enable all, NONE = Disable all, Item Name = Enable/Disable selected')
            print(' NEXT = Accept list and proceed to the next screen, EXIT = Return to main menu')
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 2:
                if d_select.lower() == 'exit':
                    return
                elif d_select.lower() == 'next':
                    break
                elif d_select.lower() == 'all':
                    for key in range(len(selection)):
                        selection[key]['use'] = True
                elif d_select.lower() == 'none':
                    for key in range(len(selection)):
                        selection[key]['use'] = False
                else:
                    for key in range(len(selection)):
                        if d_select.lower() in selection[key]['item'].lower():
                            selection[key]['use'] = True if selection[key]['use'] is False else False
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['use'] is True:
            d_speed.append(selection[x])

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Instructions')
        ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
        ctr_it('Slots To Fill: {0}'.format(d_slots))
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Proceed With Filling Slots?')
        ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
        ctr_it('Slots To Fill: {0}   Delay: {1}'.format(d_slots, d_delay))
        d_proceed = proceed_run('Filling Building Slots')
        if d_proceed == 'exit':
            return

    # Run Auto Fill
    global realm
    screen_update(title, 'Progress Report')
    ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
    ctr_it('Slots To Fill: {0}   Delay: {1}'.format(d_slots, d_delay))
    div_line('-')
    progress(0, 1, 'Initializing...')
    d_start = time()
    speeds_used = {}
    d_conn = http.client.HTTPConnection(realm, 80)
    slots = list()
    count = 0
    if d_list[0]['location'] == 'city':
        for x in range(d_list[0]['c_slot_max']):
            if x not in d_list[0]['c_slot']:
                slots.append(x)
    else:
        for x in range(d_list[0]['f_slot_max']):
            if x not in d_list[0]['f_slot']:
                slots.append(x)
    for x in range(d_slots):
        jobid = 0
        duration = -1
        while duration != 0:
            screen_update(title, 'Progress Report')
            ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
            ctr_it('Slots To Fill: {0}   Delay: {1}   Elapsed Time: {2}'.format(
                    d_slots, d_delay, cvt_time(time() - d_start)))
            div_line('-')
            if speeds_used:
                progress(count, d_slots, 'Filling Slot {0} of {1}'.format(count, d_slots))
                ctr_it(' ')
                ctr_it('~~~ Speed Items Used ~~~')
                display_it(speeds_used, single=False)
            elif duration != -1:
                progress(count, d_slots, 'Filling Slot {0} of {1}'.format(count, d_slots),
                         'Waiting {0} for job to finish...'.format(cvt_time(duration)))
            else:
                progress(count, d_slots, 'Filling Slot {0} of {1}'.format(count, d_slots), 'Initializing...')
            if duration == -1:
                x_param = 'city%5F{0}%5B{0}%5Ftype%5D={1}&%5Fmethod=post&city%5F{0}%5Bslot%5D={2}&'.format(
                        'building', d_building, slots[x])
                for web_retry in range(5):
                    try:
                        sleep(d_delay)
                        json_data = web_ops(d_conn, 'cities/{0}/buildings'.format(
                                d_list[0]['location_id']), x_param)
                        result = json_data['result']['success']
                        if result:
                            duration = json_data['result']['job']['duration']
                            jobid = json_data['result']['job']['id']
                            count += 1
                            break
                    except (KeyError, TypeError):
                        sleep(1)
                        continue
            elif duration != 0 and len(d_speed) > 0:
                speed_item = None
                for y in range(len(d_speed)):
                    if duration > d_speed[y]['exceed']:
                        speed_item = d_speed[y]['item']
                        break
                if speed_item is None:
                    if len(d_speed) == 1:
                        speed_item = d_speed[0]['item']
                    else:
                        for y in range(len(d_speed) + 1, -1, -1):
                            if duration <= d_speed[y]['time']:
                                speed_item = d_speed[y]['item']
                                break
                x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(jobid)
                for web_retry in range(5):
                    try:
                        sleep(d_delay)
                        json_data = web_ops(d_conn, 'player_items/{0}'.format(speed_item), x_param)
                        result = json_data['result']['success']
                        if result:
                            if speed_item in speeds_used:
                                speeds_used[speed_item] += 1
                            else:
                                speeds_used[speed_item] = 1
                            duration = int(json_data['result']['item_response']['run_at'] - json_data['timestamp'])
                            if duration < 1:
                                duration = 0
                            break
                    except TypeError:
                        sleep(1)
                        continue
            else:
                duration -= 1
                if duration < 1:
                    duration = 0
                sleep(1)
    screen_update(title, 'Summary Report')
    ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
    ctr_it('Slots To Fill: {0}   Delay: {1}'.format(d_slots, d_delay))
    div_line('-')
    progress(1, 1, 'Filling Completed Successfully!', 'Process completed in {0}'.format(
            cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ Speed Items Used ~~~', prefix=True)
        display_it(speeds_used, single=False)
    if len(requirements['items']) >= 1:
        ctr_it('~~~ Seals & Grants Used ~~~', prefix=True)
        for key, value in requirements['items'].items():
            ctr_it('{0:>}: {1:,}'.format(t(key), value))
    if len(requirements['resources']) >= 1:
        ctr_it('~~~ Resources Used  ~~~', prefix=True)
        for key, value in requirements['resources'].items():
            ctr_it('{0:>5}: {1:,}'.format(key.title(), value))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, data5=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def upgrade_building(title):
    # Initialize
    screen_update(title, 'Choose A Location To Upgrade')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    capital_buildings = {}
    for x in range(len(cData['capital']['city']['buildings'])):
        if cData['capital']['city']['buildings'][x]['type'] not in capital_buildings:
            capital_buildings[cData['capital']['city']['buildings'][x]['type']] = \
                cData['capital']['city']['buildings'][x]['level']
    for key in cData.keys():
        city_busy = False
        if len(cData[key]['city']['jobs']) != 0:
            for check_jobs in range(len(cData[key]['city']['jobs'])):
                if cData[key]['city']['jobs'][check_jobs]['queue'] == 'building':
                    city_busy = True
                    break
        if not city_busy:
            for x in range(len(cData[key]['city']['buildings'])):
                city = cData[key]['city']['buildings'][x]
                for y in range(len(mData['buildings'])):
                    manifest = mData['buildings'][y]
                    levels = list()
                    if city['type'] == manifest['type'] and city['level'] < manifest['city_max'][key]:
                        for z in range(city['level'] + 1, manifest['city_max'][key] + 1):
                            for lvl in range(len(manifest['levels'])):
                                if z == manifest['levels'][lvl]['level']:
                                    levels.append(manifest['levels'][lvl])
                        my_dict = {'city': key, 'max_level': manifest['city_max'][key], 'building_id': city['id'],
                                   'type': city['type'], 'level': city['level'], 'levels': levels,
                                   'location_id': cData[key]['city']['id']}
                        d_list.append(my_dict)
                        break

    if not d_list:
        nothing_to_do(title, 'Choose A Location To Upgrade', 'Buildings')
        return
    if len(d_list) == 1:
        d_location = d_list[0]['city']
    else:
        d_location = None
        for x in range(len(d_list)):
            if d_list[x]['city'] not in selection.keys():
                selection[d_list[x]['city']] = t(d_list[x]['city'])
        # Select Location
        while d_location is None:
            screen_update(title, 'Choose A Location To Upgrade')
            ctr_it('~~~ Available Locations ~~~')
            display_it(selection)
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 3:
                if all(i.isalpha() or i == ' ' for i in d_select):
                    if d_select.lower() == 'exit':
                        return
                    else:
                        for key, value in selection.items():
                            if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                                d_location = key
                                break
    d_list[:] = [d for d in d_list if d.get('city') == d_location]
    d_building = None
    selection.clear()
    if len(d_list) == 1:
        d_building = d_list[0]['type']
    else:
        for x in range(len(d_list)):
            if d_list[x]['type'] not in selection:
                selection[d_list[x]['type']] = t(d_list[x]['type'])

    # Select Building
    while d_building is None:
        screen_update(title, 'Choose Building For Location')
        ctr_it('Location: {0}'.format(t(d_location)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Buildings ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            d_building = key
                            break
    d_list[:] = [d for d in d_list if d.get('type') == d_building]
    max_level = d_list[0]['max_level']
    min_level = max_level
    for x in range(len(d_list)):
        if d_list[x]['level'] < min_level:
            min_level = d_list[x]['level']

    # Select Level
    gtg = False
    d_level = 0
    requirements = {}
    while d_level is 0:
        screen_update(title, 'Select Level To Upgrade')
        ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
        div_line('-')
        ctr_it('')
        ctr_it('Which Level Would You Like To Upgrade This Building To?')
        ctr_it('')
        div_line('-')
        print(' Selection options available:')
        print(' {0}-{1} = Level to upgrade, EXIT = Return to main menu'.format(min_level + 1, max_level))
        div_line()
        d_select = input('Enter selection : ')
        if len(d_select) >= 1:
            if d_select.lower() == 'exit':
                return
            if not d_select.isnumeric():
                sleep(1)
            else:
                if int(d_select) in range(min_level + 1, max_level + 1):
                    d_level = int(d_select)
    while gtg is False:
        requirements = {'items': {}, 'buildings': {}, 'research': {}, 'resources': {}}
        req_check = list()
        for x in range(len(d_list)):
            for y in range(len(d_list[x]['levels'])):
                if d_list[x]['levels'][y]['level'] <= d_level:
                    req = d_list[x]['levels'][y]['requirements']
                    for key in req.keys():
                        for c_key, c_value in req[key].items():
                            if c_key in requirements[key]:
                                if key == 'buildings':
                                    if requirements[key][c_key] < c_value:
                                        requirements[key][c_key] = c_value
                                else:
                                    requirements[key][c_key] += c_value
                            else:
                                requirements[key][c_key] = c_value
        if len(requirements['items']) + len(requirements['buildings']) + len(requirements['resources']) > 0:
            for key in requirements:
                if key == 'buildings':
                    for c_key, c_value in requirements[key].items():
                        if c_key in capital_buildings.keys():
                            if c_value > capital_buildings[c_key]:
                                req = '{0} Level {1} Required. Yours is level {2}'.format(
                                        c_key, c_value, capital_buildings[c_key])
                                req_check.append(req)
                        else:
                            req = '{0} Level {1} Required. Yours is not built'.format(c_key, c_value)
                            req_check.append(req)
                if key == 'items':
                    for c_key, c_value in requirements[key].items():
                        if c_key in pData['items']:
                            if pData['items'][c_key] < c_value:
                                req = '{0:,} {1} Required. You have {2:,}'.format(
                                        c_value, c_key, pData['items'][c_key])
                                req_check.append(req)
                        else:
                            req = '{0:,} {1} Required. You have none'.format(c_value, c_key)
                            req_check.append(req)
                if key == 'research':
                    for c_key, c_value in requirements[key].items():
                        if c_key in pData['research']:
                            if pData['research'][c_key] < c_value:
                                req = '{1} Level {0} Required. Your {1} is at {2}'.format(
                                        c_value, c_key, pData['research'][c_key])
                                req_check.append(req)
                        else:
                            req = '{1} Level {0} Required. You are yet to start on {1}'.format(c_value, c_key)
                            req_check.append(req)
                if key == 'resources':
                    for c_key, c_value in requirements[key].items():
                        if c_key in cData['capital']['city']['resources']:
                            if cData['capital']['city']['resources'][c_key] < c_value:
                                req = '{0:,} {1} Required. You have {2:,}'.format(
                                        c_value, c_key, cData['capital']['city']['resources'][c_key])
                                req_check.append(req)
        screen_update(title, 'Select Level To Upgrade')
        ctr_it('Location: {0}   Building: {1}'.format(t(d_location), t(d_building)))
        div_line('-')
        if len(req_check) != 0:
            for x in range(len(req_check)):
                ctr_it(req_check[x])
            ctr_it('')
            ctr_it('Requirements Not Met. Try Lowering Upgrade Level')
            ctr_it('')
            div_line('-')
            print(' Selection options available:')
            print(' {0}-{1} = Slots to fill, EXIT = Return to main menu'.format(min_level + 1, max_level))
            div_line()
        if len(req_check) == 0 and d_level != 0:
            gtg = True
        else:
            d_select = input('Enter selection : ')
            if len(d_select) >= 1:
                if d_select.lower() == 'exit':
                    return
                if not d_select.isnumeric():
                    sleep(1)
                else:
                    if int(d_select) in range(min_level + 1, max_level + 1):
                        d_level = int(d_select)
                        max_level = int(d_select) - 1
                        req_check.clear()

    # Select Speed Items
    selection = list()
    a, b, c, d, len_a, len_b, len_c, len_d = ['Item', 'Description', 'Available', 'Exceeding', 4, 11, 9, 9]
    for key in range(len(speed_items_dict)):
        look_up = speed_items_dict[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['item']) > len_a:
                len_a = len(look_up['item'])
            if len(cvt_time(look_up['time'], show_seconds=False)) > len_b:
                len_b = len(cvt_time(look_up['time'], show_seconds=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > len_c:
                len_c = len('{0:,}'.format(pData['items'][look_up['item']]))
            if len(cvt_time(look_up['exceed'], show_seconds=False)) > len_d:
                len_d = len(cvt_time(look_up['exceed'], show_seconds=False))
            my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                       'quantity': pData['items'][look_up['item']], 'use': False}
            selection.append(my_dict)
    if selection:
        while True:
            screen_update(title, 'Select Speed Items To Use')
            ctr_it('Location: {0}   Building: {1}   Target Level: {2}'.format(t(d_location), t(d_building), d_level))
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  Use'.format(a, len_a, b, len_b, c, len_c, d, len_d))
            ctr_it('{0}  {1}  {2}  {3}  ~~~'.format('~' * len_a, '~' * len_b, '~' * len_c, '~' * len_d))
            for key in range(len(selection)):
                use_item = 'Yes' if selection[key]['use'] is True else 'No'
                ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>3}'.format(
                        selection[key]['item'], len_a, cvt_time(selection[key]['time'], show_seconds=False), len_b,
                        selection[key]['quantity'], len_c, cvt_time(selection[key]['exceed'], show_seconds=False),
                        len_d, use_item))
            print('\n Exceeding - Item used when duration exceeds the displayed time')
            div_line('-')
            print(' Selection options available:')
            print(' ALL = Enable all, NONE = Disable all, Item Name = Enable/Disable selected')
            print(' NEXT = Accept list and proceed to the next screen, EXIT = Return to main menu')
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 2:
                if d_select.lower() == 'exit':
                    return
                elif d_select.lower() == 'next':
                    break
                elif d_select.lower() == 'all':
                    for key in range(len(selection)):
                        selection[key]['use'] = True
                elif d_select.lower() == 'none':
                    for key in range(len(selection)):
                        selection[key]['use'] = False
                else:
                    for key in range(len(selection)):
                        if d_select.lower() in selection[key]['item'].lower():
                            selection[key]['use'] = True if selection[key]['use'] is False else False
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['use'] is True:
            d_speed.append(selection[x])

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Requests')
        ctr_it('Location: {0}   Building: {1}   Target Level: {2}'.format(t(d_location), t(d_building), d_level))
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Proceed With Upgrading?')
        ctr_it('Location: {0}   Building: {1}   Target Level: {2}'.format(t(d_location), t(d_building), d_level))
        ctr_it('Delay: {0}s'.format(d_delay))
        d_proceed = proceed_run('Unpacking of Troop Bins')
        if d_proceed == 'exit':
            return

    # Run Auto Upgrade
    global realm
    screen_update(title, 'Progress Report...')
    ctr_it('Location: {0}   Building: {1}   Target Level: {2}'.format(t(d_location), t(d_building), d_level))
    ctr_it('Delay: {0}'.format(d_delay))
    ctr_it('')
    div_line('-')
    progress(0, 1, 'Initializing...')
    d_start = time()
    speeds_used = {}
    d_conn = http.client.HTTPConnection(realm, 80)
    d_list_len = len(d_list)
    for y in range(min_level, d_level):
        total = len([d for d in d_list if d.get('level') == y])
        count = 0
        for x in range(d_list_len):
            if d_list[x]['level'] == y:
                jobid = 0
                duration = -1
                speed_item = None
                while duration != 0:
                    screen_update('UPGRADE BUILDING', 'Progress Report...')
                    ctr_it('Location: {0}   Building: {1}   Target Level: {2}'.format(
                            t(d_location), t(d_building), d_level))
                    ctr_it('Delay: {0}s   Elapsed Time: {1}'.format(d_delay, cvt_time(time() - d_start)))
                    div_line('-')
                    if (d_level - min_level) > 1:
                        progress((d_level - min_level) - (d_level - y) + 1, d_level - min_level,
                                 'Upgrading From Level {0} to Level {1}'.format(y, d_level))
                    if total > 1:
                        progress(count, total, 'Upgrading Slot {0} of {1}'.format(count, total))
                    elif speed_item:
                        progress(prog_dur - duration, prog_dur, 'Used {0} to speed through'.format(speed_item))
                    else:
                        pass
                    if speeds_used:
                        ctr_it(' ')
                        ctr_it('~~~ Speed Items Used ~~~')
                        display_it(speeds_used, single=False)
                    if duration == -1:
                        x_param = '%5Fmethod=put&'
                        for server_retry in range(5):
                            sleep(d_delay + 1)
                            try:
                                main_json = web_ops(d_conn, 'cities/{0}/buildings/{1}'.format(
                                        d_list[x]['location_id'], d_list[x]['building_id']), x_param)
                                result = main_json['result']['success']
                                if result:
                                    duration = int(main_json['result']['job']['duration'])
                                    prog_dur = duration
                                    jobid = main_json['result']['job']['id']
                                    count += 1
                                    break
                            except (KeyError, TypeError):
                                sleep(1)
                                continue
                    elif duration > 0 and len(d_speed) > 0:
                        speed_item = None
                        for z in range(len(d_speed)):
                            if duration > d_speed[z]['exceed'] and d_speed[z]['quantity'] != 0:
                                speed_item = d_speed[z]['item']
                                break
                        if speed_item is None:
                            if len(d_speed) == 1 and d_speed[0]['quantity'] != 0:
                                speed_item = d_speed[0]['item']
                            else:
                                for z in range(len(d_speed) - 1, -1, -1):
                                    if duration <= d_speed[z]['time'] and d_speed[z]['quantity'] != 0:
                                        speed_item = d_speed[z]['item']
                                        break
                        x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(jobid)
                        for server_retry in range(5):
                            sleep(d_delay + 1)
                            try:
                                item_json = web_ops(d_conn, 'player_items/{0}'.format(speed_item), x_param)
                                result = item_json['result']['success']
                                if result:
                                    for z in range(len(d_speed)):
                                        if speed_item == d_speed[z]['item']:
                                            d_speed[z]['quantity'] -= 1
                                    if speed_item in speeds_used:
                                        speeds_used[speed_item] += 1
                                    else:
                                        speeds_used[speed_item] = 1
                                    duration = int(
                                            item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                    if duration < 1:
                                        duration = 0
                                        d_list[x]['level'] = item_json['result']['item_response']['level']
                                    break
                            except (KeyError, TypeError):
                                sleep(1)
                                continue
                    else:
                        duration -= 1
                        if duration < 1:
                            duration = 0
                            d_list[x]['level'] += 1
                        sleep(1)
    screen_update(title, 'Summary Report')
    ctr_it('Location: {0}   Building: {1}   Target Level: {2}'.format(t(d_location), t(d_building), d_level))
    ctr_it('Delay: {0}s'.format(d_delay, cvt_time(time() - d_start)))
    div_line('-')
    progress(1, 1, 'Upgrade Completed Successfully!', 'Process completed in {0}'.format(
            cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ Speed Items Used ~~~', prefix=True)
        display_it(speeds_used, single=False)
    if len(requirements['items']) >= 1:
        ctr_it('~~~ Seals & Grants Used ~~~', prefix=True)
        for key, value in requirements['items'].items():
            ctr_it('{0:>}: {1:,}'.format(t(key), value))
    if len(requirements['resources']) >= 1:
        ctr_it('~~~ Resources Used  ~~~', prefix=True)
        for key, value in requirements['resources'].items():
            ctr_it('{0:>5}: {1:,}'.format(key.title(), value))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, data5=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def train_troop(title):
    # Initialize
    screen_update(title, 'Select Troop To Train')
    ctr_it(' Initializing...')
    d_list = list()
    selection = {}
    pseudo_tc = ('Garrison', 'TrainingCamp', 'CaveTrainingCamp')
    for x in cData:
        tc_level, tc_total, tc_combo = [0, 0, 0]
        for y in range(len(cData[x]['city']['buildings'])):
            if cData[x]['city']['buildings'][y]['type'] in pseudo_tc:
                tc_level = cData[x]['city']['buildings'][y]['level'] if tc_level < cData[x]['city']['buildings'][y][
                    'level'] else tc_level
                tc_total += 1
                tc_combo += cData[x]['city']['buildings'][y]['level']
        my_dict = {'tc_level': tc_level, 'tc_combo': tc_combo, 'tc_total': tc_total}
        selection[x] = my_dict
    d_rookery = 0
    for x in range(len(mData['units'])):
        if mData['units'][x]['trainable_in']:
            d_max_queue = d_pop = -1
            met_research = met_resource = met_item = met_unit = met_idle = met_building = True
            d_unit = mData['units'][x]
            d_req = d_unit['requirements']['capital']
            if 'research' in d_req.keys():
                met_req = len(d_req['research'])
                for key, value in d_req['research'].items():
                    if key in pData['research']:
                        if value <= pData['research'][key]:
                            met_req -= 1
                met_research = True if met_req == 0 else False
            if 'resources' in d_req.keys():
                met_req = len(d_req['resources'])
                lookup = cData['capital']['city']['resources']
                for key, value in d_req['resources'].items():
                    if key in lookup:
                        if value <= lookup[key]:
                            met_req -= 1
                            if value != 0:
                                if d_max_queue > int(lookup[key] / value) or d_max_queue == -1:
                                    d_max_queue = int(lookup[key] / value)
                met_resource = True if met_req == 0 else False
            if 'items' in d_req.keys():
                met_req = len(d_req['items'])
                lookup = pData['items']
                for key, value in d_req['items'].items():
                    if key in lookup:
                        if value <= lookup[key]:
                            met_req -= 1
                            if value != 0:
                                if d_max_queue > int(lookup[key] / value) or d_max_queue == -1:
                                    d_max_queue = int(lookup[key] / value)
                met_item = True if met_req == 0 else False
            if 'units' in d_req.keys():
                met_req = len(d_req['units'])
                lookup = cData['capital']['city']['units']
                for key, value in d_req['units'].items():
                    if key in lookup:
                        if value <= lookup[key]:
                            met_req -= 1
                            if value != 0:
                                if d_max_queue > int(lookup[key] / value) or d_max_queue == -1:
                                    d_max_queue = int(lookup[key] / value)
                met_unit = True if met_req == 0 else False
            if 'population' in d_req.keys():
                lookup = cData['capital']['city']['figures']['population']
                if d_req['population']['idle'] <= lookup['current'] - (lookup['laborers'] + lookup['armed_forces']) - 1:
                    met_idle = True
                    d_pop = int((lookup['current'] - (lookup['laborers'] + lookup['armed_forces']) - 1) /
                                d_req['population']['idle'])
                else:
                    met_idle = False
            if 'buildings' in d_req.keys():
                met_req = len(d_req['buildings'])
                lookup = cData['capital']['city']['buildings']
                for key, value in d_req['buildings'].items():
                    if key in pseudo_tc:
                        met_req -= 1
                    else:
                        for y in range(len(lookup)):
                            if key == lookup[y]['type'] and value <= lookup[y]['level']:
                                met_req -= 1
                                d_rookery = lookup[y]['level'] if key == 'Rookery' else 0
                                break
                met_building = True if met_req == 0 else False
            if met_research and met_resource and met_item and met_unit and met_idle and met_building:
                for d_loc in mData['units'][x]['trainable_in']:
                    if 'buildings' in d_req.keys():
                        for key, value in d_req['buildings'].items():
                            if key in pseudo_tc and value <= selection[d_loc]['tc_level']:
                                multiplier = selection[d_loc]['tc_total'] + \
                                             ((selection[d_loc]['tc_combo'] - selection[d_loc]['tc_total']) / 10)
                                if mData['units'][x]['type'] in ('BattleDragon', 'SwiftStrikeDragon') \
                                        and d_loc == 'capital':
                                    multiplier += (multiplier / 100) * d_rookery
                                if d_pop > d_max_queue:
                                    d_pop = d_max_queue
                                my_dict = {'troop': mData['units'][x]['type'], 'id': cData[d_loc]['city']['id'],
                                           'tc_level': selection[d_loc]['tc_level'], 'quantity': d_pop,
                                           'tc_total': selection[d_loc]['tc_total'], 'trainable': d_max_queue,
                                           'time': mData['units'][x]['time'], 'multiplier': multiplier,
                                           'power': mData['units'][x]['stats']['power'], 'location': d_loc}
                                d_list.append(my_dict)
                                break
    d_troop = None
    selection.clear()
    if not d_list:
        nothing_to_do(title, 'Select Troop To Train', 'Trainable Troops')
        return
    elif len(d_list) == 1:
        d_troop = d_list[0]['troop']
    else:
        for x in range(len(d_list)):
            if d_list[x]['troop'] not in selection.keys():
                selection[d_list[x]['troop']] = t(d_list[x]['troop'])

    # Select Troop To Train
    while d_troop is None:
        screen_update(title, 'Select Troop To Train')
        ctr_it('~~~ Available Troops ~~~')
        display_it(selection)
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if all(i.isalpha() or i == ' ' for i in d_select):
                if d_select.lower() == 'exit':
                    return
                else:
                    for key, value in selection.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            d_troop = key
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    selection.clear()
    if len(d_list) == 1:
        d_location = d_list[0]['location']
    else:
        d_location = None
        for x in range(len(d_list)):
            if t(d_list[x]['location']) not in selection.keys():
                my_dict = {'location': d_list[x]['location'],
                           'tc_level': d_list[x]['tc_level'],
                           'tc_total': d_list[x]['tc_total'],
                           'time': int(d_list[x]['time'] / d_list[x]['multiplier'])}
                selection[t(d_list[x]['location'])] = my_dict

        # Select Location To Train
        a, b, c, d, len_a, len_b, len_c, len_d = ['Location', 'Level', 'Total', 'Time', 8, 5, 5, 4]
        for x in selection.keys():
            if len(x) > len_a:
                len_a = len(x)
            if len('{0}'.format(selection[x]['tc_level'])) > len_b:
                len_b = len('{0}'.format(selection[x]['tc_level']))
            if len('{0}'.format(selection[x]['tc_total'])) > len_c:
                len_c = len('{0}'.format(selection[x]['tc_total']))
            if len(cvt_time(selection[x]['time'])) > len_d:
                len_d = len(cvt_time(selection[x]['time']))
        while d_location is None:
            screen_update(title, 'Select Location To Train')
            ctr_it('Troop: {0}'.format(t(d_troop)))
            ctr_it(' ')
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, len_a, b, len_b, c, len_c, d, len_d))
            ctr_it('{0}  {1}  {2}  {3}'.format('~' * len_a, '~' * len_b, '~' * len_c, '~' * len_d))
            for x in sorted(selection.keys()):
                ctr_it('{0:<{1}}  {2:^{3}}  {4:^{5}}  {6:>{7}}'.format(
                        x, len_a, selection[x]['tc_level'], len_b, selection[x]['tc_total'], len_c,
                        cvt_time(selection[x]['time']), len_d))
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 3:
                if all(i.isalpha() or i == ' ' for i in d_select):
                    if d_select.lower() == 'exit':
                        return
                    else:
                        for x in sorted(selection.keys()):
                            if d_select.lower() in x.lower() or d_select.lower() == x.lower():
                                d_location = selection[x]['location']
    d_list[:] = [d for d in d_list if d.get('location') == d_location]
    d_max_queue = 1 if d_list[0]['quantity'] == 1 else 0

    # Set Training Queue Size
    while d_max_queue is 0:
        screen_update(title, 'Set Quantity for Training Queue')
        ctr_it('Troop: {0}   Location: {1}'.format(t(d_troop), t(d_location)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ Available Options ~~~')
        ctr_it('1 to {0}'.format(d_list[0]['quantity']), suffix=True)
        print(' NOTE: Enter MAX for maximum queue')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 1:
            if d_select.lower() == 'exit':
                return
            elif d_select.lower() == 'max':
                d_max_queue = d_list[0]['quantity']
            elif d_select.isnumeric():
                if int(d_select) in range(1, d_list[0]['quantity'] + 1):
                    d_max_queue = int(d_select)
    d_list[0]['quantity'] = d_max_queue
    selection.clear()

    # Set Speed Items
    a, b, c, d, len_a, len_b, len_c, len_d = ['Speed Item', 'Description', 'Available', 'Use', 10, 11, 9, 3]
    selection = [{'item': 'TestroniusInfusion', 'time': 0.99}, {'item': 'TestroniusDeluxe', 'time': 0.5},
                 {'item': 'TestroniusPowder', 'time': 0.3}, {'item': 'Blitz', 'time': 345600},
                 {'item': 'Blast', 'time': 216000}, {'item': 'Bolt', 'time': 86400}, {'item': 'Bore', 'time': 54000},
                 {'item': 'Bounce', 'time': 28800}, {'item': 'Leap', 'time': 9000}, {'item': 'Jump', 'time': 3600},
                 {'item': 'Skip', 'time': 900}, {'item': 'Hop', 'time': 300}, {'item': 'Blink', 'time': 60}]
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['item'] in pData['items']:
            if pData['items'][selection[x]['item']] > 0:
                if selection[x]['time'] < 1:
                    y = '{0}% Reduced'.format(int(selection[x]['time'] * 100))
                else:
                    y = '{0}'.format(cvt_time(selection[x]['time'], show_seconds=False))
                my_dict = {'item': selection[x]['item'], 'qty': pData['items'][selection[x]['item']],
                           'time': selection[x]['time'], 'desc': y, 'use': 0}
                d_speed.append(my_dict)
                if len(t(selection[x]['item'])) > len_a:
                    len_a = len(t(selection[x]['item']))
                if len(y) > len_b:
                    len_b = len(y)
                z = '{0:,}'.format(pData['items'][selection[x]['item']])
                if len(z) > len_c:
                    len_c = len(str(pData['items'][selection[x]['item']]))
    while True:
        screen_update(title, 'Set Speed Items To Use For Each Queue')
        ctr_it('Troop: {0}   Location: {1}   Queue Size: {2:,}'.format(
                t(d_troop), t(d_location), d_list[0]['quantity']))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, len_a, b, len_b, c, len_c, d, len_d))
        ctr_it('{0}  {1}  {2}  {3}'.format('-' * len_a, '-' * len_b, '-' * len_c, '-' * len_d))
        reduced_time = (d_list[0]['time'] / d_list[0]['multiplier']) * d_list[0]['quantity']
        for x in range(len(d_speed)):
            ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                    t(d_speed[x]['item']), len_a, d_speed[x]['desc'], len_b, d_speed[x]['qty'], len_c,
                    d_speed[x]['use'], len_d))
            if d_speed[x]['use'] != 0:
                if d_speed[x]['time'] < 1:
                    for y in range(d_speed[x]['use']):
                        reduced_time *= (1 - d_speed[x]['time'])
                else:
                    for y in range(d_speed[x]['use']):
                        reduced_time -= d_speed[x]['time']
        else:
            reduced_time = 0 if reduced_time < 0 else cvt_time(reduced_time)
            ctr_it('Training Duration: {0}'.format(reduced_time), prefix=True, suffix=True)
        if reduced_time != 0:
            print(' NOTE: Enter ITEM=QUANTITY (e.g. Infusion=3)')
        else:
            print(' Enter NEXT to proceed...')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 3:
            if d_select.lower() == 'exit':
                return
            elif d_select.lower() == 'next' and reduced_time == 0:
                break
            else:
                try:
                    i_item, i_qty = d_select.split('=')
                    if i_item.replace(' ', '').isalpha() and i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() in t(d_speed[x]['item']).lower() or \
                                                    i_item.lower() == t(d_speed[x]['item']).lower() and \
                                                    int(i_qty) < d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                except(TypeError, ValueError):
                    sleep(1)
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_max_queue = int(d_list[0]['trainable'] / d_list[0]['quantity'])
    speed_cut_off = 0
    for x in range(len(d_speed)):
        if d_max_queue > (d_speed[x]['qty'] / d_speed[x]['use']):
            d_max_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
        if 'Testronius' not in d_speed[x]['item']:
            speed_cut_off += d_speed[x]['time']
    d_batch = 1 if d_max_queue == 1 else None

    # Set Number Of Batches
    while d_batch is None:
        screen_update(title, 'Set Training Batches')
        ctr_it('Troop: {0}   Location: {1}   Queue Size: {2:,}'.format(
                t(d_troop), t(d_location), d_list[0]['quantity']))
        ctr_it(' ')
        d_batch = set_batch(d_max_queue + 1, 'batches to train?')
        if d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, 'Set Delay Between Game Requests')
        ctr_it('Troop: {0}   Location: {1}   Queue Size: {2:,}'.format(
                t(d_troop), t(d_location), d_list[0]['quantity']))
        ctr_it('Target Batches: {0:,}'.format(d_batch))
        d_delay = set_delay()
        if d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, 'Proceed With Troop Training?')
        ctr_it('Troop: {0}   Location: {1}   Queue Size: {2:,}'.format(
                t(d_troop), t(d_location), d_list[0]['quantity']))
        ctr_it('Target Batches: {0:,}   Delay: {1}s'.format(d_batch, d_delay))
        d_proceed = proceed_run('training of troops?')
        if d_proceed == 'exit':
            return

    # Train Troops
    global realm
    speeds_used = {}
    d_start = time()
    d_conn = http.client.HTTPConnection(realm, 80)
    for x in range(d_batch):
        dur = -1
        job_id = 0
        for item in d_speed:
            for y in range(item['use']):
                if 'Testronius' in item['item'] and speed_cut_off >= dur != -1 or dur == 0:
                    break
                screen_update(title, 'Progress Report...')
                ctr_it('Troop: {0}   Location: {1}   Queue Size: {2:,}'.format(
                        t(d_troop), t(d_location), d_list[0]['quantity']))
                ctr_it('Target Batches: {0:,}   Delay: {1}s   Elapsed Time: {2}'.format(
                        d_batch, d_delay, cvt_time(time() - d_start)))
                div_line('-')
                progress(x + 1, d_batch, 'Training Batch {0:,} of {1:,}'.format(x + 1, d_batch))
                if speeds_used:
                    init = 'Initializing Queue...' if dur == -1 else 'Remaning Duration: {0}'.format(cvt_time(dur))
                    progress(y + 1, item['use'], 'Using {0}'.format(t(item['item'])), init)
                    ctr_it('~~~ Speed Items Used ~~~', prefix=True)
                    for key, value in speeds_used.items():
                        ctr_it('{0}: {1:,}'.format(t(key), value))
                    if x > 0:
                        ctr_it('~~~ Troops Trained ~~~', prefix=True)
                        ctr_it('{0:,}'.format(d_list[0]['quantity'] * x))
                        ctr_it('~~~ Power Gained ~~~', prefix=True)
                        ctr_it('{0:,}'.format(d_list[0]['quantity'] * x * d_list[0]['power']))
                else:
                    progress(0, 1, 'Initializing...')
                if dur == -1:
                    x_param = 'units%5Bquantity%5D={0}&units%5Bunit%5Ftype%5D={1}&%5Fmethod=post&'.format(
                            d_list[0]['quantity'], d_troop)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            main_json = web_ops(d_conn, 'cities/{0}/units'.format(d_list[0]['id']), x_param)
                            result = main_json['result']['success']
                            if result:
                                job_id = main_json['result']['job']['id']
                                dur = int(main_json['result']['job']['duration'])
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                if dur > (d_delay + 1):
                    x_param = 'job%5Fid={0}&%5Fmethod=delete&'.format(job_id)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            item_json = web_ops(d_conn, 'player_items/{0}'.format(item['item']), x_param)
                            result = item_json['result']['success']
                            if result:
                                dur = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                if dur < 0:
                                    dur = 0
                                if t(item['item']) in speeds_used:
                                    speeds_used[t(item['item'])] += 1
                                else:
                                    speeds_used[t(item['item'])] = 1
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
    screen_update(title, 'Summary Report')
    ctr_it('Troop: {0}   Location: {1}   Queue Size: {2:,}'.format(t(d_troop), t(d_location), d_list[0]['quantity']))
    ctr_it('Target Batches: {0:,}   Delay: {1}s'.format(d_batch, d_delay))
    div_line('-')
    progress(1, 1, 'Training Completed Successfully!', 'Process completed in {0}'.format(cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ Speed Items Used ~~~', prefix=True)
        for key, value in speeds_used.items():
            ctr_it('{0}: {1:,}'.format(t(key), value))
    ctr_it('~~~ Troops Trained ~~~', prefix=True)
    ctr_it('{0:,}'.format(d_list[0]['quantity'] * d_batch))
    ctr_it('~~~ Power Gained ~~~', prefix=True)
    ctr_it('{0:,}'.format(d_list[0]['quantity'] * d_batch * d_list[0]['power']))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print('Refreshing... Please wait!')
    get_data(title, data3=True, data5=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def revive_soul(title):
    # Initialize
    screen_update(title, 'Select Souls To Revive')
    ctr_it(' Initializing...')
    d_list = list()
    dp_level, dp_total, dp_combo = [0, 0, 0]
    try:
        spec = cData['spectral']['city']['buildings']
    except KeyError:
        spec = None
    if spec:
        be = cData['capital']['city']['resources']['blue_energy']
        for x in range(len(spec)):
            if spec[x]['type'] == 'DarkPortal':
                if dp_level < spec[x]['level']:
                    dp_level = spec[x]['level']
                dp_total += 1
                dp_combo += spec[x]['level']
        for key, value in cData['capital']['city']['souls'].items():
            for x in range(len(mData['units'])):
                if key == mData['units'][x]['type']:
                    if dp_level >= mData['units'][x]['requirements']['spectral']['buildings']['DarkPortal'] and be >= \
                            mData['units'][x]['requirements']['spectral']['resources']['blue_energy']:
                        y = int(be / mData['units'][x]['requirements']['spectral']['resources']['blue_energy'])
                        if y > value:
                            y = value
                        my_dict = {'troop': key, 'total': value, 'max': y}
                        d_list.append(my_dict)
    if not d_list:
        nothing_to_do(title, 'Select Souls To Revive', 'no souls')
        return
    if len(d_list) == 1:
        d_troop = d_list[0]['troop']
    else:
        d_troop = None
        a, b, c, len_a, len_b, len_c = ['Souls', 'Total', 'Revivable', 5, 5, 9]
        for x in range(len(d_list)):
            if len(t(d_list[x]['troop'])) > len_a:
                len_a = len(t(d_list[x]['troop']))
            if len('{0:,}'.format(d_list[x]['total'])) > len_b:
                len_b = len('{0:,}'.format(d_list[x]['total']))
            if len('{0:,}'.format(d_list[x]['max'])) > len_c:
                len_c = len('{0:,}'.format(d_list[x]['max']))
        while d_troop is None:
            screen_update(title, 'Select Souls To Revive')
            ctr_it('~~~ Available Souls ~~~')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, len_a, b, len_b, c, len_c))
            ctr_it('{0}  {1}  {2}'.format('~' * len_a, '~' * len_b, '~' * len_c))
            for x in range(len(d_list)):
                ctr_it('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                        t(d_list[x]['troop']), len_a, d_list[x]['total'], len_b, d_list[x]['max'], len_c))
            div_line()
            d_select = input(' Enter selection : ')
            if len(d_select) >= 3:
                if d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() in t(d_list[x]['troop']).lower() or d_select.lower() == t(
                                d_list[x]['troop']).lower():
                            d_troop = d_list[x]['troop']
                            break
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    print(d_list)


# -------------------------------------------------------------------------------------------------------------------- #

def switch_realm(title, realm_no=0, c_no=0):
    global d_rn, d_cn, realm, cookie, std_param, d_si
    d_rn = realm_no
    d_cn = c_no
    get_realm_info(title)

    # Fixed Variables
    d_si = b2a_hex(os.urandom(16))
    realm = 'realm{0}.c{1}.castle.rykaiju.com'.format(d_rn, d_cn)
    cookie = 'dragons={0}'.format(d_si)
    std_param = 'dragon%5Fheart={0}&user%5Fid={1}&version=overarch&%5Fsession%5Fid={2}'.format(
            d_dh, d_ui, d_si)

    # Refresh Data Files
    refresh_data(title)


# -------------------------------------------------------------------------------------------------------------------- #

def refresh_data(title):
    global pData, mData, fData, pfData, cData, tData
    get_data(title, True, True, True, True, True, True)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      MENU CLASS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
def menu():
    module_dict = {create_equipment: 'Craft Equipment', forge_ingredient: 'Forge Ingredients',
                   farm_mission: 'Farm Mission', open_chest: 'Open Chests', unpack_arsenal: 'Unpack Arsenal',
                   upgrade_building: 'Upgrade Buildings', fill_building: 'Fill Building Slots',
                   train_troop: 'Train Troops', revive_soul: 'Revive Souls'}
    system_dict = {switch_realm: 'Switch Realm', refresh_data: 'Refresh Game', enter_script: 'Switch Account'}

    while True:
        screen_update('MAIN MENU', 'What Would You Like To Do?')
        ctr_it('~~~ Available Modules ~~~')
        display_it(module_dict)
        print(' ')
        ctr_it('~~~ System Modules ~~~')
        display_it(system_dict)
        print('\n Select from the list or enter QUIT to quit script')
        div_line()
        d_select = input(' Enter selection : ')
        if len(d_select) >= 2:
            if all(x.isalpha() or x == ' ' for x in d_select):
                if d_select.lower() == 'quit':
                    exit_script()
                else:
                    for key, value in module_dict.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            key(value.upper())
                    for key, value in system_dict.items():
                        if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                            key(value.upper())


# -------------------------------------------------------------------------------------------------------------------- #
#                                                         MAIN                                                         #
# -------------------------------------------------------------------------------------------------------------------- #

# Initialize Global Variables
d_ui, d_rn, d_cn = [0, 0, 0]
d_dh, d_si, realm, cookie, std_param = ['', '', '', '', '']
pData, mData, fData, pfData, cData, tData = ['', '', '', '', '', '']

# Launch Menu
if __name__ == '__main__':
    enter_script('INITIALIZING SCRIPT')
    menu()

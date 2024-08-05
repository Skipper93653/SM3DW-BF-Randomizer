# -*- coding: utf-8 -*-

"""
Super Mario 3D World (+ Bowser's Fury) Randomizer - A stage randomizer for Super Mario 3D World (Switch).
Copyright (C) 2024  Toby Bailey

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os  # For OS files
import shutil  # For OS files
import time  # For time calculations
import json  # For saving settings
import hashlib  # For file verification
import dearpygui.dearpygui as dpg  # User interface
import numpy as np  # Random number generation
from datetime import datetime  # For seed history
from oead import *  # For common Nintendo EAD/EPD file formats


# Level randomizer
def randomizer():
    bar = 0  # Progress bar progress
    dpg.configure_item("randoinit", enabled=False, label="Randomizing...")
    dpg.configure_item('seed', enabled=False)
    dpg.configure_item('dirbutt', enabled=False)
    dpg.configure_item('rdirbutt', enabled=False)
    dpg.configure_item("progress", default_value=0)
    dpg.hide_item('t2')
    dpg.hide_item('t3')
    user_data = [dpg.get_value('dirtext'), dpg.get_value('rdirtext')]

    # Setting up the random number generation with a seed
    if len(str(dpg.get_value("seed"))) == 0:
        seedRNG = time.time_ns()  # If no seed is entered, then it defaults to time since epoch.
    else:
        try:
            seedRNG = int(dpg.get_value("seed"))  # Try to cast the input as an integer.
        except ValueError:
            seedRNG = 0
            for i in str(dpg.get_value("seed")):
                if seedRNG == 0:
                    seedRNG += ord(i)
                else:
                    seedRNG *= ord(i)
    rng = np.random.default_rng(seedRNG)

    # SystemData Path
    oPath = os.path.join(user_data[0], 'SystemData')  # Original game path

    # Open StageList.szs and grab the BYML, convert to YML, open it as a list.
    print('Opening StageList.szs')
    with open(os.path.join(oPath, "StageList.szs"), "rb") as f:
        archive = Sarc(yaz0.decompress(f.read()))  # Decompress and load SARC
    endianness = archive.get_endianness()
    StageListNew = byml.to_text(byml.from_binary(archive.get_file("StageList.byml").data)).split('\n')  # Load BYML file (Wii U file breaks here)
    StageListNew.pop()
    StageListOld = StageListNew.copy()
    print('Opened StageList.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    # StageData Path
    sPath = os.path.join(user_data[0], 'StageData')
    rPath = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'SystemData')  # Randomizer path
    srPath = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'StageData')
    os.makedirs(rPath)
    os.makedirs(srPath)
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    worlds = [['CourseSelectW1Zone.szs', ['DofParam_obj10.bagldof',
                                          'DofParam_obj9.bagldof',
                                          'DofParam_obj11.bagldof',
                                          'CourseSelectW1ZoneDesign.byml',
                                          'DofParam_obj6.bagldof',
                                          'CourseSelectW1ZoneMap.byml',
                                          'DofParam_obj12.bagldof',
                                          'CameraParam.byml',
                                          'DofParam_obj7.bagldof',
                                          'CourseSelectW1ZoneSound.byml',
                                          'DofParam_obj8.bagldof']],
              ['CourseSelectW2Zone.szs', ['DofParam_obj4.bagldof',
                                          'CourseSelectW2ZoneMap.byml',
                                          'DofParam_obj9.bagldof',
                                          'DofParam_obj5.bagldof',
                                          'CourseSelectW2ZoneSound.byml',
                                          'DofParam_obj6.bagldof',
                                          'CameraParam.byml',
                                          'DofParam_obj7.bagldof',
                                          'DofParam_obj3.bagldof',
                                          'CourseSelectW2ZoneDesign.byml',
                                          'DofParam_obj8.bagldof']],
              ['CourseSelectW3Zone.szs', ['CourseSelectW3ZoneDesign.byml',
                                          'CourseSelectW3ZoneMap.byml',
                                          'CameraParam.byml',
                                          'DofParam_obj27.bagldof',
                                          'CourseSelectW3ZoneSound.byml',
                                          'DofParam_obj28.bagldof']],
              ['CourseSelectW4Zone.szs', ['DofParam_obj4.bagldof',
                                          'CourseSelectW4ZoneMap.byml',
                                          'DofParam_obj5.bagldof',
                                          'CourseSelectW4ZoneSound.byml',
                                          'DofParam_obj6.bagldof',
                                          'CameraParam.byml',
                                          'CourseSelectW4ZoneDesign.byml']],
              ['CourseSelectW5Zone.szs', ['DofParam_obj4.bagldof',
                                          'CourseSelectW5ZoneDesign.byml',
                                          'DofParam_obj5.bagldof',
                                          'DofParam_obj6.bagldof',
                                          'CameraParam.byml',
                                          'CourseSelectW5ZoneMap.byml',
                                          'DofParam_obj3.bagldof',
                                          'CourseSelectW5ZoneSound.byml']],
              ['CourseSelectW6Zone.szs', ['DofParam_obj18.bagldof',
                                          'DofParam_obj14.bagldof',
                                          'DofParam_obj10.bagldof',
                                          'DofParam_obj9.bagldof',
                                          'DofParam_obj19.bagldof',
                                          'DofParam_obj15.bagldof',
                                          'CourseSelectW6ZoneMap.byml',
                                          'DofParam_obj11.bagldof',
                                          'CourseSelectW6ZoneSound.byml',
                                          'DofParam_obj6.bagldof',
                                          'DofParam_obj16.bagldof',
                                          'CourseSelectW6ZoneDesign.byml',
                                          'DofParam_obj12.bagldof',
                                          'CameraParam.byml',
                                          'DofParam_obj17.bagldof',
                                          'DofParam_obj13.bagldof',
                                          'DofParam_obj8.bagldof']],
              ['CourseSelectW7Zone.szs', ['CourseSelectW7ZoneDesign.byml',
                                          'DofParam_obj19.bagldof',
                                          'DofParam_obj22.bagldof',
                                          'CameraParam.byml',
                                          'DofParam_obj23.bagldof',
                                          'CourseSelectW7ZoneMap.byml',
                                          'CourseSelectW7ZoneSound.byml']],
              ['CourseSelectW8Zone.szs', ['DofParam_obj130.bagldof',
                                          'DofParam_obj129.bagldof',
                                          'DofParam_obj131.bagldof',
                                          'CourseSelectW8ZoneMap.byml',
                                          'CourseSelectW8ZoneSound.byml',
                                          'CourseSelectW8ZoneDesign.byml',
                                          'DofParam_obj132.bagldof',
                                          'CameraParam.byml',
                                          'DofParam_obj133.bagldof']],
              ['CourseSelectS1Zone.szs', ['CourseSelectS1ZoneSound.byml',
                                          'CameraParam.byml',
                                          'CourseSelectS1ZoneMap.byml']]]
    worldArchives = []
    mapYMLs = []

    # Open each world map file and convert the map BYML into a readable format.
    for i in worlds:
        print('Opening ' + i[0])
        with open(os.path.join(sPath, i[0]), 'rb') as f:
            worldArchives.append(Sarc(yaz0.decompress(f.read())))
        mapYMLs.append(byml.to_text(byml.from_binary(worldArchives[-1].get_file(i[0][:i[0].index('.')] + 'Map.byml').data)).split('\n'))
        mapYMLs[-1].pop()
        print('Opened ' + i[0])
        bar += 1
        dpg.configure_item("progress", default_value=bar / 172)

    # Creating base variables to be used and iterated on in the randomizer loop
    worldNo = 1
    currentGreenStars = 0
    currentGreenStarsOld = 0
    GreenStarLockHistory = []
    GreenStarLockHistory2 = []  # Only used when the user has selected 'Fully random' for the green star lock setting

    # 154 different stages in total. The next two code blocks are making several checks to make sure nothing gets
    # broken in the actual stage shuffling process
    stageID_order = []
    for i in range(1, 34):
        stageID_order.append(i)
    for i in range(35, 62):
        stageID_order.append(i)
    for i in range(67, 81):
        stageID_order.append(i)
    for i in range(82, 97):
        stageID_order.append(i)
    for i in range(98, 115):
        stageID_order.append(i)
    for i in range(116, 155):
        stageID_order.append(i)
    print(stageID_order)
    rstageID_order = rng.choice(stageID_order, size=len(stageID_order), replace=False)
    ready = False
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    # This loop happens when stageID generates a special level when stageNo is currently a castle stage and forces
    # stageID to randomize again until it's not a special level (basically until it gives you a stage where it's
    # possible to give you the golden goal pole).
    while not ready:
        ready = True
        for i in stageID_order:
            for j in rstageID_order:
                if (i == 9 or i == 20 or i == 33 or i == 46 or i == 61 or i == 80 or i == 96 or i == 114) and (
                        j == 6 or j == 7 or j == 8 or j == 10 or j == 11 or j == 17 or j == 18 or j == 21 or j == 22 or
                        j == 30 or j == 31 or j == 32 or j == 35 or j == 36 or j == 43 or j == 44 or j == 47 or j == 48
                        or j == 49 or j == 57 or j == 58 or j == 59 or j == 60 or j == 67 or j == 68 or j == 69 or
                        j == 77 or j == 78 or j == 82 or j == 83 or j == 84 or j == 93 or j == 94 or j == 95 or j == 98
                        or j == 99 or j == 100 or j == 101 or j == 109 or j == 110 or j == 111 or j == 116 or j == 128
                        or j == 129 or j == 130 or j == 152 or j == 153) and (stageID_order.index(i) == np.where(rstageID_order == j)[0]):
                    rstageID_order = rng.choice(stageID_order, size=len(stageID_order), replace=False)
                    ready = False
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    print('Random stage order:', rstageID_order)

    for stageNo in stageID_order:
        if stageNo == 12 or stageNo == 23 or stageNo == 38 or stageNo == 50 or stageNo == 70 or stageNo == 86 or stageNo == 102 or stageNo == 119 or stageNo == 131 or stageNo == 139 or stageNo == 151:
            worldNo += 1
        stageID = rstageID_order[stageID_order.index(stageNo)]
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 1] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 1]  # DoubleMarioNum
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 2] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 2]  # GhostBaseTime
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 3] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 3]  # GhostId
        GreenStarLock = StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4]  # GreenStarLock line
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 5] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 5]  # GreenStarNum
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 6] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 6]  # IllustItemNum
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 8]  # StageName
        currentGreenStarsOld += int(StageListOld[(StageListOld.index('  - CourseId: ' + str(stageNo))) + 5][-2:])
        GreenStarLockValue = int(currentGreenStars * int(GreenStarLock[GreenStarLock.index(':') + 2:]) / currentGreenStarsOld)  # For 'Random values'
        GreenStarLockHistory.append([stageNo, GreenStarLockValue])
        GreenStarLockHistory2.append([rng.choice([True, False], size=1, p=[float(dpg.get_value('pslider')), float(1 - dpg.get_value('pslider'))], replace=True), int(currentGreenStars * float(dpg.get_value('sslider')))])
        if stageNo == 114:
            GreenStarLockHistory2[-1][0] = True  # Force Bowser-Castle to have a star lock when setting is on 'Fully random'
        if dpg.get_value("star") == 'Disabled' or float(dpg.get_value('sslider')) == 0 or stageNo == 11 or stageNo == 22 or stageNo == 36 or stageNo == 48 or stageNo == 49 or stageNo == 68 or stageNo == 83 or stageNo == 99 or stageNo == 100 or stageNo == 113 or stageNo == 117 or stageNo == 118:
            # Remove all Green Star Locks when encountered
            print('Removing green star lock...')
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4] = '    GreenStarLock: 0'
            GreenStarLockHistory2[-1][0] = False
        elif dpg.get_value("star") == 'Random values':
            # Calculate a new green star lock based on the vanilla lock value and multiply it by the ratio of the new star count to the old star count up to that point
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4] = GreenStarLock[:GreenStarLock.index(':') + 2] + str(GreenStarLockValue)
            print('Changing green star lock value!')
        elif dpg.get_value("star") == 'Fully random':
            # Fully new star lock
            if GreenStarLockHistory2[-1][0]:
                print('Adding fully custom star lock...')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4] = GreenStarLock[:GreenStarLock.index(':') + 2] + str(GreenStarLockHistory2[-1][1])
            else:
                print('Removing green star lock...')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4] = '    GreenStarLock: 0'
        currentGreenStars += int(StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 5][-2:])

        if ('クッパ城' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] or '�N�b�p��' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10]) and stageNo != 113:
            print('Reached castle slot! Copying original StageType of this slot.')
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageNo))) + 10]  # Makes sure all castle slots are the same slots when the levels are randomized.
        else:
            # Making sure Gimmick stages, Captain Toad stages, Mystery Houses, Toad Houses, Stamp Houses, Roulettes, Blockades, and Golden Express have the correct StageType depending on the slot they are on after they are randomized.
            if 'KinopioBrigade' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                print('Captain Toad StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: キノピオ探検隊'  # StageType for Captain Toad levels.
            elif 'KinopioHouse' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                print('Toad House StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: キノピオの家'  # StageType for Toad Houses.
            elif 'FairyHouse' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                print('Stamp House StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: 妖精の家'  # StageType for Stamp Houses.
            elif 'RouletteRoomZone' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                # Making sure a roulette being randomized onto a roulette slot keeps the roulette StageType.
                if (stageNo == 10 or stageNo == 21 or stageNo == 35 or stageNo == 47 or stageNo == 67 or stageNo == 82 or stageNo == 98 or stageNo == 116 or stageNo == 130) and ((GreenStarLockHistory[-1][1] == 0 and dpg.get_value('star') == 'Random values') or (((GreenStarLockHistory2[-1][1] == 0 and GreenStarLockHistory2[-1][0]) or not GreenStarLockHistory2[-1][0]) and dpg.get_value('star') == 'Fully random')):
                    print('Roulette StageType fixed with Roulette StageType!')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: カジノ部屋'  # StageType for Roulettes.
                # A lucky house where the golden express usually is gets it the golden express stage type.
                elif stageNo == 57:
                    print('Roulette StageType fixed with Golden Express StageType!')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ゴールデンエクスプレス'  # StageType for Roulettes (カジノ部屋) is not used because they don't appear on the world map immediately which can cause progression issues. So the golden express is used instead.
                # To avoid a lucky house from being already active on the world map path, we use the Toad House StageType.
                else:
                    print('Roulette StageType fixed with Toad House StageType!')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: キノピオの家'  # StageType for Toad Houses.
            elif 'GoldenExpressStage' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                # Forcing golden express StageType when in a slot originally belonging to a roulette or the golden express itself
                if stageNo == 10 or stageNo == 21 or stageNo == 35 or stageNo == 47 or stageNo == 57 or stageNo == 67 or stageNo == 82 or stageNo == 98 or stageNo == 116 or stageNo == 130:
                    print('Golden Express StageType fixed!')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ゴールデンエクスプレス'  # StageType for golden express.
                # Forcing Toad Houses in other scenarios (see: lucky house reasoning)
                else:
                    print('Golden Express StageType fixed with Toad House!')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: キノピオの家'  # StageType for Toad Houses.
            elif 'MysteryHouse' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                print('Mystery House StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ミステリーハウス'  # StageType for MysteryHouses.
            elif 'GateKeeper' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                # If it is a boss blockade...
                if StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] == '    StageName: GateKeeperTentackLv1Stage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] == '    StageName: GateKeeperTentackLv2Stage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] == '    StageName: GateKeeperBossBunretsuLv1Stage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] == '    StageName: GateKeeperBossBunretsuLv2Stage':
                    print('Boss Blockade StageType fixed!')
                    if ((GreenStarLockHistory[-1][1] == 0 and dpg.get_value('star') == 'Random values') or (((GreenStarLockHistory2[-1][1] == 0 and GreenStarLockHistory2[-1][0]) or not GreenStarLockHistory2[-1][0]) and dpg.get_value('star') == 'Fully random')) and (stageNo != 7 and stageNo != 110):
                        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ゲートキーパー[GPあり]'  # StageType for Boss Blockades.
                    else:
                        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: 通常'  # StageType for normal levels.
                # If it is a normal boss blockade...
                else:
                    print('Blockade StageType fixed!')
                    if ((GreenStarLockHistory[-1][1] == 0 and dpg.get_value('star') == 'Random values') or (((GreenStarLockHistory2[-1][1] == 0 and GreenStarLockHistory2[-1][0]) or not GreenStarLockHistory2[-1][0]) and dpg.get_value('star') == 'Fully random')) and (stageNo != 7 and stageNo != 110):
                        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ゲートキーパー'  # StageType for Blockades.
                    else:
                        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ミステリーハウス'  # StageType for MysteryHouses.
            elif 'TouchAndMike' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] or 'KarakuriCastle' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]:
                print('Gimmick stage StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: DRC専用'
            # Fix certain stages having a StageType which breaks certain things.
            elif ('KinopioBrigade' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: キノピオ探検隊') or ('KinopioHouse' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and (StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: キノピオの家' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: 隠しキノピオの家' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: 隠し土管')) or ('FairyHouse' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: 妖精の家') or ('RouletteRoomZone' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: カジノ部屋') or ('GoldenExpressStage' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and (StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: ゴールデンエクスプレス')) or ('GateKeeper' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and (StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: ゲートキーパー[GPあり]' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: ゲートキーパー')) or ('MysteryHouse' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: ミステリーハウス') or (('TouchAndMike' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] or 'KarakuriCastle' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]) and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: DRC専用') or ('EnemyExpress' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] == '    StageType: クッパ城[列車通常]'):
                print('Non-\'special\' level with \'special\' StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: 通常'  # StageType for normal levels.
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 9] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID))) + 9]  # StageTimer

        StageName = StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8]
        StageID = StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 7]

        # These are placed into the world map files for the model names.
        # New
        if 'RouletteRoom' in StageName:
            MiniatureName = 'MiniatureBonusRoom'
        elif 'GateKeeperBoss' in StageName or 'GateKeeperTentack' in StageName:
            MiniatureName = 'MiniatureEventGateKeeper'
        elif 'GateKeeper' in StageName:
            MiniatureName = 'Miniature'+StageName[StageName.index(':')+2:-8]
        elif 'KinopioHouse' in StageName:
            MiniatureName = 'MiniatureKinopioHouse'
        elif 'FairyHouse' in StageName:
            MiniatureName = 'MiniatureFairyHouse'
        elif 'MysteryHouse' in StageName:
            MiniatureName = 'MiniatureMysteryBox'
        elif 'KinopioBrigade' in StageName:
            MiniatureName = 'MiniatureKinopioBrigade'
        elif 'Teresa' in StageName or 'WeavingShip' in StageName or 'Haunted' in StageName or 'Fog' in StageName:
            MiniatureName = 'MiniatureTeresaHouse'
        elif 'Arrange' in StageName:
            if 'BossParade' in StageName:
                MiniatureName = 'MiniatureArrangeBossParade'
            else:
                MiniatureName = 'Miniature'+StageName[StageName.index(':')+9:-5]
        elif 'Boss' in StageName or 'KillerTank' in StageName or 'BombTank' in StageName or 'KillerExpress' in StageName or 'KoopaChase' in StageName or 'KoopaLast' in StageName:
            if 'KoopaLast' in StageName:
                MiniatureName = 'MiniatureKoopaCastleW8'
            elif 'KoopaChaseLv2' in StageName:
                MiniatureName = 'MiniatureKoopaCastleW7'
            else:
                MiniatureName = 'MiniatureKoopaCastle'
        elif 'DashRidge' in StageName:
            MiniatureName = 'MiniatureDashRidgeStage'
        else:
            MiniatureName = 'Miniature'+StageName[StageName.index(':')+2:-5]

        if worldNo <= 8:
            mapYMLs_index = worldNo - 1
        else:
            mapYMLs_index = 8

        # Enumerating the YML to replace world map models to show the randomized stage.
        for i, elem in enumerate(mapYMLs[mapYMLs_index]):
            if StageID[StageID.index('S'):].lower() in elem.lower() and ((worldNo == 1 and '70' not in elem and '35' not in elem) or ((worldNo == 2 or worldNo == 4 or worldNo == 5 or worldNo >= 9) and '70' not in elem) or (worldNo == 3 and '70' not in elem and '101' not in elem) or (worldNo == 6 and '70' not in elem and '102' not in elem) or worldNo == 7 or (worldNo == 8 and '35' not in elem)):
                if 'ModelName: Miniature' in mapYMLs[mapYMLs_index][i - 4] and mapYMLs[mapYMLs_index][i + 11][mapYMLs[mapYMLs_index][i + 11].index(':') + 2:] == str(worldNo):
                    mapYMLs[mapYMLs_index][i - 4] = mapYMLs[mapYMLs_index][i - 4][:mapYMLs[mapYMLs_index][i - 4].index(':') + 2] + MiniatureName
                elif 'ModelName: Miniature' in mapYMLs[mapYMLs_index][i - 6] and mapYMLs[mapYMLs_index][i + 15][mapYMLs[mapYMLs_index][i + 15].index(':') + 2:] == str(worldNo):
                    mapYMLs[mapYMLs_index][i - 6] = mapYMLs[mapYMLs_index][i - 6][:mapYMLs[mapYMLs_index][i - 6].index(':') + 2] + MiniatureName
                if worldNo == 1 and StageID[StageID.index(':') + 2:] == '1':
                    if ' Rotate: ' in mapYMLs[mapYMLs_index][i - 2]:
                        mapYMLs[mapYMLs_index][i - 2] = mapYMLs[mapYMLs_index][i - 2][:mapYMLs[mapYMLs_index][i - 2].index(':') + 2] + '{X: 0.0, Y: -0.0, Z: 0.0}'  # Fix rotation for World 1-1
                    elif ' Rotate: ' in mapYMLs[mapYMLs_index][i - 4]:
                        mapYMLs[mapYMLs_index][i - 4] = mapYMLs[mapYMLs_index][i - 4][:mapYMLs[mapYMLs_index][i - 4].index(':') + 2] + '{X: 0.0, Y: -0.0,'
                        mapYMLs[mapYMLs_index][i - 3] = mapYMLs[mapYMLs_index][i - 3][:mapYMLs[mapYMLs_index][i - 3].index(':') + 2] + '0.0}'

        if stageNo == 114:
            changeTo = 'GoalPoleLast'
        elif stageNo == 9 or stageNo == 20 or stageNo == 33 or stageNo == 37 or stageNo == 46 or stageNo == 61 or stageNo == 80 or stageNo == 85 or stageNo == 96 or stageNo == 113 or stageNo == 117 or stageNo == 118 or stageNo == 127 or stageNo == 137 or stageNo == 150 or stageNo == 151:
            changeTo = 'GoalPoleSuper'
        else:
            changeTo = 'GoalPole'

        if stageID == 114:
            changeFrom = 'GoalPoleLast'
        elif stageID == 9 or stageID == 20 or stageID == 33 or stageID == 37 or stageID == 46 or stageID == 61 or stageID == 80 or stageID == 85 or stageID == 96 or stageID == 113 or stageID == 117 or stageID == 118 or stageID == 127 or stageID == 150 or stageID == 151:
            changeFrom = 'GoalPoleSuper'
        else:
            changeFrom = 'GoalPole'

        if StageName[StageName.index(':') + 2:] not in ['EnterCatMarioStage', 'SnowBallParkStage', 'ShortGardenStage', 'KillerExpressStage', 'SavannaRockStage', 'BombCaveStage', 'GearSweetsStage', 'EnemyExpressStage', 'ArrangeSavannaRockStage']:  # These stages are avoided as opening them causes a stack error due to recursive loops within the map BYML
            if changeFrom != changeTo:
                goalPoleChanges(changeTo, changeFrom, StageName[StageName.index(':') + 2:], sPath, srPath, endianness)  # Correct the Goal Pole at the end of the stages if possible.
            else:
                print('Goal Pole change unneeded.')
        else:
            print('Skipped due to stack overflow.')

        bar += 1
        dpg.configure_item("progress", default_value=bar / 172)

    print('Total Green Star Count: ' + str(currentGreenStars))
    print('Randomized stages!')

    # Creating new SZS filers with the modified files.
    print('Writing StageList.szs')
    writer = SarcWriter()
    writer.set_endianness(endianness)
    writer.files['StageList.byml'] = byml.to_binary(byml.from_text('\n'.join(StageListNew)), False, 2)  # Adding to SARC.
    data = writer.write()  # Write to SARC

    with open(os.path.join(rPath, "StageList.szs"), "wb") as randoSZS:
        randoSZS.write(yaz0.compress(data[1]))  # Compress with YAZ0 and write to the SZS.
    print('Written StageList.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    print('Writing world files:')

    for i in worlds:
        print('Writing ' + i[0])
        writer = SarcWriter()
        writer.set_endianness(endianness)
        for j in i[1]:
            if j == i[0][:i[0].index('.')] + 'Map.byml':
                writer.files[j] = byml.to_binary(byml.from_text('\n'.join(mapYMLs[worlds.index(i)])), False, 2)
            else:
                writer.files[j] = Bytes(worldArchives[worlds.index(i)].get_file(j).data)
        data = writer.write()

        with open(os.path.join(srPath, i[0]), 'wb') as f:
            f.write(yaz0.compress(data[1]))
        print('Written ' + i[0])
        bar += 1
        dpg.configure_item("progress", default_value=bar / 172)

    print('Finished writing world files.')

    musicRandomizer(rng, seedRNG, user_data)
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)
    langRandomizer(rng, seedRNG, user_data)
    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    # For seed history and non-spoiler text file
    if len(str(dpg.get_value('seed'))) == 0:
        stageID_Name = ['Seed: ' + str(seedRNG) + ' (Random seed, ' + version + ')\n\n']
    else:
        stageID_Name = ['Seed: ' + str(seedRNG) + ' (Set seed, ' + version + ')\n\n']
    stageID_Name.append('Settings:\n')
    stageID_Name.append('Speedrunner mode: ' + str(dpg.get_value('speedrun')) + '\n')
    stageID_Name.append('Generate spoiler file?: ' + str(dpg.get_value('spoil')) + '\n')
    stageID_Name.append('Randomize music?: ' + str(dpg.get_value('music')) + '\n')
    stageID_Name.append('Randomize language?: ' + str(dpg.get_value('lang')) + '\n')
    if str(dpg.get_value('star')) == 'Fully random':
        stageID_Name.append('Green star locks?: ' + str(dpg.get_value('star')) + '\n')
        stageID_Name.append('Green star lock probability: ' + str(dpg.get_value('pslider')) + '\n')
        stageID_Name.append('Green star lock strictness: ' + str(dpg.get_value('sslider')) + '\n\n')
    else:
        stageID_Name.append('Green star locks?: ' + str(dpg.get_value('star')) + '\n\n')
    for i in hashDict:
        try:
            with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', i[0]), 'rb') as f:
                hash_object = hashlib.md5(f.read())
                stageID_Name.append(i[0] + ' - ' + hash_object.hexdigest() + '\n')
        except FileNotFoundError:
            print(i[0] + ' not modified.')

    if dpg.get_value("spoil"):
        spoilerFile(StageListNew, seedRNG, dict(GreenStarLockHistory), GreenStarLockHistory2, user_data)
    else:
        print('Not generating spoiler file, only generating seed/settings/hash text file.')
        with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), str(seedRNG)+'.txt'), 'w', encoding='utf-8') as s:
            # Creating a new spoiler text file.
            s.write(''.join(stageID_Name)[:-1])

    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    with open('seedHistory.txt', 'a+') as h:
        # Seed History file
        h.seek(0)
        now = datetime.now()
        if len(h.read()) == 0:
            h.write(str(now.strftime("%Y-%m-%d")) + '\n' + ''.join(stageID_Name)[:-1])
        else:
            stageID_Name[0] = '\n\n-------------------------------------------------------------\n\n' + str(now.strftime("%Y-%m-%d")) + '\n' + stageID_Name[0]
            h.write(''.join(stageID_Name)[:-1])

    bar += 1
    dpg.configure_item("progress", default_value=bar / 172)

    dpg.configure_item("progress", default_value=1)
    dpg.configure_item('dirbutt', enabled=True)
    dpg.configure_item('rdirbutt', enabled=True)
    dpg.configure_item('seed', enabled=True)
    dpg.configure_item("randoinit", enabled=True, label="Randomize!")
    dpg.show_item('t2')
    dpg.show_item('t3')
    saveSettings()
    checkDirectory()

    if len(str(dpg.get_value('seed'))) == 0:
        dpg.set_value('popupSeed', 'Seed: ' + str(seedRNG) + ' (Random seed, ' + version + ')')
    else:
        dpg.set_value('popupSeed', 'Seed: ' + str(seedRNG) + ' (Set seed, ' + version + ')')
    dpg.set_value('popupSpeedrun', 'Speedrunner mode: ' + str(dpg.get_value('speedrun')))
    dpg.set_value('popupSpoil', "Generate spoiler file?: " + str(dpg.get_value('spoil')))
    dpg.set_value('popupMusic', "Randomize music?: " + str(dpg.get_value('music')))
    dpg.set_value('popupLang', "Randomize language?: " + str(dpg.get_value('lang')))
    dpg.set_value('popupStar', "Green star locks: " + str(dpg.get_value('star')))
    if str(dpg.get_value('star')) == 'Fully random':
        dpg.set_value('popupPslider', "Green star lock probability: " + str(dpg.get_value('pslider')))
        dpg.show_item('popupPslider')
        dpg.set_value('popupSslider', "Green star lock strictness: " + str(dpg.get_value('sslider')))
        dpg.show_item('popupSslider')
    else:
        dpg.set_value('popupPslider', "")
        dpg.hide_item('popupPslider')
        dpg.set_value('popupSslider', "")
        dpg.hide_item('popupSslider')

    print('Randomization complete!')
    dpg.configure_item("popup", show=True)


# Goal pole changes
def goalPoleChanges(changeTo, changeFrom, StageName, sPath, srPath, endianness):
    # Dictionary keyed by the StageName from the StageList which then points to a list with the first index being the file name of the Goal Pole area with the second index being another list with every file within the file of the first index.
    try:
        stages = {'EnterCatMarioStage': ['EnterCatMarioStage.szs', ['DofParam_obj14.bagldof',
                                                                    'DofParam_obj0.bagldof',
                                                                    'EnterCatMarioStageDesign.byml',
                                                                    'YFog.baglfog',
                                                                    'EnterCatMarioStageSound.byml',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'CameraParam2.byml',
                                                                    'DofParam_obj2.bagldof',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DofParam_obj7.bagldof',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'DofParam_obj17.bagldof',
                                                                    'EnterCatMarioStageMap.byml',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'Fog.baglfog',
                                                                    'UnitPointIlluminant.baglcube']],
                  'NokonokoCaveStage': ['NokonokoCaveStage.szs', ['NokonokoCaveStageSound.byml',
                                                                  'NokonokoCaveStageDesign.byml',
                                                                  'YFog.baglfog',
                                                                  'DofParam_obj25.bagldof',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'DofParam_obj6.bagldof',
                                                                  'DofParam_obj36.bagldof',
                                                                  'DofParam_obj26.bagldof',
                                                                  'DofParam_obj32.bagldof',
                                                                  'DefaultParam.baglblm',
                                                                  'DefaultParam.baglexp',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'CameraParam.byml',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'DofParam_obj33.bagldof',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'Fog.baglfog',
                                                                  'NokonokoCaveStageMap.byml',
                                                                  'CaveZone.baglssao',
                                                                  'UnitPointIlluminant.baglcube',
                                                                  'Default.baglssao',
                                                                  'GraphicsStress.baglstress']],
                  'ClimbMountainStage': ['ClimbMountainStage.szs', ['DofParam_obj4.bagldof',
                                                                    'ClimbMountainStageDesign.byml',
                                                                    'DofParam_obj10.bagldof',
                                                                    'DofParam_obj9.bagldof',
                                                                    'DofParam_obj5.bagldof',
                                                                    'DofParam_obj1.bagldof',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'ClimbMountainStageSound.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'ClimbMountainStageMap.byml',
                                                                    'UnitPointIlluminant.baglcube']],
                  'DownRiverStage': ['DownRiverStage.szs', ['DofParam_obj18.bagldof',
                                                            'DofParam_obj4.bagldof',
                                                            'DownRiverStageMap.byml',
                                                            'DofParam_obj19.bagldof',
                                                            'DofParam_obj5.bagldof',
                                                            'DirectionalLight.bagldirlit',
                                                            'LightStreak.baglgodray',
                                                            'DownRiverStageSound.byml',
                                                            'DefaultParam.baglblm',
                                                            'DefaultParam.baglexp',
                                                            'AreaParamList.baglapl',
                                                            'CubeMapMgr.baglcube',
                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                            'CameraParam.byml',
                                                            'DepthShadow.bagldptsdw',
                                                            'CategoryLightInfo.bagllitinfostandard',
                                                            'UnitPointIlluminant.baglcube',
                                                            'DownRiverStageDesign.byml']],
                  'FlipCircusStage': ['FlipCircusStage.szs', ['DofParam_obj74.bagldof',
                                                              'MirrorRendering.baglmirror',
                                                              'YFog.baglfog',
                                                              'DirectionalLight.bagldirlit',
                                                              'FlipCircusStageDesign.byml',
                                                              'FlipCircusStageMap.byml',
                                                              'FlipCircusStageSound.byml',
                                                              'LightStreak.baglgodray',
                                                              'GodRay.baglgodray',
                                                              'DefaultParam.baglblm',
                                                              'DefaultParam.baglexp',
                                                              'AreaParamList.baglapl',
                                                              'CubeMapMgr.baglcube',
                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                              'CameraParam.byml',
                                                              'DepthShadow.bagldptsdw',
                                                              'DofParam_obj33.bagldof',
                                                              'CategoryLightInfo.bagllitinfostandard',
                                                              'DofParam_obj13.bagldof',
                                                              'Fog.baglfog',
                                                              'UnitPointIlluminant.baglcube',
                                                              'GraphicsStress.baglstress']],
                  'KoopaChaseLv1Stage': ['KoopaChaseLv1Stage.szs', ['KoopaChaseLv1StageSound.byml',
                                                                    'DofParam_obj14.bagldof',
                                                                    'DofParam_obj20.bagldof',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'KoopaChaseLv1StageMap.byml',
                                                                    'KoopaChaseLv1StageDesign.byml',
                                                                    'LightStreak.baglgodray',
                                                                    'DofParam_obj2.bagldof',
                                                                    'GodRay.baglgodray',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'DofParam_obj13.bagldof',
                                                                    'Fog.baglfog',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'GraphicsStress.baglstress']],
                  'SideWaveDesertStage': ['SideWaveDesertStage.szs', ['DofParam_obj0.bagldof',
                                                                      'DofParam_obj9.bagldof',
                                                                      'YFog.baglfog',
                                                                      'BonusRoom.baglssao',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'DofParam_obj11.bagldof',
                                                                      'SideWaveDesertStageDesign.byml',
                                                                      'SideWaveDesertStageSound.byml',
                                                                      'DofParam_obj12.bagldof',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'CameraParam.byml',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'DofParam_obj13.bagldof',
                                                                      'Fog.baglfog',
                                                                      'SideWaveDesertStageMap.byml',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'Default.baglssao',
                                                                      'DofParam_obj8.bagldof']],
                  'TouchAndMikeStage': ['TouchAndMikeSecondZone.szs', ['DofParam_obj1.bagldof',
                                                                       'TouchAndMikeSecondZoneMap.byml',
                                                                       'CameraParam.byml',
                                                                       'TouchAndMikeSecondZoneDesign.byml']],
                  'ShadowTunnelStage': ['ShadowTunnelStage.szs', ['DofParam_obj10.bagldof',
                                                                  'YFog.baglfog',
                                                                  'ShadowTunnelStageDesign.byml',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'DofParam_obj11.bagldof',
                                                                  'GoalArea.baglcc',
                                                                  'ShadowTunnelStageSound.byml',
                                                                  'ShadowTunnelStageMap.byml',
                                                                  'DefaultParam.baglamp',
                                                                  'DefaultParam.baglblm',
                                                                  'DefaultParam.baglexp',
                                                                  'Default.baglcc',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'CameraParam.byml',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'DofParam_obj13.bagldof',
                                                                  'UnitPointIlluminant.baglcube',
                                                                  'Default.baglssao']],
                  'RotateFieldStage': ['RotateFieldGoalZone.szs', ['RotateFieldGoalZoneDesign.byml',
                                                                   'RotateFieldGoalZoneMap.byml',
                                                                   'DofParam_obj22.bagldof',
                                                                   'CameraParam.byml',
                                                                   'DofParam_obj23.bagldof']],
                  'DoubleMarioFieldStage': ['DoubleMarioFieldStage.szs', ['DofParam_obj18.bagldof',
                                                                          'YFog.baglfog',
                                                                          'DirectionalLight.bagldirlit',
                                                                          'DoubleMarioFieldStageSound.byml',
                                                                          'DoubleMarioFieldStageDesign.byml',
                                                                          'DefaultParam.baglblm',
                                                                          'DefaultParam.baglexp',
                                                                          'AreaParamList.baglapl',
                                                                          'CubeMapMgr.baglcube',
                                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                                          'CameraParam.byml',
                                                                          'DoubleMarioFieldStageMap.byml',
                                                                          'DofParam_obj7.bagldof',
                                                                          'DepthShadow.bagldptsdw',
                                                                          'DofParam_obj3.bagldof',
                                                                          'CategoryLightInfo.bagllitinfostandard',
                                                                          'Fog.baglfog',
                                                                          'UnitPointIlluminant.baglcube']],
                  'KillerTankStage': ['KillerTankStage.szs', ['DofParam_obj18.bagldof',
                                                              'KillerTankStageSound.byml',
                                                              'KillerTankStageMap.byml',
                                                              'DofParam_obj9.bagldof',
                                                              'KillerTankStageDesign.byml',
                                                              'YFog.baglfog',
                                                              'DofParam_obj15.bagldof',
                                                              'DirectionalLight.bagldirlit',
                                                              'GodRay.baglgodray',
                                                              'DefaultParam.baglblm',
                                                              'DefaultParam.baglexp',
                                                              'AreaParamList.baglapl',
                                                              'CubeMapMgr.baglcube',
                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                              'CameraParam.byml',
                                                              'DofParam_obj7.bagldof',
                                                              'DepthShadow.bagldptsdw',
                                                              'DofParam_obj17.bagldof',
                                                              'CategoryLightInfo.bagllitinfostandard',
                                                              'Fog.baglfog',
                                                              'UnitPointIlluminant.baglcube',
                                                              'GraphicsStress.baglstress']],
                  'SnowBallParkStage': ['SnowBallParkStage.szs', ['DofParam_obj5.bagldof',
                                                                  'YFog.baglfog',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'LightStreak.baglgodray',
                                                                  'SnowBallParkStageMap.byml',
                                                                  'DefaultParam.baglblm',
                                                                  'DefaultParam.baglexp',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'HdrCompose.baglhdrcompose',
                                                                  'SnowBallParkStageDesign.byml',
                                                                  'CameraParam.byml',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'SnowBallParkStageSound.byml',
                                                                  'Fog.baglfog',
                                                                  'GraphicsStress.baglstress',
                                                                  'DofParam_obj8.bagldof']],
                  'ClimbWirenetStage': ['ClimbWirenetStage.szs', ['DofParam_obj4.bagldof',
                                                                  'ClimbWirenetStageSound.byml',
                                                                  'DofParam_obj1.bagldof',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'DefaultParam.baglblm',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'ClimbWirenetStageMap.byml',
                                                                  'CameraParam.byml',
                                                                  'ClimbWirenetStageDesign.byml',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'UnitPointIlluminant.baglcube',
                                                                  'Default.baglssao']],
                  'TeresaConveyorStage': ['TeresaConveyorStage.szs', ['MirrorRendering.baglmirror',
                                                                      'TeresaConveyorStageSound.byml',
                                                                      'BonusArea.baglssao',
                                                                      'YFog.baglfog',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'DofParam_obj204.bagldof',
                                                                      'GodRay.baglgodray',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'Default.baglcc',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'HdrCompose.baglhdrcompose',
                                                                      'TeresaConveyorStageDesign.byml',
                                                                      'CameraParam.byml',
                                                                      'DofParam_obj201.bagldof',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'TeresaConveyorStageMap.byml',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'Fog.baglfog',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'Default.baglssao',
                                                                      'GraphicsStress.baglstress',
                                                                      'DofParam_obj206.bagldof']],
                  'ShortGardenStage': ['ShortGardenStage.szs', ['DofParam_obj4.bagldof',
                                                                'DofParam_obj556.bagldof',
                                                                'YFog.baglfog',
                                                                'DirectionalLight.bagldirlit',
                                                                'ShortGardenStageMap.byml',
                                                                'ShortGardenStageSound.byml',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'ShortGardenStageDesign.byml',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'DofParam_obj7.bagldof',
                                                                'DepthShadow.bagldptsdw',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'Fog.baglfog',
                                                                'UnitPointIlluminant.baglcube',
                                                                'DofParam_obj8.bagldof']],
                  'DokanAquariumStage': ['DokanAquariumGoalZone.szs', ['DofParam_obj29.bagldof',
                                                                       'DokanAquariumGoalZoneMap.byml',
                                                                       'CameraParam.byml',
                                                                       'DokanAquariumGoalZoneDesign.byml']],
                  'DashRidgeStage': ['DashRidgeGoalZone.szs', ['DashRidgeGoalZoneMap.byml',
                                                               'DashRidgeGoalZoneSound.byml',
                                                               'DofParam_obj2.bagldof',
                                                               'CameraParam.byml',
                                                               'DashRidgeGoalZoneDesign.byml']],
                  'TruckWaterfallStage': ['TruckWaterfallStage.szs', ['DofParam_obj4.bagldof',
                                                                      'DofParam_obj14.bagldof',
                                                                      'DofParam_obj9.bagldof',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'TruckWaterfallStageMap.byml',
                                                                      'CameraParam.byml',
                                                                      'DofParam_obj7.bagldof',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'DofParam_obj3.bagldof',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'TruckWaterfallStageDesign.byml',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'TruckWaterfallStageSound.byml']],
                  'KillerExpressStage': ['KillerExpressStage.szs', ['DofParam_obj18.bagldof',
                                                                    'DofParam_obj4.bagldof',
                                                                    'DofParam_obj14.bagldof',
                                                                    'DofParam_obj20.bagldof',
                                                                    'DofParam_obj10.bagldof',
                                                                    'DofParam_obj9.bagldof',
                                                                    'KillerExpressStageSound.byml',
                                                                    'YFog.baglfog',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'DofParam_obj16.bagldof',
                                                                    'GodRay.baglgodray',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'KillerExpressStageDesign.byml',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'Fog.baglfog',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'KillerExpressStageMap.byml',
                                                                    'GraphicsStress.baglstress']],
                  'GateKeeperTentackLv1Stage': ['GateKeeperTentackLv1Stage.szs', ['GateKeeperTentackLv1StageDesign.byml',
                                                                                  'DofParam_obj79.bagldof',
                                                                                  'DofParam_obj65.bagldof',
                                                                                  'YFog.baglfog',
                                                                                  'DirectionalLight.bagldirlit',
                                                                                  'DofParam_obj151.bagldof',
                                                                                  'GateKeeperTentackLv1StageSound.byml',
                                                                                  'GateKeeperTentackLv1StageMap.byml',
                                                                                  'DofParam_obj152.bagldof',
                                                                                  'DefaultParam.baglblm',
                                                                                  'DefaultParam.baglexp',
                                                                                  'AreaParamList.baglapl',
                                                                                  'CubeMapMgr.baglcube',
                                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                                  'CameraParam.byml',
                                                                                  'DepthShadow.bagldptsdw',
                                                                                  'DofParam_obj147.bagldof',
                                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                                  'Fog.baglfog',
                                                                                  'UnitPointIlluminant.baglcube']],
                  'CrawlerHillStage': ['CrawlerHillStage.szs', ['DofParam_obj14.bagldof',
                                                                'DofParam_obj10.bagldof',
                                                                'CrawlerHillStageDesign.byml',
                                                                'DofParam_obj5.bagldof',
                                                                'YFog.baglfog',
                                                                'DofParam_obj15.bagldof',
                                                                'DirectionalLight.bagldirlit',
                                                                'CrawlerHillStageMap.byml',
                                                                'DofParam_obj16.bagldof',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CrawlerHillStageSound.byml',
                                                                'HdrCompose.baglhdrcompose',
                                                                'CameraParam.byml',
                                                                'DepthShadow.bagldptsdw',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'Fog.baglfog',
                                                                'UnitPointIlluminant.baglcube']],
                  'PipePackunDenStage': ['PipePackunDenGoalZone.szs', ['DofParam_obj1.bagldof',
                                                                       'PipePackunDenGoalZoneMap.byml',
                                                                       'CameraParam.byml',
                                                                       'PipePackunDenGoalZoneDesign.byml']],
                  'ChikaChikaBoomerangStage': ['ChikaChikaBoomerangCZone.szs', ['DofParam_obj0.bagldof',
                                                                                'ChikaChikaBoomerangCZoneDesign.byml',
                                                                                'CameraParam.byml',
                                                                                'ChikaChikaBoomerangCZoneMap.byml']],
                  'TrampolineHighlandStage': ['TrampolineHighlandStage.szs', ['DofParam_obj18.bagldof',
                                                                              'DofParam_obj4.bagldof',
                                                                              'TrampolineHighlandStageDesign.byml',
                                                                              'DofParam_obj5.bagldof',
                                                                              'BonusArea.baglssao',
                                                                              'DirectionalLight.bagldirlit',
                                                                              'TrampolineHighlandStageMap.byml',
                                                                              'DofParam_obj6.bagldof',
                                                                              'DefaultParam.baglblm',
                                                                              'DefaultParam.baglexp',
                                                                              'AreaParamList.baglapl',
                                                                              'CubeMapMgr.baglcube',
                                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                                              'CameraParam.byml',
                                                                              'DepthShadow.bagldptsdw',
                                                                              'TrampolineHighlandStageSound.byml',
                                                                              'CategoryLightInfo.bagllitinfostandard',
                                                                              'UnitPointIlluminant.baglcube',
                                                                              'Default.baglssao',
                                                                              'DofParam_obj889.bagldof']],
                  'GabonMountainStage': ['GabonMountainStage.szs', ['DofParam_obj14.bagldof',
                                                                    'DofParam_obj9.bagldof',
                                                                    'GabonMountainStageDesign.byml',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'GabonMountainStageSound.byml',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'GabonMountainStageMap.byml',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'DofParam_obj8.bagldof']],
                  'BossGorobonStage': ['BossGorobonStage.szs', ['BossGorobonStagePosY.bntx',
                                                                'DirectionalLight.bagldirlit',
                                                                'DofParam_obj31.bagldof',
                                                                'BossGorobonStageNegZ.bntx',
                                                                'BossGorobonStageNegX.bntx',
                                                                'DofParam_obj2.bagldof',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'BossGorobonStagePosZ.bntx',
                                                                'DepthShadow.bagldptsdw',
                                                                'DofParam_obj33.bagldof',
                                                                'BossGorobonStagePosX.bntx',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'Fog.baglfog',
                                                                'BossGorobonStageMap.byml',
                                                                'UnitPointIlluminant.baglcube',
                                                                'BossGorobonStageSound.byml',
                                                                'GraphicsStress.baglstress',
                                                                'BossGorobonStageDesign.byml',
                                                                'BossGorobonStageNegY.bntx']],
                  'NokonokoBeachStage': ['NokonokoBeachStage.szs', ['NokonokoBeachStageDesign.byml',
                                                                    'DofParam_obj19.bagldof',
                                                                    'YFog.baglfog',
                                                                    'DofParam_obj1.bagldof',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'DofParam_obj11.bagldof',
                                                                    'NokonokoBeachStageMap.byml',
                                                                    'LightStreak.baglgodray',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'NokonokoBeachStageSound.byml',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'DofParam_obj17.bagldof',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'DofParam_obj8.bagldof']],
                  'SwingCircusStage': ['SwingCircusStage.szs', ['DofParam_obj64.bagldof',
                                                                'SwingCircusStageSound.byml',
                                                                'DofParam_obj65.bagldof',
                                                                'YFog.baglfog',
                                                                'DirectionalLight.bagldirlit',
                                                                'LightStreak.baglgodray',
                                                                'SwingCircusStageMap.byml',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'DofParam_obj77.bagldof',
                                                                'DepthShadow.bagldptsdw',
                                                                'DofParam_obj63.bagldof',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'Fog.baglfog',
                                                                'UnitPointIlluminant.baglcube',
                                                                'SwingCircusStageDesign.byml',
                                                                'GraphicsStress.baglstress']],
                  'ShortMultiLiftStage': ['ShortMultiLiftStage.szs', ['DofParam_obj18.bagldof',
                                                                       'DofParam_obj10.bagldof',
                                                                       'YFog.baglfog',
                                                                       'DirectionalLight.bagldirlit',
                                                                       'ShortMultiLiftStageMap.byml',
                                                                       'DefaultParam.baglblm',
                                                                       'DefaultParam.baglexp',
                                                                       'AreaParamList.baglapl',
                                                                       'CubeMapMgr.baglcube',
                                                                       'CategoryLightInfo.bagllitinfocharacter',
                                                                       'CameraParam.byml',
                                                                       'DepthShadow.bagldptsdw',
                                                                       'CategoryLightInfo.bagllitinfostandard',
                                                                       'Fog.baglfog',
                                                                       'ShortMultiLiftStageDesign.byml',
                                                                       'ShortMultiLiftStageSound.byml']],
                  'SavannaRockStage': ['SavannaRockStage.szs', ['DofParam_obj4.bagldof',
                                                                'SavannaRockStageSound.byml',
                                                                'DofParam_obj10.bagldof',
                                                                'SavannaRockStageMap.byml',
                                                                'DirectionalLight.bagldirlit',
                                                                'SavannaRockStageDesign.byml',
                                                                'DofParam_obj2.bagldof',
                                                                'DofParam_obj12.bagldof',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'DepthShadow.bagldptsdw',
                                                                'DofParam_obj17.bagldof',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'UnitPointIlluminant.baglcube',
                                                                'DofParam_obj8.bagldof']],
                  'BombCaveStage': ['BombCaveStage.szs', ['InsideArea.baglssao',
                                                          'DofParam_obj10.bagldof',
                                                          'YFog.baglfog',
                                                          'DirectionalLight.bagldirlit',
                                                          'DofParam_obj11.bagldof',
                                                          'DofParam_obj12.bagldof',
                                                          'DefaultParam.baglblm',
                                                          'DefaultParam.baglexp',
                                                          'AreaParamList.baglapl',
                                                          'CubeMapMgr.baglcube',
                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                          'CameraParam.byml',
                                                          'DepthShadow.bagldptsdw',
                                                          'BombCaveStageDesign.byml',
                                                          'CategoryLightInfo.bagllitinfostandard',
                                                          'DofParam_obj13.bagldof',
                                                          'UnitPointIlluminant.baglcube',
                                                          'Default.baglssao',
                                                          'BombCaveStageSound.byml',
                                                          'BombCaveStageMap.byml']],
                  'JumpFlipSweetsStage': ['JumpFlipSweetsStage.szs', ['JumpFlipSweetsStageSound.byml',
                                                                      'DofParam_obj9.bagldof',
                                                                      'BonusArea.baglssao',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'DofParam_obj21.bagldof',
                                                                      'DofParam_obj11.bagldof',
                                                                      'JumpFlipSweetsStageDesign.byml',
                                                                      'LightStreak.baglgodray',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'CameraParam.byml',
                                                                      'DofParam_obj7.bagldof',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'JumpFlipSweetsStageMap.byml',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'DofParam_obj13.bagldof',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'Default.baglssao',
                                                                      'GraphicsStress.baglstress']],
                  'SneakingLightStage': ['SneakingLightStage.szs', ['DofParam_obj20.bagldof',
                                                                    'BonusArea.baglssao',
                                                                    'YFog.baglfog',
                                                                    'DofParam_obj25.bagldof',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'DofParam_obj21.bagldof',
                                                                    'DofParam_obj26.bagldof',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'SneakingLightStageMap.byml',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'SneakingLightStageSound.byml',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'Default.baglssao',
                                                                    'SneakingLightStageDesign.byml']],
                  'BossWackunFortressStage': ['BossWackunFortressStage.szs', ['DofParam_obj0.bagldof',
                                                                              'YFog.baglfog',
                                                                              'BossWackunFortressStageMap.byml',
                                                                              'DirectionalLight.bagldirlit',
                                                                              'DofParam_obj11.bagldof',
                                                                              'DefaultParam.baglblm',
                                                                              'DefaultParam.baglexp',
                                                                              'BossWackunFortressStageDesign.byml',
                                                                              'BossWackunFortressStageSound.byml',
                                                                              'AreaParamList.baglapl',
                                                                              'CubeMapMgr.baglcube',
                                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                                              'CameraParam.byml',
                                                                              'DepthShadow.bagldptsdw',
                                                                              'CategoryLightInfo.bagllitinfostandard',
                                                                              'Fog.baglfog',
                                                                              'UnitPointIlluminant.baglcube']],
                  'RouteDokanTourStage': ['RouteDokanTourStage.szs', ['RouteDokanTourStageMap.byml',
                                                                      'DofParam_obj5.bagldof',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'RouteDokanTourStageSound.byml',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'RouteDokanTourStageDesign.byml',
                                                                      'CameraParam.byml',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'DofParam_obj8.bagldof']],
                  'WeavingShipStage': ['WeavingShipGoalZone.szs', ['DofParam_obj0.bagldof',
                                                                   'WeavingShipGoalZoneMap.byml',
                                                                   'WeavingShipGoalZoneDesign.byml',
                                                                   'CameraParam.byml']],
                  'KarakuriCastleStage': ['KarakuriCastleStage.szs', ['DofParam_obj18.bagldof',
                                                                      'DofParam_obj118.bagldof',
                                                                      'DofParam_obj120.bagldof',
                                                                      'KarakuriCastleStageMap.byml',
                                                                      'CastleInside.baglssao',
                                                                      'DofParam_obj119.bagldof',
                                                                      'YFog.baglfog',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'DofParam_obj121.bagldof',
                                                                      'KarakuriCastleStageDesign.byml',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'CameraParam.byml',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'Default.baglssao',
                                                                      'KarakuriCastleStageSound.byml']],
                  'JungleCruiseStage': ['JungleCruiseStage.szs', ['DofParam_obj4.bagldof',
                                                                  'JungleCruiseStageDesign.byml',
                                                                  'YFog.baglfog',
                                                                  'DofParam_obj35.bagldof',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'JungleCruiseStageSound.byml',
                                                                  'ShadowMask.baglsdw_mask',
                                                                  'DefaultParam.baglblm',
                                                                  'DefaultParam.baglexp',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'CameraParam.byml',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'Fog.baglfog',
                                                                  'UnitPointIlluminant.baglcube',
                                                                  'GraphicsStress.baglstress',
                                                                  'JungleCruiseStageMap.byml']],
                  'BlastSnowFieldStage': ['BlastSnowFieldStage.szs', ['DirectionalLight.bagldirlit',
                                                                      'LightStreak.baglgodray',
                                                                      'DofParam_obj2.bagldof',
                                                                      'BlastSnowFieldStageDesign.byml',
                                                                      'DofParam_obj12.bagldof',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'BlastSnowFieldStageSound.byml',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'HdrCompose.baglhdrcompose',
                                                                      'CameraParam.byml',
                                                                      'BlastSnowFieldStageMap.byml',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'DofParam_obj3.bagldof',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'UnitPointIlluminant.baglcube',
                                                                      'GraphicsStress.baglstress',
                                                                      'DofParam_obj8.bagldof']],
                  'ClimbFortressStage': ['ClimbFortressStage.szs', ['DofParam_obj4.bagldof',
                                                                    'DofParam_obj10.bagldof',
                                                                    'ClimbFortressStageSound.byml',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'ClimbFortressStageMap.byml',
                                                                    'DofParam_obj6.bagldof',
                                                                    'DofParam_obj2.bagldof',
                                                                    'ClimbFortressStageDesign.byml',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'Fog.baglfog',
                                                                    'UnitPointIlluminant.baglcube']],
                  'ChorobonTowerStage': ['ChorobonTowerStage.szs', ['ChorobonTowerStageSound.byml',
                                                                    'DofParam_obj25.bagldof',
                                                                    'ChorobonTowerStageMap.byml',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'ChorobonTowerStageDesign.byml',
                                                                    'DofParam_obj26.bagldof',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'DofParam_obj28.bagldof']],
                  'BombTankStage': ['BombTankStage.szs', ['DofParam_obj54.bagldof',
                                                          'DofParam_obj30.bagldof',
                                                          'BombTankStageSound.byml',
                                                          'YFog.baglfog',
                                                          'DirectionalLight.bagldirlit',
                                                          'BombTankStageDesign.byml',
                                                          'DofParam_obj26.bagldof',
                                                          'DefaultParam.baglblm',
                                                          'DefaultParam.baglexp',
                                                          'AreaParamList.baglapl',
                                                          'CubeMapMgr.baglcube',
                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                          'BossArea.baglssao',
                                                          'CameraParam.byml',
                                                          'DepthShadow.bagldptsdw',
                                                          'DofParam_obj27.bagldof',
                                                          'CategoryLightInfo.bagllitinfostandard',
                                                          'UnitPointIlluminant.baglcube',
                                                          'Default.baglssao',
                                                          'GraphicsStress.baglstress',
                                                          'BombTankStageMap.byml',
                                                          'DofParam_obj28.bagldof']],
                  'GateKeeperBossBunretsuLv1Stage': ['GateKeeperBossBunretsuLv1Stage.szs', ['DofParam_obj79.bagldof',
                                                                                            'DofParam_obj65.bagldof',
                                                                                            'YFog.baglfog',
                                                                                            'DirectionalLight.bagldirlit',
                                                                                            'DofParam_obj146.bagldof',
                                                                                            'DefaultParam.baglblm',
                                                                                            'DefaultParam.baglexp',
                                                                                            'AreaParamList.baglapl',
                                                                                            'CubeMapMgr.baglcube',
                                                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                                                            'CameraParam.byml',
                                                                                            'GateKeeperBossBunretsuLv1StageDesign.byml',
                                                                                            'DepthShadow.bagldptsdw',
                                                                                            'CategoryLightInfo.bagllitinfostandard',
                                                                                            'Fog.baglfog',
                                                                                            'UnitPointIlluminant.baglcube',
                                                                                            'GateKeeperBossBunretsuLv1StageSound.byml',
                                                                                            'GateKeeperBossBunretsuLv1StageMap.byml']],
                  'FireBrosFortressStage': ['FireBrosFortressStage.szs', ['FireBrosFortressStageMap.byml',
                                                                          'FireBrosFortressStageSound.byml',
                                                                          'DofParam_obj50.bagldof',
                                                                          'DirectionalLight.bagldirlit',
                                                                          'DofParam_obj867.bagldof',
                                                                          'DofParam_obj2.bagldof',
                                                                          'DofParam_obj62.bagldof',
                                                                          'DefaultParam.baglblm',
                                                                          'DefaultParam.baglexp',
                                                                          'AreaParamList.baglapl',
                                                                          'CubeMapMgr.baglcube',
                                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                                          'FireBrosFortressStageDesign.byml',
                                                                          'CameraParam.byml',
                                                                          'DepthShadow.bagldptsdw',
                                                                          'CategoryLightInfo.bagllitinfostandard',
                                                                          'Fog.baglfog',
                                                                          'UnitPointIlluminant.baglcube',
                                                                          'GraphicsStress.baglstress',
                                                                          'DofParam_obj68.bagldof']],
                  'DarkFlipPanelStage': ['DarkFlipPanelStage.szs', ['DofParam_obj80.bagldof',
                                                                    'DarkFlipPanelStageSound.byml',
                                                                    'DarkFlipPanelStageDesign.byml',
                                                                    'DofParam_obj59.bagldof',
                                                                    'Default.baglflarefilter',
                                                                    'YFog.baglfog',
                                                                    'SSII.baglssii',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'DofParam_obj82.bagldof',
                                                                    'GodRay.baglgodray',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'HdrCompose.baglhdrcompose',
                                                                    'Dark.baglflarefilter',
                                                                    'CameraParam.byml',
                                                                    'DofParam_obj57.bagldof',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'DarkFlipPanelStageMap.byml',
                                                                    'DofParam_obj83.bagldof',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'DofParam_obj58.bagldof']],
                  'ShortAmidaStage': ['ShortAmidaStage.szs', ['DofParam_obj0.bagldof',
                                                              'DofParam_obj10.bagldof',
                                                              'DofParam_obj9.bagldof',
                                                              'YFog.baglfog',
                                                              'DirectionalLight.bagldirlit',
                                                              'ShortAmidaStageDesign.byml',
                                                              'DefaultParam.baglblm',
                                                              'DefaultParam.baglexp',
                                                              'AreaParamList.baglapl',
                                                              'CubeMapMgr.baglcube',
                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                              'CameraParam.byml',
                                                              'ShortAmidaStageSound.byml',
                                                              'DepthShadow.bagldptsdw',
                                                              'CategoryLightInfo.bagllitinfostandard',
                                                              'Fog.baglfog',
                                                              'UnitPointIlluminant.baglcube',
                                                              'ShortAmidaStageMap.byml']],
                  'DonketsuArrowStepStage': ['DonketsuArrowStepGoalZone.szs', ['DonketsuArrowStepGoalZoneDesign.byml',
                                                                               'DofParam_obj0.bagldof',
                                                                               'DonketsuArrowStepGoalZoneMap.byml',
                                                                               'DonketsuArrowStepGoalZoneSound.byml',
                                                                               'CameraParam.byml']],
                  'ZigzagBuildingStage': ['ZigzagBuildingStage.szs', ['DofParam_obj4.bagldof',
                                                                      'ZigzagBuildingStageSound.byml',
                                                                      'DofParam_obj5.bagldof',
                                                                      'ZigzagBuildingStageDesign.byml',
                                                                      'DofParam_obj1.bagldof',
                                                                      'DirectionalLight.bagldirlit',
                                                                      'ZigzagBuildingStageMap.byml',
                                                                      'DofParam_obj6.bagldof',
                                                                      'DefaultParam.baglamp',
                                                                      'DefaultParam.baglblm',
                                                                      'DefaultParam.baglexp',
                                                                      'AreaParamList.baglapl',
                                                                      'CubeMapMgr.baglcube',
                                                                      'CategoryLightInfo.bagllitinfocharacter',
                                                                      'CameraParam.byml',
                                                                      'DepthShadow.bagldptsdw',
                                                                      'CategoryLightInfo.bagllitinfostandard',
                                                                      'UnitPointIlluminant.baglcube']],
                  'SyumockSpotStage': ['SyumockSpotGoalZone.szs', ['SyumockSpotGoalZoneSound.byml',
                                                                   'DofParam_obj2.bagldof',
                                                                   'CameraParam.byml',
                                                                   'SyumockSpotGoalZoneMap.byml',
                                                                   'SyumockSpotGoalZoneDesign.byml']],
                  'RagingMagmaStage': ['RagingMagmaStage.szs', ['DofParam_obj0.bagldof',
                                                                'DofParam_obj1.bagldof',
                                                                'DirectionalLight.bagldirlit',
                                                                'DofParam_obj1424.bagldof',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'DepthShadow.bagldptsdw',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'UnitPointIlluminant.baglcube',
                                                                'RagingMagmaStageMap.byml',
                                                                'RagingMagmaStageDesign.byml']],
                  'KoopaChaseLv2Stage': ['KoopaChaseLv2Stage.szs', ['DofParam_obj10.bagldof',
                                                                    'YFog.baglfog',
                                                                    'DofParam_obj1.bagldof',
                                                                    'DirectionalLight.bagldirlit',
                                                                    'DofParam_obj11.bagldof',
                                                                    'KoopaChaseLv2StageSound.byml',
                                                                    'GodRay.baglgodray',
                                                                    'DofParam_obj12.bagldof',
                                                                    'DefaultParam.baglblm',
                                                                    'DefaultParam.baglexp',
                                                                    'AreaParamList.baglapl',
                                                                    'CubeMapMgr.baglcube',
                                                                    'CategoryLightInfo.bagllitinfocharacter',
                                                                    'CameraParam.byml',
                                                                    'DofParam_obj7.bagldof',
                                                                    'DepthShadow.bagldptsdw',
                                                                    'KoopaChaseLv2StageDesign.byml',
                                                                    'CategoryLightInfo.bagllitinfostandard',
                                                                    'DofParam_obj13.bagldof',
                                                                    'Fog.baglfog',
                                                                    'KoopaChaseLv2StageMap.byml',
                                                                    'UnitPointIlluminant.baglcube',
                                                                    'GraphicsStress.baglstress',
                                                                    'DofParam_obj8.bagldof']],
                  'NeedleBridgeStage': ['NeedleBridgeStage.szs', ['NeedleBridgeStageSound.byml',
                                                                  'BonusArea.baglssao',
                                                                  'YFog.baglfog',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'DofParam_obj6.bagldof',
                                                                  'DefaultParam.baglblm',
                                                                  'DefaultParam.baglexp',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'HdrCompose.baglhdrcompose',
                                                                  'NeedleBridgeStageMap.byml',
                                                                  'CameraParam.byml',
                                                                  'DofParam_obj7.bagldof',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'DofParam_obj3.bagldof',
                                                                  'NeedleBridgeStageDesign.byml',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'Fog.baglfog',
                                                                  'UnitPointIlluminant.baglcube',
                                                                  'Default.baglssao']],
                  'DownDesertStage': ['DownDesertStage.szs', ['DofParam_obj5.bagldof',
                                                              'DofParam_obj1.bagldof',
                                                              'DirectionalLight.bagldirlit',
                                                              'DownDesertStageMap.byml',
                                                              'DofParam_obj6.bagldof',
                                                              'DownDesertStageSound.byml',
                                                              'DefaultParam.baglblm',
                                                              'DefaultParam.baglexp',
                                                              'AreaParamList.baglapl',
                                                              'CubeMapMgr.baglcube',
                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                              'CameraParam.byml',
                                                              'DofParam_obj7.bagldof',
                                                              'DepthShadow.bagldptsdw',
                                                              'DofParam_obj3.bagldof',
                                                              'CategoryLightInfo.bagllitinfostandard',
                                                              'Fog.baglfog',
                                                              'UnitPointIlluminant.baglcube',
                                                              'DownDesertStageDesign.byml']],
                  'GearSweetsStage': ['GearSweetsStage.szs', ['DofParam_obj9.bagldof',
                                                              'DofParam_obj1.bagldof',
                                                              'DirectionalLight.bagldirlit',
                                                              'LightStreak.baglgodray',
                                                              'DofParam_obj2.bagldof',
                                                              'DefaultParam.baglexp',
                                                              'GearSweetsStageSound.byml',
                                                              'AreaParamList.baglapl',
                                                              'CubeMapMgr.baglcube',
                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                              'CameraParam.byml',
                                                              'GearSweetsStageMap.byml',
                                                              'DepthShadow.bagldptsdw',
                                                              'GearSweetsStageDesign.byml',
                                                              'DofParam_obj17.bagldof',
                                                              'CategoryLightInfo.bagllitinfostandard',
                                                              'UnitPointIlluminant.baglcube']],
                  'EchoRoadStage': ['EchoRoadStage.szs', ['DofParam_obj4.bagldof',
                                                          'EchoRoadStageSound.byml',
                                                          'YFog.baglfog',
                                                          'DirectionalLight.bagldirlit',
                                                          'DofParam_obj121.bagldof',
                                                          'EchoRoadStageDesign.byml',
                                                          'DefaultParam.baglblm',
                                                          'DefaultParam.baglexp',
                                                          'AreaParamList.baglapl',
                                                          'CubeMapMgr.baglcube',
                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                          'EchoRoadStageMap.byml',
                                                          'CameraParam.byml',
                                                          'DepthShadow.bagldptsdw',
                                                          'CategoryLightInfo.bagllitinfostandard',
                                                          'Fog.baglfog',
                                                          'UnitPointIlluminant.baglcube']],
                  'WaterElevatorCaveStage': ['WaterElevatorCaveStage.szs', ['DofParam_obj30.bagldof',
                                                                            'DofParam_obj29.bagldof',
                                                                            'YFog.baglfog',
                                                                            'DofParam_obj35.bagldof',
                                                                            'WaterElevatorCaveStageMap.byml',
                                                                            'DirectionalLight.bagldirlit',
                                                                            'DofParam_obj31.bagldof',
                                                                            'WaterElevatorCaveStageSound.byml',
                                                                            'DefaultParam.baglblm',
                                                                            'DefaultParam.baglexp',
                                                                            'AreaParamList.baglapl',
                                                                            'CubeMapMgr.baglcube',
                                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                                            'CameraParam.byml',
                                                                            'WaterElevatorCaveStageDesign.byml',
                                                                            'DepthShadow.bagldptsdw',
                                                                            'DofParam_obj27.bagldof',
                                                                            'CategoryLightInfo.bagllitinfostandard',
                                                                            'UnitPointIlluminant.baglcube',
                                                                            'DofParam_obj28.bagldof']],
                  'DarknessHauntedHouseStage': ['DarknessHauntedHouseStage.szs', ['DofParam_obj277.bagldof',
                                                                                  'MirrorRendering.baglmirror',
                                                                                  'DofParam_obj273.bagldof',
                                                                                  'BonusArea.baglssao',
                                                                                  'SSII.baglssii',
                                                                                  'DirectionalLight.bagldirlit',
                                                                                  'DofParam_obj274.bagldof',
                                                                                  'DofParam_obj280.bagldof',
                                                                                  'DofParam_obj230.bagldof',
                                                                                  'DefaultParam.baglamp',
                                                                                  'DefaultParam.baglblm',
                                                                                  'DefaultParam.baglexp',
                                                                                  'AreaParamList.baglapl',
                                                                                  'CubeMapMgr.baglcube',
                                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                                  'DofParam_obj275.bagldof',
                                                                                  'CameraParam.byml',
                                                                                  'DofParam_obj261.bagldof',
                                                                                  'DepthShadow.bagldptsdw',
                                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                                  'UnitPointIlluminant.baglcube',
                                                                                  'Default.baglssao',
                                                                                  'DarknessHauntedHouseStageSound.byml',
                                                                                  'GraphicsStress.baglstress',
                                                                                  'DarknessHauntedHouseStageDesign.byml',
                                                                                  'DarknessHauntedHouseStageMap.byml']],
                  'GotogotonValleyStage': ['GotogotonValleyStage.szs', ['DofParam_obj20.bagldof',
                                                                        'GotogotonValleyStageDesign.byml',
                                                                        'DirectionalLight.bagldirlit',
                                                                        'DofParam_obj21.bagldof',
                                                                        'GotogotonValleyStageSound.byml',
                                                                        'DefaultParam.baglblm',
                                                                        'DefaultParam.baglexp',
                                                                        'CubeMapMgr.baglcube',
                                                                        'CategoryLightInfo.bagllitinfocharacter',
                                                                        'CameraParam.byml',
                                                                        'CategoryLightInfo.bagllitinfostandard',
                                                                        'UnitPointIlluminant.baglcube',
                                                                        'GotogotonValleyStageMap.byml']],
                  'EnemyExpressStage': ['EnemyExpressStage.szs', ['EnemyExpressStageMap.byml',
                                                                  'DofParam_obj40.bagldof',
                                                                  'EnemyExpressStageDesign.byml',
                                                                  'EnemyExpressStageSound.byml',
                                                                  'DofParam_obj39.bagldof',
                                                                  'DofParam_obj29.bagldof',
                                                                  'YFog.baglfog',
                                                                  'DofParam_obj45.bagldof',
                                                                  'DirectionalLight.bagldirlit',
                                                                  'LightStreak.baglgodray',
                                                                  'DofParam_obj42.bagldof',
                                                                  'DefaultParam.baglblm',
                                                                  'DefaultParam.baglexp',
                                                                  'AreaParamList.baglapl',
                                                                  'CubeMapMgr.baglcube',
                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                  'CameraParam.byml',
                                                                  'DepthShadow.bagldptsdw',
                                                                  'DofParam_obj23.bagldof',
                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                  'Fog.baglfog',
                                                                  'UnitPointIlluminant.baglcube',
                                                                  'DofParam_obj38.bagldof']],
                  'KoopaLastStage': ['KoopaLastBZone.szs', ['DofParam_obj0.bagldof',
                                                            'KoopaLastBZoneMap.byml',
                                                            'DofParam_obj1.bagldof',
                                                            'KoopaLastBZoneDesign.byml',
                                                            'KoopaLastBZoneSound.byml',
                                                            'CubeMapMgr.baglcube',
                                                            'CameraParam.byml']],
                  'GateKeeperBossBunretsuLv2Stage': ['GateKeeperBossBunretsuLv2Stage.szs', ['DofParam_obj79.bagldof',
                                                                                            'DofParam_obj65.bagldof',
                                                                                            'YFog.baglfog',
                                                                                            'DirectionalLight.bagldirlit',
                                                                                            'GateKeeperBossBunretsuLv2StageSound.byml',
                                                                                            'GateKeeperBossBunretsuLv2StageMap.byml',
                                                                                            'DofParam_obj146.bagldof',
                                                                                            'DefaultParam.baglblm',
                                                                                            'DefaultParam.baglexp',
                                                                                            'AreaParamList.baglapl',
                                                                                            'CubeMapMgr.baglcube',
                                                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                                                            'CameraParam.byml',
                                                                                            'DepthShadow.bagldptsdw',
                                                                                            'CategoryLightInfo.bagllitinfostandard',
                                                                                            'Fog.baglfog',
                                                                                            'UnitPointIlluminant.baglcube',
                                                                                            'GateKeeperBossBunretsuLv2StageDesign.byml']],
                  'GateKeeperTentackLv2Stage': ['GateKeeperTentackLv2Stage.szs', ['DofParam_obj79.bagldof',
                                                                                  'DofParam_obj65.bagldof',
                                                                                  'YFog.baglfog',
                                                                                  'DirectionalLight.bagldirlit',
                                                                                  'GateKeeperTentackLv2StageDesign.byml',
                                                                                  'DofParam_obj146.bagldof',
                                                                                  'DefaultParam.baglblm',
                                                                                  'DefaultParam.baglexp',
                                                                                  'AreaParamList.baglapl',
                                                                                  'CubeMapMgr.baglcube',
                                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                                  'CameraParam.byml',
                                                                                  'DepthShadow.bagldptsdw',
                                                                                  'GateKeeperTentackLv2StageSound.byml',
                                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                                  'Fog.baglfog',
                                                                                  'UnitPointIlluminant.baglcube',
                                                                                  'GateKeeperTentackLv2StageMap.byml']],
                  'RainbowRoadStage': ['RainbowRoadStage.szs', ['DofParam_obj40.bagldof',
                                                                'RainbowRoadStageMap.byml',
                                                                'DirectionalLight.bagldirlit',
                                                                'DofParam_obj31.bagldof',
                                                                'RainbowRoadStageSound.byml',
                                                                'DofParam_obj42.bagldof',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'RainbowRoadStageDesign.byml',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'UnitPointIlluminant.baglcube',
                                                                'DofParam_obj8.bagldof',
                                                                'DofParam_obj38.bagldof']],
                  'GalaxyRoadStage': ['GalaxyRoadStage.szs', ['DofParam_obj79.bagldof',
                                                              'DofParam_obj1.bagldof',
                                                              'DirectionalLight.bagldirlit',
                                                              'GalaxyRoadStageDesign.byml',
                                                              'DofParam_obj106.bagldof',
                                                              'DefaultParam.baglblm',
                                                              'DefaultParam.baglexp',
                                                              'AreaParamList.baglapl',
                                                              'CubeMapMgr.baglcube',
                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                              'GalaxyRoadStageMap.byml',
                                                              'CameraParam.byml',
                                                              'DepthShadow.bagldptsdw',
                                                              'DofParam_obj107.bagldof',
                                                              'CategoryLightInfo.bagllitinfostandard',
                                                              'UnitPointIlluminant.baglcube',
                                                              'GalaxyRoadStageSound.byml']],
                  'WheelCanyonStage': ['WheelCanyonStage.szs', ['DofParam_obj0.bagldof',
                                                                'DofParam_obj10.bagldof',
                                                                'WheelCanyonStageMap.byml',
                                                                'DofParam_obj1.bagldof',
                                                                'DirectionalLight.bagldirlit',
                                                                'WheelCanyonStageDesign.byml',
                                                                'DefaultParam.baglblm',
                                                                'DefaultParam.baglexp',
                                                                'AreaParamList.baglapl',
                                                                'CubeMapMgr.baglcube',
                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                'CameraParam.byml',
                                                                'DepthShadow.bagldptsdw',
                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                'WheelCanyonStageSound.byml']],
                  'BlockLandStage': ['BlockLandStage.szs', ['DofParam_obj4.bagldof',
                                                            'BlockLandStageDesign.byml',
                                                            'DirectionalLight.bagldirlit',
                                                            'BlockLandStageSound.byml',
                                                            'DofParam_obj12.bagldof',
                                                            'DefaultParam.baglblm',
                                                            'DefaultParam.baglexp',
                                                            'AreaParamList.baglapl',
                                                            'CubeMapMgr.baglcube',
                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                            'CameraParam.byml',
                                                            'DepthShadow.bagldptsdw',
                                                            'CategoryLightInfo.bagllitinfostandard',
                                                            'DofParam_obj13.bagldof',
                                                            'UnitPointIlluminant.baglcube',
                                                            'BlockLandStageMap.byml']],
                  'HexScrollStage': ['HexScrollStage.szs', ['DofParam_obj4.bagldof',
                                                            'DofParam_obj5.bagldof',
                                                            'YFog.baglfog',
                                                            'HexScrollStageDesign.byml',
                                                            'DirectionalLight.bagldirlit',
                                                            'HexScrollStageSound.byml',
                                                            'DofParam_obj2.bagldof',
                                                            'DefaultParam.baglblm',
                                                            'DefaultParam.baglexp',
                                                            'AreaParamList.baglapl',
                                                            'CubeMapMgr.baglcube',
                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                            'HexScrollStageMap.byml',
                                                            'CameraParam.byml',
                                                            'DepthShadow.bagldptsdw',
                                                            'CategoryLightInfo.bagllitinfostandard',
                                                            'UnitPointIlluminant.baglcube']],
                  'GiantUnderGroundStage': ['GiantUnderGroundStage.szs', ['DofParam_obj39.bagldof',
                                                                          'YFog.baglfog',
                                                                          'DirectionalLight.bagldirlit',
                                                                          'ShadowMask.baglsdw_mask',
                                                                          'GodRay.baglgodray',
                                                                          'DofParam_obj42.bagldof',
                                                                          'DefaultParam.baglblm',
                                                                          'DefaultParam.baglexp',
                                                                          'GiantUnderGroundStageSound.byml',
                                                                          'AreaParamList.baglapl',
                                                                          'CubeMapMgr.baglcube',
                                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                                          'CameraParam.byml',
                                                                          'DepthShadow.bagldptsdw',
                                                                          'GiantUnderGroundStageMap.byml',
                                                                          'CategoryLightInfo.bagllitinfostandard',
                                                                          'Fog.baglfog',
                                                                          'UnitPointIlluminant.baglcube',
                                                                          'GiantUnderGroundStageDesign.byml',
                                                                          'DofParam_obj38.bagldof']],
                  'TerenFogStage': ['TerenFogGoalZone.szs', ['DofParam_obj1.bagldof',
                                                             'CameraParam.byml',
                                                             'TerenFogGoalZoneDesign.byml',
                                                             'TerenFogGoalZoneMap.byml']],
                  'BoxKillerStage': ['BoxKillerStage.szs', ['BoxKillerStageMap.byml',
                                                            'DofParam_obj19.bagldof',
                                                            'DofParam_obj1.bagldof',
                                                            'DirectionalLight.bagldirlit',
                                                            'DefaultParam.baglblm',
                                                            'DefaultParam.baglexp',
                                                            'BoxKillerStageSound.byml',
                                                            'AreaParamList.baglapl',
                                                            'CubeMapMgr.baglcube',
                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                            'CameraParam.byml',
                                                            'BoxKillerStageDesign.byml',
                                                            'DepthShadow.bagldptsdw',
                                                            'CategoryLightInfo.bagllitinfostandard',
                                                            'UnitPointIlluminant.baglcube']],
                  'ArrangeRotateFieldStage': ['ArrangeRotateFieldGoalZone.szs', ['ArrangeRotateFieldGoalZoneDesign.byml',
                                                                                 'ArrangeRotateFieldGoalZoneMap.byml',
                                                                                 'DofParam_obj22.bagldof',
                                                                                 'CameraParam.byml']],
                  'ArrangeClimbMountainStage': ['ArrangeClimbMountainStage.szs', ['ArrangeClimbMountainStageDesign.byml',
                                                                                  'DofParam_obj0.bagldof',
                                                                                  'ArrangeClimbMountainStageSound.byml',
                                                                                  'YFog.baglfog',
                                                                                  'DirectionalLight.bagldirlit',
                                                                                  'DofParam_obj6.bagldof',
                                                                                  'ArrangeClimbMountainStageMap.byml',
                                                                                  'DefaultParam.baglblm',
                                                                                  'DefaultParam.baglexp',
                                                                                  'AreaParamList.baglapl',
                                                                                  'CubeMapMgr.baglcube',
                                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                                  'CameraParam.byml',
                                                                                  'DofParam_obj7.bagldof',
                                                                                  'DepthShadow.bagldptsdw',
                                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                                  'Fog.baglfog',
                                                                                  'UnitPointIlluminant.baglcube',
                                                                                  'DofParam_obj8.bagldof']],
                  'ArrangeJungleCruiseStage': ['ArrangeJungleCruiseStage.szs', ['DofParam_obj9.bagldof',
                                                                                'DirectionalLight.bagldirlit',
                                                                                'ArrangeJungleCruiseStageDesign.byml',
                                                                                'ArrangeJungleCruiseStageSound.byml',
                                                                                'DefaultParam.baglblm',
                                                                                'DefaultParam.baglexp',
                                                                                'AreaParamList.baglapl',
                                                                                'CubeMapMgr.baglcube',
                                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                                'CameraParam.byml',
                                                                                'DepthShadow.bagldptsdw',
                                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                                'Fog.baglfog',
                                                                                'UnitPointIlluminant.baglcube',
                                                                                'ArrangeJungleCruiseStageMap.byml',
                                                                                'DofParam_obj8.bagldof']],
                  'ArrangeShadowTunnelStage': ['ArrangeShadowTunnelStage.szs', ['DofParam_obj14.bagldof',
                                                                                'DofParam_obj15.bagldof',
                                                                                'DirectionalLight.bagldirlit',
                                                                                'GoalArea.baglcc',
                                                                                'ArrangeShadowTunnelStageMap.byml',
                                                                                'DefaultParam.baglexp',
                                                                                'Default.baglcc',
                                                                                'AreaParamList.baglapl',
                                                                                'CubeMapMgr.baglcube',
                                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                                'ArrangeShadowTunnelStageDesign.byml',
                                                                                'CameraParam.byml',
                                                                                'ArrangeShadowTunnelStageSound.byml',
                                                                                'DepthShadow.bagldptsdw',
                                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                                'DofParam_obj13.bagldof',
                                                                                'UnitPointIlluminant.baglcube']],
                  'ArrangeWeavingShipStage': ['ArrangeWeavingShipGoalZone.szs', ['DofParam_obj0.bagldof',
                                                                                 'ArrangeWeavingShipGoalZoneMap.byml',
                                                                                 'ArrangeWeavingShipGoalZoneDesign.byml',
                                                                                 'CameraParam.byml']],
                  'ArrangeDonketsuArrowStepStage': ['ArrangeDonketsuArrowStepZone.szs', ['ArrangeDonketsuArrowStepZoneMap.byml',
                                                                                         'DofParam_obj0.bagldof',
                                                                                         'CameraParam.byml',
                                                                                         'ArrangeDonketsuArrowStepZoneDesign.byml']],
                  'ArrangeFlipCircusStage': ['ArrangeFlipCircusStage.szs', ['ArrangeFlipCircusStageDesign.byml',
                                                                            'MirrorRendering.baglmirror',
                                                                            'YFog.baglfog',
                                                                            'ArrangeFlipCircusStageMap.byml',
                                                                            'DirectionalLight.bagldirlit',
                                                                            'ArrangeFlipCircusStageSound.byml',
                                                                            'DofParam_obj16.bagldof',
                                                                            'LightStreak.baglgodray',
                                                                            'GodRay.baglgodray',
                                                                            'DefaultParam.baglblm',
                                                                            'DefaultParam.baglexp',
                                                                            'AreaParamList.baglapl',
                                                                            'CubeMapMgr.baglcube',
                                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                                            'CameraParam.byml',
                                                                            'DofParam_obj77.bagldof',
                                                                            'DepthShadow.bagldptsdw',
                                                                            'DofParam_obj83.bagldof',
                                                                            'CategoryLightInfo.bagllitinfostandard',
                                                                            'Fog.baglfog',
                                                                            'UnitPointIlluminant.baglcube',
                                                                            'GraphicsStress.baglstress']],
                  'ArrangeChorobonTowerStage': ['ArrangeChorobonTowerStage.szs', ['ArrangeChorobonTowerStageMap.byml',
                                                                             'DofParam_obj24.bagldof',
                                                                             'DofParam_obj25.bagldof',
                                                                             'DirectionalLight.bagldirlit',
                                                                             'DofParam_obj11.bagldof',
                                                                             'ArrangeChorobonTowerStageDesign.byml',
                                                                             'DefaultParam.baglblm',
                                                                             'DefaultParam.baglexp',
                                                                             'AreaParamList.baglapl',
                                                                             'ArrangeChorobonTowerStageSound.byml',
                                                                             'CubeMapMgr.baglcube',
                                                                             'CategoryLightInfo.bagllitinfocharacter',
                                                                             'CameraParam.byml',
                                                                             'DepthShadow.bagldptsdw',
                                                                             'CategoryLightInfo.bagllitinfostandard',
                                                                             'UnitPointIlluminant.baglcube']],
                  'ArrangePipePackunDenStage': ['ArrangePipePackunDenGoalZone.szs', ['ArrangePipePackunDenGoalZoneDesign.byml',
                                                                                     'DofParam_obj1.bagldof',
                                                                                     'DirectionalLight.bagldirlit',
                                                                                     'ArrangePipePackunDenGoalZoneMap.byml',
                                                                                     'CubeMapMgr.baglcube',
                                                                                     'CameraParam.byml']],
                  'ArrangeFireBrosFortressStage': ['ArrangeFireBrosFortressStage.szs', ['ArrangeFireBrosFortressStageDesign.byml',
                                                                                        'DirectionalLight.bagldirlit',
                                                                                        'DofParam_obj867.bagldof',
                                                                                        'ArrangeFireBrosFortressStageSound.byml',
                                                                                        'DofParam_obj36.bagldof',
                                                                                        'DofParam_obj2.bagldof',
                                                                                        'DefaultParam.baglblm',
                                                                                        'DefaultParam.baglexp',
                                                                                        'AreaParamList.baglapl',
                                                                                        'CubeMapMgr.baglcube',
                                                                                        'CategoryLightInfo.bagllitinfocharacter',
                                                                                        'CameraParam.byml',
                                                                                        'DepthShadow.bagldptsdw',
                                                                                        'DofParam_obj37.bagldof',
                                                                                        'CategoryLightInfo.bagllitinfostandard',
                                                                                        'Fog.baglfog',
                                                                                        'UnitPointIlluminant.baglcube',
                                                                                        'GraphicsStress.baglstress',
                                                                                        'ArrangeFireBrosFortressStageMap.byml']],
                  'ArrangeSavannaRockStage': ['ArrangeSavannaRockStage.szs', ['DofParam_obj4.bagldof',
                                                                              'DofParam_obj10.bagldof',
                                                                              'DirectionalLight.bagldirlit',
                                                                              'DofParam_obj2.bagldof',
                                                                              'DofParam_obj12.bagldof',
                                                                              'DefaultParam.baglblm',
                                                                              'DefaultParam.baglexp',
                                                                              'AreaParamList.baglapl',
                                                                              'ArrangeSavannaRockStageDesign.byml',
                                                                              'CubeMapMgr.baglcube',
                                                                              'CategoryLightInfo.bagllitinfocharacter',
                                                                              'CameraParam.byml',
                                                                              'DepthShadow.bagldptsdw',
                                                                              'ArrangeSavannaRockStageMap.byml',
                                                                              'CategoryLightInfo.bagllitinfostandard',
                                                                              'DofParam_obj13.bagldof',
                                                                              'UnitPointIlluminant.baglcube',
                                                                              'ArrangeSavannaRockStageSound.byml',
                                                                              'DofParam_obj8.bagldof']],
                  'ArrangeTeresaConveorStage': ['ArrangeTeresaConveorStage.szs', ['ArrangeTeresaConveorStageDesign.byml',
                                                                                  'DofParam_obj195.bagldof',
                                                                                  'YFog.baglfog',
                                                                                  'DirectionalLight.bagldirlit',
                                                                                  'DofParam_obj196.bagldof',
                                                                                  'ArrangeTeresaConveorStageMap.byml',
                                                                                  'DefaultParam.baglblm',
                                                                                  'DefaultParam.baglexp',
                                                                                  'Default.baglcc',
                                                                                  'AreaParamList.baglapl',
                                                                                  'CubeMapMgr.baglcube',
                                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                                  'ArrangeTeresaConveorStageSound.byml',
                                                                                  'CameraParam.byml',
                                                                                  'DepthShadow.bagldptsdw',
                                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                                  'Fog.baglfog',
                                                                                  'UnitPointIlluminant.baglcube']],
                  'ArrangeDokanAquariumStage': ['ArrangeAquariumCZone.szs', ['DirectionalLight.bagldirlit',
                                                                             'ArrangeAquariumCZoneDesign.byml',
                                                                             'CubeMapMgr.baglcube',
                                                                             'CameraParam.byml',
                                                                             'ArrangeAquariumCZoneMap.byml',
                                                                             'DofParam_obj28.bagldof']],
                  'ArrangeChikaChikaBoomerangStage': ['ArrangeChikaCZone.szs', ['DofParam_obj0.bagldof',
                                                                                'ArrangeChikaCZoneDesign.byml',
                                                                                'ArrangeChikaCZoneMap.byml',
                                                                                'CameraParam.byml']],
                  'ArrangeNokonokoBeachStage': ['ArrangeNokonokoBeachStage.szs', ['ArrangeNokonokoBeachStageSound.byml',
                                                                                  'ArrangeNokonokoBeachStageDesign.byml',
                                                                                  'ArrangeNokonokoBeachStageMap.byml',
                                                                                  'YFog.baglfog',
                                                                                  'DofParam_obj1.bagldof',
                                                                                  'DirectionalLight.bagldirlit',
                                                                                  'LightStreak.baglgodray',
                                                                                  'DofParam_obj2.bagldof',
                                                                                  'GodRay.baglgodray',
                                                                                  'DefaultParam.baglblm',
                                                                                  'Default.baglcc',
                                                                                  'AreaParamList.baglapl',
                                                                                  'CubeMapMgr.baglcube',
                                                                                  'CategoryLightInfo.bagllitinfocharacter',
                                                                                  'CameraParam.byml',
                                                                                  'DepthShadow.bagldptsdw',
                                                                                  'CategoryLightInfo.bagllitinfostandard',
                                                                                  'Fog.baglfog',
                                                                                  'UnitPointIlluminant.baglcube',
                                                                                  'GraphicsStress.baglstress',
                                                                                  'DofParam_obj8.bagldof']],
                  'ArrangeHexScrollStage': ['ArrangeHexScrollStage.szs', ['ArrangeHexScrollStageMap.byml',
                                                                          'ArrangeHexScrollStageDesign.byml',
                                                                          'DirectionalLight.bagldirlit',
                                                                          'DofParam_obj6.bagldof',
                                                                          'DofParam_obj2.bagldof',
                                                                          'DefaultParam.baglblm',
                                                                          'DefaultParam.baglexp',
                                                                          'AreaParamList.baglapl',
                                                                          'CubeMapMgr.baglcube',
                                                                          'CategoryLightInfo.bagllitinfocharacter',
                                                                          'CameraParam.byml',
                                                                          'DepthShadow.bagldptsdw',
                                                                          'DofParam_obj3.bagldof',
                                                                          'CategoryLightInfo.bagllitinfostandard',
                                                                          'UnitPointIlluminant.baglcube']],
                  'ArrangeNeedleBridgeStage': ['ArrangeNeedleBridgeStage.szs', ['ArrangeNeedleBridgeStageDesign.byml',
                                                                                'DofParam_obj5.bagldof',
                                                                                'DirectionalLight.bagldirlit',
                                                                                'ArrangeNeedleBridgeStageSound.byml',
                                                                                'DofParam_obj2.bagldof',
                                                                                'DefaultParam.baglexp',
                                                                                'AreaParamList.baglapl',
                                                                                'CubeMapMgr.baglcube',
                                                                                'CategoryLightInfo.bagllitinfocharacter',
                                                                                'HdrCompose.baglhdrcompose',
                                                                                'ArrangeNeedleBridgeStageMap.byml',
                                                                                'CameraParam.byml',
                                                                                'DepthShadow.bagldptsdw',
                                                                                'CategoryLightInfo.bagllitinfostandard',
                                                                                'UnitPointIlluminant.baglcube']],
                  'ArrangeBossParadeStage': ['ArrangeBossParadeStage.szs', ['DofParam_obj44.bagldof',
                                                                            'ArrangeBossParadeStageDesign.byml',
                                                                            'DofParam_obj59.bagldof',
                                                                            'YFog.baglfog',
                                                                            'ArrangeBossParadeStageMap.byml',
                                                                            'DofParam_obj45.bagldof',
                                                                            'ArrangeBossParadeStageSound.byml',
                                                                            'DirectionalLight.bagldirlit',
                                                                            'ShadowMask.baglsdw_mask',
                                                                            'DofParam_obj46.bagldof',
                                                                            'LightStreak.baglgodray',
                                                                            'GodRay.baglgodray',
                                                                            'DofParam_obj42.bagldof',
                                                                            'DefaultParam.baglblm',
                                                                            'DefaultParam.baglexp',
                                                                            'AreaParamList.baglapl',
                                                                            'CubeMapMgr.baglcube',
                                                                            'CategoryLightInfo.bagllitinfocharacter',
                                                                            'CameraParam.byml',
                                                                            'DofParam_obj57.bagldof',
                                                                            'DepthShadow.bagldptsdw',
                                                                            'DofParam_obj47.bagldof',
                                                                            'DofParam_obj43.bagldof',
                                                                            'CategoryLightInfo.bagllitinfostandard',
                                                                            'Fog.baglfog',
                                                                            'UnitPointIlluminant.baglcube',
                                                                            'GraphicsStress.baglstress',
                                                                            'DofParam_obj8.bagldof',
                                                                            'DofParam_obj58.bagldof']],
                  'ChampionshipStage': ['ChampionshipGoalZone.szs', ['DofParam_obj0.bagldof',
                                                                     'ChampionshipGoalZoneMap.byml',
                                                                     'CameraParam.byml',
                                                                     'ChampionshipGoalZoneDesign.byml']]
                  }

        print('Opening ' + stages[StageName][0])
        with open(os.path.join(sPath, stages[StageName][0]), 'rb') as f:
            archive = Sarc(yaz0.decompress(f.read()))
        mapYML = byml.to_text(byml.from_binary(archive.get_file(stages[StageName][0][:stages[StageName][0].index('.')] + 'Map.byml').data)).split('\n')  # Stack Overflow occurs with some files when running byml.from_binary(<file>), hence the affected stages are blocked from using this function.
        mapYML.pop()
        print('Opened ' + stages[StageName][0])

        # Loop through the YML to find and replace the proper Goal Pole
        if StageName in ['KoopaChaseLv1Stage', 'KillerTankStage', 'KillerExpressStage', 'GateKeeperTentackLv1Stage', 'BossGorobonStage', 'BossWackunFortressStage', 'BombTankStage', 'GateKeeperBossBunretsuLv1Stage', 'KoopaChaseLv2Stage', 'EnemyExpressStage', 'GateKeeperBossBunretsuLv2Stage', 'GateKeeperTentackLv2Stage', 'ArrangeBossParadeStage']:
            # Stages which share goal zones
            shared = {'CastleGoalZone': ['CastleGoalZone.szs', ['DofParam_obj0.bagldof',
                                                                'CastleGoalZoneDesign.byml',
                                                                'DofParam_obj1.bagldof',
                                                                'DofParam_obj2.bagldof',
                                                                'CameraParam.byml',
                                                                'CastleGoalZoneMap.byml']],
                      'GKCastleGoalZone': ['GKCastleGoalZone.szs', ['DofParam_obj0.bagldof',
                                                                    'DofParam_obj1.bagldof',
                                                                    'GKCastleGoalZoneMap.byml',
                                                                    'DofParam_obj2.bagldof',
                                                                    'CameraParam.byml',
                                                                    'GKCastleGoalZoneDesign.byml']]
                      }
            if 'GateKeeper' in StageName:
                zone = 'GKCastleGoalZone'
            else:
                zone = 'CastleGoalZone'
            zoneName = zone[:-8] + changeTo + 'Zone'
            if not os.path.isfile(os.path.join(srPath, zoneName + '.szs')):
                print('Opening ' + shared[zone][0])
                with open(os.path.join(sPath, shared[zone][0]), 'rb') as f:
                    archive1 = Sarc(yaz0.decompress(f.read()))
                zoneYML = byml.to_text(byml.from_binary(archive1.get_file(shared[zone][0][:shared[zone][0].index('.')] + 'Map.byml').data)).split('\n')
                zoneYML.pop()
                print('Opened ' + shared[zone][0])

                for line in zoneYML:
                    if line[line.index(':') + 2:] == str(changeFrom) and 'UnitConfigName: ' in line:
                        zoneYML[zoneYML.index(line)] = line[:line.index(':') + 2] + str(changeTo)
                        print(str(StageName) + ': Changing from ' + str(changeFrom) + ' to ' + str(changeTo))
                print(str(zone) + ': Changed from ' + str(changeFrom) + ' to ' + str(changeTo))

                print('Writing ' + zoneName + '.szs')
                writer = SarcWriter()
                writer.set_endianness(endianness)
                for i in shared[zone][1]:
                    if zone in i:
                        if 'Map' in i:
                            writer.files[zoneName + i[len(zone):]] = byml.to_binary(byml.from_text('\n'.join(zoneYML)), False, 2)
                        else:
                            writer.files[zoneName + i[len(zone):]] = Bytes(archive1.get_file(i).data)
                    else:
                        writer.files[i] = Bytes(archive1.get_file(i).data)
                data = writer.write()

                with open(os.path.join(srPath, zoneName + '.szs'), 'wb') as f:
                    f.write(yaz0.compress(data[1]))
                print('Written ' + zoneName + '.szs')
            else:
                print('New zone file already exists.')

            for line in mapYML:
                if line[line.index(':') + 2:] == str(zone) and 'UnitConfigName: ' in line:
                    mapYML[mapYML.index(line)] = line[:line.index(':') + 2] + str(zoneName)
                    print(str(StageName) + ': Changing from ' + str(zone) + ' to ' + str(zoneName))
            print(str(StageName) + ': Changed from ' + str(zone) + ' to ' + str(zoneName))

        else:
            # All other stages
            for line in mapYML:
                if line[line.index(':') + 2:] == str(changeFrom) and 'UnitConfigName: ' in line:
                    mapYML[mapYML.index(line)] = line[:line.index(':') + 2] + str(changeTo)
                    print(str(StageName) + ': Changing from ' + str(changeFrom) + ' to ' + str(changeTo))
            print(str(StageName) + ': Changed from ' + str(changeFrom) + ' to ' + str(changeTo))

        print('Writing ' + stages[StageName][0])
        writer = SarcWriter()
        writer.set_endianness(endianness)
        for i in stages[StageName][1]:
            if i == stages[StageName][0][:stages[StageName][0].index('.')] + 'Map.byml':
                writer.files[i] = byml.to_binary(byml.from_text('\n'.join(mapYML)), False, 2)
            else:
                writer.files[i] = Bytes(archive.get_file(i).data)
        data = writer.write()

        with open(os.path.join(srPath, stages[StageName][0]), 'wb') as f:
            f.write(yaz0.compress(data[1]))
        print('Written ' + stages[StageName][0])
    except KeyError:
        print('No Goal Pole present.')


# Music randomizer
def musicRandomizer(rng, seedRNG, user_data):
    print('Randomizing music...')

    # Creating variables for the directories we are working with.
    mPath = os.path.join(user_data[0], 'SoundData', 'stream')
    rPath = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'SoundData', 'stream')
    os.makedirs(rPath)
    if os.path.isdir(os.path.join(user_data[0], 'SoundData', 'streamSe')):
        mPath2 = os.path.join(user_data[0], 'SoundData', 'streamSe')
        rPath2 = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'SoundData', 'streamSe')
        os.makedirs(rPath2)
        # Making a list comprising the names of every file in the directory
        musicRando_order = os.listdir(mPath) + os.listdir(mPath2)
    else:
        # This is here for the Wii U version which doesn't have the Bowser's Fury music folder
        musicRando_order = os.listdir(mPath)

    # Creating a music index variable and randomized number history variable in a similar to the level randomizer.
    rmusicRando_order = rng.choice(musicRando_order, size=len(musicRando_order), replace=False)

    if dpg.get_value("music"):
        # Loop for music randomization
        for music in musicRando_order:
            rmusic = rmusicRando_order[musicRando_order.index(music)]
            # Renaming music file to randomized music file using the list.
            if (music == 'DemoSingleModeEnding.dspadpcm.bfstm' or music == 'SingleModeOpening.dspadpcm.bfstm') and (
                    rmusic == 'DemoSingleModeEnding.dspadpcm.bfstm' or rmusic == 'SingleModeOpening.dspadpcm.bfstm'):
                shutil.copy2(os.path.join(mPath2, music), os.path.join(rPath2, rmusic))
            elif (music != 'DemoSingleModeEnding.dspadpcm.bfstm' or music != 'SingleModeOpening.dspadpcm.bfstm') and (
                    rmusic == 'DemoSingleModeEnding.dspadpcm.bfstm' or rmusic == 'SingleModeOpening.dspadpcm.bfstm'):
                shutil.copy2(os.path.join(mPath, music), os.path.join(rPath2, rmusic))
            elif (music == 'DemoSingleModeEnding.dspadpcm.bfstm' or music == 'SingleModeOpening.dspadpcm.bfstm') and (
                    rmusic != 'DemoSingleModeEnding.dspadpcm.bfstm' or rmusic != 'SingleModeOpening.dspadpcm.bfstm'):
                shutil.copy2(os.path.join(mPath2, music), os.path.join(rPath, rmusic))
            else:
                shutil.copy2(os.path.join(mPath, music), os.path.join(rPath, rmusic))
            print('Renamed', music, 'to', rmusic)

        print('Music randomizer procedure complete!')
    else:
        print('Not changing music files.')


# Language randomizer
def langRandomizer(rng, seedRNG, user_data):
    print('Randomizing language...')

    lPath = os.path.join(user_data[0], 'LocalizedData')
    rlPath = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'LocalizedData')
    os.makedirs(rlPath)

    Lang_order = os.listdir(lPath)
    Lang_order.pop(Lang_order.index('Common'))
    rLang_order = rng.choice(Lang_order, size=len(Lang_order), replace=False)

    if dpg.get_value('lang'):
        for lang in Lang_order:
            rlang = rLang_order[Lang_order.index(lang)]
            shutil.copytree(os.path.join(lPath, lang), os.path.join(rlPath, rlang))
            print('Renamed', lang, 'to', rlang)

        print('Language randomizer procedure complete!')
    else:
        print('Not changing language files.')


# Spoiler file generation
def spoilerFile(StageListNew, seedRNG, GreenStarLockHistory, GreenStarLockHistory2, user_data):
    print('Generating spoiler file...')
    levelIndex = 1
    worldIndex = 1
    overallIndex = 1
    overallIndex2 = 1
    if len(str(dpg.get_value('seed'))) == 0:
        stageID_Name = ['Seed: ' + str(seedRNG) + ' (Random seed, ' + version + ')\n\n']
    else:
        stageID_Name = ['Seed: ' + str(seedRNG) + ' (Set seed, ' + version + ')\n\n']
    stageID_Name.append('Settings:\n')
    stageID_Name.append('Speedrunner mode: ' + str(dpg.get_value('speedrun')) + '\n')
    stageID_Name.append('Generate spoiler file?: ' + str(dpg.get_value('spoil')) + '\n')
    stageID_Name.append('Randomize music?: ' + str(dpg.get_value('music')) + '\n')
    stageID_Name.append('Randomize language?: ' + str(dpg.get_value('lang')) + '\n')
    if str(dpg.get_value('star')) == 'Fully random':
        stageID_Name.append('Green star locks?: ' + str(dpg.get_value('star')) + '\n')
        stageID_Name.append('Green star lock probability: ' + str(dpg.get_value('pslider')) + '\n')
        stageID_Name.append('Green star lock strictness: ' + str(dpg.get_value('sslider')))
    else:
        stageID_Name.append('Green star locks?: ' + str(dpg.get_value('star')))
    stageID_Name.append('\n\nLevel slot: Level name (Original level slot) (Green Stars required to unlock)\n\nWorld ' + str(worldIndex) + '\n')

    # Appending the name of each stage to stageID_name.
    while overallIndex <= 154:
        if overallIndex != 34 and overallIndex != 62 and overallIndex != 63 and overallIndex != 64 and overallIndex != 65 and overallIndex != 66 and overallIndex != 81 and overallIndex != 97 and overallIndex != 115:
            # World 1
            if StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: EnterCatMarioStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Super Bell Hill (1-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: NokonokoCaveStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Koopa Troopa Cave (1-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ClimbMountainStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mount Beanpole (1-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DownRiverStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Plessie\'s Plunging Falls (1-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: FlipCircusStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Switch Scramble Circus (1-5)\n')
            # Toad House
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioHouseLv1BlueStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioHouseLv2BlueStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioHouseLv3BlueStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioHouseLv1InsideStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioHouseLv3LavaStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioHouseLv3NightStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Toad House\n')
            # World 1 continued
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioBrigadeTentenStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Captain Toad Goes Forth (1-Captain Toad)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KoopaChaseLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Bowser\'s Highway Showdown (1-Castle)\n')
            # Lucky House (Roulette)
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: RouletteRoomZone':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Lucky House\n')
            # World 1 continued
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperBullLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Chargin\' Chuck Blockade (1-A)\n')
            # World 2
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: SideWaveDesertStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Conkdor Canyon (2-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: TouchAndMikeStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Puffprod Peaks (2-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ShadowTunnelStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Shadow-Play Alley (2-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: RotateFieldStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Really Rolling Hills (2-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DoubleMarioFieldStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Double Cherry Pass (2-5)\n')
            # Stamp House
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: FairyHouseBlueStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: FairyHouseInsideStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: FairyHouseLavaStage' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: FairyHouseNightStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Sprixie House\n')
            # World 2 continued
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: MysteryHouseEnemyStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mystery House Melee (2-Mystery House)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KillerTankStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Bowser\'s Bullet Bill Brigade (2-Tank)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperKuribonLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Big Galoomba Blockade (2-A)\n')
            # World 3
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: SnowBallParkStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Snowball Park (3-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ClimbWirenetStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Chainlink Charge (3-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: TeresaConveyorStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Shifty Boo Mansion (3-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ShortGardenStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Pretty Plaza Panic (3-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DokanAquariumStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Pipeline Lagoon (3-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DashRidgeStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mount Must Dash (3-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: TruckWaterfallStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Switchboard Falls (3-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioBrigadeWaterStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Captain Toad Makes a Splash (3-Captain Toad)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KillerExpressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': The Bullet Bill Express (3-Train)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperKameckLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Magikoopa Blockade (3-A)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperTentackLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': A Banquet with Hisstrocrat (3-B)\n')
            # World 4
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: CrawlerHillStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Ant Trooper Hill (4-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: PipePackunDenStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Piranha Creeper Creek (4-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ChikaChikaBoomerangStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Beep Block Skyway (4-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: TrampolineHighlandStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Big Bounce Byway (4-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GabonMountainStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Spike\'s Lost City (4-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: MysteryHouseDashStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mystery House Mad Dash (4-Mystery House)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BossGorobonStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Lava Rock Lair (4-Castle)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperGorobonLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Brolder Blockade (4-A)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperFireBrosLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Fire Bros. Hideout #1 (4-B)\n')
            # World 5
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: NokonokoBeachStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Sunshine Seaside (5-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: SwingCircusStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Tricky Trapeze Theater (5-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ShortMultiLiftStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Backstreet Bustle (5-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: SavannaRockStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Sprawling Savanna (5-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BombCaveStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Bob-ombs Below (5-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: JumpFlipSweetsStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Cakewalk Flip (5-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: SneakingLightStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Searchlight Sneak (5-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GoldenExpressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Coin Express (5-Train)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioBrigadeTeresaStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Captain Toad Plays Peek-a-Boo (5-Captain Toad)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BossWackunFortressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': King Ka-thunk\'s Castle (5-Castle)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperBullLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Chargin\' Chuck Blockade is Back (5-A)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperFireBrosLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Fire Bros. Hideout #2 (5-B)\n')
            # World 6
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: RouteDokanTourStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Clear Pipe Cruise (6-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: WeavingShipStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Spooky Seasick Wreck (6-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KarakuriCastleStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Hands-On Hall (6-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: JungleCruiseStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Deep Jungle Drift (6-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BlastSnowFieldStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Ty-Foo Flurries (6-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ClimbFortressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Bullet Bill Base (6-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ChorobonTowerStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Fuzzy Time Mine (6-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: MysteryHouseBallStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mystery House Throwdown (6-Mystery House)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BombTankStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Bowser\'s Bob-omb Brigade (6-Tank)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperKyupponLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Prince Bully Blockade (6-A)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperFireBrosLv3Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Fire Bros. Hideout #3 (6-B)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperBossBunretsuLv1Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Motley Bossblob\'s Big Battle (6-C)\n')
            # World Castle
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: FireBrosFortressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Fort Fire Bros. (Castle-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DarkFlipPanelStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Switchblack Ruins (Castle-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ShortAmidaStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Red-Hot Run (Castle-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DonketsuArrowStepStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Boiling Blue Bully Belt (Castle-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ZigzagBuildingStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Trick Trap Tower (Castle-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: SyumockSpotStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Rammerhead Reef (Castle-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: RagingMagmaStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Simmering Lava Lake (Castle-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioBrigadeConveyorStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Captain Toad Gets Thwomped (Castle-Captain Toad)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KoopaChaseLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Bowser\'s Lava Lake Keep (Castle-Castle)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperGorobonLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Brolder Blockade Is Back (Castle-A)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperKyupponLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Prince Bully Blockade Is Back (Castle-B)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperFireBrosLv4Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Fire Bros. Hideout #4 (Castle-C)\n')
            # World Bowser
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: NeedleBridgeStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Spiky Spike Bridge (Bowser-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DownDesertStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Plessie\'s Dune Downhill (Bowser-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GearSweetsStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Cookie Cogworks (Bowser-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: EchoRoadStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Footlight Lane (Bowser-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: WaterElevatorCaveStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Deepwater Dungeon (Bowser-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: DarknessHauntedHouseStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': A Beam in the Dark (Bowser-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GotogotonValleyStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Grumblump Inferno (Bowser-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: MysteryHouseClimbStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mystery House Claw Climb (Bowser-Mystery House)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: EnemyExpressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': The Bowser Express (Bowser-Train)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KoopaLastStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': The Great Tower of Bowser Land (Bowser-Castle)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperBossBunretsuLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Motley Bossblob\'s Encore (Bowser-A)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GateKeeperTentackLv2Stage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Hisstocrat Returns (Bowser-B)\n')
            # World Star
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: RainbowRoadStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Rainbow Run (Star-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GalaxyRoadStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Super Galaxy (Star-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: WheelCanyonStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Rolling Ride Run (Star-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GoalPoleRunawayStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': The Great Goal Pole (Star-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BlockLandStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Super Block Land (Star-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: HexScrollStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Honeycomb Starway (Star-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: GiantUnderGroundStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Gargantuan Grotto (Star-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: TerenFogStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Peepa\'s Fog Bog (Star-8)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: BoxKillerStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Cosmic Cannon Cluster (Star-9)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioBrigadeRotateRoomStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Captain Toad Takes a Spin (Star-Captain Toad)\n')
            # World Mushroom
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeRotateFieldStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Night Falls on Really Rolling Hills (Mushroom-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeClimbMountainStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Spiky Mount Beanpole (Mushroom-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeJungleCruiseStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Deep-Black Jungle Drift (Mushroom-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeShadowTunnelStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Trouble in Shadow-Play Alley (Mushroom-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeKarakuriCastleStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Back to Hands-On Hall (Mushroom-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeWeavingShipStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Gigantic Seasick Wreck (Mushroom-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeDonketsuArrowStepStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Broken Blue Bully Belt (Mushroom-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeMysteryHouseEnemyStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mystery House Brawl (Mushroom-Mystery House)\n')
            # World Flower
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeFlipCircusStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Switch Shock Circus (Flower-1)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeChorobonTowerStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Floating Fuzzy Time Mine (Flower-2)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangePipePackunDenStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Piranha Creeper Creek after Dark (Flower-3)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeFireBrosFortressStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Faster Fort Fire Bros. (Flower-4)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeSavannaRockStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Sprawling Savanna Rabbit Run (Flower-5)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeTeresaConveorStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Shiftier Boo Mansion (Flower-6)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeDokanAquariumStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Pipeline Boom Lagoon (Flower-7)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeChikaChikaBoomerangStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Blast Block Skyway (Flower-8)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeNokonokoBeachStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Towering Sunshine Seaside (Flower-9)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeHexScrollStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Honeycomb Skyway (Flower-10)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeNeedleBridgeStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Spiky Spike Bridge Sneak (Flower-11)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ArrangeBossParadeStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Boss Blitz (Flower-12)\n')
            # World Crown
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: ChampionshipStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Champion\'s Road (Crown-Crown)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: KinopioBrigadeInfernoStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Captain Toad\'s Fiery Finale (Crown-Captain Toad)\n')
            elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex))) + 8] == '    StageName: MysteryHouseMaxStage':
                stageID_Name.append(str(worldIndex)+'-' + str(levelIndex) + ': Mystery House Marathon (Crown-Mystery House)\n')

            # Denoting Green Star Lock requirements
            if dpg.get_value("star") == 'Random values':
                try:
                    if int(GreenStarLockHistory[overallIndex]) > 1:
                        stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory[overallIndex]) + ' Green Stars to unlock)\n'
                    elif int(GreenStarLockHistory[overallIndex]) == 1:
                        stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory[overallIndex]) + ' Green Star to unlock)\n'
                except KeyError:
                    pass
            elif dpg.get_value("star") == 'Fully random':
                try:
                    if GreenStarLockHistory2[overallIndex2 - 1][1] != 0 and GreenStarLockHistory2[overallIndex2 - 1][0] and overallIndex != 34 and overallIndex != 62 and overallIndex != 63 and overallIndex != 64 and overallIndex != 65 and overallIndex != 66 and overallIndex != 81 and overallIndex != 97 and overallIndex != 115:
                        if int(GreenStarLockHistory2[overallIndex2 - 1][1]) > 1:
                            stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory2[overallIndex2 - 1][1]) + ' Green Stars to unlock)\n'
                        else:
                            stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory2[overallIndex2 - 1][1]) + ' Green Star to unlock)\n'
                except KeyError:
                    pass

        # Increment to next world.
        if worldIndex == 1 and levelIndex == 11:
            worldIndex = 2
            stageID_Name.append('\nWorld ' + str(worldIndex) + '\n')
            levelIndex = 1
        elif worldIndex == 2 and levelIndex == 11:
            worldIndex = 3
            stageID_Name.append('\nWorld ' + str(worldIndex) + '\n')
            levelIndex = 1
        elif worldIndex == 3 and levelIndex == 15:
            worldIndex = 4
            stageID_Name.append('\nWorld ' + str(worldIndex) + '\n')
            levelIndex = 1
        elif worldIndex == 4 and levelIndex == 12:
            worldIndex = 5
            stageID_Name.append('\nWorld ' + str(worldIndex) + '\n')
            levelIndex = 1
        elif worldIndex == 5 and levelIndex == 20:
            worldIndex = 6
            stageID_Name.append('\nWorld ' + str(worldIndex) + '\n')
            levelIndex = 1
        elif worldIndex == 6 and levelIndex == 16:
            worldIndex = 7
            stageID_Name.append('\nWorld Castle\n')
            levelIndex = 1
        elif worldIndex == 7 and levelIndex == 16:
            worldIndex = 8
            stageID_Name.append('\nWorld Bowser\n')
            levelIndex = 1
        elif worldIndex == 8 and levelIndex == 17:
            worldIndex = 9
            stageID_Name.append('\nWorld Star\n')
            levelIndex = 1
        elif worldIndex == 9 and levelIndex == 12:
            worldIndex = 10
            stageID_Name.append('\nWorld Mushroom\n')
            levelIndex = 1
        elif worldIndex == 10 and levelIndex == 8:
            worldIndex = 11
            stageID_Name.append('\nWorld Flower\n')
            levelIndex = 1
        elif worldIndex == 11 and levelIndex == 12:
            worldIndex = 12
            stageID_Name.append('\nWorld Crown\n')
            levelIndex = 1
        else:
            levelIndex += 1
        overallIndex += 1
        if overallIndex != 34 and overallIndex != 62 and overallIndex != 63 and overallIndex != 64 and overallIndex != 65 and overallIndex != 66 and overallIndex != 81 and overallIndex != 97 and overallIndex != 115:
            overallIndex2 += 1

    stageID_Name[-1] = stageID_Name[-1] + '\n\n'
    for i in hashDict:
        try:
            with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', i[0]), 'rb') as f:
                hash_object = hashlib.md5(f.read())
                stageID_Name.append(i[0] + ' - ' + hash_object.hexdigest() + '\n')
        except FileNotFoundError:
            pass

    spoiler = ''.join(stageID_Name)[:-1]
    # Making sure levels have the correct names.
    rep = spoiler.replace('11-6', 'Flower-6').replace('11-7', 'Flower-7').replace('11-8', 'Flower-8').replace('11-9', 'Flower-9').replace('11-10', 'Flower-10').replace('11-11', 'Flower-11').replace('11-12', 'Flower-12').replace('12-1', 'Crown-Crown').replace('1-9', '1-Castle').replace('4-9', '4-Castle').replace('5-12', '5-Castle').replace('7-11', 'Castle-Castle').replace('8-13', 'Bowser-Castle').replace('2-9', '2-Tank').replace('6-11', '6-Tank').replace('3-11', '3-Train').replace('8-12', 'Bowser-Train').replace('1-6', '1-Toad House 1').replace('1-7', '1-Toad House 2').replace('2-6', '2-Toad House').replace('3-8', '3-Toad House').replace('3-12', '3-Toad House 2 (Unused)').replace('4-6', '4-Toad House').replace('5-9', '5-Toad House').replace('5-13', '5-Toad House 2 (Unused)').replace('5-14', '5-Toad House 3 (Unused)').replace('5-15', '5-Toad House 4 (Unused)').replace('5-16', '5-Toad House 5 (Unused)').replace('5-17', '5-Toad House 6 (Unused)').replace('6-8', '6-Toad House').replace('6-12', '6-Toad House 2 (Unused)').replace('7-8', 'Castle-Toad House').replace('7-12', 'Castle-Toad House 2 (Unused)').replace('8-8', 'Bowser-Toad House 1').replace('8-9', 'Bowser-Toad House 2').replace('8-14', 'Bowser-Toad House 3 (Unused)').replace('2-7', '2-Sprixie House').replace('3-9', '3-Sprixie House').replace('4-7', '4-Sprixie House').replace('5-10', '5-Sprixie House').replace('6-9', '6-Sprixie House').replace('7-9', 'Castle-Sprixie House').replace('8-10', 'Bowser-Sprixie House').replace('9-10', 'Star-Sprixie House').replace('12-2', 'Crown-Sprixie House').replace('1-8', '1-Captain Toad').replace('3-10', '3-Captain Toad').replace('5-11', '5-Captain Toad').replace('7-10', 'Castle-Captain Toad').replace('9-11', 'Star-Captain Toad').replace('12-3', 'Crown-Captain Toad').replace('1-10', 'Lucky House').replace('2-10', 'Lucky House').replace('3-13', 'Lucky House').replace('4-10', 'Lucky House').replace('5-18', 'Lucky House').replace('6-13', 'Lucky House').replace('7-13', 'Lucky House').replace('8-15', 'Lucky House').replace('9-12', 'Lucky House').replace('1-11', '1-A').replace('2-11', '2-A').replace('3-14', '3-A').replace('4-11', '4-A').replace('5-19', '5-A').replace('6-14', '6-A').replace('7-14', 'Castle-A').replace('8-16', 'Bowser-A').replace('3-15', '3-B').replace('4-12', '4-B').replace('5-20', '5-B').replace('6-15', '6-B').replace('7-15', 'Castle-B').replace('8-17', 'Bowser-B').replace('6-16', '6-C').replace('7-16', 'Castle-C').replace('5-8', 'Coin Express').replace('2-8', '2-Mystery House').replace('4-8', '4-Mystery House').replace('6-10', '6-Mystery House').replace('8-11', 'Bowser-Mystery House').replace('10-8', 'Mushroom-Mystery House').replace('12-4', 'Crown-Mystery House').replace('7-', 'Castle-').replace('8-', 'Bowser-').replace('9-', 'Star-').replace('10-', 'Mushroom-').replace('11-', 'Flower-').replace('12-', 'Crown-')

    with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), str(seedRNG) + '-spoiler.txt'), 'w', encoding='utf-8') as s:
        s.write(rep)  # Writing the corrected level slots back to the file.

    print('Generated spoiler file!')


# Load input directory
def directory(sender, app_data):
    dpg.set_value("dirtext", app_data['file_path_name'])  # Update directory text box with selected directory
    checkDirectory()


# Load output directory
def rdirectory(sender, app_data):
    dpg.set_value("rdirtext", app_data['file_path_name'])
    checkDirectory()


# Check if selected directories are valid
def checkDirectory():
    valid = True

    if len(str(dpg.get_value("seed"))) == 0:
        seedRNG = time.time_ns()  # If no seed is entered, then it defaults to time since epoch.
    else:
        try:
            seedRNG = int(dpg.get_value("seed"))  # Try to cast the input as an integer.
        except ValueError:
            seedRNG = 0
            for i in str(dpg.get_value("seed")):
                if seedRNG == 0:
                    seedRNG += ord(i)
                else:
                    seedRNG *= ord(i)

    for i in hashDict:  # Loop through the array to compare the hash, if one file fails, the entire check fails.
        if os.path.isfile(os.path.join(dpg.get_value('dirtext'), i[0])):
            with open(os.path.join(dpg.get_value('dirtext'), i[0]), 'rb') as f:
                hash_object = hashlib.md5(f.read())
                if hash_object.hexdigest() == i[1]:
                    dpg.configure_item("dirbutt", label="Valid Input Directory Loaded!")
                    dpg.configure_item('dirtext', color=(0, 255, 0, 255))
                else:
                    dpg.configure_item("dirbutt", label="Load Input Directory")
                    dpg.configure_item('dirtext', color=(255, 0, 0, 255))
                    valid = False
                    break
        else:
            dpg.configure_item("dirbutt", label="Load Input Directory")
            dpg.configure_item('dirtext', color=(255, 0, 0, 255))
            valid = False

    if os.path.isdir(dpg.get_value('rdirtext')) and not os.path.isdir(os.path.join(dpg.get_value('rdirtext'), 'SM3DWR-' + str(seedRNG))):
        dpg.configure_item('rdirbutt', label='Valid Output Directory Loaded!')
        dpg.configure_item('rdirtext', color=(0, 255, 0, 255))
    else:
        dpg.configure_item("rdirbutt", label="Load Output Directory")
        dpg.configure_item('rdirtext', color=(255, 0, 0, 255))
        valid = False

    if valid:
        dpg.configure_item('randoinit', enabled=True)
        dpg.set_value('randotip', 'Start the randomizer!')
    else:
        dpg.configure_item('randoinit', enabled=False)
        dpg.set_value('randotip', 'To be able to start the randomizer, select a valid input and output directory.')


# Show slider depending on green star setting
def showSlider():
    if dpg.get_value('star') == 'Fully random':
        dpg.show_item('pslider')
        dpg.show_item('sslider')
    else:
        dpg.hide_item('pslider')
        dpg.hide_item('sslider')


# Save settings to json
def saveSettings():
    settings.update({'dir': str(dpg.get_value('dirtext')),
                     'rdir': str(dpg.get_value('rdirtext')),
                     'speedrun': bool(dpg.get_value('speedrun')),
                     'spoil': bool(dpg.get_value('spoil')),
                     'music': bool(dpg.get_value('music')),
                     'lang': bool(dpg.get_value('lang')),
                     'star': str(dpg.get_value('star')),
                     'pslider': float(dpg.get_value('pslider')),
                     'sslider': float(dpg.get_value('sslider'))})

    with open('settings.json', 'w') as s:
        s.write(json.dumps(settings))


# Speedrunner mode locking settings
def speedrunner():
    if dpg.get_value('speedrun'):
        dpg.set_value('spoil', False)
        dpg.configure_item('spoil', enabled=False)
        dpg.set_value('music', False)
        dpg.configure_item('music', enabled=False)
        dpg.set_value('lang', False)
        dpg.configure_item('lang', enabled=False)
        dpg.set_value('star', 'Fully random')
        dpg.configure_item('star', enabled=False)
        dpg.set_value('pslider', 0.15000000596046448)
        dpg.configure_item('pslider', enabled=False, show=True)
        dpg.set_value('sslider', 0.606080949306488)
        dpg.configure_item('sslider', enabled=False, show=True)
    else:
        dpg.configure_item('spoil', enabled=True)
        dpg.configure_item('music', enabled=True)
        dpg.configure_item('lang', enabled=True)
        dpg.configure_item('star', enabled=True)
        dpg.configure_item('pslider', enabled=True)
        dpg.configure_item('sslider', enabled=True)


# Render DearPyGUI
def show():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main Window", True)  # Makes it so the UI fills the window
    dpg.start_dearpygui()
    dpg.destroy_context()


# Main Program Window
class GUI:
    def __init__(self, p_title, p_size, p_settings):
        # DearPyGUI setup
        dpg.create_context()
        dpg.create_viewport(title=p_title, width=p_size[0], height=p_size[1])
        dpg.set_viewport_small_icon("ico.ico")
        dpg.set_viewport_large_icon("ico.ico")

        with dpg.window(tag="Main Window", label="Program"):
            with dpg.tab_bar():  # Add tabs which the user can change between
                with dpg.tab(tag="t1", label="Program"):  # The main, default tab
                    dpg.add_text("Hello, welcome to the Super Mario 3D World Randomizer!")
                    dpg.add_text(tag="dirtext", default_value=str(p_settings['dir']))  # Selected Directory
                    dpg.add_file_dialog(directory_selector=True, show=False, tag="dir", width=600, height=600, callback=directory, default_path=str(dpg.get_value('dirtext')))  # Directory Selector
                    self.dir = dpg.add_button(tag="dirbutt", label="Load Input Directory", callback=lambda: dpg.show_item("dir"))  # Load Directory Button
                    dpg.add_text(tag="rdirtext", default_value=str(p_settings['rdir']))  # Selected Directory
                    dpg.add_file_dialog(directory_selector=True, show=False, tag="rdir", width=600, height=600, callback=rdirectory, default_path=str(dpg.get_value('rdirtext')))  # Directory Selector
                    self.rdir = dpg.add_button(tag="rdirbutt", label="Load Output Directory", callback=lambda: dpg.show_item("rdir"))  # Load Directory Button
                    self.seed = dpg.add_input_text(tag="seed", label="Seed", default_value="", callback=checkDirectory)  # Seed Input Text
                    self.rando = dpg.add_button(tag="randoinit", label="Randomize!", enabled=False, callback=randomizer)  # Randomize Button
                    dpg.add_progress_bar(tag="progress", label="progress", default_value=0)
                    dpg.add_text("This randomizer only effects Super Mario 3D World (Switch), not Bowser's Fury.")
                    self.test = dpg.add_button(tag="test", label="test", callback=lambda: dpg.configure_item("progress", default_value=1), show=False)
                    with dpg.tooltip("dirbutt"):
                        dpg.add_text("The directory selected must be the root directory of an unmodified dump of the game:\n" +
                                     "\"" + os.path.join("010028600EBDA000", "romfs") + "\" - Super Mario 3D World + Bowser's Fury")
                    with dpg.tooltip("rdirbutt"):
                        dpg.add_text("Select your desired output folder of choice. The recommended output folder would "
                                     "be your mods folder:\n" +
                                     "\"" + os.path.join("sd:", "atmosphere", "contents", "010028600EBDA000") + "\"* - Atmosphere (Switch)\n"
                                     "\"" + os.path.join("sd:", "mods", "Super Mario 3D World + Bowser's Fury", "<name of your choice>", "contents", "010028600EBDA000") + "\"* - SMM (Switch)\n"
                                     "\"" + os.path.join("Ryujinx", "mods", "contents", "010028600EBDA000") + "\" - Ryujinx (Switch)\n\n"
                                     "*The \"romfs\" folder inside the generated \"SM3DWR-<seed>\" folder should be taken out and placed into the\n"
                                     "specified Atmosphere or SimpleModManager (SMM) folder.\n\n"
                                     "Note: Yuzu is not officially supported and you may encounter issues if you use it.")
                    with dpg.tooltip('randoinit'):
                        dpg.add_text('To be able to start the randomizer, select a valid input directory.', tag='randotip')
                checkDirectory()
                with dpg.tab(tag="t2", label="Misc. Settings"):  # Settings tab
                    self.speedrun = dpg.add_checkbox(tag='speedrun', label='Speedrunner mode', default_value=bool(p_settings['speedrun']), callback=speedrunner)
                    self.spoil = dpg.add_checkbox(tag="spoil", label="Generate spoiler file?", default_value=bool(p_settings['spoil']))
                    self.music = dpg.add_checkbox(tag="music", label="Randomize music?", default_value=bool(p_settings['music']))
                    self.lang = dpg.add_checkbox(tag="lang", label="Randomize language?", default_value=bool(p_settings['lang']))
                    dpg.add_text('Green star locks:')
                    self.star = dpg.add_radio_button(('Fully random', 'Random values', 'Disabled'), tag='star', horizontal=True, default_value=str(p_settings['star']), callback=showSlider)
                    self.pslider = dpg.add_slider_float(tag='pslider', label='Green star lock probability', default_value=float(p_settings['pslider']), min_value=0, max_value=1, show=True, clamped=True)
                    self.sslider = dpg.add_slider_float(tag='sslider', label='Green star lock strictness', default_value=float(p_settings['sslider']), min_value=0, max_value=1, show=True, clamped=True)
                    self.save = dpg.add_button(tag='save', label='Save Settings', callback=saveSettings)
                    with dpg.tooltip('speedrun'):
                        dpg.add_text('Lock the settings to be compatible with the official speedrun leaderboards.')
                    with dpg.tooltip('spoil'):
                        dpg.add_text('Generate a text file which contains the full list of levels and what they have\n'
                                     'been randomized to, along with any green star lock values.')
                    with dpg.tooltip('star'):
                        dpg.add_text('Fully random: The green star locks can be placed anywhere and their\n'
                                     'requirement value will change accordingly.\n'
                                     'Random values: The green star locks are in their vanilla positions\n'
                                     'but their requirement value will change depending on the levels\n'
                                     'generated beforehand.\n'
                                     'Disabled: All green star locks will be removed from the game.')
                    with dpg.tooltip('music'):
                        dpg.add_text('Randomize the filenames for the music files.')
                    with dpg.tooltip('lang'):
                        dpg.add_text('Randomize the selected language. Will be the same language for everything.')
                    with dpg.tooltip('pslider'):
                        dpg.add_text('CTRL+Left Click to enter a specific value.\n'
                                     'Control how often green star locks should appear.\n'
                                     'Setting the slider to 1 (maximum) will not make every level have a star lock to avoid softlocks.')
                    with dpg.tooltip('sslider'):
                        dpg.add_text('CTRL+Left Click to enter a specific value.\n'
                                     'Control the strictness for how many green stars you need to have to open the green star locks.')
                showSlider()
                speedrunner()
                with dpg.tab(tag="t3", label="Credits"):  # Credits tab
                    dpg.add_text("Super Mario 3D World Randomizer credits:\n\n"
                                 "Executable built using Nuitka.\n\n"
                                 "Developer:\n"
                                 "Skipper93653 (Toby Bailey)\n\n"
                                 "Module Credits:\n"
                                 "ZeldaMods for oead. oead is licensed under GPL-v2.0. Copyright (c) 2024 ZeldaMods\n"
                                 "Jonathan Hoffstadt for Dear PyGUI. Dear PyGUI is licensed under MIT. Copyright (c) 2024 Dear PyGui, LLC\n"
                                 "Built-in Python modules.\n"
                                 "...And all of their contributors.\n\n"
                                 "Testers:\n"
                                 "Skipper93653\n"
                                 "Nintensive\n"
                                 "FortTheo\n"
                                 "Baconsizzles_\n"
                                 "RKGGame\n\n"
                                 "Special Thanks:\n"
                                 "Nintendo EAD/EPD for creating the game.\n"
                                 "Members of the ZeldaMods Discord server for oead help.\n"
                                 "Members of the 3D World Modding Community Discord server for general help.\n\n"
                                 "SM3DW-BF-Randomizer is licensed under GPL-v2.0.\n"
                                 "Copyright (c) 2024 Toby Bailey")
        with dpg.window(label="Finished!", modal=True, tag="popup", show=False, autosize=True):
            dpg.add_text("Randomization complete!")
            dpg.add_text("", tag='popupSeed')
            dpg.add_text("Settings:")
            dpg.add_text('Speedrunner mode: '+str(dpg.get_value('speedrun')), tag='popupSpeedrun')
            dpg.add_text("Generate spoiler file?: "+str(dpg.get_value('spoil')), tag='popupSpoil')
            dpg.add_text("Randomize music?: "+str(dpg.get_value('music')), tag='popupMusic')
            dpg.add_text("Randomize language?: "+str(dpg.get_value('lang')), tag='popupLang')
            dpg.add_text("Green star locks: "+str(dpg.get_value('star')), tag='popupStar')
            dpg.add_text("", tag='popupPslider')
            dpg.add_text("", tag='popupSslider')
            dpg.add_button(label="Close", callback=lambda: dpg.configure_item("popup", show=False))


# Main program
def main():
    global settings, interface, version, hashDict
    version = 'v3.0.0'

    # MD5 hash 2D array for file verification, only Switch version at the moment.
    hashDict = [[os.path.join('SystemData', 'StageList.szs'), 'e267c452769c2cc45670b58234fbc3e5'],
                [os.path.join('StageData', 'CourseSelectW1Zone.szs'), '372523814613f05923fd8672938324de'],
                [os.path.join('StageData', 'CourseSelectW2Zone.szs'), '79d177268cc140588da9af1b0ccee25b'],
                [os.path.join('StageData', 'CourseSelectW3Zone.szs'), 'f49ae49045ab8918731bb2a7510a1afe'],
                [os.path.join('StageData', 'CourseSelectW4Zone.szs'), 'b20cbac5ecc3cbfe751fd632e36285a7'],
                [os.path.join('StageData', 'CourseSelectW5Zone.szs'), '14133c3aa06838074b483f4d8c7aaddc'],
                [os.path.join('StageData', 'CourseSelectW6Zone.szs'), '33beb74589dab18b328a855e43195b38'],
                [os.path.join('StageData', 'CourseSelectW7Zone.szs'), 'e95a6fd9162f5eeefb06fb461e9ad514'],
                [os.path.join('StageData', 'CourseSelectW8Zone.szs'), '0c93355dd9a30287006d97a90b2fc9c1'],
                [os.path.join('StageData', 'CourseSelectS1Zone.szs'), '5e534b8ea2068faa1cba9d0e124135e6'],
                [os.path.join('StageData', 'EnterCatMarioStage.szs'), 'af8dcf610c34e5bd64fb8344062a24fd'],
                [os.path.join('StageData', 'NokonokoCaveStage.szs'), '9a4d24f348bb7c4d52748d8bb3849245'],
                [os.path.join('StageData', 'ClimbMountainStage.szs'), '6507f04bf7e6b8cefe8db7c89aaa3d66'],
                [os.path.join('StageData', 'DownRiverStage.szs'), 'f705560b0befa8eb403fce9681f2766c'],
                [os.path.join('StageData', 'FlipCircusStage.szs'), 'd3b65824e48df2c20f36cf88457fba07'],
                [os.path.join('StageData', 'KoopaChaseLv1Stage.szs'), 'd771745e10a450c4c418760f58f132fd'],
                [os.path.join('StageData', 'SideWaveDesertStage.szs'), 'db058aabcf057c7e22d7b86b84331550'],
                [os.path.join('StageData', 'TouchAndMikeSecondZone.szs'), '716248ef3b7342b1957cdc02f264bf39'],
                [os.path.join('StageData', 'ShadowTunnelStage.szs'), 'cff0484f5df61f53adda6ba00a7de22a'],
                [os.path.join('StageData', 'RotateFieldGoalZone.szs'), '10edd81cd378dd38d8029a03c3c9b13c'],
                [os.path.join('StageData', 'DoubleMarioFieldStage.szs'), '476b0ed08205b201d7e4ce48791a8b6b'],
                [os.path.join('StageData', 'KillerTankStage.szs'), '7b49f92b6d7cfc114caa7328a09a157f'],
                [os.path.join('StageData', 'SnowBallParkStage.szs'), '4d156d72768e7af2349633bb0002d6c0'],
                [os.path.join('StageData', 'ClimbWirenetStage.szs'), '9566a5d3efed98459623be0519bb8922'],
                [os.path.join('StageData', 'TeresaConveyorStage.szs'), 'c734a9133dc75d116693f37f8fb8967e'],
                [os.path.join('StageData', 'ShortGardenStage.szs'), 'a38c6383e82fe80f095119c243240a07'],
                [os.path.join('StageData', 'DokanAquariumGoalZone.szs'), '4a9610b02a249c3f51897b690f5c51de'],
                [os.path.join('StageData', 'DashRidgeGoalZone.szs'), '5d38430abef73e734bb16b1768a6a8db'],
                [os.path.join('StageData', 'TruckWaterfallStage.szs'), 'a65c4858a04c898b8797265c56f90e9d'],
                [os.path.join('StageData', 'KillerExpressStage.szs'), 'a163415a0a334b4313f9f05985799743'],
                [os.path.join('StageData', 'GateKeeperTentackLv1Stage.szs'), '1c0fdaf0c01cd6273e19434615e35d42'],
                [os.path.join('StageData', 'CrawlerHillStage.szs'), '283bd56ba10751165ec0ffb2c8a429a1'],
                [os.path.join('StageData', 'PipePackunDenGoalZone.szs'), '0659d312297da35639371ee8b232f261'],
                [os.path.join('StageData', 'ChikaChikaBoomerangCZone.szs'), '22461f6f2e7e419840ea5e6ae2bcc1c7'],
                [os.path.join('StageData', 'TrampolineHighlandStage.szs'), '811bf2091826a35df319317253144dd0'],
                [os.path.join('StageData', 'GabonMountainStage.szs'), '5b1f5678cbe47860de1d7b671d8d1f46'],
                [os.path.join('StageData', 'BossGorobonStage.szs'), '4a268c4dc6c3d561b72e07cfc2fdcbc4'],
                [os.path.join('StageData', 'NokonokoBeachStage.szs'), '0ddbd3cc3863db4fff7fe8660e3e8b7a'],
                [os.path.join('StageData', 'SwingCircusStage.szs'), '73838e44253443b9aa74429197470109'],
                [os.path.join('StageData', 'ShortMultiLiftStage.szs'), '02cf1c2d5c7e87949e5dc54b5ece0aa1'],
                [os.path.join('StageData', 'SavannaRockStage.szs'), 'b788f07122974d3b4bb4645fda6b9b9c'],
                [os.path.join('StageData', 'BombCaveStage.szs'), '0e9b4c10f4055a71ad4e2f0c01f6e5e2'],
                [os.path.join('StageData', 'JumpFlipSweetsStage.szs'), '42634042934091cc3535c080fd309ec7'],
                [os.path.join('StageData', 'SneakingLightStage.szs'), '965dafa390180456cf13cad6e3d54045'],
                [os.path.join('StageData', 'BossWackunFortressStage.szs'), '9942855cb7167e2b8198c00ac9d7d156'],
                [os.path.join('StageData', 'RouteDokanTourStage.szs'), '97aa1f39863f800b063b249b4a8f450c'],
                [os.path.join('StageData', 'WeavingShipGoalZone.szs'), '99c0dbf5c3a3895c43d7719f490b5d4c'],
                [os.path.join('StageData', 'KarakuriCastleStage.szs'), 'f935189ad818b1c79c99f725171be01e'],
                [os.path.join('StageData', 'JungleCruiseStage.szs'), 'd133ee09acf25ff0d7717075ac9044d0'],
                [os.path.join('StageData', 'BlastSnowFieldStage.szs'), '1c4b703322345a4356fd2d662bec4b66'],
                [os.path.join('StageData', 'ClimbFortressStage.szs'), '1c3e981f58997376e975022dcf0b8f55'],
                [os.path.join('StageData', 'ChorobonTowerStage.szs'), '146216d73b521cbc89661968b6a2aa78'],
                [os.path.join('StageData', 'BombTankStage.szs'), '8a8392bdf2330472ee343823c06a19a0'],
                [os.path.join('StageData', 'GateKeeperBossBunretsuLv1Stage.szs'), 'c9e78cdbfe1d03deb8980fcd6bcddeba'],
                [os.path.join('StageData', 'FireBrosFortressStage.szs'), '719f42e796d70f5763ed81ff478f6db9'],
                [os.path.join('StageData', 'DarkFlipPanelStage.szs'), '1dc1b6241522f5fb2b3b9b3667ee3bea'],
                [os.path.join('StageData', 'ShortAmidaStage.szs'), '7658cafe08abf7eeb6bc513d1c1f48ef'],
                [os.path.join('StageData', 'DonketsuArrowStepGoalZone.szs'), '358672426df75ef2b065d9741c51880c'],
                [os.path.join('StageData', 'ZigzagBuildingStage.szs'), '5e2af872e6ccb1e5a5fa2cab6356b6df'],
                [os.path.join('StageData', 'SyumockSpotGoalZone.szs'), 'b1f9f4545071a29b90ac99b082e3a8ad'],
                [os.path.join('StageData', 'RagingMagmaStage.szs'), '70223364916c33d01a58a194e1858295'],
                [os.path.join('StageData', 'KoopaChaseLv2Stage.szs'), '55cbb6bc99e98259f2ad2e05dae70df5'],
                [os.path.join('StageData', 'NeedleBridgeStage.szs'), 'd02912a80bc1db3ed7746d47b9e8d994'],
                [os.path.join('StageData', 'DownDesertStage.szs'), 'ceca66363c25623ea9e4c78bf2d3b7aa'],
                [os.path.join('StageData', 'GearSweetsStage.szs'), 'b53e6e2b38d6582995fa71ac596990c6'],
                [os.path.join('StageData', 'EchoRoadStage.szs'), 'c373e9ec48d243f53f56c043c178d642'],
                [os.path.join('StageData', 'WaterElevatorCaveStage.szs'), 'ccda4a7f1295f8b4ff38263f19a78c34'],
                [os.path.join('StageData', 'DarknessHauntedHouseStage.szs'), '849623e724d6a7d9e3ce65137743f691'],
                [os.path.join('StageData', 'GotogotonValleyStage.szs'), 'c92c8bd7516043870bafcd397186d6a0'],
                [os.path.join('StageData', 'EnemyExpressStage.szs'), 'fbdb7032420186a14491643ac46591f0'],
                [os.path.join('StageData', 'KoopaLastBZone.szs'), '4146dbdd3200ca39f100a02253e4b5d6'],
                [os.path.join('StageData', 'GateKeeperBossBunretsuLv2Stage.szs'), '93f906bbce3459ea324649b111609a08'],
                [os.path.join('StageData', 'GateKeeperTentackLv2Stage.szs'), 'c7866bd0bb637864e7f554df698742e1'],
                [os.path.join('StageData', 'RainbowRoadStage.szs'), '9c112b9a88b2736a3147bd34d7e9b885'],
                [os.path.join('StageData', 'GalaxyRoadStage.szs'), '7c42386b3ae84188cd3d97354e03f334'],
                [os.path.join('StageData', 'WheelCanyonStage.szs'), '184cfc1fb0087c3cfb95c47ea8508dd9'],
                [os.path.join('StageData', 'BlockLandStage.szs'), '69c602419d7e47d8b6b383f92694c9b5'],
                [os.path.join('StageData', 'HexScrollStage.szs'), '23401c2a1ffb4fb2574fb8c87c37b903'],
                [os.path.join('StageData', 'GiantUnderGroundStage.szs'), '7eea69679f0d95d34320b1021d0ce77e'],
                [os.path.join('StageData', 'TerenFogGoalZone.szs'), '6bf73f54e26e537a935ba07ba7748470'],
                [os.path.join('StageData', 'BoxKillerStage.szs'), '62b28d84ab8f9c3bb9f8a44ffda2db85'],
                [os.path.join('StageData', 'ArrangeRotateFieldGoalZone.szs'), 'ffaad5b488bc8d430459ffd83d30c455'],
                [os.path.join('StageData', 'ArrangeClimbMountainStage.szs'), '949d29ca349bc1ab7c11eba74e8e5df1'],
                [os.path.join('StageData', 'ArrangeJungleCruiseStage.szs'), '3df2810ac0fd0defa9c10d92c4587293'],
                [os.path.join('StageData', 'ArrangeShadowTunnelStage.szs'), '3879b4249cfbd7c8f2015b911354e580'],
                [os.path.join('StageData', 'ArrangeWeavingShipGoalZone.szs'), '7a7c7fe125ed6011fdd24dd5a9a212c3'],
                [os.path.join('StageData', 'ArrangeDonketsuArrowStepZone.szs'), '7335f2663534b8e3912d70c45ce09495'],
                [os.path.join('StageData', 'ArrangeFlipCircusStage.szs'), 'f393029262be02c578716645137e9eb0'],
                [os.path.join('StageData', 'ArrangeChorobonTowerStage.szs'), 'f560dbc0505af477e8adbbd771cd05c4'],
                [os.path.join('StageData', 'ArrangePipePackunDenGoalZone.szs'), 'ab1a0dfe429b44c93bf5798381f5a746'],
                [os.path.join('StageData', 'ArrangeFireBrosFortressStage.szs'), '51f89626e0420d5a6577af33f08ba36d'],
                [os.path.join('StageData', 'ArrangeSavannaRockStage.szs'), '92c85014d500785205d00b6ef0309c7b'],
                [os.path.join('StageData', 'ArrangeTeresaConveorStage.szs'), '02415855a845d388b9f01868ea0730f8'],
                [os.path.join('StageData', 'ArrangeAquariumCZone.szs'), '58b57ab9baa1cee7a2c337ad8fe35e4f'],
                [os.path.join('StageData', 'ArrangeChikaCZone.szs'), 'df40bcfc25142721a1f9cf3fea788d1a'],
                [os.path.join('StageData', 'ArrangeNokonokoBeachStage.szs'), 'ca7d07aa341d9f62c3edc40bab035be8'],
                [os.path.join('StageData', 'ArrangeHexScrollStage.szs'), '6afac4848b5eeab1a05d5d569049823d'],
                [os.path.join('StageData', 'ArrangeNeedleBridgeStage.szs'), '94d4f54b266a69c9abb3d5e048f001a3'],
                [os.path.join('StageData', 'ArrangeBossParadeStage.szs'), '9fdaca7ff79141026f303011434ddd56'],
                [os.path.join('StageData', 'ChampionshipGoalZone.szs'), '4e32514bf17a4d2627c3119382910454'],
                [os.path.join('StageData', 'CastleGoalZone.szs'), '92370bd36a2da3eda344cbf4592d5835'],
                [os.path.join('StageData', 'GKCastleGoalZone.szs'), '7caea9de120c2dadf5ead05f08a0a1aa']]

    if os.path.isfile('settings.json'):
        with open('settings.json', 'r') as s:
            settings = json.loads(s.read())
    else:
        with open('settings.json', 'w') as s:
            settings = {'dir': os.getcwd(),
                        'rdir': os.getcwd(),
                        'speedrun': False,
                        'spoil': True,
                        'music': False,
                        'lang': False,
                        'star': 'Fully random',
                        'pslider': 0.15000000596046448,
                        'sslider': 0.606080949306488}   # 0.6060809576 is the average
            s.write(json.dumps(settings))
    try:
        if float(settings['pslider']) < 0 or float(settings['pslider']) > 1:
            settings.update({'pslider': 0.15000000596046448})
        if float(settings['sslider']) < 0 or float(settings['sslider']) > 1:
            settings.update({'sslider': 0.606080949306488})
        if str(settings['star']) != 'Fully random' and str(settings['star']) != 'Random values' and str(settings['star']) != 'Disabled':
            settings.update({'star': 'Fully random'})
        bool(settings['speedrun'])
        bool(settings['spoil'])
        bool(settings['music'])
        bool(settings['lang'])
    except:
        with open('settings.json', 'w') as s:
            settings = {'dir': os.getcwd(),
                        'rdir': os.getcwd(),
                        'speedrun': False,
                        'spoil': True,
                        'music': False,
                        'lang': False,
                        'star': 'Fully random',
                        'pslider': 0.15000000596046448,
                        'sslider': 0.606080949306488}
            s.write(json.dumps(settings))
    interface = GUI('Super Mario 3D World Randomizer', (800, 800), settings)  # Initialise the main window
    show()  # Show the main window


if __name__ == "__main__":
    main()

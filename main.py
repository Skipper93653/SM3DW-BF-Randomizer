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
    raw = archive.get_file("StageList.byml").data
    raw_binary = byml.from_binary(raw)
    doc = byml.to_text(raw_binary)  # Load BYML file (Wii U file breaks here)
    StageListNew = doc.split('\n')
    StageListNew.pop()
    StageListOld = StageListNew.copy()
    print('Opened StageList.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    # StageData Path
    sPath = os.path.join(user_data[0], 'StageData')
    rPath = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'SystemData')  # Randomizer path
    srPath = os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', 'StageData')
    os.makedirs(rPath)
    os.makedirs(srPath)
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    # Open each world map file and convert the map BYML into a readable format.
    print('Opening CourseSelectW1Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW1Zone.szs'), 'rb') as f:
        w1archive = Sarc(yaz0.decompress(f.read()))
    w1archive1 = w1archive.get_file('DofParam_obj10.bagldof').data
    w1archive2 = w1archive.get_file('DofParam_obj9.bagldof').data
    w1archive3 = w1archive.get_file('DofParam_obj11.bagldof').data
    w1archive4 = w1archive.get_file('CourseSelectW1ZoneDesign.byml').data
    w1archive5 = w1archive.get_file('DofParam_obj6.bagldof').data
    w1archive6 = byml.to_text(byml.from_binary(w1archive.get_file('CourseSelectW1ZoneMap.byml').data))
    w1archive7 = w1archive.get_file('DofParam_obj12.bagldof').data
    w1archive8 = w1archive.get_file('CameraParam.byml').data
    w1archive9 = w1archive.get_file('DofParam_obj7.bagldof').data
    w1archive10 = w1archive.get_file('CourseSelectW1ZoneSound.byml').data
    w1archive11 = w1archive.get_file('DofParam_obj8.bagldof').data
    CourseSelectW1ZoneMapn = w1archive6.split('\n')
    CourseSelectW1ZoneMapn.pop()
    CourseSelectW1ZoneMapo = CourseSelectW1ZoneMapn.copy()
    print('Opened CourseSelectW1Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW2Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW2Zone.szs'), 'rb') as f:
        w2archive = Sarc(yaz0.decompress(f.read()))
    w2archive1 = w2archive.get_file('DofParam_obj4.bagldof').data
    w2archive2 = byml.to_text(byml.from_binary(w2archive.get_file('CourseSelectW2ZoneMap.byml').data))
    w2archive3 = w2archive.get_file('DofParam_obj9.bagldof').data
    w2archive4 = w2archive.get_file('DofParam_obj5.bagldof').data
    w2archive5 = w2archive.get_file('CourseSelectW2ZoneSound.byml').data
    w2archive6 = w2archive.get_file('DofParam_obj6.bagldof').data
    w2archive7 = w2archive.get_file('CameraParam.byml').data
    w2archive8 = w2archive.get_file('DofParam_obj7.bagldof').data
    w2archive9 = w2archive.get_file('DofParam_obj3.bagldof').data
    w2archive10 = w2archive.get_file('CourseSelectW2ZoneDesign.byml').data
    w2archive11 = w2archive.get_file('DofParam_obj8.bagldof').data
    CourseSelectW2ZoneMapn = w2archive2.split('\n')
    CourseSelectW2ZoneMapn.pop()
    CourseSelectW2ZoneMapo = CourseSelectW2ZoneMapn.copy()
    print('Opened CourseSelectW2Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW3Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW3Zone.szs'), 'rb') as f:
        w3archive = Sarc(yaz0.decompress(f.read()))
    w3archive1 = w3archive.get_file('CourseSelectW3ZoneDesign.byml').data
    w3archive2 = byml.to_text(byml.from_binary(w3archive.get_file('CourseSelectW3ZoneMap.byml').data))
    w3archive3 = w3archive.get_file('CameraParam.byml').data
    w3archive4 = w3archive.get_file('DofParam_obj27.bagldof').data
    w3archive5 = w3archive.get_file('CourseSelectW3ZoneSound.byml').data
    w3archive6 = w3archive.get_file('DofParam_obj28.bagldof').data
    CourseSelectW3ZoneMapn = w3archive2.split('\n')
    CourseSelectW3ZoneMapn.pop()
    CourseSelectW3ZoneMapo = CourseSelectW3ZoneMapn.copy()
    print('Opened CourseSelectW3Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW4Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW4Zone.szs'), 'rb') as f:
        w4archive = Sarc(yaz0.decompress(f.read()))
    w4archive1 = w4archive.get_file('DofParam_obj4.bagldof').data
    w4archive2 = byml.to_text(byml.from_binary(w4archive.get_file('CourseSelectW4ZoneMap.byml').data))
    w4archive3 = w4archive.get_file('DofParam_obj5.bagldof').data
    w4archive4 = w4archive.get_file('CourseSelectW4ZoneSound.byml').data
    w4archive5 = w4archive.get_file('DofParam_obj6.bagldof').data
    w4archive6 = w4archive.get_file('CameraParam.byml').data
    w4archive7 = w4archive.get_file('CourseSelectW4ZoneDesign.byml').data
    CourseSelectW4ZoneMapn = w4archive2.split('\n')
    CourseSelectW4ZoneMapn.pop()
    CourseSelectW4ZoneMapo = CourseSelectW4ZoneMapn.copy()
    print('Opened CourseSelectW4Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW5Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW5Zone.szs'), 'rb') as f:
        w5archive = Sarc(yaz0.decompress(f.read()))
    w5archive1 = w5archive.get_file('DofParam_obj4.bagldof').data
    w5archive2 = w5archive.get_file('CourseSelectW5ZoneDesign.byml').data
    w5archive3 = w5archive.get_file('DofParam_obj5.bagldof').data
    w5archive4 = w5archive.get_file('DofParam_obj6.bagldof').data
    w5archive5 = w5archive.get_file('CameraParam.byml').data
    w5archive6 = byml.to_text(byml.from_binary(w5archive.get_file('CourseSelectW5ZoneMap.byml').data))
    w5archive7 = w5archive.get_file('DofParam_obj3.bagldof').data
    w5archive8 = w5archive.get_file('CourseSelectW5ZoneSound.byml').data
    CourseSelectW5ZoneMapn = w5archive6.split('\n')
    CourseSelectW5ZoneMapn.pop()
    CourseSelectW5ZoneMapo = CourseSelectW5ZoneMapn.copy()
    print('Opened CourseSelectW5Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW6Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW6Zone.szs'), 'rb') as f:
        w6archive = Sarc(yaz0.decompress(f.read()))
    w6archive1 = w6archive.get_file('DofParam_obj18.bagldof').data
    w6archive2 = w6archive.get_file('DofParam_obj14.bagldof').data
    w6archive3 = w6archive.get_file('DofParam_obj10.bagldof').data
    w6archive4 = w6archive.get_file('DofParam_obj9.bagldof').data
    w6archive5 = w6archive.get_file('DofParam_obj19.bagldof').data
    w6archive6 = w6archive.get_file('DofParam_obj15.bagldof').data
    w6archive7 = byml.to_text(byml.from_binary(w6archive.get_file('CourseSelectW6ZoneMap.byml').data))
    w6archive8 = w6archive.get_file('DofParam_obj11.bagldof').data
    w6archive9 = w6archive.get_file('CourseSelectW6ZoneSound.byml').data
    w6archive10 = w6archive.get_file('DofParam_obj6.bagldof').data
    w6archive11 = w6archive.get_file('DofParam_obj16.bagldof').data
    w6archive12 = w6archive.get_file('CourseSelectW6ZoneDesign.byml').data
    w6archive13 = w6archive.get_file('DofParam_obj12.bagldof').data
    w6archive14 = w6archive.get_file('CameraParam.byml').data
    w6archive15 = w6archive.get_file('DofParam_obj17.bagldof').data
    w6archive16 = w6archive.get_file('DofParam_obj13.bagldof').data
    w6archive17 = w6archive.get_file('DofParam_obj8.bagldof').data
    CourseSelectW6ZoneMapn = w6archive7.split('\n')
    CourseSelectW6ZoneMapn.pop()
    CourseSelectW6ZoneMapo = CourseSelectW6ZoneMapn.copy()
    print('Opened CourseSelectW6Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW7Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW7Zone.szs'), 'rb') as f:
        w7archive = Sarc(yaz0.decompress(f.read()))
    w7archive1 = w7archive.get_file('CourseSelectW7ZoneDesign.byml').data
    w7archive2 = w7archive.get_file('DofParam_obj19.bagldof').data
    w7archive3 = w7archive.get_file('DofParam_obj22.bagldof').data
    w7archive4 = w7archive.get_file('CameraParam.byml').data
    w7archive5 = w7archive.get_file('DofParam_obj23.bagldof').data
    w7archive6 = byml.to_text(byml.from_binary(w7archive.get_file('CourseSelectW7ZoneMap.byml').data))
    w7archive7 = w7archive.get_file('CourseSelectW7ZoneSound.byml').data
    CourseSelectW7ZoneMapn = w7archive6.split('\n')
    CourseSelectW7ZoneMapn.pop()
    CourseSelectW7ZoneMapo = CourseSelectW7ZoneMapn.copy()
    print('Opened CourseSelectW7Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectW8Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectW8Zone.szs'), 'rb') as f:
        w8archive = Sarc(yaz0.decompress(f.read()))
    w8archive1 = w8archive.get_file('DofParam_obj130.bagldof').data
    w8archive2 = w8archive.get_file('DofParam_obj129.bagldof').data
    w8archive3 = w8archive.get_file('DofParam_obj131.bagldof').data
    w8archive4 = byml.to_text(byml.from_binary(w8archive.get_file('CourseSelectW8ZoneMap.byml').data))
    w8archive5 = w8archive.get_file('CourseSelectW8ZoneSound.byml').data
    w8archive6 = w8archive.get_file('CourseSelectW8ZoneDesign.byml').data
    w8archive7 = w8archive.get_file('DofParam_obj132.bagldof').data
    w8archive8 = w8archive.get_file('CameraParam.byml').data
    w8archive9 = w8archive.get_file('DofParam_obj133.bagldof').data
    CourseSelectW8ZoneMapn = w8archive4.split('\n')
    CourseSelectW8ZoneMapn.pop()
    CourseSelectW8ZoneMapo = CourseSelectW8ZoneMapn.copy()
    print('Opened CourseSelectW8Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening CourseSelectS1Zone.szs')
    with open(os.path.join(sPath, 'CourseSelectS1Zone.szs'), 'rb') as f:
        s1archive = Sarc(yaz0.decompress(f.read()))
    s1archive1 = s1archive.get_file('CourseSelectS1ZoneSound.byml').data
    s1archive2 = s1archive.get_file('CameraParam.byml').data
    s1archive3 = byml.to_text(byml.from_binary(s1archive.get_file('CourseSelectS1ZoneMap.byml').data))
    CourseSelectS1ZoneMapn = s1archive3.split('\n')
    CourseSelectS1ZoneMapn.pop()
    CourseSelectS1ZoneMapo = CourseSelectS1ZoneMapn.copy()
    print('Opened CourseSelectS1Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Opening KoopaLastBZone.szs')
    with open(os.path.join(sPath, 'KoopaLastBZone.szs'), 'rb') as f:
        KoopaLastBZone = Sarc(yaz0.decompress(f.read()))
    KoopaLastBZone1 = KoopaLastBZone.get_file('DofParam_obj0.bagldof').data
    KoopaLastBZone2 = byml.to_text(byml.from_binary(KoopaLastBZone.get_file('KoopaLastBZoneMap.byml').data))
    KoopaLastBZone3 = KoopaLastBZone.get_file('DofParam_obj1.bagldof').data
    KoopaLastBZone4 = KoopaLastBZone.get_file('KoopaLastBZoneDesign.byml').data
    KoopaLastBZone5 = KoopaLastBZone.get_file('KoopaLastBZoneSound.byml').data
    KoopaLastBZone6 = KoopaLastBZone.get_file('CubeMapMgr.baglcube').data
    KoopaLastBZone7 = KoopaLastBZone.get_file('CameraParam.byml').data
    KoopaLastBZoneMap = KoopaLastBZone2.split('\n')
    KoopaLastBZoneMap.pop()
    print('Opened KoopaLastBZone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

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
    dpg.configure_item("progress", default_value=bar / 174)

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
    dpg.configure_item("progress", default_value=bar / 174)

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
        GreenStarLockHistory2.append([rng.choice([True, False], size=1, p=[float(dpg.get_value('pslider')), float(1 - dpg.get_value('pslider'))], replace=True), int(currentGreenStars * float(dpg.get_value('sslider')))])
        if stageNo == 114:
            GreenStarLockHistory2[-1][0] = True  # Force Bowser-Castle to have a star lock when setting is on 'Fully random'
        if dpg.get_value("star") == 'Disabled' or float(dpg.get_value('sslider')) == 0 or 'GateKeeper' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 8] or stageNo == 11 or stageNo == 22 or stageNo == 36 or stageNo == 48 or stageNo == 49 or stageNo == 68 or stageNo == 83 or stageNo == 99 or stageNo == 100 or stageNo == 113 or stageNo == 117 or stageNo == 118:
            # Remove all Green Star Locks when encountered
            print('Removing green star lock...')
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4] = '    GreenStarLock: 0'
            GreenStarLockHistory2[-1][0] = False
        elif dpg.get_value("star") == 'Random values':
            # Calculate a new green star lock based on the vanilla lock value and multiply it by the ratio of the new star count to the old star count up to that point
            GreenStarLockValue = int(currentGreenStars * int(GreenStarLock[GreenStarLock.index(':') + 2:]) / currentGreenStarsOld)
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 4] = GreenStarLock[:GreenStarLock.index(':') + 2] + str(GreenStarLockValue)
            print('Changing green star lock value!')
            if GreenStarLockValue != 0:
                GreenStarLockHistory.append([stageNo, GreenStarLockValue])
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
                if stageNo == 10 or stageNo == 21 or stageNo == 35 or stageNo == 47 or stageNo == 67 or stageNo == 82 or stageNo == 98 or stageNo == 116 or stageNo == 130:
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
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ゲートキーパー[GPあり]'  # StageType for Boss Blockades.
                # If it is a normal boss blockade...
                else:
                    print('Blockade StageType fixed!')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo))) + 10] = '    StageType: ゲートキーパー'  # StageType for Blockades.
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
            StageName = 'MiniatureBonusRoom'
        elif 'GateKeeperBoss' in StageName or 'GateKeeperTentack' in StageName:
            StageName = 'MiniatureEventGateKeeper'
        elif 'GateKeeper' in StageName:
            StageName = 'Miniature'+StageName[StageName.index(':')+2:-8]
        elif 'KinopioHouse' in StageName:
            StageName = 'MiniatureKinopioHouse'
        elif 'FairyHouse' in StageName:
            StageName = 'MiniatureFairyHouse'
        elif 'MysteryHouse' in StageName:
            StageName = 'MiniatureMysteryBox'
        elif 'KinopioBrigade' in StageName:
            StageName = 'MiniatureKinopioBrigade'
        elif 'Teresa' in StageName or 'WeavingShip' in StageName or 'Haunted' in StageName or 'Fog' in StageName:
            StageName = 'MiniatureTeresaHouse'
        elif 'Arrange' in StageName:
            if 'BossParade' in StageName:
                StageName = 'MiniatureArrangeBossParade'
            else:
                StageName = 'Miniature'+StageName[StageName.index(':')+9:-5]
        elif 'Boss' in StageName or 'KillerTank' in StageName or 'BombTank' in StageName or 'KillerExpress' in StageName or 'KoopaChase' in StageName or 'KoopaLast' in StageName:
            if 'KoopaLast' in StageName:
                StageName = 'MiniatureKoopaCastleW8'
            elif 'KoopaChaseLv2' in StageName:
                StageName = 'MiniatureKoopaCastleW7'
            else:
                StageName = 'MiniatureKoopaCastle'
        elif 'DashRidge' in StageName:
            StageName = 'MiniatureDashRidgeStage'
        else:
            StageName = 'Miniature'+StageName[StageName.index(':')+2:-5]

        # Enumerating the YML to replace world map models to show the randomized stage.
        if worldNo == 1 and StageID[StageID.index(':') + 2:] != '70' and StageID[StageID.index(':') + 2:] != '35':
            for i, elem in enumerate(CourseSelectW1ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem and '35' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW1ZoneMapo[i - 4]:
                        CourseSelectW1ZoneMapn[i - 4] = CourseSelectW1ZoneMapo[i - 4][:CourseSelectW1ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW1ZoneMapo[i - 6]:
                        CourseSelectW1ZoneMapn[i - 6] = CourseSelectW1ZoneMapo[i - 6][:CourseSelectW1ZoneMapo[i - 6].index(':') + 2] + StageName
                    if StageID[StageID.index(':')+2:] == '1':
                        if ' Rotate: ' in CourseSelectW1ZoneMapo[i - 2]:
                            CourseSelectW1ZoneMapn[i - 2] = CourseSelectW1ZoneMapo[i - 2][:CourseSelectW1ZoneMapo[i - 2].index(':') + 2] + '{X: 0.0, Y: -0.0, Z: 0.0}'  # Fix rotation for World 1-1
                        elif ' Rotate: ' in CourseSelectW1ZoneMapo[i - 4]:
                            CourseSelectW1ZoneMapn[i - 4] = CourseSelectW1ZoneMapo[i - 4][:CourseSelectW1ZoneMapo[i - 4].index(':') + 2] + '{X: 0.0, Y: -0.0,'
                            CourseSelectW1ZoneMapn[i - 3] = CourseSelectW1ZoneMapo[i - 3][:CourseSelectW1ZoneMapo[i - 3].index(':') + 2] + '0.0}'
        elif worldNo == 2 and StageID[StageID.index(':') + 2:] != '70':
            for i, elem in enumerate(CourseSelectW2ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW2ZoneMapo[i - 4]:
                        CourseSelectW2ZoneMapn[i - 4] = CourseSelectW2ZoneMapo[i - 4][:CourseSelectW2ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW2ZoneMapo[i - 6]:
                        CourseSelectW2ZoneMapn[i - 6] = CourseSelectW2ZoneMapo[i - 6][:CourseSelectW2ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo == 3 and StageID[StageID.index(':') + 2:] != '70' and StageID[StageID.index(':') + 2:] != '101':
            for i, elem in enumerate(CourseSelectW3ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem and '101' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW3ZoneMapo[i - 4]:
                        CourseSelectW3ZoneMapn[i - 4] = CourseSelectW3ZoneMapo[i - 4][:CourseSelectW3ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW3ZoneMapo[i - 6]:
                        CourseSelectW3ZoneMapn[i - 6] = CourseSelectW3ZoneMapo[i - 6][:CourseSelectW3ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo == 4 and StageID[StageID.index(':') + 2:] != '70':
            for i, elem in enumerate(CourseSelectW4ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW4ZoneMapo[i - 4]:
                        CourseSelectW4ZoneMapn[i - 4] = CourseSelectW4ZoneMapo[i - 4][:CourseSelectW4ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW4ZoneMapo[i - 6]:
                        CourseSelectW4ZoneMapn[i - 6] = CourseSelectW4ZoneMapo[i - 6][:CourseSelectW4ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo == 5 and StageID[StageID.index(':') + 2:] != '70':
            for i, elem in enumerate(CourseSelectW5ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW5ZoneMapo[i - 4]:
                        CourseSelectW5ZoneMapn[i - 4] = CourseSelectW5ZoneMapo[i - 4][:CourseSelectW5ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW5ZoneMapo[i - 6]:
                        CourseSelectW5ZoneMapn[i - 6] = CourseSelectW5ZoneMapo[i - 6][:CourseSelectW5ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo == 6 and StageID[StageID.index(':') + 2:] != '70' and StageID[StageID.index(':') + 2:] != '102':
            for i, elem in enumerate(CourseSelectW6ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem and '102' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW6ZoneMapo[i - 4]:
                        CourseSelectW6ZoneMapn[i - 4] = CourseSelectW6ZoneMapo[i - 4][:CourseSelectW6ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW6ZoneMapo[i - 6]:
                        CourseSelectW6ZoneMapn[i - 6] = CourseSelectW6ZoneMapo[i - 6][:CourseSelectW6ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo == 7:
            for i, elem in enumerate(CourseSelectW7ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower():
                    if 'ModelName: Miniature' in CourseSelectW7ZoneMapo[i - 4]:
                        CourseSelectW7ZoneMapn[i - 4] = CourseSelectW7ZoneMapo[i - 4][:CourseSelectW7ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW7ZoneMapo[i - 6]:
                        CourseSelectW7ZoneMapn[i - 6] = CourseSelectW7ZoneMapo[i - 6][:CourseSelectW7ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo == 8 and StageID[StageID.index(':') + 2:] != '35':
            for i, elem in enumerate(CourseSelectW8ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '35' not in elem:
                    if 'ModelName: Miniature' in CourseSelectW8ZoneMapo[i - 4]:
                        CourseSelectW8ZoneMapn[i - 4] = CourseSelectW8ZoneMapo[i - 4][:CourseSelectW8ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectW8ZoneMapo[i - 6]:
                        CourseSelectW8ZoneMapn[i - 6] = CourseSelectW8ZoneMapo[i - 6][:CourseSelectW8ZoneMapo[i - 6].index(':') + 2] + StageName
        elif worldNo >= 9 and StageID[StageID.index(':') + 2:] != '70':
            for i, elem in enumerate(CourseSelectS1ZoneMapo):
                if StageID[StageID.index('S'):].lower() in elem.lower() and '70' not in elem:
                    if 'ModelName: Miniature' in CourseSelectS1ZoneMapo[i - 4] and CourseSelectS1ZoneMapo[i + 11][CourseSelectS1ZoneMapo[i + 11].index(':') + 2:] == str(worldNo):
                        CourseSelectS1ZoneMapn[i - 4] = CourseSelectS1ZoneMapo[i - 4][:CourseSelectS1ZoneMapo[i - 4].index(':') + 2] + StageName
                    elif 'ModelName: Miniature' in CourseSelectS1ZoneMapo[i - 6] and CourseSelectS1ZoneMapo[i + 15][CourseSelectS1ZoneMapo[i + 15].index(':') + 2:] == str(worldNo):
                        CourseSelectS1ZoneMapn[i - 6] = CourseSelectS1ZoneMapo[i - 6][:CourseSelectS1ZoneMapo[i - 6].index(':') + 2] + StageName
        bar += 1
        dpg.configure_item("progress", default_value=bar / 174)

    print('Total Green Star Count: ' + str(currentGreenStars))
    print('Randomized stages!')

    for b in KoopaLastBZoneMap:
        if 'GoalPoleLast' in b:
            KoopaLastBZoneMap[KoopaLastBZoneMap.index(b)] = KoopaLastBZoneMap[KoopaLastBZoneMap.index(b)][:KoopaLastBZoneMap[KoopaLastBZoneMap.index(b)].index(':') + 2] + 'GoalPoleSuper'
            print('Changed GoalPoleLast to GoalPoalSuper in KoopaLastBZone.')
    KoopaLastBZone2 = '\n'.join(KoopaLastBZoneMap)

    doc = '\n'.join(StageListNew)
    # Creating new SZS filers with the modified files.
    print('Writing StageList.szs')
    writer = SarcWriter()
    writer.set_endianness(endianness)
    writer.files['StageList.byml'] = byml.to_binary(byml.from_text(doc), False, 2)  # Adding to SARC.
    data = writer.write()  # Write to SARC

    with open(os.path.join(rPath, "StageList.szs"), "wb") as randoSZS:
        randoSZS.write(yaz0.compress(data[1]))  # Compress with YAZ0 and write to the SZS.
    print('Written StageList.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing world files:')

    print('Writing CourseSelectW1Zone.szs')
    w1archive6 = '\n'.join(CourseSelectW1ZoneMapn)
    w1writer = SarcWriter()
    w1writer.set_endianness(endianness)
    w1writer.files['DofParam_obj10.bagldof'] = Bytes(w1archive1)
    w1writer.files['DofParam_obj9.bagldof'] = Bytes(w1archive2)
    w1writer.files['DofParam_obj11.bagldof'] = Bytes(w1archive3)
    w1writer.files['CourseSelectW1ZoneDesign.byml'] = Bytes(w1archive4)
    w1writer.files['DofParam_obj6.bagldof'] = Bytes(w1archive5)
    w1writer.files['CourseSelectW1ZoneMap.byml'] = byml.to_binary(byml.from_text(w1archive6), False, 2)
    w1writer.files['DofParam_obj12.bagldof'] = Bytes(w1archive7)
    w1writer.files['CameraParam.byml'] = Bytes(w1archive8)
    w1writer.files['DofParam_obj7.bagldof'] = Bytes(w1archive9)
    w1writer.files['CourseSelectW1ZoneSound.byml'] = Bytes(w1archive10)
    w1writer.files['DofParam_obj8.bagldof'] = Bytes(w1archive11)
    w1data = w1writer.write()

    with open(os.path.join(srPath, 'CourseSelectW1Zone.szs'), 'wb') as w1:
        w1.write(yaz0.compress(w1data[1]))
    print('Written CourseSelectW1Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW2Zone.szs')
    w2archive2 = '\n'.join(CourseSelectW2ZoneMapn)
    w2writer = SarcWriter()
    w2writer.set_endianness(endianness)
    w2writer.files['DofParam_obj4.bagldof'] = Bytes(w2archive1)
    w2writer.files['CourseSelectW2ZoneMap.byml'] = byml.to_binary(byml.from_text(w2archive2), False, 2)
    w2writer.files['DofParam_obj9.bagldof'] = Bytes(w2archive3)
    w2writer.files['DofParam_obj5.bagldof'] = Bytes(w2archive4)
    w2writer.files['CourseSelectW2ZoneSound.byml'] = Bytes(w2archive5)
    w2writer.files['DofParam_obj6.bagldof'] = Bytes(w2archive6)
    w2writer.files['CameraParam.byml'] = Bytes(w2archive7)
    w2writer.files['DofParam_obj7.bagldof'] = Bytes(w2archive8)
    w2writer.files['DofParam_obj3.bagldof'] = Bytes(w2archive9)
    w2writer.files['CourseSelectW2ZoneDesign.byml'] = Bytes(w2archive10)
    w2writer.files['DofParam_obj8.bagldof'] = Bytes(w2archive11)
    w2data = w2writer.write()

    with open(os.path.join(srPath, 'CourseSelectW2Zone.szs'), 'wb') as w2:
        w2.write(yaz0.compress(w2data[1]))
    print('Written CourseSelectW2Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW3Zone.szs')
    w3archive2 = '\n'.join(CourseSelectW3ZoneMapn)
    w3writer = SarcWriter()
    w3writer.set_endianness(endianness)
    w3writer.files['CourseSelectW3ZoneDesign.byml'] = Bytes(w3archive1)
    w3writer.files['CourseSelectW3ZoneMap.byml'] = byml.to_binary(byml.from_text(w3archive2), False, 2)
    w3writer.files['CameraParam.byml'] = Bytes(w3archive3)
    w3writer.files['DofParam_obj27.bagldof'] = Bytes(w3archive4)
    w3writer.files['CourseSelectW3ZoneSound.byml'] = Bytes(w3archive5)
    w3writer.files['DofParam_obj28.bagldof'] = Bytes(w3archive6)
    w3data = w3writer.write()

    with open(os.path.join(srPath, 'CourseSelectW3Zone.szs'), 'wb') as w3:
        w3.write(yaz0.compress(w3data[1]))
    print('Written CourseSelectW3Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW4Zone.szs')
    w4archive2 = '\n'.join(CourseSelectW4ZoneMapn)
    w4writer = SarcWriter()
    w4writer.set_endianness(endianness)
    w4writer.files['DofParam_obj4.bagldof'] = Bytes(w4archive1)
    w4writer.files['CourseSelectW4ZoneMap.byml'] = byml.to_binary(byml.from_text(w4archive2), False, 2)
    w4writer.files['DofParam_obj5.bagldof'] = Bytes(w4archive3)
    w4writer.files['CourseSelectW4ZoneSound.byml'] = Bytes(w4archive4)
    w4writer.files['DofParam_obj6.bagldof'] = Bytes(w4archive5)
    w4writer.files['CameraParam.byml'] = Bytes(w4archive6)
    w4writer.files['CourseSelectW4ZoneDesign.byml'] = Bytes(w4archive7)
    w4data = w4writer.write()

    with open(os.path.join(srPath, 'CourseSelectW4Zone.szs'), 'wb') as w4:
        w4.write(yaz0.compress(w4data[1]))
    print('Written CourseSelectW4Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW5Zone.szs')
    w5archive6 = '\n'.join(CourseSelectW5ZoneMapn)
    w5writer = SarcWriter()
    w5writer.set_endianness(endianness)
    w5writer.files['DofParam_obj4.bagldof'] = Bytes(w5archive1)
    w5writer.files['CourseSelectW5ZoneDesign.byml'] = Bytes(w5archive2)
    w5writer.files['DofParam_obj5.bagldof'] = Bytes(w5archive3)
    w5writer.files['DofParam_obj6.bagldof'] = Bytes(w5archive4)
    w5writer.files['CameraParam.byml'] = Bytes(w5archive5)
    w5writer.files['CourseSelectW5ZoneMap.byml'] = byml.to_binary(byml.from_text(w5archive6), False, 2)
    w5writer.files['DofParam_obj3.bagldof'] = Bytes(w5archive7)
    w5writer.files['CourseSelectW5ZoneSound.byml'] = Bytes(w5archive8)
    w5data = w5writer.write()

    with open(os.path.join(srPath, 'CourseSelectW5Zone.szs'), 'wb') as w5:
        w5.write(yaz0.compress(w5data[1]))
    print('Written CourseSelectW5Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW6Zone.szs')
    w6archive7 = '\n'.join(CourseSelectW6ZoneMapn)
    w6writer = SarcWriter()
    w6writer.set_endianness(endianness)
    w6writer.files['DofParam_obj18.bagldof'] = Bytes(w6archive1)
    w6writer.files['DofParam_obj14.bagldof'] = Bytes(w6archive2)
    w6writer.files['DofParam_obj10.bagldof'] = Bytes(w6archive3)
    w6writer.files['DofParam_obj9.bagldof'] = Bytes(w6archive4)
    w6writer.files['DofParam_obj19.bagldof'] = Bytes(w6archive5)
    w6writer.files['DofParam_obj15.bagldof'] = Bytes(w6archive6)
    w6writer.files['CourseSelectW6ZoneMap.byml'] = byml.to_binary(byml.from_text(w6archive7), False, 2)
    w6writer.files['DofParam_obj11.bagldof'] = Bytes(w6archive8)
    w6writer.files['CourseSelectW6ZoneSound.byml'] = Bytes(w6archive9)
    w6writer.files['DofParam_obj6.bagldof'] = Bytes(w6archive10)
    w6writer.files['DofParam_obj16.bagldof'] = Bytes(w6archive11)
    w6writer.files['CourseSelectW6ZoneDesign.byml'] = Bytes(w6archive12)
    w6writer.files['DofParam_obj12.bagldof'] = Bytes(w6archive13)
    w6writer.files['CameraParam.byml'] = Bytes(w6archive14)
    w6writer.files['DofParam_obj17.bagldof'] = Bytes(w6archive15)
    w6writer.files['DofParam_obj13.bagldof'] = Bytes(w6archive16)
    w6writer.files['DofParam_obj8.bagldof'] = Bytes(w6archive17)
    w6data = w6writer.write()

    with open(os.path.join(srPath, 'CourseSelectW6Zone.szs'), 'wb') as w6:
        w6.write(yaz0.compress(w6data[1]))
    print('Written CourseSelectW6Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW7Zone.szs')
    w7archive6 = '\n'.join(CourseSelectW7ZoneMapn)
    w7writer = SarcWriter()
    w7writer.set_endianness(endianness)
    w7writer.files['CourseSelectW7ZoneDesign.byml'] = Bytes(w7archive1)
    w7writer.files['DofParam_obj19.bagldof'] = Bytes(w7archive2)
    w7writer.files['DofParam_obj22.bagldof'] = Bytes(w7archive3)
    w7writer.files['CameraParam.byml'] = Bytes(w7archive4)
    w7writer.files['DofParam_obj23.bagldof'] = Bytes(w7archive5)
    w7writer.files['CourseSelectW7ZoneMap.byml'] = byml.to_binary(byml.from_text(w7archive6), False, 2)
    w7writer.files['CourseSelectW7ZoneSound.byml'] = Bytes(w7archive7)
    w7data = w7writer.write()

    with open(os.path.join(srPath, 'CourseSelectW7Zone.szs'), 'wb') as w7:
        w7.write(yaz0.compress(w7data[1]))
    print('Written CourseSelectW7Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectW8Zone.szs')
    w8archive4 = '\n'.join(CourseSelectW8ZoneMapn)
    w8writer = SarcWriter()
    w8writer.set_endianness(endianness)
    w8writer.files['DofParam_obj130.bagldof'] = Bytes(w8archive1)
    w8writer.files['DofParam_obj129.bagldof'] = Bytes(w8archive2)
    w8writer.files['DofParam_obj131.bagldof'] = Bytes(w8archive3)
    w8writer.files['CourseSelectW8ZoneMap.byml'] = byml.to_binary(byml.from_text(w8archive4), False, 2)
    w8writer.files['CourseSelectW8ZoneSound.byml'] = Bytes(w8archive5)
    w8writer.files['CourseSelectW8ZoneDesign.byml'] = Bytes(w8archive6)
    w8writer.files['DofParam_obj132.bagldof'] = Bytes(w8archive7)
    w8writer.files['CameraParam.byml'] = Bytes(w8archive8)
    w8writer.files['DofParam_obj133.bagldof'] = Bytes(w8archive9)
    w8data = w8writer.write()

    with open(os.path.join(srPath, 'CourseSelectW8Zone.szs'), 'wb') as w8:
        w8.write(yaz0.compress(w8data[1]))
    print('Written CourseSelectW8Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing CourseSelectS1Zone.szs')
    s1archive3 = '\n'.join(CourseSelectS1ZoneMapn)
    s1writer = SarcWriter()
    s1writer.set_endianness(endianness)
    s1writer.files['CourseSelectS1ZoneSound.byml'] = Bytes(s1archive1)
    s1writer.files['CameraParam.byml'] = Bytes(s1archive2)
    s1writer.files['CourseSelectS1ZoneMap.byml'] = byml.to_binary(byml.from_text(s1archive3), False, 2)
    s1data = s1writer.write()

    with open(os.path.join(srPath, 'CourseSelectS1Zone.szs'), 'wb') as s1:
        s1.write(yaz0.compress(s1data[1]))
    print('Written CourseSelectS1Zone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Writing KoopaLastBZone.szs')
    bzwriter = SarcWriter()
    bzwriter.set_endianness(endianness)
    bzwriter.files['DofParam_obj0.bagldof'] = Bytes(KoopaLastBZone1)
    bzwriter.files['KoopaLastBZoneMap.byml'] = byml.to_binary(byml.from_text(KoopaLastBZone2), False, 2)
    bzwriter.files['DofParam_obj1.bagldof'] = Bytes(KoopaLastBZone3)
    bzwriter.files['KoopaLastBZoneDesign.byml'] = Bytes(KoopaLastBZone4)
    bzwriter.files['KoopaLastBZoneSound.byml'] = Bytes(KoopaLastBZone5)
    bzwriter.files['CubeMapMgr.baglcube'] = Bytes(KoopaLastBZone6)
    bzwriter.files['CameraParam.byml'] = Bytes(KoopaLastBZone7)
    bzdata = bzwriter.write()

    with open(os.path.join(srPath, 'KoopaLastBZone.szs'), 'wb') as bz:
        bz.write(yaz0.compress(bzdata[1]))
    print('Written KoopaLastBZone.szs')
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

    print('Finished writing stage files.')

    musicRandomizer(rng, seedRNG, user_data)
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)
    langRandomizer(rng, seedRNG, user_data)
    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

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
        with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', i[0]), 'rb') as f:
            hash_object = hashlib.md5(f.read())
            stageID_Name.append(i[0] + ' - ' + hash_object.hexdigest() + '\n')

    if dpg.get_value("spoil"):
        spoilerFile(StageListNew, seedRNG, dict(GreenStarLockHistory), GreenStarLockHistory2, user_data)
    else:
        print('Not generating spoiler file, only generating seed/settings/hash text file.')
        with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), str(seedRNG)+'.txt'), 'w', encoding='utf-8') as s:
            # Creating a new spoiler text file.
            s.write(''.join(stageID_Name)[:-1])

    bar += 1
    dpg.configure_item("progress", default_value=bar / 174)

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
    dpg.configure_item("progress", default_value=bar / 174)

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
    stageID_Name.append('\n\nLevel slot, Level name (Original level slot) (Green Stars required, if needed)\n\nWorld ' + str(worldIndex) + '\n')

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
                        stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory[overallIndex]) + ' Green Stars)\n'
                    else:
                        stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory[overallIndex]) + ' Green Star)\n'
                except KeyError:
                    pass
            elif dpg.get_value("star") == 'Fully random':
                try:
                    if GreenStarLockHistory2[overallIndex2 - 1][1] != 0 and GreenStarLockHistory2[overallIndex2 - 1][0] and overallIndex != 34 and overallIndex != 62 and overallIndex != 63 and overallIndex != 64 and overallIndex != 65 and overallIndex != 66 and overallIndex != 81 and overallIndex != 97 and overallIndex != 115:
                        if int(GreenStarLockHistory2[overallIndex2 - 1][1]) > 1:
                            stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory2[overallIndex2 - 1][1]) + ' Green Stars)\n'
                        else:
                            stageID_Name[-1] = stageID_Name[-1][:-1] + ' (requires ' + str(GreenStarLockHistory2[overallIndex2 - 1][1]) + ' Green Star)\n'
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
        with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), 'romfs', i[0]), 'rb') as f:
            hash_object = hashlib.md5(f.read())
            stageID_Name.append(i[0] + ' - ' + hash_object.hexdigest() + '\n')

    spoiler = ''.join(stageID_Name)[:-1]
    # Making sure levels have the correct names.
    rep = spoiler.replace('11-6', 'Flower-6').replace('11-7', 'Flower-7').replace('11-8', 'Flower-8').replace('11-9', 'Flower-9').replace('11-10', 'Flower-10').replace('11-11', 'Flower-11').replace('11-12', 'Flower-12').replace('12-1', 'Crown-Crown').replace('1-9', '1-Castle').replace('4-9', '4-Castle').replace('5-12', '5-Castle').replace('7-11', 'Castle-Castle').replace('8-13', 'Bowser-Castle').replace('2-9', '2-Tank').replace('6-11', '6-Tank').replace('3-11', '3-Train').replace('8-12', 'Bowser-Train').replace('1-6', '1-Toad House 1').replace('1-7', '1-Toad House 2').replace('2-6', '2-Toad House').replace('3-8', '3-Toad House').replace('3-12', '3-Toad House 2 (Unused)').replace('4-6', '4-Toad House').replace('5-9', '5-Toad House').replace('5-13', '5-Toad House 2 (Unused)').replace('5-14', '5-Toad House 3 (Unused)').replace('5-15', '5-Toad House 4 (Unused)').replace('5-16', '5-Toad House 5 (Unused)').replace('5-17', '5-Toad House 6 (Unused)').replace('6-8', '6-Toad House').replace('6-12', '6-Toad House 2 (Unused)').replace('7-8', 'Castle-Toad House').replace('7-12', 'Castle-Toad House 2 (Unused)').replace('8-8', 'Bowser-Toad House 1').replace('8-9', 'Bowser-Toad House 2').replace('8-14', 'Bowser-Toad House 3 (Unused)').replace('2-7', '2-Sprixie House').replace('3-9', '3-Sprixie House').replace('4-7', '4-Sprixie House').replace('5-10', '5-Sprixie House').replace('6-9', '6-Sprixie House').replace('7-9', 'Castle-Sprixie House').replace('8-10', 'Bowser-Sprixie House').replace('9-10', 'Star-Sprixie House').replace('12-2', 'Crown-Sprixie House').replace('1-8', '1-Captain Toad').replace('3-10', '3-Captain Toad').replace('5-11', '5-Captain Toad').replace('7-10', 'Castle-Captain Toad').replace('9-11', 'Star-Captain Toad').replace('12-3', 'Crown-Captain Toad').replace('1-10', 'Lucky House').replace('2-10', 'Lucky House').replace('3-13', 'Lucky House').replace('4-10', 'Lucky House').replace('5-18', 'Lucky House').replace('6-13', 'Lucky House').replace('7-13', 'Lucky House').replace('8-15', 'Lucky House').replace('9-12', 'Lucky House').replace('1-11', '1-A').replace('2-11', '2-A').replace('3-14', '3-A').replace('4-11', '4-A').replace('5-19', '5-A').replace('6-14', '6-A').replace('7-14', 'Castle-A').replace('8-16', 'Bowser-A').replace('3-15', '3-B').replace('4-12', '4-B').replace('5-20', '5-B').replace('6-15', '6-B').replace('7-15', 'Castle-B').replace('8-17', 'Bowser-B').replace('6-16', '6-C').replace('7-16', 'Castle-C').replace('5-8', 'Coin Express').replace('2-8', '2-Mystery House').replace('4-8', '4-Mystery House').replace('6-10', '6-Mystery House').replace('8-11', 'Bowser-Mystery House').replace('10-8', 'Mushroom-Mystery House').replace('12-4', 'Crown-Mystery House').replace('7-', 'Castle-').replace('8-', 'Bowser-').replace('9-', 'Star-').replace('10-', 'Mushroom-').replace('11-', 'Flower-').replace('12-', 'Crown-')

    with open(os.path.join(user_data[1], 'SM3DWR-' + str(seedRNG), str(seedRNG) + '-spoiler.txt'), 'w', encoding='utf-8') as s:
        s.write(rep)  # Writing the corrected level slots back to the file.

    print('Generated spoiler file!')


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
                                 "Developer:\n"
                                 "Skipper93653\n\n"
                                 "Module Credits:\n"
                                 "ZeldaMods for oead.\n"
                                 "Jonathan Hoffstadt for Dear PyGUI.\n"
                                 "Nuitka for Nuitka.\n"
                                 "Built-in Pythod modules.\n"
                                 "...And all of their contributors.\n\n"
                                 "Special Thanks:\n"
                                 "Nintendo EAD/EPD for creating the game.\n"
                                 "Members of the ZeldaMods Discord server for oead help.\n"
                                 "Members of the 3D World Modding Community Discord server for general help.\n"
                                 "All testers.")
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


def directory(sender, app_data):
    dpg.set_value("dirtext", app_data['file_path_name'])  # Update directory text box with selected directory
    checkDirectory()


def rdirectory(sender, app_data):
    dpg.set_value("rdirtext", app_data['file_path_name'])
    checkDirectory()


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


def showSlider():
    if dpg.get_value('star') == 'Fully random':
        dpg.show_item('pslider')
        dpg.show_item('sslider')
    else:
        dpg.hide_item('pslider')
        dpg.hide_item('sslider')


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


def show():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main Window", True)  # Makes it so the UI fills the window
    dpg.start_dearpygui()
    dpg.destroy_context()


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
                [os.path.join('StageData', 'KoopaLastBZone.szs'), '4146dbdd3200ca39f100a02253e4b5d6']]

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
        if str(settings['star']) != 'Fully random' or str(settings['star']) != 'Random values' or str(settings['star']) != 'Disabled':
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

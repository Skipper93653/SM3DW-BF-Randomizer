# coding=utf-8
from random import *
from datetime import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from oead import *
import os, shutil

# Global variables
global folderSelected

root = Tk()
root.iconbitmap('ico.ico')
root.title('Super Mario 3D World (+ Bowser\'s Fury) Randomizer')
root.geometry('500x100')

spoil = IntVar()


# Developer credits.
def creditsDev():
    showinfo("Credits", "Super Mario 3D World Randomizer Credits\n\nDeveloper:\nToby Bailey - (Skipper93653)\n\nSpecial Thanks:\nNintendo for creating the game.\nMembers of the ZeldaMods Discord server for oead help.\nAll used third party Python module developers.")


# Error when trying to execute randomizer when a valid directory has not been specified.
def errorPopUp():
    showinfo('Error', 'An invalid RomFS directory has been specified.\nPlease select a valid Super Mario 3D World + Bowser\'s Fury RomFS directory.')


# Search for correct RomFS directory.
def browseDIR():
    global folderSelected

    folderSelected = askdirectory()
    if not folderSelected:
        return
    fileExist = os.path.isfile(folderSelected+'/SystemData/StageList.szs')
    print('Selected', folderSelected, fileExist)

    # Check if the RomFS directory is valid.
    if fileExist:
        openDIR.configure(text='Valid directory!', fg='green')
        run.configure(fg='green', command=randomizer)
    else:
        openDIR.configure(text='Load RomFS directory', fg='red')
        run.configure(fg='red', command=errorPopUp)

    # Cutting off the displayed label if directory is too long.
    if len(folderSelected) > 55:
        dirLabel.configure(text=folderSelected[:55]+'...')
    else:
        dirLabel.configure(text=folderSelected)


# Level randomizer
def randomizer():
    global folderSelected

    quitB.configure(command=None)

    # Getting date and time.
    now = datetime.now()
    currentTime = now.strftime('%H.%M.%S')
    currentDate = now.strftime('%d-%m-%y')
    currentDateTime = currentDate+'-'+currentTime

    oPath = os.path.join(folderSelected, 'SystemData/')  # Original game path
    rPath = os.path.join('./romfs-'+currentDateTime, 'SystemData/')  # Randomizer path

    os.makedirs(rPath)
    os.mkdir('./tmp-'+currentDateTime)

    shutil.copy2(oPath+'StageList.szs', rPath)

    with open(rPath+"StageList.szs", "rb") as f:
        archive = Sarc(yaz0.decompress(f.read()))  # Decompress and load SARC

    doc = byml.to_text(byml.from_binary(archive.get_file("StageList.byml").data))  # Load BYML file

    with open('./tmp-'+currentDateTime+'/StageList.yml', 'w', encoding='utf-8') as s:
        s.write(doc)  # Create a YML

    with open('./tmp-'+currentDateTime+'/StageList.yml', 'r', encoding='utf-8') as old:
        StageListOld = [line for line in old.readlines()]  # Open the YML as old and make a list.

    with open('./tmp-'+currentDateTime+'/StageList.yml', 'r', encoding='utf-8') as new:
        StageListNew = [line for line in new.readlines()]  # Open the YML as new and make a list from it.

    stageNo = 1
    stageID_history = [62, 63, 64, 65, 66]  # The unused Toad Houses in World 5

    # 154 different stages in total.
    while stageNo <= 154:
        stageID = randint(1, 154)
        # This loop happens when stageID generates a previously generated stageID to avoid duplicate levels.
        while stageID in stageID_history:
            print('Duplicate number '+str(stageID)+'! Regenerating...')
            stageID = randint(1, 154)

        # This loop happens when stageID generates a special level when stageNo is currently a castle stage and forces stageID to randomize again until it's not a special level (basically until it gives you a stage where it's possible to give you the golden goal pole).
        while (stageNo == 9 or stageNo == 20 or stageNo == 33 or stageNo == 46 or stageNo == 61 or stageNo == 80 or stageNo == 96 or stageNo == 114) and (stageID == 6 or stageID == 7 or stageID == 8 or stageID == 10 or stageID == 11 or stageID == 17 or stageID == 18 or stageID == 21 or stageID == 22 or stageID == 30 or stageID == 31 or stageID == 32 or stageID == 34 or stageID == 35 or stageID == 36 or stageID == 43 or stageID == 44 or stageID == 47 or stageID == 48 or stageID == 49 or stageID == 57 or stageID == 58 or stageID == 59 or stageID == 60 or stageID == 62 or stageID == 63 or stageID == 64 or stageID == 65 or stageID == 66 or stageID == 67 or stageID == 68 or stageID == 69 or stageID == 77 or stageID == 78 or stageID == 81 or stageID == 82 or stageID == 83 or stageID == 84 or stageID == 93 or stageID == 94 or stageID == 95 or stageID == 97 or stageID == 98 or stageID == 99 or stageID == 100 or stageID == 101 or stageID == 109 or stageID == 110 or stageID == 111 or stageID == 115 or stageID == 116 or stageID == 128 or stageID == 129 or stageID == 130 or stageID == 152 or stageID == 153):
            print('Special stage ('+str(stageID)+') on castle slot! Regenerating...')
            stageID = randint(1, 154)
            while stageID in stageID_history:
                print('Duplicate number '+str(stageID)+'! Regenerating...')
                stageID = randint(1, 154)

        print('Generated unique number '+str(stageID)+'!')
        stageID_history.append(stageID)  # Appends the generated stageID to the stageID_history list to help avoid generating the same number more than once when looping.
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 1] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID) + '\n')) + 1]  # DoubleMarioNum
        # Only have Bowser-Castle keep it's Star Lock of 170.
        if StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n'))] == '  - CourseId: 114\n':
            print('Reached Bowser-Castle slot! Placing 170 star lock!')
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 4] = '    GreenStarLock: 170\n'
        else:
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 4] = '    GreenStarLock: 0\n'  # GreenStarLock - gets rid of all star locks by setting it to 0.
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 5] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID) + '\n')) + 5]  # GreenStarNum
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 6] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID) + '\n')) + 6]  # IllustItemNum
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID) + '\n')) + 8]  # StageName

        if 'クッパ城' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] and stageNo != 113:
            print('Reached castle slot! Copying original StageType of this slot.')
            StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageNo) + '\n')) + 10]  # Makes sure all castle slots are the same slots when the levels are randomized.
        else:
            # Making sure Captain Toad stages, Mystery Houses, Toad Houses, Stamp Houses, Roulettes, Blockades, and Golden Express have the correct StageType.
            if 'KinopioBrigade' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                print('Captain Toad StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: キノピオ探検隊\n'  # StageType for Captain Toad levels.
            elif 'KinopioHouse' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                print('Toad House StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: キノピオの家\n'  # StageType for Toad Houses.
            elif 'FairyHouse' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                print('Stamp House StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: 妖精の家\n'  # StageType for Stamp Houses.
            elif 'RouletteRoomZone' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                print('Roulette StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: ゴールデンエクスプレス\n'  # StageType for Roulettes (カジノ部屋) is not used because they don't appear on the world map immediately which can cause progression issues. So the golden express is used instead.
            elif 'GoldenExpressStage' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                print('Golden Express StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: ゴールデンエクスプレス\n'  # StageType for golden express.
            elif 'MysteryHouse' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                print('Mystery House StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: ミステリーハウス\n'  # StageType for MysteryHouses
            elif 'GateKeeper' in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8]:
                if StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] == '    StageName: GateKeeperTentackLv1Stage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] == '    StageName: GateKeeperTentackLv2Stage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] == '    StageName: GateKeeperBossBunretsuLv1Stage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] == '    StageName: GateKeeperBossBunretsuLv2Stage\n':
                    print('Boss blockade StageType adjusted to standard course StageType.')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: 通常\n'
                else:
                    print('Blockade StageType adjusted to Mystery House StageType.')
                    StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: ミステリーハウス\n'  # StageType for MysteryHouses
            # Fix certain stages having a StageType which breaks certain things.
            elif ('KinopioBrigade' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: キノピオ探検隊\n') or ('KinopioHouse' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and (StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: キノピオの家\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: 隠しキノピオの家\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: 隠し土管')) or ('FairyHouse' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: 妖精の家\n') or ('RouletteRoomZone' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: カジノ部屋\n') or ('GoldenExpressStage' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and (StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: ゴールデンエクスプレス\n')) or ('GateKeeper' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and (StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: ゲートキーパー[GPあり]\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: ゲートキーパー\n')) or ('MysteryHouse' not in StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 8] and StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] == '    StageType: ミステリーハウス\n'):
                print('Non-\'special\' level with \'special\' StageType fixed!')
                StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 10] = '    StageType: 通常\n'  # StageType for normal levels.
        StageListNew[(StageListNew.index('  - CourseId: ' + str(stageNo) + '\n')) + 9] = StageListOld[(StageListOld.index('  - CourseId: ' + str(stageID) + '\n')) + 9]  # StageTimer
        if stageNo == 61:
            stageNo = 67
        else:
            stageNo += 1
    print('First 5 numbers in the list are unused World 5 Toad House slots:', stageID_history)

    #  Test code to print duplicate numbers in the stageID_history list, should not print anything if everything went perfectly.
    print('Duplicate StageIDs:')
    for i in range(0, len(stageID_history)):
        for j in range(i + 1, len(stageID_history)):
            if stageID_history[i] == stageID_history[j]:
                print(stageID_history[j])
    print('\nIf no indication of duplicate numbers are above, success!')

    with open('./tmp-'+currentDateTime+'/StageList.yml', 'w', encoding='utf-8') as rando:
        print('Writing randomized YML.')
        rando.write(''.join([''.join(l2) for l2 in StageListNew]))  # Writing the randomized list to the YML.

    with open('./tmp-'+currentDateTime+'/StageList.yml', 'r', encoding='utf-8') as rando:
        print('Reading randomized YML.')
        randoYML = rando.read()  # Reading the modified YML.

    randoBYML = byml.to_binary(byml.from_text(randoYML), False, 2)  # Converting YML to BYML v2.

    writer = SarcWriter()
    writer.files['StageList.byml'] = randoBYML  # Adding to SARC
    data = writer.write()  # Write to SARC

    with open(rPath+"StageList.szs", "wb") as randoSZS:
        print('Writing randomized YML to SZS.')
        randoSZS.write(yaz0.compress(data[1]))  # Compress with YAZ0 and write to the SZS.
        print('Level randomizer procedure complete!')

    shutil.rmtree('./tmp-'+currentDateTime)  # Delete temporary folder.

    if spoil.get() == 1:
        spoilerFile(StageListNew, currentDateTime)
    else:
        print('Not generating spoiler file.')

    quitB.configure(command=quit)


# Spoiler file generation
def spoilerFile(StageListNew, currentDateTime):
    print('Generating spoiler file...')
    levelIndex = 1
    worldIndex = 1
    overallIndex = 1
    stageID_Name = ['Level Slot, Level Name (Original Level Slot)\n\nWorld ' + str(worldIndex) + '\n']

    # Appending the name of each stage to stageID_name.
    while overallIndex <= 154:
        # World 1
        if StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: EnterCatMarioStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Super Bell Hill (1-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: NokonokoCaveStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Koopa Troopa Cave (1-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ClimbMountainStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mount Beanpole (1-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DownRiverStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Plessie\'s Plunging Falls (1-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: FlipCircusStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Switch Scramble Circus (1-5)\n')
        # Toad House
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioHouseLv1BlueStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioHouseLv2BlueStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioHouseLv3BlueStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioHouseLv1InsideStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioHouseLv3LavaStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioHouseLv3NightStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Toad House\n')
        # World 1 continued
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioBrigadeTentenStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Captain Toad Goes Forth (1-Captain Toad)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KoopaChaseLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Bowser\'s Highway Showdown (1-Castle)\n')
        # Lucky House (Roulette)
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: RouletteRoomZone\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Lucky House\n')
        # World 1 continued
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperBullLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Chargin\' Chuck Blockade (1-A)\n')
        # World 2
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: SideWaveDesertStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Conkdor Canyon (2-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: TouchAndMikeStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Puffprod Peaks (2-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ShadowTunnelStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Shadow-Play Alley (2-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: RotateFieldStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Really Rolling Hills (2-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DoubleMarioFieldStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Double Cherry Pass (2-5)\n')
        # Stamp House
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: FairyHouseBlueStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: FairyHouseInsideStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: FairyHouseLavaStage\n' or StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: FairyHouseNightStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Stamp House\n')
        # World 2 continued
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: MysteryHouseEnemyStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mystery House Melee (2-Mystery House)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KillerTankStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Bowser\'s Bullet Bill Brigade (2-Tank)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperKuribonLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Big Galoomba Blockade (2-A)\n')
        # World 3
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: SnowBallParkStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Snowball Park (3-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ClimbWirenetStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Chainlink Charge (3-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: TeresaConveyorStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Shifty Boo Mansion (3-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ShortGardenStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Pretty Plaza Panic (3-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DokanAquariumStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Pipeline Lagoon (3-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DashRidgeStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mount Must Dash (3-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: TruckWaterfallStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Switchboard Falls (3-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioBrigadeWaterStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Captain Toad Makes a Splash (3-Captain Toad)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KillerExpressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', The Bullet Bill Express (3-Train)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperKameckLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Magikoopa Blockade (3-A)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperTentackLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', A Banquet with Hisstrocrat (3-B)\n')
        # World 4
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: CrawlerHillStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Ant Trooper Hill (4-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: PipePackunDenStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Piranha Creeper Creek (4-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ChikaChikaBoomerangStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Beep Block Skyway (4-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: TrampolineHighlandStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Big Bounce Byway (4-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GabonMountainStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Spike\'s Lost City (4-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: MysteryHouseDashStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mystery House Mad Dash (4-Mystery House)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BossGorobonStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Lava Rock Lair (4-Castle)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperGorobonLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Brolder Blockade (4-A)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperFireBrosLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Fire Bros. Hideout #1 (4-B)\n')
        # World 5
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: NokonokoBeachStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Sunshine Seaside (5-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: SwingCircusStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Tricky Trapeze Theater (5-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ShortMultiLiftStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Backstreet Bustle (5-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: SavannaRockStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Sprawling Savanna (5-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BombCaveStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Bob-ombs Below (5-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: JumpFlipSweetsStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Cakewalk Flip (5-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: SneakingLightStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Searchlight Sneak (5-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GoldenExpressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Coin Express (5-Train)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioBrigadeTeresaStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Captain Toad Plays Peek-a-Boo (5-Captain Toad)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BossWackunFortressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', King Ka-thunk\'s Castle (5-Castle)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperBullLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Chargin\' Chuck Blockade is Back (5-A)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperFireBrosLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Fire Bros. Hideout #2 (5-B)\n')
        # World 6
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: RouteDokanTourStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Clear Pipe Cruise (6-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: WeavingShipStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Spooky Seasick Wreck (6-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KarakuriCastleStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Hands-On Hall (6-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: JungleCruiseStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Deep Jungle Drift (6-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BlastSnowFieldStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Ty-Foo Flurries (6-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ClimbFortressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Bullet Bill Base (6-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ChorobonTowerStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Fuzzy Time Mine (6-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: MysteryHouseBallStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mystery House Throwdown (6-Mystery House)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BombTankStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Bowser\'s Bob-omb Brigade (6-Tank)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperKyupponLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Prince Bully Blockade (6-A)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperFireBrosLv3Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Fire Bros. Hideout #3 (6-B)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperBossBunretsuLv1Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Motley Bossblob\' Big Battle (6-C)\n')
        # World Castle
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: FireBrosFortressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Fort Fire Bros. (Castle-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DarkFlipPanelStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Switchblack Ruins (Castle-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ShortAmidaStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Red-Hot Run (Castle-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DonketsuArrowStepStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Boiling Blue Bully Belt (Castle-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ZigzagBuildingStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Trick Trap Tower (Castle-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: SyumockSpotStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Rammerhead Reef (Castle-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: RagingMagmaStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Simmering Lava Lake (Castle-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioBrigadeConveyorStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Captain Toad Gets Thwomped (Castle-Captain Toad)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KoopaChaseLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Bowser\'s Lava Lake Keep (Castle-Castle)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperGorobonLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Brolder Blockade Is Back (Castle-A)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperKyupponLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Prince Bully Blockade Is Back (Castle-B)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperFireBrosLv4Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Fire Bros. Hideout #4 (Castle-C)\n')
        # World Bowser
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: NeedleBridgeStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Spiky Spike Bridge (Bowser-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DownDesertStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Plessie\'s Dune Downhill (Bowser-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GearSweetsStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Cookie Cogworks (Bowser-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: EchoRoadStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Footlight Lane (Bowser-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: WaterElevatorCaveStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Deepwater Dungeon (Bowser-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: DarknessHauntedHouseStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', A Beam in the Dark (Bowser-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GotogotonValleyStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Grumblump Inferno (Bowser-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: MysteryHouseClimbStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mystery House Claw Climb (Bowser-Mystery House)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: EnemyExpressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', The Bowser Express (Bowser-Train)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KoopaLastStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', The Great Tower of Bowser Land (Bowser-Castle)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperBossBunretsuLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Motley Bossblob\'s Encore (Bowser-A)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GateKeeperTentackLv2Stage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Hisstocrat Returns (Bowser-B)\n')
        # World Star
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: RainbowRoadStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Rainbow Run (Star-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GalaxyRoadStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Super Galaxy (Star-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: WheelCanyonStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Rolling Ride Run (Star-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GoalPoleRunawayStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', The Great Goal Pole (Star-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BlockLandStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Super Block Land (Star-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: HexScrollStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Honeycomb Starway (Star-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: GiantUnderGroundStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Gargantuan Grotto (Star-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: TerenFogStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Peepa\'s Fog Bog (Star-8)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: BoxKillerStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Cosmic Cannon Cluster (Star-9)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioBrigadeRotateRoomStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Captain Toad Takes a Spin (Star-Captain Toad)\n')
        # World Mushroom
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeRotateFieldStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Night Falls on Really Rolling Hills (Mushroom-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeClimbMountainStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Spiky Mount Beanpole (Mushroom-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeJungleCruiseStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Deep-Black Jungle Drift (Mushroom-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeShadowTunnelStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Trouble in Shadow-Play Alley (Mushroom-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeKarakuriCastleStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Back to Hands-On Hall (Mushroom-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeWeavingShipStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Gigantic Seasick Wreck (Mushroom-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeDonketsuArrowStepStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Broken Blue Bully Belt (Mushroom-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeMysteryHouseEnemyStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mystery House Brawl (Mushroom-Mystery House)\n')
        # World Flower
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeFlipCircusStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Switch Shock Circus (Flower-1)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeChorobonTowerStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Floating Fuzzy Time Mine (Flower-2)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangePipePackunDenStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Piranha Creeper Creek after Dark (Flower-3)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeFireBrosFortressStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Faster Fort Fire Bros. (Flower-4)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeSavannaRockStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Sprawling Savanna Rabbit Run (Flower-5)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeTeresaConveorStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Shiftier Boo Mansion (Flower-6)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeDokanAquariumStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Pipeline Boom Lagoon (Flower-7)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeChikaChikaBoomerangStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Blast Block Skyway (Flower-8)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeNokonokoBeachStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Towering Sunshine Seaside (Flower-9)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeHexScrollStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Honeycomb Skyway (Flower-10)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeNeedleBridgeStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Spiky Spike Bridge Sneak (Flower-11)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ArrangeBossParadeStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Boss Blitz (Flower-12)\n')
        # World Crown
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: ChampionshipStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Champion\'s Road (Crown-Crown)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: KinopioBrigadeInfernoStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Captain Toad\'s Fiery Finale (Crown-Captain Toad)\n')
        elif StageListNew[(StageListNew.index('  - CourseId: ' + str(overallIndex) + '\n')) + 8] == '    StageName: MysteryHouseMaxStage\n':
            stageID_Name.append(str(worldIndex)+'-'+str(levelIndex)+', Mystery House Marathon (Crown-Mystery House)\n')
        # Increment to next world.
        if worldIndex == 1 and levelIndex == 11:
            worldIndex = 2
            stageID_Name.append('\nWorld '+str(worldIndex)+'\n')
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

    with open('./romfs-'+currentDateTime+'/'+currentDateTime+'-spoiler.txt', 'w', encoding='utf-8') as s:
        s.write(''.join([''.join(l2) for l2 in stageID_Name]))  # Creating a new spoiler text file.

    with open('./romfs-'+currentDateTime+'/'+currentDateTime+'-spoiler.txt', 'r', encoding='utf-8') as s:
        s = s.read()  # Reading the spoiler file.

    # Making sure levels have the correct names.
    rep = s.replace('11-6', 'Flower-6').replace('11-7', 'Flower-7').replace('11-8', 'Flower-8').replace('11-9', 'Flower-9').replace('11-10', 'Flower-10').replace('11-11', 'Flower-11').replace('11-12', 'Flower-12').replace('12-1', 'Crown-Crown').replace('1-9', '1-Castle').replace('4-9', '4-Castle').replace('5-12', '5-Castle').replace('7-11', 'Castle-Castle').replace('8-13', 'Bowser-Castle').replace('2-9', '2-Tank').replace('6-11', '6-Tank').replace('3-11', '3-Train').replace('8-12', 'Bowser-Train').replace('1-6', '1-Toad House 1').replace('1-7', '1-Toad House 2').replace('2-6', '2-Toad House').replace('3-8', '3-Toad House 1').replace('3-12', '3-Toad House 2').replace('4-6', '4-Toad House').replace('5-9', '5-Toad House 1').replace('5-13', '5-Toad House 2').replace('5-14', '5-Toad House 3').replace('5-15', '5-Toad House 4').replace('5-16', '5-Toad House 5').replace('5-17', '5-Toad House 6').replace('6-8', '6-Toad House 1').replace('6-12', '6-Toad House 2').replace('7-8', 'Castle-Toad House 1').replace('7-12', 'Castle-Toad House 2').replace('8-8', 'Bowser-Toad House 1').replace('8-9', 'Bowser-Toad House 2').replace('8-14', 'Bowser-Toad House 3').replace('2-7', '2-Stamp House').replace('3-9', '3-Stamp House').replace('4-7', '4-Stamp House').replace('5-10', '5-Stamp House').replace('6-9', '6-Stamp House').replace('7-9', 'Castle-Stamp House').replace('8-10', 'Bowser-Stamp House').replace('9-10', 'Star-Stamp House').replace('12-2', 'Crown-Stamp House').replace('1-8', '1-Captain Toad').replace('3-10', '3-Captain Toad').replace('5-11', '5-Captain Toad').replace('7-10', 'Castle-Captain Toad').replace('9-11', 'Star-Captain Toad').replace('12-3', 'Crown-Captain Toad').replace('1-10', 'Lucky House').replace('2-10', 'Lucky House').replace('3-13', 'Lucky House').replace('4-10', 'Lucky House').replace('5-18', 'Lucky House').replace('6-13', 'Lucky House').replace('7-13', 'Lucky House').replace('8-15', 'Lucky House').replace('9-12', 'Lucky House').replace('1-11', '1-A').replace('2-11', '2-A').replace('3-14', '3-A').replace('4-11', '4-A').replace('5-19', '5-A').replace('6-14', '6-A').replace('7-14', 'Castle-A').replace('8-16', 'Bowser-A').replace('3-15', '3-B').replace('4-12', '4-B').replace('5-20', '5-B').replace('6-15', '6-B').replace('7-15', 'Castle-B').replace('8-17', 'Bowser-B').replace('6-16', '6-C').replace('7-16', 'Castle-C').replace('5-8', 'Coin Express').replace('2-8', '2-Mystery House').replace('4-8', '4-Mystery House').replace('6-10', '6-Mystery House').replace('8-11', 'Bowser-Mystery House').replace('10-8', 'Mushroom-Mystery House').replace('12-4', 'Crown-Mystery House').replace('7-', 'Castle-').replace('8-', 'Bowser-').replace('9-', 'Star-').replace('10-', 'Mushroom-').replace('11-', 'Flower-').replace('12-', 'Crown-')

    with open('./romfs-'+currentDateTime+'/'+currentDateTime+'-spoiler.txt', 'w', encoding='utf-8') as s:
        s.write(rep)  # Writing the corrected level slots back to the file.

    print('Generated spoiler file!')


# Buttons
run = Button(root, text='Randomize', fg='red', command=errorPopUp)
openDIR = Button(root, text='Load RomFS directory', fg='red', command=browseDIR)
cred = Button(root, text='Credits', command=creditsDev)
quitB = Button(root, text='Quit', command=root.destroy)

# Check boxes
spoilerCheck = Checkbutton(root, text='Generate spoiler file?', variable=spoil)

# Labels
dirLabel = Label(root, text='Load directory')
noticeLabel = Label(root, text='The Wii U version of Super Mario 3D World is unsupported at this time.')

# Place buttons
cred.place(relx=0.35, rely=0.99, anchor=S)
openDIR.place(relx=0.99, rely=0.2, anchor=E)
run.place(relx=0.5, rely=0.99, anchor=S)
quitB.place(relx=0.65, rely=0.99, anchor=S)

# Place check boxes
spoilerCheck.place(relx=0.01, rely=0.45, anchor=W)

# Place labels
dirLabel.place(relx=0.01, rely=0.2, anchor=W)
noticeLabel.place(relx=0.01, rely=0.62, anchor=W)

root.resizable(False, False)
root.mainloop()

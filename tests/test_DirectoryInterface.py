import pytest
from unittest.mock import MagicMock, patch
import src.lib.DirectoryInterface as DirectoryInterface
from datetime import datetime
from enum import Enum

FIRST_FILE = 0
SECOND_FILE = 1
THIRD_FILE = 2

testFilesNames = [
    'arbitraryFile1',   
    'arbitraryFile2',
    'arbitraryFile3'
]

testFilesSizes = [
    123_321,
    1,
    1_199_999
]

testFilesTimes = [
    datetime(1995, 1, 9, 13, 30, 5), #January 1,   1995,  1:30pm
    datetime(2023, 12, 25, 1, 0, 0), #December 25, 2023,  1:00am
    datetime(2011, 11, 11, 0, 0, 0)  #November 11, 2011, 12:00am
]

def GetSize_SideEffect(filePath):
    size : int
    if testFilesNames[FIRST_FILE] in filePath:
        size = testFilesSizes[FIRST_FILE]
    elif testFilesNames[SECOND_FILE] in filePath:
        size = testFilesSizes[SECOND_FILE]
    elif testFilesNames[THIRD_FILE] in filePath:
        size = testFilesSizes[THIRD_FILE]
    else:
        raise(ValueError)   
    
    return size    

def GetTimes_SideEffect(filePath) -> datetime:
    date : datetime
    if testFilesNames[FIRST_FILE] in filePath:
        date = testFilesTimes[FIRST_FILE].timestamp()
    elif testFilesNames[SECOND_FILE] in filePath:
        date = testFilesTimes[SECOND_FILE].timestamp()
    elif testFilesNames[THIRD_FILE] in filePath:
        date = testFilesTimes[THIRD_FILE].timestamp()
    else:
        raise(ValueError)    

    return date 
    
@pytest.fixture
def MockOS(mocker):
    mocker.patch('os.listdir', return_value = testFilesNames)
    mocker.patch('os.path.isfile', return_value = True)
    #below patches will invoke the _SideEffect methods with the same parameter as what gets sent into the patched method
    mocker.patch('os.path.getsize', side_effect=GetSize_SideEffect) #side_effect allows returning results of 
    mocker.patch('os.path.getmtime', side_effect=GetTimes_SideEffect) # a method or an iterable object like a list

#<<<<<<<<<<<<<<<<<<<< Begin Test >>>>>>>>>>>>>>>>>>>>
def test_GivenPathAndFileWithListOfArbitraryPropertiesExpectZippedDataFormattedCorrectly(MockOS):
    testPath = 'arbitrary/path/'
    expectedTimes = [
        '13:30:05 01-09-1995',
        '01:00:00 12-25-2023',
        '00:00:00 11-11-2011'
    ]

    expectedSizes = [
        123.32,
        0.0,
        1200.00
    ]
    
    expectedResult = list(zip(testFilesNames, expectedSizes, expectedTimes))
    actualResult = list(DirectoryInterface.GetDirectoryContents(testPath)) #GetDirectoryContents returns a zip 
    assert expectedResult == actualResult


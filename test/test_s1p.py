import vna_driver.s1p as s1p
from pathlib import Path
import pytest

@pytest.fixture
def s1p_files_path(): #raw
    return [Path('./s1p_test_files/agua_litevna.s1p'),
            Path('./s1p_test_files/ar.s1p'), 
            Path('./s1p_test_files/AGUA_AGILENT.S1P')] # raw, no comments, with comments


def test_get_comments(s1p_files_path):
    
    c1 = s1p.get_comments(s1p_files_path[0]) 
    c2 = s1p.get_comments(s1p_files_path[1])
    c3 = s1p.get_comments(s1p_files_path[2])
    
    assert len(c1) == 0
    assert len(c2) == 0
    assert len(c3) == 7

    assert c1 == []
    assert c2 == []
    assert c3 == [
        'Agilent Technologies,E5071C,MY46316983,A.11.08',
        'Date: Tue Mar 10 01:37:43 2026',
        'Data & Calibration Information:',
        'Freq	S11:NONE(--)',
        'PortZ  Port1:50+j0',
        'Above PortZ is port z conversion or system Z0 setting when saving the data.',
        'When reading, reference impedance value at option line is always used.']

def test_get_option(s1p_files_path):
    c1 = s1p.get_option(s1p_files_path[0]) 
    c2 = s1p.get_option(s1p_files_path[1])
    c3 = s1p.get_option(s1p_files_path[2])

    assert c1 == []
    assert c2 == ['Hz', 'S', 'RI', 'R', '50']
    assert c3 == ['Hz', 'S', 'dB', 'R', '50']

def test_get_data():
    
    
    pass

def test_read_s1p(s1p_files_path): #no comments and header
    
    _,_,data1 = s1p.read_s1p(s1p_files_path[0])
    _,_,data2 = s1p.read_s1p(s1p_files_path[1])
    _,_,data3 = s1p.read_s1p(s1p_files_path[2])


    #NUMBER OF COLUMNS

    assert len(data1) == 3
    assert len(data2) == 3
    assert len(data3) == 3


    #NUMBER OF LINES IN ONE COLUMNVV
    assert len(data1[0]) == 401
    assert len(data2[0]) == 201
    assert len(data3[0]) == 401



    freq1 = data1[0]
    r1 = data1[1]
    i1 = data1[2]    

    freq2 = data2[0]
    r2 = data2[1]
    i2 = data2[2]

    freq3 = data3[0]
    r3 = data3[1]
    i3 = data3[2]


    assert freq1[0] == 1000000000
    assert freq1[-1] == 5987530800
    assert r1[0] == -0.794140636920929
    assert r1[-1] == 0.40582869946956635
    assert i1[0] == -0.5999352931976318
    assert i1[-1] == 0.15490838885307312

    assert freq2[0] == 1000000000
    assert freq2[-1] == 5975124200
    assert r2[0] == 0.75937262921
    assert r2[-1] == -0.26498062920
    assert i2[0] == 0.60360266461
    assert i2[-1] == -0.85413519178


    assert freq3[0] == 1000000000
    assert freq3[-1] == 6000000000
    assert r3[0] == -1.122726e+000
    assert r3[-1] == -4.490525e+000
    assert i3[0] == -3.995665e+000
    assert i3[-1] == 7.913907e+001


def test_write():
    pass
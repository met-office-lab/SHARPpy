from StringIO import StringIO
from sharppy.sharptab.profile import Profile
import urllib
import time as gmtime
import datetime
import sys
import numpy as np

## get the current utc time and format it into
## a string that can be used for the SPC url.
if sys.argv[1] != "test":
    gmtime = datetime.datetime.utcnow()
    t_str = str( gmtime )
    year = t_str[2:4]
    month = t_str[5:7]
    day = t_str[8:10]
    hour = t_str[11:13]
    if int( hour ) > 12:
        current_ob = '12'
    else:
        current_ob = '00'
        
    obstring = year + month + day + current_ob
    obstime = datetime.datetime.strptime( obstring, '%y%m%d%H')
    delta1 = datetime.timedelta( hours=12 )
    delta2 = datetime.timedelta( hours=24 )
    obs12 = obstime - delta1
    obs24 = obstime - delta2
        
    t_str = str( obs12 )
    year = t_str[2:4]
    month = t_str[5:7]
    day = t_str[8:10]
    hour = t_str[11:13]
    obstring2 = year + month + day + hour

        
    url = urllib.urlopen('http://www.spc.noaa.gov/exper/soundings/LATEST/' + str( sys.argv[1] ).upper() + '.txt')
    data = np.array(url.read().split('\n'))
    title_idx = np.where( data == '%TITLE%')[0][0]
    start_idx = np.where( data == '%RAW%' )[0] + 1
    finish_idx = np.where( data == '%END%')[0]
    plot_title = data[title_idx + 1] + ' (Observed)'
    full_data = '\n'.join(data[start_idx : finish_idx][:])
    sound_data = StringIO( full_data )
    p, h, T, Td, wdir, wspd = np.genfromtxt( sound_data, delimiter=',', comments="%", unpack=True )
    prof = Profile( pres=p, hght=h, tmpc=T, dwpc=Td, wdir=wdir, wspd=wspd, location=sys.argv[1])


else:
	sound = '''
	  966.0,    345,   21.6,   19.7,     89,  15.19,    160,      7,  297.7,  341.9,  300.4
	  958.0,    416,   21.2,   19.5,     90,  15.13,    167,     12,  298.0,  342.1,  300.7
	  936.6,    610,   20.4,   19.2,     93,  15.17,    185,     27,  299.1,  343.5,  301.8
	  925.0,    717,   20.0,   19.0,     94,  15.19,    195,     34,  299.8,  344.3,  302.5
	  909.0,    868,   19.0,   18.8,     99,  15.27,    214,     39,  300.2,  345.1,  303.0
	  904.2,    914,   19.7,   19.3,     98,  15.89,    220,     40,  301.4,  348.3,  304.2
	  893.0,   1022,   21.2,   20.6,     96,  17.43,    224,     38,  304.0,  356.1,  307.2
	  879.0,   1160,   24.0,   13.0,     50,  10.82,    228,     34,  308.3,  341.4,  310.3
	  873.1,   1219,   23.9,   11.0,     44,   9.54,    230,     33,  308.8,  338.1,  310.5
	  863.0,   1321,   23.6,    7.6,     36,   7.64,    226,     29,  309.5,  333.3,  310.9
	  850.0,   1453,   22.6,    4.6,     31,   6.29,    220,     24,  309.8,  329.6,  311.0
	  817.0,   1795,   20.2,   -3.8,     20,   3.55,    220,     20,  310.8,  322.3,  311.5
	  813.8,   1829,   19.9,   -4.0,     19,   3.50,    220,     20,  310.9,  322.2,  311.5
	  785.3,   2134,   17.7,   -6.3,     19,   3.04,    235,     17,  311.6,  321.6,  312.2
	  770.0,   2302,   16.4,   -7.6,     19,   2.82,    232,     19,  312.0,  321.3,  312.5
	  757.6,   2438,   15.1,   -7.7,     20,   2.84,    230,     20,  312.0,  321.4,  312.6
	  730.5,   2743,   12.1,   -7.9,     24,   2.89,    225,     21,  312.1,  321.6,  312.6
	  701.0,   3088,    8.8,   -8.2,     29,   2.95,    220,     25,  312.1,  321.8,  312.6
	  700.0,   3100,    8.6,   -8.4,     29,   2.91,    220,     25,  312.0,  321.5,  312.5
	  653.6,   3658,    3.8,  -11.3,     32,   2.48,    215,     36,  312.7,  321.0,  313.2
	  628.0,   3984,    1.0,  -13.0,     34,   2.25,    220,     35,  313.1,  320.6,  313.6
	  605.7,   4267,   -1.6,  -14.0,     38,   2.15,    225,     35,  313.4,  320.6,  313.8
	  582.6,   4572,   -4.4,  -15.1,     43,   2.04,    235,     32,  313.6,  320.4,  314.0
	  560.4,   4877,   -7.2,  -16.2,     49,   1.94,    235,     35,  313.8,  320.3,  314.1
	  524.0,   5403,  -12.1,  -18.1,     61,   1.77,    248,     50,  314.0,  320.0,  314.3
	  518.3,   5486,  -12.6,  -19.7,     55,   1.56,    250,     53,  314.4,  319.8,  314.7
	  504.0,   5700,  -13.7,  -23.7,     43,   1.13,    250,     47,  315.6,  319.5,  315.8
	  500.0,   5760,  -14.1,  -24.1,     43,   1.10,    250,     45,  315.8,  319.6,  316.0
	  485.0,   5991,  -16.1,  -25.1,     46,   1.03,    247,     48,  316.1,  319.7,  316.3
	  479.0,   6085,  -15.3,  -30.3,     27,   0.65,    245,     50,  318.2,  320.6,  318.3
	  478.3,   6096,  -15.3,  -30.8,     25,   0.62,    245,     50,  318.3,  320.6,  318.4
	  472.0,   6197,  -15.3,  -35.3,     16,   0.40,    245,     50,  319.5,  321.1,  319.6
	  468.0,   6262,  -13.9,  -41.9,      7,   0.21,    245,     50,  322.1,  322.9,  322.1
	  446.0,   6627,  -15.5,  -49.5,      4,   0.09,    245,     51,  324.5,  324.9,  324.5
	  400.0,   7440,  -22.7,  -51.7,      5,   0.08,    245,     53,  325.4,  325.7,  325.4
	  390.2,   7620,  -24.3,  -52.4,      6,   0.08,    240,     55,  325.6,  325.9,  325.6
	  389.0,   7643,  -24.5,  -52.5,      6,   0.08,    240,     55,  325.6,  326.0,  325.7
	  373.9,   7925,  -26.5,  -53.4,      6,   0.07,    240,     59,  326.7,  327.0,  326.8
	  314.9,   9144,  -35.0,  -57.3,      8,   0.05,    250,     57,  331.2,  331.5,  331.3
	  312.0,   9209,  -35.5,  -57.5,      9,   0.05,    250,     57,  331.5,  331.7,  331.5
	  301.4,   9449,  -37.6,  -58.7,      9,   0.05,    250,     56,  331.8,  332.0,  331.8
	  300.0,   9480,  -37.9,  -58.9,      9,   0.05,    250,     56,  331.8,  332.0,  331.9
	  251.6,  10668,  -48.3,  -63.5,     16,   0.03,    240,     52,  333.5,  333.6,  333.5
	  250.0,  10710,  -48.7,  -63.7,     16,   0.03,    240,     52,  333.5,  333.7,  333.5
	  247.0,  10789,  -49.5,  -63.5,     18,   0.03,    240,     53,  333.5,  333.6,  333.5
	  210.0,  11830,  -56.3,  -68.3,     21,   0.02,    240,     65,  338.7,  338.8,  338.7
	  208.1,  11887,  -55.9,  -68.1,     20,   0.02,    245,     70,  340.2,  340.3,  340.2
	  205.0,  11983,  -55.2,  -67.9,     19,   0.02,    245,     70,  342.8,  342.9,  342.8
	  203.0,  12045,  -54.7,  -67.7,     19,   0.02,    247,     70,  344.5,  344.6,  344.5
	  200.0,  12140,  -54.7,  -67.7,     19,   0.02,    250,     69,  346.0,  346.1,  346.0
	  193.0,  12368,  -55.1,  -68.1,     18,   0.02,    250,     69,  348.9,  349.0,  348.9
	  191.0,  12435,  -53.9,  -66.9,     19,   0.02,    250,     69,  351.9,  352.0,  351.9
	  185.0,  12640,  -54.7,  -67.7,     19,   0.02,    250,     68,  353.8,  353.9,  353.8
	  183.0,  12710,  -53.3,  -66.3,     19,   0.03,    250,     68,  357.1,  357.3,  357.2
	  180.4,  12802,  -53.0,  -66.5,     18,   0.03,    250,     68,  359.1,  359.2,  359.1
	  178.0,  12889,  -52.7,  -66.7,     17,   0.03,    250,     64,  361.0,  361.1,  361.0
	  167.0,  13301,  -54.3,  -67.3,     19,   0.03,    250,     48,  364.9,  365.1,  364.9
	  164.2,  13411,  -54.0,  -67.0,     19,   0.03,    250,     43,  367.3,  367.4,  367.3
	  162.0,  13496,  -53.7,  -66.7,     19,   0.03,    252,     43,  369.1,  369.3,  369.1
	  151.0,  13948,  -55.7,  -68.7,     18,   0.02,    264,     41,  373.2,  373.3,  373.2
	  150.0,  13990,  -55.5,  -68.5,     18,   0.03,    265,     41,  374.2,  374.4,  374.3
	  147.0,  14119,  -55.5,  -68.5,     18,   0.03,    263,     40,  376.4,  376.6,  376.4
	  140.0,  14429,  -57.7,  -70.7,     18,   0.02,    260,     36,  377.8,  377.9,  377.9
	  138.0,  14520,  -56.3,  -69.3,     18,   0.02,    259,     35,  381.9,  382.0,  381.9
	  136.0,  14613,  -56.3,  -69.3,     18,   0.02,    258,     34,  383.5,  383.6,  383.5
	  123.0,  15240,  -61.4,  -73.1,     20,   0.02,    250,     27,  385.4,  385.5,  385.4
	  116.0,  15606,  -64.3,  -75.3,     21,   0.01,    264,     27,  386.5,  386.6,  386.5
	  108.0,  16042,  -66.1,  -77.1,     20,   0.01,    281,     26,  391.1,  391.1,  391.1
	  105.0,  16213,  -65.7,  -76.7,     20,   0.01,    288,     26,  395.0,  395.0,  395.0
	  102.0,  16389,  -66.7,  -77.7,     20,   0.01,    295,     26,  396.3,  396.4,  396.4
	  101.0,  16449,  -64.9,  -75.9,     21,   0.01,    302,     24,  400.9,  401.0,  400.9
	  100.0,  16510,  -63.5,  -74.5,     21,   0.02,    310,     21,  404.8,  404.9,  404.8
	   97.3,  16679,  -61.5,  -73.5,     19,   0.02,      6,     10,  411.8,  411.9,  411.9
	   96.0,  16764,  -62.0,  -73.9,     19,   0.02,     35,      4,  412.5,  412.6,  412.5
	   91.3,  17069,  -63.7,  -75.2,     20,   0.02,    120,     10,  415.0,  415.1,  415.0
	   85.7,  17456,  -65.9,  -76.9,     20,   0.01,    175,      6,  418.2,  418.2,  418.2
	   79.6,  17904,  -65.5,  -76.5,     20,   0.01,    239,      2,  427.9,  428.0,  427.9
	   78.6,  17983,  -65.7,  -76.7,     20,   0.01,    250,      1,  429.1,  429.1,  429.1
	   74.7,  18288,  -66.6,  -77.6,     20,   0.01,    205,      8,  433.5,  433.6,  433.5
	   70.0,  18680,  -67.7,  -78.7,     20,   0.01,    305,      5,  439.2,  439.3,  439.2
	   69.1,  18758,  -65.7,  -76.7,     20,   0.02,    310,      5,  445.1,  445.2,  445.1
	   67.0,  18945,  -66.5,  -77.5,     20,   0.01,    324,      6,  447.4,  447.4,  447.4
	   63.5,  19273,  -63.7,  -75.7,     18,   0.02,    346,      7,  460.4,  460.6,  460.4
	   55.3,  20118,  -65.1,  -76.1,     21,   0.02,     45,     11,  475.8,  475.9,  475.8
	   52.6,  20422,  -62.2,  -73.9,     19,   0.03,     75,     20,  489.3,  489.6,  489.3
	   51.7,  20532,  -61.1,  -73.1,     19,   0.04,     86,     17,  494.3,  494.6,  494.3
	   50.1,  20726,  -61.5,  -73.5,     19,   0.04,    105,     13,  497.9,  498.1,  497.9
	   50.0,  20740,  -61.5,  -73.5,     19,   0.04,    105,     13,  498.1,  498.4,  498.1
	   49.4,  20815,  -61.3,  -73.3,     19,   0.04,     95,     14,  500.3,  500.6,  500.3
	   47.7,  21031,  -60.2,  -72.6,     18,   0.04,     65,     15,  508.0,  508.3,  508.0
	   45.4,  21336,  -58.6,  -71.6,     17,   0.05,     85,     15,  518.9,  519.3,  518.9
	   45.3,  21356,  -58.5,  -71.5,     17,   0.05,     85,     15,  519.6,  520.0,  519.7
	   43.3,  21641,  -58.2,  -71.4,     17,   0.06,     80,     16,  527.0,  527.4,  527.0
	   39.3,  22250,  -57.7,  -71.1,     17,   0.07,    115,     13,  543.1,  543.6,  543.1
	   37.5,  22555,  -57.4,  -71.0,     16,   0.07,     90,     12,  551.3,  551.9,  551.4
	   35.7,  22860,  -57.2,  -70.8,     16,   0.08,     60,      8,  559.7,  560.3,  559.7
	   34.0,  23165,  -56.9,  -70.7,     16,   0.08,     60,     20,  568.2,  568.8,  568.2
	   32.4,  23470,  -56.6,  -70.6,     16,   0.09,     80,     23,  576.8,  577.5,  576.8
	   31.6,  23629,  -56.5,  -70.5,     16,   0.09,     82,     20,  581.3,  582.1,  581.4
	   30.0,  23960,  -54.5,  -69.5,     14,   0.11,     85,     14,  595.5,  596.4,  595.5
	   28.1,  24384,  -53.2,  -69.0,     13,   0.13,     95,     14,  610.5,  611.5,  610.5
	   27.7,  24473,  -52.9,  -68.9,     13,   0.13,     93,     14,  613.6,  614.8,  613.7
	   26.2,  24831,  -53.9,  -69.9,     12,   0.12,     86,     13,  620.7,  621.7,  620.7
	   22.9,  25698,  -52.7,  -70.7,     10,   0.12,     68,     10,  648.5,  649.6,  648.6
	   20.0,  26580,  -49.1,  -72.1,      5,   0.11,     50,      7,  685.1,  686.2,  685.2
	   19.9,  26613,  -48.9,  -71.9,      5,   0.12,     50,      7,  686.7,  687.8,  686.8
	   17.7,  27377,  -51.7,  -73.7,      5,   0.10,     59,     14,  701.2,  702.2,  701.3
	   17.6,  27432,  -51.4,  -73.8,      5,   0.10,     60,     15,  704.0,  705.0,  704.0
	   15.3,  28346,  -45.6,  -74.8,      2,   0.10,    230,      6,  751.3,  752.4,  751.4
	   15.0,  28467,  -44.9,  -74.9,      2,   0.10,  -9999.00,  -999.00,  757.8,  758.8,  757.8'''
	sound_data = StringIO( sound )
	p2, h2, T2, Td2, Rh2, mix, wdir2, wspd2, thta, thte, thtv = np.genfromtxt( sound_data, delimiter=',', comments="%", unpack=True )
	test = Profile( pres=p2, hght=h2, tmpc=T2, dwpc=Td2, wdir=wdir2, wspd=wspd2, location='OUN' )

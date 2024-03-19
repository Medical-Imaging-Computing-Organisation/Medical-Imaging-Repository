import os
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
# import scipy.ndimage as nd
# import pandas as pd
# from pathlib import Path
# from numba import njit
# from numba import prange
# from numba import set_num_threads

# import CSV_Multiple_Detector_File_Extraction as ExH0 Feb29 Setup 8 A
import CSV_Data_Extraction as Ex
import Detector_time_fit as Df
import Find_True_Coincidences_No_Time_Swap as Co
import Function1 as F1
import Func2SphericPolar as F2
import Function3 as F3
import Function4HeatmapHybridVectorized as F4
import Function5 as F5

E0 = 0.662  # MeV
dE0 = 3E-5  # MeV
Me = 0.51099895000  # MeV
tau = 0
epsilon = 0.05
Delimiter = ','
Header = 0
Folder_Path = os.getcwd()
ETFile0 = 'CSV1_Exact_G_D1.csv'
ETFile1 = 'CSV1_Exact_G_D2.csv'
ETFile2 = 'CSV1_Exact_G_D3.csv'
# ETFile3 = 'CSV1_Exact_G_D4.csv'
ETFile4 = 'CSV1_Exact_G_D5.csv'
ETFile5 = 'CSV1_Exact_G_D6.csv'
ETFile6 = 'CSV1_Exact_G_D7.csv'
ETFile7 = 'CSV1_Exact_G_D8.csv'
ETFile8 = 'CSV1_Exact_G_D9.csv'
ETFile9 = 'CSV1_Exact_G_D10.csv'
ETFile10 = 'CSV1_Exact_G_D11.csv'
ETFile11 = 'CSV1_Exact_G_D12.csv'
ETFile12 = 'CSV1_Exact_G_D13.csv'
ETFile13 = 'CSV1_Exact_G_D14.csv'
ETFile14 = 'CSV1_Exact_G_D15.csv'
ETFile15 = 'CSV1_Exact_G_D16.csv'
ETFile16 = 'CSV1_Exact_G_D17.csv'
ETFile17 = 'CSV1_Exact_G_D18.csv'
ETFile18 = 'CSV1_Exact_G_D19.csv'
ETFile19 = 'CSV1_Exact_G_D20.csv'
ETFile20 = 'CSV1_Exact_G_D21.csv'
ETFile21 = 'CSV1_Exact_G_D22.csv'
ETFile22 = 'CSV1_Exact_G_D23.csv'
ETFile23 = 'CSV1_Exact_G_D24.csv'
ETFile24 = 'CSV1_Exact_G_D25.csv'
ETFile25 = 'CSV1_Exact_G_D26.csv'
ETFile26 = 'CSV1_Exact_G_D27.csv'
ETFile27 = 'CSV1_Exact_G_D28.csv'
ETFile28 = 'CSV1_Exact_G_D29.csv'
ETFile29 = 'CSV1_Exact_G_D30.csv'
ETFile30 = 'CSV1_Exact_G_D31.csv'
ETFile31 = 'CSV1_Exact_G_D32.csv'
ETFile32 = 'CSV1_Exact_G_D33.csv'
ETFile33 = 'CSV1_Exact_G_D34.csv'
ETFile34 = 'CSV1_Exact_G_D35.csv'
ETFile35 = 'CSV1_Exact_G_D36.csv'
ETFile36 = 'CSV1_Exact_G_D37.csv'
ETFile37 = 'CSV1_Exact_G_D38.csv'
ETFile38 = 'CSV1_Exact_G_D39.csv'
ETFile39 = 'CSV1_Exact_G_D40.csv'
ETFile40 = 'CSV1_Exact_G_D41.csv'
ETFile41 = 'CSV1_Exact_G_D42.csv'
ETFile42 = 'CSV1_Exact_G_D43.csv'
ETFile43 = 'CSV1_Exact_G_D44.csv'
ETFile44 = 'CSV1_Exact_G_D45.csv'
ETFile45 = 'CSV1_Exact_G_D46.csv'
ETFile46 = 'CSV1_Exact_G_D47.csv'
ETFile47 = 'CSV1_Exact_G_D48.csv'
ETFile48 = 'CSV1_Exact_G_D49.csv'
ETFile49 = 'CSV1_Exact_G_D50.csv'
ETFile50 = 'CSV1_Exact_G_D51.csv'
ETFile51 = 'CSV1_Exact_G_D52.csv'
ETFile52 = 'CSV1_Exact_G_D53.csv'
ETFile53 = 'CSV1_Exact_G_D54.csv'
ETFile54 = 'CSV1_Exact_G_D55.csv'
ETFile55 = 'CSV1_Exact_G_D56.csv'
ETFile56 = 'CSV1_Exact_G_D57.csv'
ETFile57 = 'CSV1_Exact_G_D58.csv'
ETFile58 = 'CSV1_Exact_G_D59.csv'
ETFile59 = 'CSV1_Exact_G_D60.csv'
ETFile60 = 'CSV1_Exact_G_D61.csv'
ETFile61 = 'CSV1_Exact_G_D62.csv'
ETFile62 = 'CSV1_Exact_G_D63.csv'
ETFile63 = 'CSV1_Exact_G_D64.csv'
ETFile64 = 'CSV1_Exact_G_D65.csv'
ETFile65 = 'CSV1_Exact_G_D66.csv'
ETFile66 = 'CSV1_Exact_G_D67.csv'
ETFile67 = 'CSV1_Exact_G_D68.csv'
ETFile68 = 'CSV1_Exact_G_D69.csv'
ETFile69 = 'CSV1_Exact_G_D70.csv'
ETFile70 = 'CSV1_Exact_G_D71.csv'
ETFile71 = 'CSV1_Exact_G_D72.csv'
ETFile72 = 'CSV1_Exact_G_D73.csv'
ETFile73 = 'CSV1_Exact_G_D74.csv'
ETFile74 = 'CSV1_Exact_G_D75.csv'
ETFile75 = 'CSV1_Exact_G_D76.csv'
ETFile76 = 'CSV1_Exact_G_D77.csv'
ETFile77 = 'CSV1_Exact_G_D78.csv'
ETFile78 = 'CSV1_Exact_G_D79.csv'
ETFile79 = 'CSV1_Exact_G_D80.csv'
ETFile80 = 'CSV1_Exact_G_D81.csv'
ETFile81 = 'CSV1_Exact_G_D82.csv'
ETFile82 = 'CSV1_Exact_G_D83.csv'
ETFile83 = 'CSV1_Exact_G_D84.csv'
ETFile84 = 'CSV1_Exact_G_D85.csv'
ETFile85 = 'CSV1_Exact_G_D86.csv'
ETFile86 = 'CSV1_Exact_G_D87.csv'
ETFile87 = 'CSV1_Exact_G_D88.csv'
ETFile88 = 'CSV1_Exact_G_D89.csv'
ETFile89 = 'CSV1_Exact_G_D90.csv'
ETFile90 = 'CSV1_Exact_G_D91.csv'
ETFile91 = 'CSV1_Exact_G_D92.csv'
ETFile92 = 'CSV1_Exact_G_D93.csv'
ETFile93 = 'CSV1_Exact_G_D94.csv'
ETFile94 = 'CSV1_Exact_G_D95.csv'
ETFile95 = 'CSV1_Exact_G_D96.csv'
ETFile96 = 'CSV1_Exact_G_D97.csv'
ETFile97 = 'CSV1_Exact_G_D98.csv'
ETFile98 = 'CSV1_Exact_G_D99.csv'
ETFile99 = 'CSV1_Exact_G_D100.csv'
Det_Pos = 'MC Pixelator CSV2 Full.csv'
# Number_of_Files = 4
start = timer()

print("Started!")
CSV_Start = timer()
_, Det_Pos_arr = Ex.CSV_Extract(',', Folder_Path, Det_Pos, Det_Pos)
arr0 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile0)
arr1 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile1)
arr2 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile2)
# arr3 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile3)
arr4 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile4)
arr5 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile5)
arr6 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile6)
arr7 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile7)
arr8 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile8)
arr9 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile9)
arr10 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile10)
arr11 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile11)
arr12 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile12)
arr13 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile13)
arr14 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile14)
arr15 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile15)
arr16 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile16)
arr17 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile17)
arr18 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile18)
arr19 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile19)
arr20 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile20)
arr21 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile21)
arr22 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile22)
arr23 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile23)
arr24 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile24)
arr25 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile25)
arr26 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile26)
arr27 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile27)
arr28 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile28)
arr29 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile29)
arr30 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile30)
arr31 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile31)
arr32 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile32)
arr33 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile33)
arr34 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile34)
arr35 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile35)
arr36 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile36)
arr37 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile37)
arr38 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile38)
arr39 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile39)
arr40 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile40)
arr41 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile41)
arr42 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile42)
arr43 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile43)
arr44 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile44)
arr45 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile45)
arr46 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile46)
arr47 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile47)
arr48 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile48)
arr49 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile49)
arr50 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile50)
arr51 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile51)
arr52 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile52)
arr53 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile53)
arr54 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile54)
arr55 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile55)
arr56 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile56)
arr57 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile57)
arr58 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile58)
arr59 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile59)
arr60 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile60)
arr61 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile61)
arr62 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile62)
arr63 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile63)
arr64 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile64)
arr65 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile65)
arr66 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile66)
arr67 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile67)
arr68 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile68)
arr69 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile69)
arr70 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile70)
arr71 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile71)
arr72 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile72)
arr73 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile73)
arr74 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile74)
arr75 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile75)
arr76 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile76)
arr77 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile77)
arr78 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile78)
arr79 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile79)
arr80 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile80)
arr81 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile81)
arr82 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile82)
arr83 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile83)
arr84 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile84)
arr85 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile85)
arr86 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile86)
arr87 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile87)
arr88 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile88)
arr89 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile89)
arr90 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile90)
arr91 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile91)
arr92 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile92)
arr93 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile93)
arr94 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile94)
arr95 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile95)
arr96 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile96)
arr97 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile97)
arr98 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile98)
arr99 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile99)


print("CSV Extraction Done in {} s".format(timer() - CSV_Start))

Fit_Start = timer()
arr0_coeffs, arr0_difference = Df.detector_time_fit(arr0, False, False)
arr1_coeffs, arr1_difference = Df.detector_time_fit(arr1, False, False)
arr2_coeffs, arr2_difference = Df.detector_time_fit(arr2, False, False)
# arr3_coeffs, arr3_difference = Df.detector_time_fit(arr3, False, False)
arr4_coeffs, arr4_difference = Df.detector_time_fit(arr4, False, False)
arr5_coeffs, arr5_difference = Df.detector_time_fit(arr5, False, False)
arr6_coeffs, arr6_difference = Df.detector_time_fit(arr6, False, False)
arr7_coeffs, arr7_difference = Df.detector_time_fit(arr7, False, False)
arr8_coeffs, arr8_difference = Df.detector_time_fit(arr8, False, False)
arr9_coeffs, arr9_difference = Df.detector_time_fit(arr9, False, False)
arr10_coeffs, arr10_difference = Df.detector_time_fit(arr10, False, False)
arr11_coeffs, arr11_difference = Df.detector_time_fit(arr11, False, False)
arr12_coeffs, arr12_difference = Df.detector_time_fit(arr12, False, False)
arr13_coeffs, arr13_difference = Df.detector_time_fit(arr13, False, False)
arr14_coeffs, arr14_difference = Df.detector_time_fit(arr14, False, False)
arr15_coeffs, arr15_difference = Df.detector_time_fit(arr15, False, False)
arr16_coeffs, arr16_difference = Df.detector_time_fit(arr16, False, False)
arr17_coeffs, arr17_difference = Df.detector_time_fit(arr17, False, False)
arr18_coeffs, arr18_difference = Df.detector_time_fit(arr18, False, False)
arr19_coeffs, arr19_difference = Df.detector_time_fit(arr19, False, False)
arr20_coeffs, arr20_difference = Df.detector_time_fit(arr20, False, False)
arr21_coeffs, arr21_difference = Df.detector_time_fit(arr21, False, False)
arr22_coeffs, arr22_difference = Df.detector_time_fit(arr22, False, False)
arr23_coeffs, arr23_difference = Df.detector_time_fit(arr23, False, False)
arr24_coeffs, arr24_difference = Df.detector_time_fit(arr24, False, False)
arr25_coeffs, arr25_difference = Df.detector_time_fit(arr25, False, False)
arr26_coeffs, arr26_difference = Df.detector_time_fit(arr26, False, False)
arr27_coeffs, arr27_difference = Df.detector_time_fit(arr27, False, False)
arr28_coeffs, arr28_difference = Df.detector_time_fit(arr28, False, False)
arr29_coeffs, arr29_difference = Df.detector_time_fit(arr29, False, False)
arr30_coeffs, arr30_difference = Df.detector_time_fit(arr30, False, False)
arr31_coeffs, arr31_difference = Df.detector_time_fit(arr31, False, False)
arr32_coeffs, arr32_difference = Df.detector_time_fit(arr32, False, False)
arr33_coeffs, arr33_difference = Df.detector_time_fit(arr33, False, False)
arr34_coeffs, arr34_difference = Df.detector_time_fit(arr34, False, False)
arr35_coeffs, arr35_difference = Df.detector_time_fit(arr35, False, False)
arr36_coeffs, arr36_difference = Df.detector_time_fit(arr36, False, False)
arr37_coeffs, arr37_difference = Df.detector_time_fit(arr37, False, False)
arr38_coeffs, arr38_difference = Df.detector_time_fit(arr38, False, False)
arr39_coeffs, arr39_difference = Df.detector_time_fit(arr39, False, False)
arr40_coeffs, arr40_difference = Df.detector_time_fit(arr40, False, False)
arr41_coeffs, arr41_difference = Df.detector_time_fit(arr41, False, False)
arr42_coeffs, arr42_difference = Df.detector_time_fit(arr42, False, False)
arr43_coeffs, arr43_difference = Df.detector_time_fit(arr43, False, False)
arr44_coeffs, arr44_difference = Df.detector_time_fit(arr44, False, False)
arr45_coeffs, arr45_difference = Df.detector_time_fit(arr45, False, False)
arr46_coeffs, arr46_difference = Df.detector_time_fit(arr46, False, False)
arr47_coeffs, arr47_difference = Df.detector_time_fit(arr47, False, False)
arr48_coeffs, arr48_difference = Df.detector_time_fit(arr48, False, False)
arr49_coeffs, arr49_difference = Df.detector_time_fit(arr49, False, False)
arr50_coeffs, arr50_difference = Df.detector_time_fit(arr50, False, False)
arr51_coeffs, arr51_difference = Df.detector_time_fit(arr51, False, False)
arr52_coeffs, arr52_difference = Df.detector_time_fit(arr52, False, False)
arr53_coeffs, arr53_difference = Df.detector_time_fit(arr53, False, False)
arr54_coeffs, arr54_difference = Df.detector_time_fit(arr54, False, False)
arr55_coeffs, arr55_difference = Df.detector_time_fit(arr55, False, False)
arr56_coeffs, arr56_difference = Df.detector_time_fit(arr56, False, False)
arr57_coeffs, arr57_difference = Df.detector_time_fit(arr57, False, False)
arr58_coeffs, arr58_difference = Df.detector_time_fit(arr58, False, False)
arr59_coeffs, arr59_difference = Df.detector_time_fit(arr59, False, False)
arr60_coeffs, arr60_difference = Df.detector_time_fit(arr60, False, False)
arr61_coeffs, arr61_difference = Df.detector_time_fit(arr61, False, False)
arr62_coeffs, arr62_difference = Df.detector_time_fit(arr62, False, False)
arr63_coeffs, arr63_difference = Df.detector_time_fit(arr63, False, False)
arr64_coeffs, arr64_difference = Df.detector_time_fit(arr64, False, False)
arr65_coeffs, arr65_difference = Df.detector_time_fit(arr65, False, False)
arr66_coeffs, arr66_difference = Df.detector_time_fit(arr66, False, False)
arr67_coeffs, arr67_difference = Df.detector_time_fit(arr67, False, False)
arr68_coeffs, arr68_difference = Df.detector_time_fit(arr68, False, False)
arr69_coeffs, arr69_difference = Df.detector_time_fit(arr69, False, False)
arr70_coeffs, arr70_difference = Df.detector_time_fit(arr70, False, False)
arr71_coeffs, arr71_difference = Df.detector_time_fit(arr71, False, False)
arr72_coeffs, arr72_difference = Df.detector_time_fit(arr72, False, False)
arr73_coeffs, arr73_difference = Df.detector_time_fit(arr73, False, False)
arr74_coeffs, arr74_difference = Df.detector_time_fit(arr74, False, False)
arr75_coeffs, arr75_difference = Df.detector_time_fit(arr75, False, False)
arr76_coeffs, arr76_difference = Df.detector_time_fit(arr76, False, False)
arr77_coeffs, arr77_difference = Df.detector_time_fit(arr77, False, False)
arr78_coeffs, arr78_difference = Df.detector_time_fit(arr78, False, False)
arr79_coeffs, arr79_difference = Df.detector_time_fit(arr79, False, False)
arr80_coeffs, arr80_difference = Df.detector_time_fit(arr80, False, False)
arr81_coeffs, arr81_difference = Df.detector_time_fit(arr81, False, False)
arr82_coeffs, arr82_difference = Df.detector_time_fit(arr82, False, False)
arr83_coeffs, arr83_difference = Df.detector_time_fit(arr83, False, False)
arr84_coeffs, arr84_difference = Df.detector_time_fit(arr84, False, False)
arr85_coeffs, arr85_difference = Df.detector_time_fit(arr85, False, False)
arr86_coeffs, arr86_difference = Df.detector_time_fit(arr86, False, False)
arr87_coeffs, arr87_difference = Df.detector_time_fit(arr87, False, False)
arr88_coeffs, arr88_difference = Df.detector_time_fit(arr88, False, False)
arr89_coeffs, arr89_difference = Df.detector_time_fit(arr89, False, False)
arr90_coeffs, arr90_difference = Df.detector_time_fit(arr90, False, False)
arr91_coeffs, arr91_difference = Df.detector_time_fit(arr91, False, False)
arr92_coeffs, arr92_difference = Df.detector_time_fit(arr92, False, False)
arr93_coeffs, arr93_difference = Df.detector_time_fit(arr93, False, False)
arr94_coeffs, arr94_difference = Df.detector_time_fit(arr94, False, False)
arr95_coeffs, arr95_difference = Df.detector_time_fit(arr95, False, False)
arr96_coeffs, arr96_difference = Df.detector_time_fit(arr96, False, False)
arr97_coeffs, arr97_difference = Df.detector_time_fit(arr97, False, False)
arr98_coeffs, arr98_difference = Df.detector_time_fit(arr98, False, False)
arr99_coeffs, arr99_difference = Df.detector_time_fit(arr99, False, False)


print("Detector Fits Done in {} s".format(timer() - Fit_Start))


Coincidence_Start = timer()
Coincidence_Start01 = timer()
fCo04 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr4, arr0_coeffs, arr4_coeffs, arr0_difference, arr4_difference)
print("Coincidence 04 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo05 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr5, arr0_coeffs, arr5_coeffs, arr0_difference, arr5_difference)
print("Coincidence 05 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo06 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr6, arr0_coeffs, arr6_coeffs, arr0_difference, arr6_difference)
print("Coincidence 06 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo07 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr7, arr0_coeffs, arr7_coeffs, arr0_difference, arr7_difference)
print("Coincidence 07 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo08 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr8, arr0_coeffs, arr8_coeffs, arr0_difference, arr8_difference)
print("Coincidence 08 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo09 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr9, arr0_coeffs, arr9_coeffs, arr0_difference, arr9_difference)
print("Coincidence 09 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo010 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr10, arr0_coeffs, arr10_coeffs, arr0_difference, arr10_difference)
print("Coincidence 10 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo011 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr11, arr0_coeffs, arr11_coeffs, arr0_difference, arr11_difference)
print("Coincidence 11 done in {} s".format(timer()-Coincidence_Start01))


Coincidence_Start01 = timer()
fCo012 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr12, arr0_coeffs, arr12_coeffs, arr0_difference, arr12_difference)
print("Coincidence 12 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo013 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr13, arr0_coeffs, arr13_coeffs, arr0_difference, arr13_difference)
print("Coincidence 13 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo014 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr14, arr0_coeffs, arr14_coeffs, arr0_difference, arr14_difference)
print("Coincidence 14 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo015 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr15, arr0_coeffs, arr15_coeffs, arr0_difference, arr15_difference)
print("Coincidence 15 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo016 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr16, arr0_coeffs, arr16_coeffs, arr0_difference, arr16_difference)
print("Coincidence 16 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo017 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr17, arr0_coeffs, arr17_coeffs, arr0_difference, arr17_difference)
print("Coincidence 17 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo018 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr18, arr0_coeffs, arr18_coeffs, arr0_difference, arr18_difference)
print("Coincidence 18 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo019 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr19, arr0_coeffs, arr19_coeffs, arr0_difference, arr19_difference)
print("Coincidence 19 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo020 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr20, arr0_coeffs, arr20_coeffs, arr0_difference, arr20_difference)
print("Coincidence 20 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo021 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr21, arr0_coeffs, arr21_coeffs, arr0_difference, arr21_difference)
print("Coincidence 21 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo022 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr22, arr0_coeffs, arr22_coeffs, arr0_difference, arr22_difference)
print("Coincidence 22 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo023 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr23, arr0_coeffs, arr23_coeffs, arr0_difference, arr23_difference)
print("Coincidence 23 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo024 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr24, arr0_coeffs, arr24_coeffs, arr0_difference, arr24_difference)
print("Coincidence 24 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo025 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr25, arr0_coeffs, arr25_coeffs, arr0_difference, arr25_difference)
print("Coincidence 25 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo026 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr26, arr0_coeffs, arr26_coeffs, arr0_difference, arr26_difference)
print("Coincidence 26 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo027 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr27, arr0_coeffs, arr27_coeffs, arr0_difference, arr27_difference)
print("Coincidence 27 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo028 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr28, arr0_coeffs, arr28_coeffs, arr0_difference, arr28_difference)
print("Coincidence 28 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo029 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr29, arr0_coeffs, arr29_coeffs, arr0_difference, arr29_difference)
print("Coincidence 29 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo030 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr30, arr0_coeffs, arr30_coeffs, arr0_difference, arr30_difference)
print("Coincidence 30 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo031 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr31, arr0_coeffs, arr31_coeffs, arr0_difference, arr31_difference)
print("Coincidence 31 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo032 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr32, arr0_coeffs, arr32_coeffs, arr0_difference, arr32_difference)
print("Coincidence 32 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo033 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr33, arr0_coeffs, arr33_coeffs, arr0_difference, arr33_difference)
print("Coincidence 33 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo034 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr34, arr0_coeffs, arr34_coeffs, arr0_difference, arr34_difference)
print("Coincidence 34 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo035 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr35, arr0_coeffs, arr35_coeffs, arr0_difference, arr35_difference)
print("Coincidence 35 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo036 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr36, arr0_coeffs, arr36_coeffs, arr0_difference, arr36_difference)
print("Coincidence 36 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo037 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr37, arr0_coeffs, arr37_coeffs, arr0_difference, arr37_difference)
print("Coincidence 37 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo038 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr38, arr0_coeffs, arr38_coeffs, arr0_difference, arr38_difference)
print("Coincidence 38 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo039 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr39, arr0_coeffs, arr36_coeffs, arr0_difference, arr39_difference)
print("Coincidence 39 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo040 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr40, arr0_coeffs, arr40_coeffs, arr0_difference, arr40_difference)
print("Coincidence 40 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo041 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr41, arr0_coeffs, arr41_coeffs, arr0_difference, arr41_difference)
print("Coincidence 41 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo042 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr42, arr0_coeffs, arr42_coeffs, arr0_difference, arr42_difference)
print("Coincidence 42 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo043 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr43, arr0_coeffs, arr43_coeffs, arr0_difference, arr43_difference)
print("Coincidence 43 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo044 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr44, arr0_coeffs, arr44_coeffs, arr0_difference, arr44_difference)
print("Coincidence 44 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo045 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr45, arr0_coeffs, arr45_coeffs, arr0_difference, arr45_difference)
print("Coincidence 45 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo046 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr46, arr0_coeffs, arr46_coeffs, arr0_difference, arr46_difference)
print("Coincidence 46 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo047 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr47, arr0_coeffs, arr47_coeffs, arr0_difference, arr47_difference)
print("Coincidence 47 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo048 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr48, arr0_coeffs, arr48_coeffs, arr0_difference, arr48_difference)
print("Coincidence 48 done in {} s".format(timer()-Coincidence_Start01))

# Coincidence_Start01 = timer()
# fCo049 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr49, arr0_coeffs, arr49_coeffs, arr0_difference, arr49_difference)
# print("Coincidence 49 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo050 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr50, arr0_coeffs, arr50_coeffs, arr0_difference, arr50_difference)
print("Coincidence 50 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo051 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr51, arr0_coeffs, arr51_coeffs, arr0_difference, arr51_difference)
print("Coincidence 51 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo052 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr52, arr0_coeffs, arr52_coeffs, arr0_difference, arr52_difference)
print("Coincidence 52 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo053 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr53, arr0_coeffs, arr53_coeffs, arr0_difference, arr53_difference)
print("Coincidence 53 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo054 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr54, arr0_coeffs, arr54_coeffs, arr0_difference, arr54_difference)
print("Coincidence 54 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo055 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr55, arr0_coeffs, arr55_coeffs, arr0_difference, arr55_difference)
print("Coincidence 55 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo056 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr56, arr0_coeffs, arr56_coeffs, arr0_difference, arr56_difference)
print("Coincidence 56 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo057 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr57, arr0_coeffs, arr57_coeffs, arr0_difference, arr57_difference)
print("Coincidence 57 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo058 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr58, arr0_coeffs, arr58_coeffs, arr0_difference, arr58_difference)
print("Coincidence 58 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo059 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr59, arr0_coeffs, arr59_coeffs, arr0_difference, arr59_difference)
print("Coincidence 59 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo060 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr60, arr0_coeffs, arr60_coeffs, arr0_difference, arr60_difference)
print("Coincidence 60 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo061 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr61, arr0_coeffs, arr61_coeffs, arr0_difference, arr61_difference)
print("Coincidence 61 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo062 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr62, arr0_coeffs, arr62_coeffs, arr0_difference, arr62_difference)
print("Coincidence 62 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo063 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr63, arr0_coeffs, arr63_coeffs, arr0_difference, arr63_difference)
print("Coincidence 63 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo064 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr64, arr0_coeffs, arr64_coeffs, arr0_difference, arr64_difference)
print("Coincidence 64 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo065 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr65, arr0_coeffs, arr65_coeffs, arr0_difference, arr65_difference)
print("Coincidence 65 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo066 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr66, arr0_coeffs, arr66_coeffs, arr0_difference, arr66_difference)
print("Coincidence 66 done in {} s".format(timer()-Coincidence_Start01))


Coincidence_Start01 = timer()
fCo067 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr67, arr0_coeffs, arr67_coeffs, arr0_difference, arr67_difference)
print("Coincidence 67 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo068 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr68, arr0_coeffs, arr68_coeffs, arr0_difference, arr68_difference)
print("Coincidence 68 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo069 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr69, arr0_coeffs, arr69_coeffs, arr0_difference, arr69_difference)
print("Coincidence 69 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo070 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr70, arr0_coeffs, arr70_coeffs, arr0_difference, arr70_difference)
print("Coincidence 70 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo071 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr71, arr0_coeffs, arr71_coeffs, arr0_difference, arr71_difference)
print("Coincidence 71 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo072 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr72, arr0_coeffs, arr72_coeffs, arr0_difference, arr72_difference)
print("Coincidence 72 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo073 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr73, arr0_coeffs, arr73_coeffs, arr0_difference, arr73_difference)
print("Coincidence 73 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo074 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr74, arr0_coeffs, arr74_coeffs, arr0_difference, arr74_difference)
print("Coincidence 74 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo075 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr75, arr0_coeffs, arr75_coeffs, arr0_difference, arr75_difference)
print("Coincidence 75 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo076 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr76, arr0_coeffs, arr76_coeffs, arr0_difference, arr76_difference)
print("Coincidence 76 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo077 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr77, arr0_coeffs, arr77_coeffs, arr0_difference, arr77_difference)
print("Coincidence 77 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo078 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr78, arr0_coeffs, arr78_coeffs, arr0_difference, arr78_difference)
print("Coincidence 78 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo079 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr79, arr0_coeffs, arr79_coeffs, arr0_difference, arr79_difference)
print("Coincidence 79 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo080 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr80, arr0_coeffs, arr80_coeffs, arr0_difference, arr80_difference)
print("Coincidence 80 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo081 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr81, arr0_coeffs, arr81_coeffs, arr0_difference, arr81_difference)
print("Coincidence 81 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo082 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr82, arr0_coeffs, arr82_coeffs, arr0_difference, arr82_difference)
print("Coincidence 82 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo083 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr83, arr0_coeffs, arr83_coeffs, arr0_difference, arr83_difference)
print("Coincidence 83 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo084 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr84, arr0_coeffs, arr84_coeffs, arr0_difference, arr84_difference)
print("Coincidence 84 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo085 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr85, arr0_coeffs, arr85_coeffs, arr0_difference, arr85_difference)
print("Coincidence 85 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo086 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr86, arr0_coeffs, arr86_coeffs, arr0_difference, arr86_difference)
print("Coincidence 86 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo087 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr87, arr0_coeffs, arr87_coeffs, arr0_difference, arr87_difference)
print("Coincidence 87 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo088 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr88, arr0_coeffs, arr88_coeffs, arr0_difference, arr88_difference)
print("Coincidence 88 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo089 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr89, arr0_coeffs, arr89_coeffs, arr0_difference, arr89_difference)
print("Coincidence 89 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo090 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr90, arr0_coeffs, arr90_coeffs, arr0_difference, arr90_difference)
print("Coincidence 90 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo091 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr91, arr0_coeffs, arr91_coeffs, arr0_difference, arr91_difference)
print("Coincidence 91 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo092 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr92, arr0_coeffs, arr92_coeffs, arr0_difference, arr92_difference)
print("Coincidence 92 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo093 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr93, arr0_coeffs, arr93_coeffs, arr0_difference, arr93_difference)
print("Coincidence 93 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo094 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr94, arr0_coeffs, arr94_coeffs, arr0_difference, arr94_difference)
print("Coincidence 94 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo095 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr95, arr0_coeffs, arr95_coeffs, arr0_difference, arr95_difference)
print("Coincidence 95 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo096 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr96, arr0_coeffs, arr96_coeffs, arr0_difference, arr96_difference)
print("Coincidence 96 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo097 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr97, arr0_coeffs, arr97_coeffs, arr0_difference, arr97_difference)
print("Coincidence 97 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo098 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr98, arr0_coeffs, arr98_coeffs, arr0_difference, arr98_difference)
print("Coincidence 98 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo099 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr99, arr0_coeffs, arr99_coeffs, arr0_difference, arr99_difference)
print("Coincidence 99 done in {} s".format(timer()-Coincidence_Start01))





# Coincidence_Start11 = timer()
# fCo14 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr4, arr1_coeffs, arr4_coeffs, arr1_difference, arr4_difference)
# print("Coincidence 14 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo15 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr5, arr1_coeffs, arr5_coeffs, arr1_difference, arr5_difference)
print("Coincidence 15 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo16 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr6, arr1_coeffs, arr6_coeffs, arr1_difference, arr6_difference)
print("Coincidence 16 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo17 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr7, arr1_coeffs, arr7_coeffs, arr1_difference, arr7_difference)
print("Coincidence 17 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo18 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr8, arr1_coeffs, arr8_coeffs, arr1_difference, arr8_difference)
print("Coincidence 18 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo19 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr9, arr1_coeffs, arr9_coeffs, arr1_difference, arr9_difference)
print("Coincidence 19 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo110 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr10, arr1_coeffs, arr10_coeffs, arr1_difference, arr10_difference)
print("Coincidence 11 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo111 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr11, arr1_coeffs, arr11_coeffs, arr1_difference, arr11_difference)
# print("Coincidence 11 done in {} s".format(timer()-Coincidence_Start11))


Coincidence_Start11 = timer()
fCo112 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr12, arr1_coeffs, arr12_coeffs, arr1_difference, arr12_difference)
print("Coincidence 12 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo113 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr13, arr1_coeffs, arr13_coeffs, arr1_difference, arr13_difference)
print("Coincidence 13 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo114 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr14, arr1_coeffs, arr14_coeffs, arr1_difference, arr14_difference)
print("Coincidence 14 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo115 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr15, arr1_coeffs, arr15_coeffs, arr1_difference, arr15_difference)
print("Coincidence 15 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo116 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr16, arr1_coeffs, arr16_coeffs, arr1_difference, arr16_difference)
print("Coincidence 16 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo117 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr17, arr1_coeffs, arr17_coeffs, arr1_difference, arr17_difference)
# print("Coincidence 17 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo118 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr18, arr1_coeffs, arr18_coeffs, arr1_difference, arr18_difference)
print("Coincidence 18 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo119 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr19, arr1_coeffs, arr19_coeffs, arr1_difference, arr19_difference)
print("Coincidence 19 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo120 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr20, arr1_coeffs, arr20_coeffs, arr1_difference, arr20_difference)
print("Coincidence 21 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo121 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr21, arr1_coeffs, arr21_coeffs, arr1_difference, arr21_difference)
print("Coincidence 21 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo122 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr22, arr1_coeffs, arr22_coeffs, arr1_difference, arr22_difference)
print("Coincidence 22 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo123 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr23, arr1_coeffs, arr23_coeffs, arr1_difference, arr23_difference)
print("Coincidence 23 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo124 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr24, arr1_coeffs, arr24_coeffs, arr1_difference, arr24_difference)
# print("Coincidence 24 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo125 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr25, arr1_coeffs, arr25_coeffs, arr1_difference, arr25_difference)
print("Coincidence 25 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo126 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr26, arr1_coeffs, arr26_coeffs, arr1_difference, arr26_difference)
print("Coincidence 26 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo127 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr27, arr1_coeffs, arr27_coeffs, arr1_difference, arr27_difference)
print("Coincidence 27 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo128 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr28, arr1_coeffs, arr28_coeffs, arr1_difference, arr28_difference)
print("Coincidence 28 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo129 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr29, arr1_coeffs, arr29_coeffs, arr1_difference, arr29_difference)
print("Coincidence 29 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo130 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr30, arr1_coeffs, arr30_coeffs, arr1_difference, arr30_difference)
print("Coincidence 31 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo131 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr31, arr1_coeffs, arr31_coeffs, arr1_difference, arr31_difference)
# print("Coincidence 31 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo131 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr31, arr1_coeffs, arr31_coeffs, arr1_difference, arr31_difference)
print("Coincidence 31 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo132 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr32, arr1_coeffs, arr32_coeffs, arr1_difference, arr32_difference)
print("Coincidence 32 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo133 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr33, arr1_coeffs, arr33_coeffs, arr1_difference, arr33_difference)
print("Coincidence 33 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo134 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr34, arr1_coeffs, arr34_coeffs, arr1_difference, arr34_difference)
print("Coincidence 34 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo135 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr35, arr1_coeffs, arr35_coeffs, arr1_difference, arr35_difference)
print("Coincidence 35 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo136 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr36, arr1_coeffs, arr36_coeffs, arr1_difference, arr36_difference)
print("Coincidence 36 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo137 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr37, arr1_coeffs, arr37_coeffs, arr1_difference, arr37_difference)
print("Coincidence 37 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo138 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr38, arr1_coeffs, arr38_coeffs, arr1_difference, arr38_difference)
# print("Coincidence 38 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo139 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr39, arr1_coeffs, arr36_coeffs, arr1_difference, arr39_difference)
print("Coincidence 39 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo140 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr40, arr1_coeffs, arr40_coeffs, arr1_difference, arr40_difference)
print("Coincidence 41 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo141 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr41, arr1_coeffs, arr41_coeffs, arr1_difference, arr41_difference)
print("Coincidence 41 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo142 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr42, arr1_coeffs, arr42_coeffs, arr1_difference, arr42_difference)
# print("Coincidence 42 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo143 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr43, arr1_coeffs, arr43_coeffs, arr1_difference, arr43_difference)
print("Coincidence 43 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo144 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr44, arr1_coeffs, arr44_coeffs, arr1_difference, arr44_difference)
print("Coincidence 44 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo145 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr45, arr1_coeffs, arr45_coeffs, arr1_difference, arr45_difference)
print("Coincidence 45 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo146 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr46, arr1_coeffs, arr46_coeffs, arr1_difference, arr46_difference)
# print("Coincidence 46 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo147 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr47, arr1_coeffs, arr47_coeffs, arr1_difference, arr47_difference)
print("Coincidence 47 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo148 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr48, arr1_coeffs, arr48_coeffs, arr1_difference, arr48_difference)
print("Coincidence 48 done in {} s".format(timer()-Coincidence_Start11))

# Coincidence_Start11 = timer()
# fCo149 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr49, arr1_coeffs, arr49_coeffs, arr1_difference, arr49_difference)
# print("Coincidence 49 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo150 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr51, arr1_coeffs, arr50_coeffs, arr1_difference, arr50_difference)
print("Coincidence 50 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start11 = timer()
fCo151 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr51, arr1_coeffs, arr51_coeffs, arr1_difference, arr51_difference)
print("Coincidence 51 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo152 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr52, arr1_coeffs, arr52_coeffs, arr1_difference, arr52_difference)
print("Coincidence 52 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo153 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr53, arr1_coeffs, arr53_coeffs, arr1_difference, arr53_difference)
print("Coincidence 53 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo154 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr54, arr1_coeffs, arr54_coeffs, arr1_difference, arr54_difference)
print("Coincidence 54 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo155 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr55, arr1_coeffs, arr55_coeffs, arr1_difference, arr55_difference)
print("Coincidence 55 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo156 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr56, arr1_coeffs, arr56_coeffs, arr1_difference, arr56_difference)
print("Coincidence 56 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo157 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr57, arr1_coeffs, arr57_coeffs, arr1_difference, arr57_difference)
print("Coincidence 57 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo158 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr58, arr1_coeffs, arr58_coeffs, arr1_difference, arr58_difference)
print("Coincidence 58 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo159 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr59, arr1_coeffs, arr59_coeffs, arr1_difference, arr59_difference)
print("Coincidence 59 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo160 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr60, arr1_coeffs, arr60_coeffs, arr1_difference, arr60_difference)
print("Coincidence 60 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start11 = timer()
fCo161 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr61, arr1_coeffs, arr61_coeffs, arr1_difference, arr61_difference)
print("Coincidence 61 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo162 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr62, arr1_coeffs, arr62_coeffs, arr1_difference, arr62_difference)
print("Coincidence 62 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo163 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr63, arr1_coeffs, arr63_coeffs, arr1_difference, arr63_difference)
print("Coincidence 63 done in {} s".format(timer()-Coincidence_Start11))

Coincidence_Start11 = timer()
fCo164 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr64, arr1_coeffs, arr64_coeffs, arr1_difference, arr64_difference)
print("Coincidence 64 done in {} s".format(timer()-Coincidence_Start11))


Coincidence_Start01 = timer()
fCo165 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr65, arr1_coeffs, arr65_coeffs, arr1_difference, arr65_difference)
print("Coincidence 65 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo166 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr66, arr1_coeffs, arr66_coeffs, arr1_difference, arr66_difference)
print("Coincidence 66 done in {} s".format(timer()-Coincidence_Start01))


Coincidence_Start01 = timer()
fCo167 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr67, arr1_coeffs, arr67_coeffs, arr1_difference, arr67_difference)
print("Coincidence 67 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo168 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr68, arr1_coeffs, arr68_coeffs, arr1_difference, arr68_difference)
print("Coincidence 68 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo169 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr69, arr1_coeffs, arr69_coeffs, arr1_difference, arr69_difference)
print("Coincidence 69 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo170 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr70, arr1_coeffs, arr70_coeffs, arr1_difference, arr70_difference)
print("Coincidence 70 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo171 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr71, arr1_coeffs, arr71_coeffs, arr1_difference, arr71_difference)
print("Coincidence 71 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo172 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr72, arr1_coeffs, arr72_coeffs, arr1_difference, arr72_difference)
print("Coincidence 72 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo173 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr73, arr1_coeffs, arr73_coeffs, arr1_difference, arr73_difference)
print("Coincidence 73 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo174 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr74, arr1_coeffs, arr74_coeffs, arr1_difference, arr74_difference)
print("Coincidence 74 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo175 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr75, arr1_coeffs, arr75_coeffs, arr1_difference, arr75_difference)
print("Coincidence 75 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo176 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr76, arr1_coeffs, arr76_coeffs, arr1_difference, arr76_difference)
print("Coincidence 76 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo177 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr77, arr1_coeffs, arr77_coeffs, arr1_difference, arr77_difference)
print("Coincidence 77 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo178 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr78, arr1_coeffs, arr78_coeffs, arr1_difference, arr78_difference)
print("Coincidence 78 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo179 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr79, arr1_coeffs, arr79_coeffs, arr1_difference, arr79_difference)
print("Coincidence 79 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo180 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr80, arr1_coeffs, arr80_coeffs, arr1_difference, arr80_difference)
print("Coincidence 80 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo181 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr81, arr1_coeffs, arr81_coeffs, arr1_difference, arr81_difference)
print("Coincidence 81 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo182 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr82, arr1_coeffs, arr82_coeffs, arr1_difference, arr82_difference)
print("Coincidence 82 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo183 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr83, arr1_coeffs, arr83_coeffs, arr1_difference, arr83_difference)
print("Coincidence 83 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo184 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr84, arr1_coeffs, arr84_coeffs, arr1_difference, arr84_difference)
print("Coincidence 84 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo185 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr85, arr1_coeffs, arr85_coeffs, arr1_difference, arr85_difference)
print("Coincidence 85 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo186 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr86, arr1_coeffs, arr86_coeffs, arr1_difference, arr86_difference)
print("Coincidence 86 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo187 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr87, arr1_coeffs, arr87_coeffs, arr1_difference, arr87_difference)
print("Coincidence 87 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo188 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr88, arr1_coeffs, arr88_coeffs, arr1_difference, arr88_difference)
print("Coincidence 88 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo189 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr89, arr1_coeffs, arr89_coeffs, arr1_difference, arr89_difference)
print("Coincidence 89 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo190 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr90, arr1_coeffs, arr90_coeffs, arr1_difference, arr90_difference)
print("Coincidence 90 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo191 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr91, arr1_coeffs, arr91_coeffs, arr1_difference, arr91_difference)
print("Coincidence 91 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo192 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr92, arr1_coeffs, arr92_coeffs, arr1_difference, arr92_difference)
print("Coincidence 92 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo193 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr93, arr1_coeffs, arr93_coeffs, arr1_difference, arr93_difference)
print("Coincidence 93 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo194 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr94, arr1_coeffs, arr94_coeffs, arr1_difference, arr94_difference)
print("Coincidence 94 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo195 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr95, arr1_coeffs, arr95_coeffs, arr1_difference, arr95_difference)
print("Coincidence 95 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo196 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr96, arr1_coeffs, arr96_coeffs, arr1_difference, arr96_difference)
print("Coincidence 96 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo197 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr97, arr1_coeffs, arr97_coeffs, arr1_difference, arr97_difference)
print("Coincidence 97 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo198 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr98, arr1_coeffs, arr98_coeffs, arr1_difference, arr98_difference)
print("Coincidence 98 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo199 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr99, arr1_coeffs, arr99_coeffs, arr1_difference, arr99_difference)
print("Coincidence 99 done in {} s".format(timer()-Coincidence_Start01))





Coincidence_Start = timer()
Coincidence_Start01 = timer()
fCo24 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr4, arr2_coeffs, arr4_coeffs, arr2_difference, arr4_difference)
print("Coincidence 04 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo25 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr5, arr2_coeffs, arr5_coeffs, arr2_difference, arr5_difference)
print("Coincidence 05 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo26 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr6, arr2_coeffs, arr6_coeffs, arr2_difference, arr6_difference)
print("Coincidence 06 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo27 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr7, arr2_coeffs, arr7_coeffs, arr2_difference, arr7_difference)
print("Coincidence 07 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo28 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr8, arr2_coeffs, arr8_coeffs, arr2_difference, arr8_difference)
print("Coincidence 08 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo29 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr9, arr2_coeffs, arr9_coeffs, arr2_difference, arr9_difference)
print("Coincidence 09 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo210 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr10, arr2_coeffs, arr10_coeffs, arr2_difference, arr10_difference)
print("Coincidence 10 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo211 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr11, arr2_coeffs, arr11_coeffs, arr2_difference, arr11_difference)
print("Coincidence 11 done in {} s".format(timer()-Coincidence_Start01))


Coincidence_Start01 = timer()
fCo212 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr12, arr2_coeffs, arr12_coeffs, arr2_difference, arr12_difference)
print("Coincidence 12 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo213 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr13, arr2_coeffs, arr13_coeffs, arr2_difference, arr13_difference)
print("Coincidence 13 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo214 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr14, arr2_coeffs, arr14_coeffs, arr2_difference, arr14_difference)
print("Coincidence 14 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo215 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr15, arr2_coeffs, arr15_coeffs, arr2_difference, arr15_difference)
print("Coincidence 15 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo216 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr16, arr2_coeffs, arr16_coeffs, arr2_difference, arr16_difference)
print("Coincidence 16 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo217 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr17, arr2_coeffs, arr17_coeffs, arr2_difference, arr17_difference)
print("Coincidence 17 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo218 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr18, arr2_coeffs, arr18_coeffs, arr2_difference, arr18_difference)
print("Coincidence 18 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo219 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr19, arr2_coeffs, arr19_coeffs, arr2_difference, arr19_difference)
print("Coincidence 19 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo220 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr20, arr2_coeffs, arr20_coeffs, arr2_difference, arr20_difference)
print("Coincidence 20 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo221 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr21, arr2_coeffs, arr21_coeffs, arr2_difference, arr21_difference)
print("Coincidence 21 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo222 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr22, arr2_coeffs, arr22_coeffs, arr2_difference, arr22_difference)
print("Coincidence 22 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo223 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr23, arr2_coeffs, arr23_coeffs, arr2_difference, arr23_difference)
print("Coincidence 23 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo224 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr24, arr2_coeffs, arr24_coeffs, arr2_difference, arr24_difference)
print("Coincidence 24 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo225 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr25, arr2_coeffs, arr25_coeffs, arr2_difference, arr25_difference)
print("Coincidence 25 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo226 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr26, arr2_coeffs, arr26_coeffs, arr2_difference, arr26_difference)
print("Coincidence 26 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo227 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr27, arr2_coeffs, arr27_coeffs, arr2_difference, arr27_difference)
print("Coincidence 27 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo228 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr28, arr2_coeffs, arr28_coeffs, arr2_difference, arr28_difference)
print("Coincidence 28 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo229 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr29, arr2_coeffs, arr29_coeffs, arr2_difference, arr29_difference)
print("Coincidence 29 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo230 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr30, arr2_coeffs, arr30_coeffs, arr2_difference, arr30_difference)
print("Coincidence 30 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo231 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr31, arr2_coeffs, arr31_coeffs, arr2_difference, arr31_difference)
print("Coincidence 31 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo232 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr32, arr2_coeffs, arr32_coeffs, arr2_difference, arr32_difference)
print("Coincidence 32 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo233 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr33, arr2_coeffs, arr33_coeffs, arr2_difference, arr33_difference)
print("Coincidence 33 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo234 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr34, arr2_coeffs, arr34_coeffs, arr2_difference, arr34_difference)
print("Coincidence 34 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo235 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr35, arr2_coeffs, arr35_coeffs, arr2_difference, arr35_difference)
print("Coincidence 35 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo236 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr36, arr2_coeffs, arr36_coeffs, arr2_difference, arr36_difference)
print("Coincidence 36 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo237 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr37, arr2_coeffs, arr37_coeffs, arr2_difference, arr37_difference)
print("Coincidence 37 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo238 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr38, arr2_coeffs, arr38_coeffs, arr2_difference, arr38_difference)
print("Coincidence 38 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo239 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr39, arr2_coeffs, arr36_coeffs, arr2_difference, arr39_difference)
print("Coincidence 39 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo240 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr40, arr2_coeffs, arr40_coeffs, arr2_difference, arr40_difference)
print("Coincidence 40 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo241 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr41, arr2_coeffs, arr41_coeffs, arr2_difference, arr41_difference)
print("Coincidence 41 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo242 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr42, arr2_coeffs, arr42_coeffs, arr2_difference, arr42_difference)
print("Coincidence 42 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo243 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr43, arr2_coeffs, arr43_coeffs, arr2_difference, arr43_difference)
print("Coincidence 43 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo244 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr44, arr2_coeffs, arr44_coeffs, arr2_difference, arr44_difference)
print("Coincidence 44 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo245 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr45, arr2_coeffs, arr45_coeffs, arr2_difference, arr45_difference)
print("Coincidence 45 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo246 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr46, arr2_coeffs, arr46_coeffs, arr2_difference, arr46_difference)
print("Coincidence 46 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo247 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr47, arr2_coeffs, arr47_coeffs, arr2_difference, arr47_difference)
print("Coincidence 47 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo248 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr48, arr2_coeffs, arr48_coeffs, arr2_difference, arr48_difference)
print("Coincidence 48 done in {} s".format(timer()-Coincidence_Start01))

# Coincidence_Start01 = timer()
# fCo249 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr49, arr2_coeffs, arr49_coeffs, arr2_difference, arr49_difference)
# print("Coincidence 49 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo250 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr50, arr2_coeffs, arr50_coeffs, arr2_difference, arr50_difference)
print("Coincidence 50 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo251 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr51, arr2_coeffs, arr51_coeffs, arr2_difference, arr51_difference)
print("Coincidence 51 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo252 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr52, arr2_coeffs, arr52_coeffs, arr2_difference, arr52_difference)
print("Coincidence 52 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo253 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr53, arr2_coeffs, arr53_coeffs, arr2_difference, arr53_difference)
print("Coincidence 53 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo254 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr54, arr2_coeffs, arr54_coeffs, arr2_difference, arr54_difference)
print("Coincidence 54 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo255 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr55, arr2_coeffs, arr55_coeffs, arr2_difference, arr55_difference)
print("Coincidence 55 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo256 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr56, arr2_coeffs, arr56_coeffs, arr2_difference, arr56_difference)
print("Coincidence 56 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo257 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr57, arr2_coeffs, arr57_coeffs, arr2_difference, arr57_difference)
print("Coincidence 57 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo258 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr58, arr2_coeffs, arr58_coeffs, arr2_difference, arr58_difference)
print("Coincidence 58 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo259 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr59, arr2_coeffs, arr59_coeffs, arr2_difference, arr59_difference)
print("Coincidence 59 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo260 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr60, arr2_coeffs, arr60_coeffs, arr2_difference, arr60_difference)
print("Coincidence 60 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo261 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr61, arr2_coeffs, arr61_coeffs, arr2_difference, arr61_difference)
print("Coincidence 61 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo262 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr62, arr2_coeffs, arr62_coeffs, arr2_difference, arr62_difference)
print("Coincidence 62 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo263 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr63, arr2_coeffs, arr63_coeffs, arr2_difference, arr63_difference)
print("Coincidence 63 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo264 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr64, arr2_coeffs, arr64_coeffs, arr2_difference, arr64_difference)
print("Coincidence 64 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo265 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr65, arr2_coeffs, arr65_coeffs, arr2_difference, arr65_difference)
print("Coincidence 65 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo266 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr66, arr2_coeffs, arr66_coeffs, arr2_difference, arr66_difference)
print("Coincidence 66 done in {} s".format(timer()-Coincidence_Start01))


Coincidence_Start01 = timer()
fCo267 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr67, arr2_coeffs, arr67_coeffs, arr2_difference, arr67_difference)
print("Coincidence 67 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo268 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr68, arr2_coeffs, arr68_coeffs, arr2_difference, arr68_difference)
print("Coincidence 68 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo269 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr69, arr2_coeffs, arr69_coeffs, arr2_difference, arr69_difference)
print("Coincidence 69 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo270 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr70, arr2_coeffs, arr70_coeffs, arr2_difference, arr70_difference)
print("Coincidence 70 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo271 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr71, arr2_coeffs, arr71_coeffs, arr2_difference, arr71_difference)
print("Coincidence 71 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo272 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr72, arr2_coeffs, arr72_coeffs, arr2_difference, arr72_difference)
print("Coincidence 72 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo273 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr73, arr2_coeffs, arr73_coeffs, arr2_difference, arr73_difference)
print("Coincidence 73 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo274 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr74, arr2_coeffs, arr74_coeffs, arr2_difference, arr74_difference)
print("Coincidence 74 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo275 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr75, arr2_coeffs, arr75_coeffs, arr2_difference, arr75_difference)
print("Coincidence 75 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo276 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr76, arr2_coeffs, arr76_coeffs, arr2_difference, arr76_difference)
print("Coincidence 76 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo277 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr77, arr2_coeffs, arr77_coeffs, arr2_difference, arr77_difference)
print("Coincidence 77 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo278 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr78, arr2_coeffs, arr78_coeffs, arr2_difference, arr78_difference)
print("Coincidence 78 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo279 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr79, arr2_coeffs, arr79_coeffs, arr2_difference, arr79_difference)
print("Coincidence 79 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo280 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr80, arr2_coeffs, arr80_coeffs, arr2_difference, arr80_difference)
print("Coincidence 80 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo281 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr81, arr2_coeffs, arr81_coeffs, arr2_difference, arr81_difference)
print("Coincidence 81 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo282 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr82, arr2_coeffs, arr82_coeffs, arr2_difference, arr82_difference)
print("Coincidence 82 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo283 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr83, arr2_coeffs, arr83_coeffs, arr2_difference, arr83_difference)
print("Coincidence 83 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo284 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr84, arr2_coeffs, arr84_coeffs, arr2_difference, arr84_difference)
print("Coincidence 84 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo285 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr85, arr2_coeffs, arr85_coeffs, arr2_difference, arr85_difference)
print("Coincidence 85 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo286 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr86, arr2_coeffs, arr86_coeffs, arr2_difference, arr86_difference)
print("Coincidence 86 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo287 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr87, arr2_coeffs, arr87_coeffs, arr2_difference, arr87_difference)
print("Coincidence 87 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo288 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr88, arr2_coeffs, arr88_coeffs, arr2_difference, arr88_difference)
print("Coincidence 88 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo289 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr89, arr2_coeffs, arr89_coeffs, arr2_difference, arr89_difference)
print("Coincidence 89 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo290 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr90, arr2_coeffs, arr90_coeffs, arr2_difference, arr90_difference)
print("Coincidence 90 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo291 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr91, arr2_coeffs, arr91_coeffs, arr2_difference, arr91_difference)
print("Coincidence 91 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo292 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr92, arr2_coeffs, arr92_coeffs, arr2_difference, arr92_difference)
print("Coincidence 92 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo293 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr93, arr2_coeffs, arr93_coeffs, arr2_difference, arr93_difference)
print("Coincidence 93 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo294 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr94, arr2_coeffs, arr94_coeffs, arr2_difference, arr94_difference)
print("Coincidence 94 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo295 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr95, arr2_coeffs, arr95_coeffs, arr2_difference, arr95_difference)
print("Coincidence 95 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo296 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr96, arr2_coeffs, arr96_coeffs, arr2_difference, arr96_difference)
print("Coincidence 96 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo297 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr97, arr2_coeffs, arr97_coeffs, arr2_difference, arr97_difference)
print("Coincidence 97 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo298 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr98, arr2_coeffs, arr98_coeffs, arr2_difference, arr98_difference)
print("Coincidence 98 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo299 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr99, arr2_coeffs, arr99_coeffs, arr2_difference, arr99_difference)
print("Coincidence 99 done in {} s".format(timer()-Coincidence_Start01))







# Slicing arrays due to data size
# array_reducing_factor = 1

# fCo04 = fCo04[:int(fCo04.shape[0]/array_reducing_factor)]
# fCo05 = fCo05[:int(fCo05.shape[0]/array_reducing_factor)]
# fCo06 = fCo06[:int(fCo06.shape[0]/array_reducing_factor)]
# fCo07 = fCo07[:int(fCo07.shape[0]/array_reducing_factor)]
# fCo14 = fCo14[:int(fCo14.shape[0]/array_reducing_factor)]
# fCo15 = fCo15[:int(fCo15.shape[0]/array_reducing_factor)]
# fCo16 = fCo16[:int(fCo16.shape[0]/array_reducing_factor)]
# fCo17 = fCo17[:int(fCo17.shape[0]/array_reducing_factor)]
# fCo24 = fCo24[:int(fCo24.shape[0]/array_reducing_factor)]
# fCo25 = fCo25[:int(fCo25.shape[0]/array_reducing_factor)]
# fCo26 = fCo26[:int(fCo26.shape[0]/array_reducing_factor)]
# fCo27 = fCo27[:int(fCo27.shape[0]/array_reducing_factor)]
# fCo34 = fCo34[:int(fCo34.shape[0]/array_reducing_factor)]
# fCo35 = fCo35[:int(fCo35.shape[0]/array_reducing_factor)]
# fCo36 = fCo36[:int(fCo36.shape[0]/array_reducing_factor)]
# fCo37 = fCo37[:int(fCo37.shape[0]/array_reducing_factor)]





# fCo = np.vstack((fCo1, fCo2, fCo3, fCo4, fCo5, fCo6))
# fCo = np.vstack((fCo04, fCo05, fCo06, fCo14, fCo15, fCo16, fCo24, fCo25, fCo26, fCo34, fCo35, fCo36))

# fCo = np.vstack((fCo04, fCo05, fCo06, fCo07, fCo08, fCo09, fCo010, fCo011, fCo012, fCo013, fCo014, fCo015, fCo016, fCo017, fCo018, fCo019, fCo020, fCo021, fCo022, fCo023, fCo024, fCo025, fCo026, fCo027, fCo028, fCo029, fCo030, fCo031, fCo032, fCo033, fCo034, fCo035, fCo036, fCo037, fCo038, fCo039, fCo040, fCo041, fCo042, fCo043, fCo044, fCo045, fCo046, fCo047, fCo048, fCo050, fCo051, fCo052, fCo053, fCo054, fCo055, fCo056, fCo057, fCo058, fCo059, fCo060, fCo061, fCo062, fCo063, fCo064, fCo14, fCo15, fCo16, fCo17, fCo18, fCo19, fCo110, fCo111, fCo112, fCo113, fCo114, fCo115, fCo116, fCo117, fCo118, fCo119, fCo120, fCo121, fCo122, fCo123, fCo124, fCo125, fCo126, fCo127, fCo128, fCo129, fCo130, fCo131, fCo132, fCo133, fCo134, fCo135, fCo136, fCo137, fCo138, fCo139, fCo140, fCo141, fCo142, fCo143, fCo144, fCo145, fCo146, fCo147, fCo148, fCo150, fCo151, fCo152, fCo153, fCo154, fCo155, fCo156, fCo157, fCo158, fCo159, fCo160, fCo161, fCo162, fCo163, fCo164, fCo24, fCo25, fCo26, fCo27, fCo28, fCo29, fCo210, fCo211, fCo212, fCo213, fCo214, fCo215, fCo216, fCo217, fCo218, fCo219, fCo220, fCo221, fCo222, fCo223, fCo224, fCo225, fCo226, fCo227, fCo228, fCo229, fCo230, fCo231, fCo232, fCo233, fCo234, fCo235, fCo236, fCo237, fCo238, fCo239, fCo240, fCo241, fCo242, fCo243, fCo244, fCo245, fCo246, fCo247, fCo248, fCo249, fCo250, fCo251, fCo252, fCo253, fCo254, fCo255, fCo256, fCo257, fCo258, fCo259, fCo260, fCo261, fCo262, fCo263, fCo264))


fCo = np.vstack((fCo04, fCo05, fCo06, fCo07, fCo08, fCo09, fCo010, fCo011, fCo012, fCo013, fCo014, fCo015, fCo016, fCo017, fCo018, fCo019, fCo020, fCo021, fCo022, fCo023, fCo024, fCo025, fCo026, fCo027, fCo028, fCo029, fCo030, fCo031, fCo032, fCo033, fCo034, fCo035, fCo036, fCo037, fCo038, fCo039, fCo040, fCo041, fCo042, fCo043, fCo044, fCo045, fCo046, fCo047, fCo048, fCo050, fCo051, fCo052, fCo053, fCo054, fCo055, fCo056, fCo057, fCo058, fCo059, fCo060, fCo061, fCo062, fCo063, fCo064, fCo065, fCo066, fCo067, fCo068, fCo069, fCo070, fCo071, fCo072, fCo073, fCo074, fCo075, fCo076, fCo077, fCo078, fCo079, fCo080, fCo081, fCo082, fCo083, fCo084, fCo085, fCo086, fCo087, fCo088, fCo089, fCo090, fCo091, fCo092, fCo093, fCo094, fCo095, fCo096, fCo097, fCo098, fCo099, fCo15, fCo16, fCo17, fCo18, fCo19, fCo110, fCo112, fCo113, fCo114, fCo115, fCo116, fCo118, fCo119, fCo120, fCo121, fCo122, fCo123, fCo125, fCo126, fCo127, fCo128, fCo129, fCo130, fCo131, fCo132, fCo133, fCo134, fCo135, fCo136, fCo137, fCo139, fCo140, fCo141, fCo143, fCo144, fCo145, fCo147, fCo148, fCo150, fCo151, fCo152, fCo153, fCo154, fCo155, fCo156, fCo157, fCo158, fCo159, fCo160, fCo161, fCo162, fCo163, fCo164, fCo165, fCo166, fCo167, fCo168, fCo169, fCo170, fCo171, fCo172, fCo173, fCo174, fCo175, fCo176, fCo177, fCo178, fCo179, fCo180, fCo181, fCo182, fCo183, fCo184, fCo185, fCo186, fCo187, fCo188, fCo189, fCo190, fCo191, fCo192, fCo193, fCo194, fCo195, fCo196, fCo197, fCo198, fCo199, fCo24, fCo25, fCo26, fCo27, fCo28, fCo29, fCo210, fCo211, fCo212, fCo213, fCo214, fCo215, fCo216, fCo217, fCo218, fCo219, fCo220, fCo221, fCo222, fCo223, fCo224, fCo225, fCo226, fCo227, fCo228, fCo229, fCo230, fCo231, fCo232, fCo233, fCo234, fCo235, fCo236, fCo237, fCo238, fCo239, fCo240, fCo241, fCo242, fCo243, fCo244, fCo245, fCo246, fCo247, fCo248, fCo250, fCo251, fCo252, fCo253, fCo254, fCo255, fCo256, fCo257, fCo258, fCo259, fCo260, fCo261, fCo262, fCo263, fCo264, fCo265, fCo266, fCo267, fCo268, fCo269, fCo270, fCo271, fCo272, fCo273, fCo274, fCo275, fCo276, fCo277, fCo278, fCo279, fCo280, fCo281, fCo282, fCo283, fCo284, fCo285, fCo286, fCo287, fCo288, fCo289, fCo290, fCo291, fCo292, fCo293, fCo294, fCo295, fCo296, fCo297, fCo298, fCo299))


# fCo = np.vstack((fCo04, fCo05, fCo06, fCo07, fCo08, fCo09, fCo010, fCo011, fCo012, fCo013, fCo014, fCo015, fCo016, fCo017, fCo018, fCo019, fCo020, fCo021, fCo022, fCo023, fCo024, fCo025, fCo026, fCo027, fCo028, fCo029, fCo030, fCo031, fCo032, fCo033, fCo034, fCo035, fCo036, fCo14, fCo15, fCo16, fCo17, fCo18, fCo19, fCo110, fCo111, fCo112, fCo113, fCo114, fCo115, fCo116, fCo117, fCo118, fCo119, fCo120, fCo121, fCo122, fCo123, fCo124, fCo125, fCo126, fCo127, fCo128, fCo129, fCo130, fCo131, fCo132, fCo133, fCo134, fCo135, fCo136, fCo24, fCo25, fCo26, fCo27, fCo28, fCo29, fCo210, fCo211, fCo212, fCo213, fCo214, fCo215, fCo216, fCo217, fCo218, fCo219, fCo221, fCo222, fCo223, fCo224, fCo225, fCo226, fCo227, fCo228, fCo229, fCo231, fCo232, fCo233, fCo234, fCo235, fCo236  ))
print("Overall Coincidence Done in {} s".format(timer() - Coincidence_Start))

# fCo = fCo[0:1]

F1_Start = timer()
a = np.empty((fCo.shape[0], 4), dtype=np.float32)
f1 = F1.compton_function(a, fCo, E0, dE0, Me)
print("F1 Done in {} s".format(timer() - F1_Start))

F2_Start = timer()
f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, Det_Pos_arr)
print("F2 Done in {} s".format(timer() - F2_Start))

F3_Start = timer()
f3 = F3.PutEmTogether(f1, f2)
print("F3 Done in {} s".format(timer() - F3_Start))

F4_Start = timer()
h, v, d, data, voxel_r, dnsy, lim = F4.build_voxels(51, 0.4)
max_size = 15000
split_f3 = np.array_split(f3, (len(f3)+(max_size-1)) // max_size)
points = np.zeros((1, 3))
p = 32
n0 = 4000
for f3 in split_f3:
    points = np.append(points,
                F4.cones_generator(f3, p, lim, n0=n0), axis=0)
    print('%i chunk done' % f3.shape[0])
data = F4.voxel_fit(h, v, d, points[1:], data.shape, voxel_r)
print("F4 Done in {} s".format(timer() - F4_Start))

F5_Start = timer()
fig, ax = F5.draw(h, v, d, dnsy, data, voxel_r, Det_Pos_arr, 1)
print("F5 done in %f s" % (timer() - F5_Start))
runLabel = (f"Tau %.4f, Epsilon %.4fMeV, Voxel Density %i, Limits %icm, Point limits %i, Point Density %i/m$^2$"
            % (tau, epsilon, dnsy, 110*lim, p, n0))
ax[4].text(x=-12*lim, y=-2*lim, s=runLabel, fontsize=9)
plt.show()


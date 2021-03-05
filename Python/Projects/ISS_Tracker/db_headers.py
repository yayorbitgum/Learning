# Header Reference -------------------------------------------------------------
#
# Header info for National text file. ------------------------------------------
# 0: ï»¿FEATURE_ID
# 1: FEATURE_NAME       <- Usable Name for City or Land Feature.
# 2: FEATURE_CLASS
# 3: STATE_ALPHA        <- State Abbreviation.
# 4: STATE_NUMERIC
# 5: COUNTY_NAME
# 6: COUNTY_NUMERIC
# 7: PRIMARY_LAT_DMS
# 8: PRIM_LONG_DMS
# 9: PRIM_LAT_DEC       <- Latitude using decimals.
# 10: PRIM_LONG_DEC     <- Longitude using decimals.
# 11: SOURCE_LAT_DMS
# 12: SOURCE_LONG_DMS
# 13: SOURCE_LAT_DEC
# 14: SOURCE_LONG_DEC
# 15: ELEV_IN_M
# 16: ELEV_IN_FT
# 17: MAP_NAME
# 18: DATE_CREATED
# 19: DATE_EDITED
#
# All global text data sets have the same header, ------------------------------
# so we can use this for all those Countries files.
# Index: 0. Column Header: RC.
# Index: 1. Column Header: UFI.
# Index: 2. Column Header: UNI.
# Index: 3. Column Header: LAT.                 <- Latitude.
# Index: 4. Column Header: LONG.                <- Longitude.
# Index: 5. Column Header: DMS_LAT.
# Index: 6. Column Header: DMS_LONG.
# Index: 7. Column Header: MGRS.
# Index: 8. Column Header: JOG.
# Index: 9. Column Header: FC.
# Index: 10. Column Header: DSG.
# Index: 11. Column Header: PC.
# Index: 12. Column Header: CC1.
# Index: 13. Column Header: ADM1.               ! Contains mixed types.
# Index: 14. Column Header: POP.
# Index: 15. Column Header: ELEV.
# Index: 16. Column Header: CC2.                ! Contains mixed types.
# Index: 17. Column Header: NT.
# Index: 18. Column Header: LC.                 ! Contains mixed types.
# Index: 19. Column Header: SHORT_FORM.         ! Contains mixed types.
# Index: 20. Column Header: GENERIC.            <- Usable Name. Also mixed types.
# Index: 21. Column Header: SORT_NAME_RO.
# Index: 22. Column Header: FULL_NAME_RO.       <- Usable Name.
# Index: 23. Column Header: FULL_NAME_ND_RO.    <- Usable Name.
# Index: 24. Column Header: SORT_NAME_RG.       <- Usable Name.
# Index: 25. Column Header: FULL_NAME_RG.       <- Usable Name.
# Index: 26. Column Header: FULL_NAME_ND_RG.    <- Usable Name.
# Index: 27. Column Header: NOTE.               ! Contains mixed types.
# Index: 28. Column Header: MODIFY_DATE.
# Index: 29. Column Header: DISPLAY.            <- Best name?
# Index: 30. Column Header: NAME_RANK.
# Index: 31. Column Header: NAME_LINK.
# Index: 32. Column Header: TRANSL_CD.          ! Contains mixed types.
# Index: 33. Column Header: NM_MODIFY_DATE.
# Index: 34. Column Header: F_EFCTV_DT.         ! Contains mixed types.
# Index: 35. Column Header: F_TERM_DT.          ! Contains mixed types.

national_columns = ['FEATURE_NAME',
                    'FEATURE_CLASS',
                    'STATE_ALPHA',
                    'STATE_NUMERIC',
                    'COUNTY_NAME',
                    'COUNTY_NUMERIC',
                    'PRIMARY_LAT_DMS',
                    'PRIM_LONG_DMS',
                    'SOURCE_LAT_DMS',
                    'SOURCE_LONG_DMS',
                    'MAP_NAME',
                    'DATE_CREATED',
                    'DATE_EDITED']

global_columns   = ['MGRS',
                    'JOG',
                    'FC',
                    'DSG',
                    'CC1',
                    'ADM1',
                    'CC2',
                    'NT',
                    'LC',
                    'SHORT_FORM',
                    'GENERIC',
                    'SORT_NAME_RO',
                    'FULL_NAME_RO',
                    'FULL_NAME_ND_RO',
                    'SORT_NAME_RG',
                    'FULL_NAME_RG',
                    'FULL_NAME_ND_RG',
                    'NOTE',
                    'MODIFY_DATE',
                    'DISPLAY',
                    'TRANSL_CD',
                    'NM_MODIFY_DATE',
                    'F_EFCTV_DT',
                    'F_TERM_DT',
                    'DMS_LAT',
                    'DMS_LONG']

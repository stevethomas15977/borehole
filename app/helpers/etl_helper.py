from collections import defaultdict
from datetime import datetime
from logging import error, info
import stat

from pandas import read_excel, isna, notna

from models import Survey, Well
from services import SurveyService, WellService

def swope_direction(direction):
    if direction == "N":
        return "S"
    elif direction == "S":
        return "N"
    elif direction == "E":
        return "W"
    elif direction == "W":
        return "E"
    else:
        raise ValueError(f"Recieved direction of {direction} but direction must be 'N' or 'S'")

def load_wells(db_path:str , file_path: str) -> None:
    try:
        start_time = datetime.now()
        well_list = []
        wells = read_excel(file_path)
        producing_wells = wells[wells["ENVWellboreStatus"] == "PRODUCING"]
        for _, row in producing_wells.iterrows():
            api = row["API_UWI"]
            well_name = row["WellName"]
            direction = row["WellPadDirection"]
            operator = row["ENVOperator"]
            status = row["ENVWellStatus"]
            lease = row["LeaseName"]
            interval = row["ENVInterval"]
            if "DELAWARE VERTICAL" == interval:
                continue
            formation = row["Formation"]
            first_production_date = str(row["FirstProdDate"].strftime("%Y-%m-%d"))
            surface_latitude = row["Latitude"]
            surface_longitude = row["Longitude"]
            bottom_hole_latitude = row["Latitude_BH"]
            bottom_hole_longitude = row["Longitude_BH"]
            total_vertical_depth = row["TVD_FT"]
            measured_depth = row["MD_FT"]
            kelly_bushing_elevation = row["ElevationKB_FT"]
            lateral_length = row["LateralLength_FT"]
            if isna(row["PerfInterval_FT"]) or row["PerfInterval_FT"] is None:
                perf_interval = row["LateralLength_FT"] 
            else:
                perf_interval = row["PerfInterval_FT"]
            proppant_intensity = row["ProppantIntensity_LBSPerFT"]
            state = row["StateProvince"]
            county = row["County"]
            if state == "TX":
                if not isna(row["Abstract"]):
                    abstract = f"A-{row['Abstract']}"
                else:
                    abstract = None
            else:
                abstract = None
            township = row["Township"] if state in ["TX", "NM"] else None
            range = row["Range"] if state == "NM" else None
            section = str(int(row["Section"])).zfill(2) if state in ["TX", "NM"] else None
            cumlative_oil = row["CumOil_BBL"]   
            if notna(row["LastProducingMonth"]):
                last_producing_month = str(row["LastProducingMonth"].strftime("%Y-%m-%d"))
            else:
                last_producing_month = None
            if isna(row["CumOil_BBLPer1000FT"]) or row["CumOil_BBLPer1000FT"] is None:
                cumoil_bblper1000ft = None
                cumoil_bblperft = None
            else:
                cumoil_bblper1000ft = row["CumOil_BBLPer1000FT"]
                cumoil_bblperft = int(row["CumOil_BBLPer1000FT"]/1000)

            well = Well(
                api=api,
                name=well_name,
                direction=direction,
                operator=operator,
                status=status,
                lease=lease,
                interval=interval,
                formation=formation,
                first_production_date=first_production_date,
                surface_latitude=surface_latitude,
                surface_longitude=surface_longitude,
                bottom_hole_latitude=bottom_hole_latitude,
                bottom_hole_longitude=bottom_hole_longitude,
                total_vertical_depth=total_vertical_depth,
                measured_depth=measured_depth,
                kelly_bushing_elevation=kelly_bushing_elevation,
                lateral_length=lateral_length,
                perf_interval=perf_interval,
                proppant_intensity=proppant_intensity,
                state=state,
                county=county,
                abstract=abstract,
                township=township,
                range=range,
                section=section,
                cumlative_oil=cumlative_oil,
                last_producing_month=last_producing_month,
                cumoil_bblper1000ft=cumoil_bblper1000ft,
                cumoil_bblperft=cumoil_bblperft)
            well_list.append(well)
        well_service = WellService(db_path=db_path)
        well_service.add(well_list)
        end_time = datetime.now()
        duration = end_time - start_time
        info(f"Load well job completed in {duration}")
    except Exception as e:
        raise Exception(f"Error loading wells from {file_path}: {e}")

def _find_survey_revisions_to_remove(surveys: list[Survey]) -> list[str]:
    results = []
    grouped_api_uwis = defaultdict(list)
    multiple_revisions = []
    grouped_surveys = surveys.groupby(surveys["API_UWI"].apply(lambda x: x[:12]))
    for name, group in grouped_surveys:
        num_unique_api_uwi = group["API_UWI"].value_counts()
        revisions = 0
        for value, count in num_unique_api_uwi.items():
            revisions += 1
            grouped_api_uwis[name].append(num_unique_api_uwi)
        if revisions > 1:
            multiple_revisions.append(name)

    for api in multiple_revisions:
        for key, values in grouped_api_uwis.items():
            if key == api:
                for value in values:
                    for index, item in enumerate(value.items()):
                        if index == 0:
                            min_api_uwi = item[0]
                            min_count = item[1]
                            continue
                        else:
                            if item[1] < min_count:
                                if item[0] not in results:
                                    results.append(item[0])
                                    #print(f"Removing survey {item[0]} - {item[1]}")
                            else:
                                if min_api_uwi not in results:
                                    results.append(min_api_uwi)
                                    #print(f"Removing survey {min_api_uwi} - {min_count}")
                                min_api_uwi = item[0]
                                min_count = item[1]
    return results

def _remove_survey_revision(surveys, api_uwi) -> list[Survey]:
    return surveys[surveys["API_UWI"] != api_uwi]

def load_surveys(db_path:str, file_path:str) -> None:
    try:
        start_time = datetime.now()
        survey_list = []
        surveys = read_excel(file_path)

        # Remove duplicate revisions
        survey_revisions = _find_survey_revisions_to_remove(surveys)
        for survey_revision in survey_revisions:
            info(f"Removing revision {survey_revision} from surveys")
            surveys = _remove_survey_revision(surveys, survey_revision)

        for index, row in surveys.iterrows():
            api = row["API_UWI"][:12]
            station = row["StationNumber"]
            md = row["MeasuredDepth_FT"]
            inclination = row["Inclination_DEG"]
            azimuth = row["Azimuth_DEG"]
            latitude = row["Latitude"]
            longitude = row["Longitude"]
            grid_x = row["GridX_FT"]
            grid_y = row["GridY_FT"]
            subsurface_depth = row["SubseaElevation_FT"]
            survey = Survey(api=api, 
                            station=station, 
                            md=md, 
                            inclination=inclination, 
                            azimuth=azimuth, 
                            latitude=latitude, 
                            longitude=longitude, 
                            grid_x=grid_x, 
                            grid_y=grid_y, 
                            subsurface_depth=subsurface_depth)
            survey_list.append(survey)
        survey_service = SurveyService(db_path=db_path)
        survey_service.add(survey_list)
        end_time = datetime.now()
        duration = end_time - start_time
        info(f"Load surveys job completed in {duration}")
    except Exception as e:
        raise Exception(f"Error loading surveys from {file_path}: {e}")
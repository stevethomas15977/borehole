from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, create_survey_from_well_data, create_survey_from_survey_data
from services import WellService, SurveyService, AnalysisService, StratigraphicService
from traceback import format_exc

class ETLWell(Task):

    def execute(self):
        task = TASKS.ETL_WELL.value
        logger = task_logger(task, self.context.logs_path)
        try:
            well_service = WellService(db_path=self.context.db_path)
            survey_service = SurveyService(db_path=self.context.db_path)
            analysis_service = AnalysisService(db_path=self.context.db_path)
            stratigraphic_service = StratigraphicService(db_path=self.context.db_path)

            analysis_list = []
            wells = well_service.get_all()
            for well in wells:
                # if well.name not in ["LIMBER PINE A5 3LA"]:
                #     continue
                surveys = survey_service.get_by_api(api=well.api)
                if surveys is None or len(surveys) == 0:
                    logger.warning(f"Survey data found for well/api: {well.name}/{well.api}, will attempt to create survey from well data")
                    logger.info("Creating survey data")
                    analysis = create_survey_from_well_data(logger, well)
                    if analysis is not None:
                        analysis.api = well.api
                        analysis.name = well.name
                        if well.interval is not None:
                            analysis.interval = stratigraphic_service.get_by_prism_code(well.interval).union_code
                        analysis.first_production_date = str(well.first_production_date)
                        analysis.cumoil_bblperft = well.cumoil_bblperft
                        analysis_list.append(analysis)
                    else:
                        logger.error(f"Unable to create survey data for well: {well.name}")
                        continue
                else:    
                    analysis = create_survey_from_survey_data(logger, surveys)
                    if analysis is not None:
                        analysis.api = well.api
                        analysis.name = well.name
                        if well.interval is not None:
                            analysis.interval = stratigraphic_service.get_by_prism_code(well.interval).union_code
                        analysis.first_production_date = str(well.first_production_date)
                        analysis.cumoil_bblperft = well.cumoil_bblperft
                        analysis_list.append(analysis)
                    else:
                        logger.warning(f"Survey may be incomplete for well/api: {well.name}/{well.api}, will attempt to create survey from well data")
                        analysis = create_survey_from_well_data(logger, well)
                        if analysis is not None:
                            analysis.api = well.api
                            analysis.name = well.name 
                            if well.interval is not None:
                                analysis.interval = stratigraphic_service.get_by_prism_code(well.interval).union_code
                            analysis.first_production_date = str(well.first_production_date)
                            analysis.cumoil_bblperft = well.cumoil_bblperft
                            analysis_list.append(analysis) 
                        else:
                            logger.error(f"Unable to create survey data for well: {well.name}")
                            continue
            
            analysis_service.add_list(analysis_list)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")
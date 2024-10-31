
def auto_adjust_column_widths(worksheet):
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column].width = adjusted_width

def excel_columns():
    return ['API_UWI', 
            'WellName', 
            'ENVOperator', 
            'ENVInterval', 
            'FirstProdDate', 
            'TVD_FT', 
            'PerfInterval_FT', 
            'ProppantIntensity_LBSPerFT', 
            'BH_Lat', 
            'BH_Long', 
            'RKB_Elev', 
            'TVD_SS',
            'Average-Lateral-Spacing-at-BHL',
            'Co-dev',
            'Bound-Half-Bound',
            'Child', 
            'Adjacent-Child',
            'Parents',
            'Parent-1',
            'Parent-1-First-Production-Date',
            'Parent_1-Delta-First-Production-Months',
            'Parent-2',
            'Parent-2-First-Production-Date',
            'Parent_2-Delta-First-Production-Months',
            'Adjacent-2-West',
            'Adjacent-2-Distance-West',
            'Adjacent-2-Hypotenuse-Distance-West',
            'Adjacent-1-East',
            'Adjacent-1-Distance-East',
            'Adjacent-1-Hypotenuse-Distance-East',
            'Group-ID', 
            'Group-Lateral-Spacing-at-BHL'
            ]
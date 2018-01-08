import os
import pandas as pd
import pprint as pp


QUESTIONS = [
    'I am good at solving math word problems (AR)',
    'I have good spatial reasoning skills (AO)',
    'I am familiar with tools and vehicle repair (AS)',
    'I am very handy with electronics (EI)',
    'I have a good working knowledge of general science (GS)',
    'I am good at math (MK)',
    'I have a good understanding of basic physics (MC)',
    'I understand written paragraphs easily (PC)',
    'I have a strong vocabulary (WK)',
]


def main():

    army_cool_df = pd.DataFrame.from_csv("asvab_reference/armycoolreference.csv")

    print army_cool_df

    print "RATE YOURSELF ON A SCALE OF 1 TO 5"

    user_responses = []

    for question in QUESTIONS:
        response = raw_input("{0} ".format(question))
        while response not in ["1", "2", "3", "4", "5"]:
            response = raw_input(question)
        user_responses.append(int(response))

    results = {}

    cr_list = [(int(x) - 0.5) * 20 for x in user_responses]

    cl = cr_list[8] + cr_list[7] + cr_list[0] + cr_list[5]
    co = cr_list[0] + cr_list[2] + cr_list[5]
    el = cr_list[4] + cr_list[0] + cr_list[5] + cr_list[3]
    fa = cr_list[0] + cr_list[5] + cr_list[6]
    gm = cr_list[4] + cr_list[2] + cr_list[5] + cr_list[3]
    gt = cr_list[8] + cr_list[7] + cr_list[0]
    mm = cr_list[2] + cr_list[6] + cr_list[3]
    of = cr_list[8] + cr_list[7] + cr_list[2] + cr_list[6]
    sc = cr_list[8] + cr_list[7] + cr_list[0] + cr_list[2] + cr_list[6]
    st = cr_list[4] + cr_list[8] + cr_list[7] + cr_list[5] + cr_list[6]

    results["CL"] = cl
    results["CO"] = co
    results["EL"] = el
    results["FA"] = fa
    results["GM"] = gm
    results["GT"] = gt
    results["MM"] = mm
    results["OF"] = of
    results["SC"] = sc
    results["ST"] = st

    pp.pprint(results)

    mos = []

    mos.append(['92S', 'Shower/Laundry and Clothing Repair Specialist', results['GM'] - 84]) if results[
                                                                                                    'GM'] > 84 else False
    mos.append(['14S', 'Air and Missile Defense (AMD) Crewmember', results['OF'] - 85]) if results['OF'] > 85 else False
    mos.append(['88M', 'Motor Transport Operator', results['OF'] - 85]) if results['OF'] > 85 else False
    mos.append(['92G', 'Culinary Specialist', results['OF'] - 85]) if results['OF'] > 85 else False
    mos.append(['12C', 'Bridge Crewmember', results['CO'] - 87]) if results['CO'] > 87 else False
    mos.append(['19D', 'Cavalry Scout', results['CO'] - 87]) if results['CO'] > 87 else False
    mos.append(['19K', 'M1 Armor Crewman', results['CO'] - 87]) if results['CO'] > 87 else False
    mos.append(['88T', 'Railway Section Repairer (Reserves only)', results['MM'] - 87]) if results['MM'] > 87 else False
    mos.append(['12K', 'Plumber', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['12M', 'Firefighter', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['12V', 'Concrete and Asphalt Equipment Operator', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['12W', 'Carpentry and Masonry Specialist', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['88H', 'Cargo Specialist', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['92M', 'Mortuary Affairs Specialist', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['92W', 'Water Treatment Specialist', results['GM'] - 88]) if results['GM'] > 88 else False
    mos.append(['56M', 'Chaplain Assistant', results['CL'] - 90]) if results['CL'] > 90 else False
    mos.append(['68G', 'Patient Administration Specialist', results['CL'] - 90]) if results['CL'] > 90 else False
    mos.append(['68J', 'Medical Logistics Specialist', results['CL'] - 90]) if results['CL'] > 90 else False
    mos.append(['92A', 'Automated Logistical Specialist', results['CL'] - 90]) if results['CL'] > 90 else False
    mos.append(['92Y', 'Unit Supply Specialist', results['CL'] - 90]) if results['CL'] > 90 else False
    mos.append(['11B', 'Infantry', results['CO'] - 90]) if results['CO'] > 90 else False
    mos.append(['11C', 'Indirect Fire Infantryman', results['CO'] - 90]) if results['CO'] > 90 else False
    mos.append(['12N', 'Horizontal Construction Engineer', results['GM'] - 90]) if results['GM'] > 90 else False
    mos.append(['15P', 'Aviation Operations Specialist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['31B', 'Military Police', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['31K', 'Military Working Dog (MWD) Handler', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['35P', 'Cryptologic Linguist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['68D', 'Operating Room Specialist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['68E', 'Dental Specialist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['68T', 'Animal Care Specialist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['89A', 'Ammunition Stock Control and Accounting Specialist', results['ST'] - 91]) if results[
                                                                                                         'ST'] > 91 else False
    mos.append(['89B', 'Ammunition Specialist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['92L', 'Petroleum Laboratory Specialist', results['ST'] - 91]) if results['ST'] > 91 else False
    mos.append(['88U', 'Railway Operations Crewmember (Reserves only)', results['MM'] - 92]) if results[
                                                                                                    'MM'] > 92 else False
    mos.append(['14T', 'PATRIOT Launching Station Enhanced Operator/Maintainer', results['OF'] - 92]) if results[
                                                                                                             'OF'] > 92 else False
    mos.append(['12Q', 'Power Distribution Specialist', results['EL'] - 93]) if results['EL'] > 93 else False
    mos.append(['12R', 'Interior Electrician', results['EL'] - 93]) if results['EL'] > 93 else False
    mos.append(['13T', 'Field Artillery Surveyor/Meteorological Crewmember', results['EL'] - 93]) if results[
                                                                                                         'EL'] > 93 else False
    mos.append(['15N', 'Avionic Mechanic', results['EL'] - 93]) if results['EL'] > 93 else False
    mos.append(['94P', 'Multiple Launch Rocket System Repairer', results['EL'] - 93]) if results['EL'] > 93 else False
    mos.append(['13B', 'Cannon Crewmember', results['FA'] - 93]) if results['FA'] > 93 else False
    mos.append(['13D', 'Field Artillery Automated Tactical Data Systems Specialist', results['FA'] - 93]) if results[
                                                                                                                 'FA'] > 93 else False
    mos.append(['12G', 'Quarrying Specialist', results['GM'] - 93]) if results['GM'] > 93 else False
    mos.append(['88N', 'Transportation Management Coordinator', results['CL'] - 95]) if results['CL'] > 95 else False
    mos.append(['13M', 'Multiple Launch Rocket System Crewmember', results['OF'] - 95]) if results['OF'] > 95 else False
    mos.append(['68M', 'Nutrition Care Specialist', results['OF'] - 95]) if results['OF'] > 95 else False
    mos.append(['25B', 'Information Technology Specialist', results['ST'] - 95]) if results['ST'] > 95 else False
    mos.append(['31E', 'Internment/Resettlement Specialist', results['ST'] - 95]) if results['ST'] > 95 else False
    mos.append(['68Q', 'Pharmacy Specialist', results['ST'] - 95]) if results['ST'] > 95 else False
    mos.append(['68R', 'Veterinary Food Inspection Specialist', results['ST'] - 95]) if results['ST'] > 95 else False
    mos.append(['13F', 'Fire Support Specialist', results['FA'] - 96]) if results['FA'] > 96 else False
    mos.append(['13P', 'Multiple Launch Rocket System Operations/Fire Direction Specialist', results['FA'] - 96]) if \
    results['FA'] > 96 else False
    mos.append(['88P', 'Railway Equipment Repairer (Reserves only)', results['MM'] - 97]) if results[
                                                                                                 'MM'] > 97 else False
    mos.append(['12B', 'Combat Engineer', results['CO'] - 98]) if results['CO'] > 98 else False
    mos.append(['94R', 'Avionic and Survivability Equipment Repairer', results['EL'] - 98]) if results[
                                                                                                   'EL'] > 98 else False
    mos.append(['94T', 'Avenger System Repairer', results['EL'] - 98]) if results['EL'] > 98 else False
    mos.append(['68H', 'Optical Laboratory Specialist', results['GM'] - 98]) if results['GM'] > 98 else False
    mos.append(['13R', 'Field Artillery Firefinder Radar Operator', results['SC'] - 98]) if results[
                                                                                                'SC'] > 98 else False
    mos.append(['15R', 'AH-64 Attack Helicopter Repairer', results['MM'] - 99]) if results['MM'] > 99 else False
    mos.append(['15S', 'OH-58D Helicopter Repairer', results['MM'] - 99]) if results['MM'] > 99 else False
    mos.append(['88K', 'Watercraft Operator', results['MM'] - 99]) if results['MM'] > 99 else False
    mos.append(['88L', 'Watercraft Engineer', results['MM'] - 99]) if results['MM'] > 99 else False
    mos.append(['74D', 'Chemical, Biological, Radiological, and Nuclear Operations Specialist', results['ST'] - 100]) if \
    results['ST'] > 100 else False
    mos.append(['36B', 'Financial Management Technician', results['CL'] - 101]) if results['CL'] > 101 else False
    mos.append(['12T', 'Technical Engineer', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['15Q', 'Air Traffic Control (ATC) Operator', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['35F', 'Intelligence Analyst', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['35G', 'Geospatial Intelligence Imagery Analyst', results['ST'] - 101]) if results[
                                                                                               'ST'] > 101 else False
    mos.append(['35L', 'Counterintelligence Agent', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['35M', 'Human Intelligence Collector', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['35N', 'Signals Intelligence Analyst', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['35S', 'Signals Collector/Analyst', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['68S', 'Preventive Medicine Specialist', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['68X', 'Mental Health Specialist', results['ST'] - 101]) if results['ST'] > 101 else False
    mos.append(['94A', 'Land Combat Electronic Missile System Repairer', results['EL'] - 102]) if results[
                                                                                                      'EL'] > 102 else False
    mos.append(['94D', 'Air Traffic Control Equipment Repairer', results['EL'] - 102]) if results['EL'] > 102 else False
    mos.append(['94E', 'Radio and Communications Security Repairer', results['EL'] - 102]) if results[
                                                                                                  'EL'] > 102 else False
    mos.append(['94F', 'Computer/Detection Systems Repairer', results['EL'] - 102]) if results['EL'] > 102 else False
    mos.append(['15W', 'Unmanned Aircraft Systems Operator', results['SC'] - 102]) if results['SC'] > 102 else False
    mos.append(['68V', 'Respiratory Specialist', results['ST'] - 102]) if results['ST'] > 102 else False
    mos.append(['14E', 'Patriot Fire Control Enhanced Operator/Maintainer', results['MM'] - 104]) if results[
                                                                                                         'MM'] > 104 else False
    mos.append(['15B', 'Aircraft Powerplant Repairer', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['15D', 'Aircraft Powertrain Repairer', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['15F', 'Aircraft Electrician', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['15G', 'Aircraft Structural Repairer', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['15H', 'Aircraft Pneudraulics Repairer', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['15T', 'UH-60 Helicopter Repairer', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['15U', 'CH-47 Helicopter Repairer', results['MM'] - 104]) if results['MM'] > 104 else False
    mos.append(['27D', 'Paralegal Specialist', results['CL'] - 105]) if results['CL'] > 105 else False
    mos.append(['68K', 'Medical Laboratory Specialist', results['ST'] - 106]) if results['ST'] > 106 else False
    mos.append(['68P', 'Radiology Specialist', results['ST'] - 106]) if results['ST'] > 106 else False
    mos.append(['25P', 'Microwave Systems Operator/Maintainer', results['EL'] - 107]) if results['EL'] > 107 else False
    mos.append(['25R', 'Visual Information Equipment Operator/Maintainer', results['EL'] - 107]) if results[
                                                                                                        'EL'] > 107 else False
    mos.append(['68A', 'Biomedical Equipment Specialist', results['EL'] - 107]) if results['EL'] > 107 else False
    mos.append(
        ['94H', 'Test Measurement and Diagnostic Equipment Maintenance Support Specialist', results['EL'] - 107]) if \
    results['EL'] > 107 else False
    mos.append(['94M', 'Radar Repairer', results['EL'] - 107]) if results['EL'] > 107 else False
    mos.append(['94S', 'PATRIOT System Repairer', results['EL'] - 107]) if results['EL'] > 107 else False
    mos.append(['37F', 'Psychological Operations Specialist', results['GT'] - 107]) if results['GT'] > 107 else False
    mos.append(['38B', 'Civil Affairs Specialist', results['GT'] - 107]) if results['GT'] > 107 else False
    mos.append(['46Q', 'Public Affairs Specialist', results['GT'] - 107]) if results['GT'] > 107 else False
    mos.append(['46R', 'Public Affairs Broadcast Specialist Journalist', results['GT'] - 107]) if results[
                                                                                                      'GT'] > 107 else False
    mos.append(['89D', 'Explosive Ordnance Disposal (EOD) Specialist', results['ST'] - 110]) if results[
                                                                                                    'ST'] > 110 else False
    mos.append(['35Q', 'Cryptologic Network Warfare Specialist', results['ST'] - 112]) if results['ST'] > 112 else False
    mos.append(['35T', 'Military Intelligence Systems Maintainer/Integrator', results['ST'] - 112]) if results[
                                                                                                           'ST'] > 112 else False
    mos.append(['25S', 'Satellite Communication Systems Operator/Maintainer', results['EL'] - 117]) if results[
                                                                                                           'EL'] > 117 else False
    mos.append(['42A', 'Human Resources Specialist', (results['GT'] - 100 + results['CL'] - 90) / 2]) if results[
                                                                                                             'GT'] > 100 and \
                                                                                                         results[
                                                                                                             'CL'] > 90 else False
    mos.append(['12Y', 'Geospatial Engineer', (results['ST'] - 100 + results['GT'] - 100) / 2]) if results[
                                                                                                       'ST'] > 100 and \
                                                                                                   results[
                                                                                                       'GT'] > 100 else False
    mos.append(['29E', 'Electronic Warfare Specialist',
                (results['SC'] - 100 + results['ST'] - 100 + results['EL'] - 100) / 3]) if results['SC'] > 100 and \
                                                                                           results['ST'] > 100 and \
                                                                                           results[
                                                                                               'EL'] > 100 else False
    mos.append(['68B', 'Orthopedic Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results[
                                                                                                         'ST'] > 101 and \
                                                                                                     results[
                                                                                                         'GT'] > 107 else False
    mos.append(['68N', 'Cardiovascular Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results[
                                                                                                             'ST'] > 101 and \
                                                                                                         results[
                                                                                                             'GT'] > 107 else False
    mos.append(['68W', 'Healthcare Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results[
                                                                                                         'ST'] > 101 and \
                                                                                                     results[
                                                                                                         'GT'] > 107 else False
    mos.append(['68C', 'Practical Nursing Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results[
                                                                                                                'ST'] > 101 and \
                                                                                                            results[
                                                                                                                'GT'] > 107 else False
    mos.append(['68F', 'Physical Therapy Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results[
                                                                                                               'ST'] > 101 and \
                                                                                                           results[
                                                                                                               'GT'] > 107 else False
    mos.append(['68L', 'Occupational Therapy Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results[
                                                                                                                   'ST'] > 101 and \
                                                                                                               results[
                                                                                                                   'GT'] > 107 else False
    mos.append(['68Y', 'Eye Specialist', (results['ST'] - 101 + results['GT'] - 107) / 2]) if results['ST'] > 101 and \
                                                                                              results[
                                                                                                  'GT'] > 107 else False
    mos.append(['25N', 'Nodal Network Systems Operator/Maintainer', (results['EL'] - 102 + results['SC'] - 105) / 2]) if \
    results['EL'] > 102 and results['SC'] > 105 else False
    mos.append(['25D', 'Cyber Network Defender', (results['GT'] - 105 + results['ST'] - 105) / 2]) if results[
                                                                                                          'GT'] > 105 and \
                                                                                                      results[
                                                                                                          'ST'] > 105 else False
    mos.append(['12D', 'Diver', results['ST'] - 106]) if results['ST'] > 106 or (
    results['GM'] > 98 and results['GT'] > 107) else False
    mos.append(
        ['12P', 'Prime Power Specialist', (results['ST'] - 107 + results['EL'] - 107 + results['GT'] - 110) / 3]) if \
    results['ST'] > 107 and results['EL'] > 107 and results['GT'] > 110 else False
    mos.append(['18X', 'Special Forces C+idate', (results['GT'] - 110 + results['CO'] - 100) / 2]) if results[
                                                                                                          'GT'] > 110 and \
                                                                                                      results[
                                                                                                          'CO'] > 100 else False
    mos.append(['31D', 'Criminal Investigations Special Agent', (results['GT'] - 110 + results['ST'] - 107) / 2]) if \
    results['GT'] > 110 and results['ST'] > 107 else False
    mos.append(['17C', 'Cyber Operations Specialist', (results['GT'] - 110 + results['ST'] - 112) / 2]) if results[
                                                                                                               'GT'] > 110 and \
                                                                                                           results[
                                                                                                               'ST'] > 112 else False
    mos.append(['92F', 'Petroleum Supply Specialist', (results['CL'] - 86 + results['OF'] - 85) / 2]) if results[
                                                                                                             'CL'] > 86 and \
                                                                                                         results[
                                                                                                             'OF'] > 85 else False
    mos.append(['92R', 'Parachute Rigger', (results['GM'] - 88 + results['CO'] - 87) / 2]) if results['GM'] > 88 and \
                                                                                              results[
                                                                                                  'CO'] > 87 else False
    mos.append(['25L', 'Cable Systems Installer/Maintainer', (results['SC'] - 89 + results['EL'] - 89) / 2]) if results[
                                                                                                                    'SC'] > 89 and \
                                                                                                                results[
                                                                                                                    'EL'] > 89 else False
    mos.append(['25U', 'Signal Support Systems Specialist', (results['SC'] - 92 + results['EL'] - 93) / 2]) if results[
                                                                                                                   'SC'] > 92 and \
                                                                                                               results[
                                                                                                                   'EL'] > 93 else False
    mos.append(['91B', 'Wheeled Vehicle Mechanic', results['MM'] - 92]) if results['MM'] > 92 or (
    results['MM'] > 87 and results['GT'] > 85) else False
    mos.append(['91H', 'Track Vehicle Repairer', results['MM'] - 92]) if results['MM'] > 92 or (
    results['MM'] > 87 and results['GT'] > 85) else False
    mos.append(['91J', 'Quartermaster and Chemical Equipment Repairer', results['MM'] - 92]) if results['MM'] > 92 or (
    results['MM'] > 87 and results['GT'] > 85) else False
    mos.append(['91L', 'Construction Equipment Repairer', results['MM'] - 92]) if results['MM'] > 92 or (
    results['MM'] > 87 and results['GT'] > 85) else False
    mos.append(['91S', 'Stryker Systems Maintainer', results['MM'] - 92]) if results['MM'] > 92 or (
    results['MM'] > 87 and results['GT'] > 85) else False
    mos.append(['15E', 'Unmanned Aircraft Systems Repairer', (results['EL'] - 93 + results['MM'] - 104) / 2]) if \
    results['EL'] > 93 and results['MM'] > 104 else False
    mos.append(['15J', 'OH-58D Armament/Electrical/Avionics Systems Repairer',
                (results['EL'] - 93 + results['MM'] - 104) / 2]) if results['EL'] > 93 and results[
                                                                                               'MM'] > 104 else False
    mos.append(['25M', 'Multimedia Illustrator', (results['EL'] - 93 + results['ST'] - 91) / 2]) if results[
                                                                                                        'EL'] > 93 and \
                                                                                                    results[
                                                                                                        'ST'] > 91 else False
    mos.append(['25V', 'Combat Documentation/Production Specialist', (results['EL'] - 93 + results['ST'] - 91) / 2]) if \
    results['EL'] > 93 and results['ST'] > 91 else False
    mos.append(['91F', 'Small Arms/Artillery Repairer', results['GM'] - 93]) if results['GM'] > 93 or (
    results['GM'] > 88 and results['GT'] > 85) else False
    mos.append(['25C', 'Radio Operator/Maintainer', (results['SC'] - 98 + results['EL'] - 98) / 2]) if results[
                                                                                                           'SC'] > 98 and \
                                                                                                       results[
                                                                                                           'EL'] > 98 else False
    mos.append(['15Y', 'AH-64D Armament/Electrical/Avionics Systems Repairer',
                (results['EL'] - 98 + results['MM'] - 104) / 2]) if results['EL'] > 98 and results[
                                                                                               'MM'] > 104 else False
    mos.append(
        ['14G', 'Air Defense Battle Management System Operator', (results['GT'] - 98 + results['MM'] - 99) / 2]) if \
    results['GT'] > 98 and results['MM'] > 99 else False
    mos.append(['14H', 'Air Defense Early Warning System Operator', (results['GT'] - 98 + results['MM'] - 99) / 2]) if \
    results['GT'] > 98 and results['MM'] > 99 else False
    mos.append(['25Q', 'Multichannel Transmission Systems Operator/Maintainer',
                (results['EL'] - 98 + results['SC'] - 98) / 2]) if results['EL'] > 98 and results['SC'] > 98 else False
    mos.append(['91G', 'Fire Control Repairer', results['EL'] - 98]) if results['EL'] > 98 or (
    results['EL'] > 93 and results['GT'] > 88) else False
    mos.append(['91C', 'Utilities Equipment Repairer', results['GM'] - 98]) if results['GM'] > 98 or (
    results['GM'] > 88 and results['GT'] > 83) else False
    mos.append(['91D', 'Power Generation Equipment Repairer', results['GM'] - 98]) if results['GM'] > 98 or (
    results['GM'] > 88 and results['GT'] > 88) else False
    mos.append(['91E', 'Allied Trade Specialist', results['GM'] - 98]) if results['GM'] > 98 or (
    results['GM'] > 88 and results['GT'] > 92) else False
    mos.append(['91P', 'Artillery Mechanic', results['MM'] - 99]) if results['MM'] > 99 or (
    results['MM'] > 88 and results['GT'] > 88) else False
    mos.append(['91A', 'M1 Abrams Tank System Maintainer', results['MM'] - 99]) if results['MM'] > 99 or (
    results['MM'] > 88 and results['GT'] > 92) else False
    mos.append(['91M', 'Bradley Fighting Vehicle System Maintainer', results['MM'] - 99]) if results['MM'] > 99 or (
    results['MM'] > 88 and results['GT'] > 92) else False

    print len(mos)

    #TODO NEED TO UPDATE SCORING RUBRIC
    mos.sort(key=lambda x: x[2])

    mos_df = pd.DataFrame(mos, columns=["code","Title", "Score"])
    mos_df = mos_df.set_index("code")

    mos_df = mos_df.merge(army_cool_df, how='left', left_index=True, right_index=True)

    print mos_df.to_string()

    # results.append(("Clerical", "CL", cl))
    # results.append(("Combat", "CO", co))
    # results.append(("Electronics", "EL", el))
    # results.append(("Field Artillery", "FA", fa))
    # results.append(("General Maintenance", "GM", gm))
    # results.append(("General Technical", "GT", gt))
    # results.append(("Mechanical Maintenance", "MM", mm))
    # results.append(("Operators and Food", "OF", of))
    # results.append(("Surveillance and Communications", "SC", sc))
    # results.append(("Skilled Technical", "ST", st))
    # 
    # results.sort(key=lambda x: -x[1])
    # for result in results:
    #     print result[0], "|", result[1]




if __name__ == "__main__":
    main()
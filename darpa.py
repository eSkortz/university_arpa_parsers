import requests
import json
from darpa_models.program import Program

response = requests.get('https://www.darpa.mil/JSON/our-research.json')
result = json.loads(response.text)
for element in result["ListItems_rls"]:
    program = Program(element)
    program.get_program_info()
    # program.write_program_in_file()
    print(program)
    program.write_program_in_excel('output.xlsx')
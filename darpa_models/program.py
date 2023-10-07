import requests
import json
from bs4 import BeautifulSoup


class Program:
    name: str
    lead_paragraph: str
    program_url: str
    office_abbr: str
    pm_name: str
    pm_url: str
    tags: list

    description_body: str
    related_content: list

    def __init__(self, program_info: dict) -> None:
        self.name = program_info["Name_rst"]
        self.lead_paragraph = program_info["LeadParagraph_rst"]
        self.program_url = f'https://www.darpa.mil/JSON{program_info["URL_rst"].replace(".html", ".json")}'
        self.office_abbr = program_info["OfficeAbbr_rst"]
        self.pm_name = program_info["PM_Name_rst"]
        self.pm_url = program_info["Pm_Url_rst"]
        tags_result_list = []
        for element in program_info["Tags_rls"]:
            tag_dict = {
                "name": element["name_rst"],
                "shortname": element["shortName_rst"],
                "url": element["url_rst"],
            }
            tags_result_list.append(tag_dict)
        self.tags = tags_result_list

    def __str__(self) -> str:
        print(
            f"Name: {self.name}\nOffice: {self.office_abbr}\nProject manager: {self.pm_name}\n\nLead paragraph: {self.lead_paragraph}"
        )

    def get_program_info(self):
        response_program = requests.get(self.program_url)
        program_result = json.loads(response_program.text)

        html_string = program_result["Body_rst"]
        soup = BeautifulSoup(html_string, 'html.parser')
        cleaned_string = soup.get_text()
        self.description_body = cleaned_string

        related_result_list = []
        related_list = program_result["RelatedContent_rls"]
        for element in related_list:
            temporary_related_list = {
                "name": element["url_rst"],
                "url": element["content_name_rst"],
            }
            related_result_list.append(temporary_related_list)
        self.related_content = related_result_list
        
    def write_program_in_file(self):
        with open('result.txt', 'a') as general_file:
            
            tag_string = ''
            for element in self.tags:
                tag_string = tag_string + f'{element["name"]},{element["shortname"]},{element["url"]};'
            tag_string = tag_string[:-1]
            
            related_string = ''
            for element in self.related_content:
                related_string = related_string + f'{element["name"]},{element["url"]};'
            related_string = related_string[:-1]
            
            outstring = f'{self.name}|{self.lead_paragraph}|{self.program_url}|{self.office_abbr}|{self.pm_name}|{self.pm_url}|{tag_string}|{self.description_body}|{related_string}'
            outstring = outstring.replace('\n', ' ')
            try:
                general_file.write(f'{outstring}\n')
            except UnicodeEncodeError:
                print(f'* Error with parsing program "{self.name}"')

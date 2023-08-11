# This is a sample Python script.
import xml.etree.ElementTree as ET

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import requests

# Pubmed API
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
api_key = "50416027f5403b3198bd527dc00137bbcf08"

# 검색어 설정
search_term = input("논문 키워드 검색: ")

# 검색 요청 생성
search_url = f"{base_url}esearch.fcgi?db=pubmed&term={search_term}&api_key={api_key}&retmax=25"
'''
retmax: default 20개/ # of retrieved UIDs
'''
response = requests.get(search_url)
# data = response.json()
print(response.text)
# XML 응답 파싱
root = ET.fromstring(response.text)

# 논문 id 추출
paper_ids = [paper_id.text for paper_id in root.findall('.//Id')]
# 검색 결과에서 논문 ID 추출
# paper_ids = data["esearchresult"]["idlist"]
print(paper_ids)
# 추출한 논문 ID를 사용하여 논문 정보 요청 생성 및 처리
for paper_id in paper_ids:
    paper_info_url = f"{base_url}efetch.fcgi?db=pubmed&id={paper_id}&retmode=xml&api_key={api_key}"
    paper_response = requests.get(paper_info_url)
    paper_root = ET.fromstring(paper_response.text)

    # title, abstract 추출
    title = paper_root.find('.//ArticleTitle').text
    abstract_element = paper_root.find('.//AbstractText')
    abstract = abstract_element.text if abstract_element is not None else "No abstract available"
    print(f"Title: {title}\nAbstract: {abstract}\n")

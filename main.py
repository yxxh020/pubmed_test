# This is a sample Python script.
import xml.etree.ElementTree as ET
import json
import requests
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
'''
access limit: no more than 3 requests per second
esearch
querykey, WebEnv로 uid리스트 만들기
usehistory=y 해서 querykey, WebEnv 를 받아와서 eSummary나 eFetch할때 사용가능

elink: to find related records of the paper
    dbfrom, db 해서 다른 db에 검색 가능

'''
search_url = f"{base_url}esearch.fcgi?db=pubmed&term={search_term}&api_key={api_key}&retmax=10&usehistory=y"
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


# esummary

# pmids = data["esearchresult"]["idlist"]
# pmids_str = ",".join(pmids)
# summary_url = f"{base_url}esummary.fcgi?db=pubmed&id={pmids_str}&api_key={api_key}&retmode=json"
# summary_response = requests.get(summary_url)
# summary_data = summary_response.json()
#
# print(json.dumps(summary_data, indent=2))

'''
efetch
- returns full records
- rettype: 반환되는 데이터 형식 지정
    fasta: dna, rna 단백질 서열정보 나타내는 텍스트형식 (ex: GCTTCAGA....)
    abstract: 초록
- retmode=text
'''
# 추출한 논문 ID를 사용하여 논문 정보 요청 생성 및 처리
for paper_id in paper_ids:
    # efetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={paper_id}&rettype=abstract&retmode=text&api_key={api_key}"
    efetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={paper_id}&rettype=abstract&api_key={api_key}"
    efetch_response = requests.get(efetch_url)

    esummary_url = f"{base_url}esummary.fcgi?db=pubmed&id={paper_id}&api_key={api_key}&retmode=json"
    esummary_response = requests.get(esummary_url)
    esummary_result = esummary_response.text.strip()

    paper_root = ET.fromstring(efetch_response.text)
    #
    # # title, abstract 추출
    # title = paper_root.find('.//ArticleTitle').text
    abstract_element = paper_root.findall('.//AbstractText')
    abstract = [abstract_element.text.strip() for abstract_element in abstract_element]
    # print(f"Title: {title}\nAbstract: {abstract}\n")

    # abstract = efetch_response.text.strip()  # 초록을 텍스트 형식으로 추출
    keyword_element = paper_root.find('.//Keyword')
    keyword = keyword_element.text if keyword_element is not None else "no keyword"
    print(f"Paper ID: {paper_id}\nAbstract: {abstract}\nkeyword: {keyword}")
    # print(f"Paper ID: {paper_id}\nesum: {esummary_result}\n")

# NLTK로 text mining


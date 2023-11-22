from PyPDF2 import PdfFileMerger
import sys
import win32com.client
import openpyxl as op
import os
import glob

OUTPUT_EXCEL = r'c:\\Temp\\output_excel'
OUTPUT_PDF = r'c:\\Temp\\output_pdf'
OUTPUT_FINAL = r'c:\\Temp\\output_final'

def resource_path(relative_path): 
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) 
    return os.path.join(base_path, relative_path)

def excelInfo(filepath):
    excel_list = os.listdir(filepath)  # 폴더안에 잇는 엑셀파일 명을 리스트로 저장
    # print(f'excel_list : {excel_list}')
    result = []  # 빈 리스트 생성
    for file in excel_list:  # 엑셀파일명 리스트를 for문을 통해 반복
        excel_path = OUTPUT_EXCEL
        # print(f'[12/16] excel_path {excel_path}')
        wb = op.load_workbook(filepath+"/"+file)  # openpyxl workbook 생성
        ws_list = wb.sheetnames  # 해당 workbook의 시트명을 리스트로 받음
        filename = file.replace(".xlsx", "")  # 파일명을 저장하기 위해 문자열에서 확장자 제거
        for sht in ws_list:  # 시트명 리스트를 for문을 통해 반복
            temp_tuple = (filepath+"/"+file, filename,
                          sht)  # 파일경로, 파일명, sht를 튜플에 저장
            result.append(temp_tuple)  # 위 튜플을 빈 리스트에 추가
    # print(result)
    return result  # 튜플로 이루어진 리스트 리턴


def transPDF(fileinfo, savepath):
    # print()
    # print(f'[12/13] transPDF savepath : {savepath}')
    excel = win32com.client.Dispatch("Excel.Application")
    i = 0  # 파일명 중복을 방지하기 위한 인덱싱 번호

    # print(f'fileinfo : {fileinfo}')
    # excelinfo를 입력받아 for문 실행
    for info in fileinfo:
        # info가 튜플이므로 인덱싱으로 접근(0번째는 파일경로)
        # print(f'info[0] : {info[0]}')
        # wb = excel.Workbooks.Open('./example_test_01.xlsx')
        # ws = wb.Worksheets('Summary')  # 튜플의 2번째 요소는 시트명임.
        
        # print(f'[12/13] worksheet : {info[2]}')
        wb = excel.Workbooks.Open(info[0])
        ws = wb.Worksheets(info[2])
        ws.Select()  # 위 설정한 시트 선택
        wb.ActiveSheet.ExportAsFixedFormat(
            0, savepath+"/"+str(i)+"_"+info[1]+"_"+info[2]+".pdf")  # 파일명, 시트명으로 pdf 파일명 저장
        # wb.ActiveSheet.ExportAsFixedFormat(
        #     0, savepath+"/"+str(i)+"_"+'example_test_01'+"_"+'Summary'+".pdf")  # 파일명, 시트명으로 pdf 파일명 저장
        i = i+1
        wb.Close(False)  # workbook 닫기, True일 경우 그 상태를 저장한다.
        excel.Quit()  # excel application 닫기


def integrated_one_file(exec_file_path, pdf_file_path, mapfile):
    
    # print()
    # temp_output_path = file_path
    # file_path = os.path.abspath(exec_file_path)
    basename = os.path.basename(exec_file_path)
    pdf_base_name = os.path.basename(mapfile)
    pdf_file_name , ext = os.path.splitext(pdf_base_name)
    
    # print(f'[12/13] pdf_file_path : {pdf_file_path}')
    # print(f'[12/13] exec basename : {basename}')
    # print(f'[12/13] pdf file name : {pdf_file_name}')
    filelist = os.listdir(pdf_file_path )
    # print(f'[12/13] filelist :{filelist}')
    filelist.sort()  # 파일 오름차순으로 정렬

    num = len(filelist)
    merger = PdfFileMerger()

    # pdf_file_name, file_ext = os.path.splitext(map_file_name)
    for filename in filelist:
        print(f'[12/13] merger file_name : {pdf_file_path}{filename}')
        merger.append(pdf_file_path + '/' + filename)

    print()
    # print(f'[12/13] exec path : {exec_file_path}')
    # print(f'[12/13] pdf file name : {filename}' + '.pdf')
    final_pdf_file = pdf_file_name + '.pdf'
    merger.write(final_pdf_file)
    merger.write(OUTPUT_FINAL + '/' + pdf_file_name + '.pdf')
    merger.write('OUTPUT/' + pdf_file_name + '.pdf')
    merger.close()
    print()
    print(f'[12/13] final_pdf_file :{final_pdf_file}')
    

if __name__ == '__main__':
    # filepath = r'G:\\output_excel'
    # filename = r'.\test_01.xlsx'
    # pdfpath = r"G:\\output_pdf"
    # excelinfo = excelInfo(OUTPUT_EXCEL)
    # transPDF(excelinfo, OUTPUT_PDF)
    integrated_one_file('example_4.map')

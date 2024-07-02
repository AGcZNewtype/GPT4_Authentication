import PyPDF2

# 提取PDF文件内容
def extract_text_from_pdf(file_path):
    pdf_text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text


#对GPT输出问题和答案进行切分合并
def response_split(response):
    #通过字符切分问题和答案集
    allList = response.split('==')
    quesList=[]
    ansList=[]

    for i in allList:
        if i.find("++") != -1:
            templist = i.split("++")
            #加入问题集
            quesList.append(templist[0])
            #加入答案集
            ansList.append(templist[1])

    # print(queslist)
    # print(anslist)
    return quesList,ansList


def avg_similarity(similarity):
    totalSimilarity = float()
    for i in similarity:
        totalSimilarity += float(i)
    average = totalSimilarity/(len(similarity))
    print(average)
    return average


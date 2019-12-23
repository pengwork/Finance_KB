from query import Query
import re

class QuestionTemplate():
    def __init__(self):
        self.q_template_dict={
            0:self.get_company,
            1:self.get_concept,
            2:self.get_industry,
            3:self.get_stock
        }

        # 连接数据库
        self.graph = Query()
        # 测试数据库是否连接上
        # result=self.graph.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
        # print(result)
        # exit()

    def get_question_answer(self,question,template): # 传过来标记后的数据 和 相应的模板
        # 如果问题模板的格式不正确则结束
        # print("去找找模板的答案")
        assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        print("问题预处理，启动！",question)
    
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        print(len(question_flag), len(question_word))
        assert len(question_flag)==len(question_word)
        # print("渡劫成功！")
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        print("这是我找到的答案：", answer)
        return answer

    # 获取董事长的名字
    def get_executive_name(self):
        tag_index = self.question_flag.index("ne")
        print(tag_index)
        executive_name = self.question_word[tag_index]
        print(executive_name)
        return executive_name
    # 获取公司名字
    def get_company_name(self):
        tag_index = self.question_flag.index("nc")
        company_name = self.question_word[tag_index]
        return company_name


    # 0 ne管理哪些公司
    def get_company(self):
        print("找公司，启动！")
        name = self.get_executive_name()
        answer_list = self.get_company_name_list(name)
        answer = "、".join(answer_list)
        final_answer = name+"管理的公司有"+str(answer)+"。"
        return final_answer
    def get_company_name_list(self, name):
        print("搜索所有公司，启动！")
        cql = f"match(n:Person)-[:employ_of]->(c:Company) where n.name='{name}' return c.name"
        print(cql)
        answer = self.graph.run(cql)
        answer_set = set(answer)
        answer_list = list(answer_set)
        return answer_list
    #1  nc公司的概念
    def get_concept(self):
        print("开始nc公司，启动！")
        name = self.get_company_name()
        answer_list = self.get_nccompany_name_list(name)
        answer = "、".join(answer_list)
        final_answer = name+"的概念为"+str(answer)+"。"
        return final_answer
    def get_nccompany_name_list(self, name):
        print("搜索nc公司，启动！")
        cql = f"match(n:Company)-[:concept_of]->(c:Concept) where n.name='{name}' return c.name"
        # cql = f"match(n:Company) where n.name='{name}' return n.stock_id"
        print(cql)
        answer = self.graph.run(cql)
        answer_set = set(answer)
        answer_list = list(answer_set)
        return answer_list
    
    # 2 nc属于什么行业
    def get_industry(self):
        print("找行业，启动！")
        name = self.get_company_name()
        answer_list = self.get_industry_name_list(name)
        answer = "、".join(answer_list)
        final_answer = name + "所属的行业是" + str(answer) + "。"
        return final_answer
    def get_industry_name_list(self, name):
        print("搜索所有行业，启动！")
        cql = f"match(n:Company)-[:industry_of]->(c:Industry) where n.name='{name}' return c.name"
        print(cql)
        answer = self.graph.run(cql)
        answer_set = set(answer)
        answer_list = list(answer_set)
        return answer_list
    
    #3 nc股票
    def get_stock(self):
        print("开始ns公司，启动！")
        name = self.get_company_name()
        answer_list = self.get_nscompany_name_list(name)
        answer = "、".join(answer_list)
        final_answer = name+"的股票代码为"+str(answer)+"。"
        return final_answer
    def get_nscompany_name_list(self, name):
        print("搜索ns公司，启动！")
        # cql = f"match(n:Company)-[:concept_of]->(c:Concept) where n.name='{name}' return c.name"
        cql = f"match(n:Company) where n.name='{name}' return n.stock_id"
        print(cql)
        answer = self.graph.run(cql)
        answer_set = set(answer)
        answer_list = list(answer_set)
        return answer_list
